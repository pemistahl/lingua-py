#
# Copyright © 2022 Peter M. Stahl pemistahl@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import operator

from collections import Counter
from dataclasses import dataclass
from typing import Counter as TypedCounter, Dict, FrozenSet, Optional, Tuple, List

from ._constant import (
    CHARS_TO_LANGUAGES_MAPPING,
    JAPANESE_CHARACTER_SET,
    LANGUAGES_SUPPORTING_LOGOGRAMS,
    MULTIPLE_WHITESPACE,
    NO_LETTER,
    NUMBERS,
    PUNCTUATION,
)
from .language import Language, _Alphabet
from ._model import _TrainingDataLanguageModel, _TestDataLanguageModel
from ._ngram import _range_of_lower_order_ngrams

_UNIGRAM_MODELS: Dict[Language, np.ndarray] = {}
_BIGRAM_MODELS: Dict[Language, np.ndarray] = {}
_TRIGRAM_MODELS: Dict[Language, np.ndarray] = {}
_QUADRIGRAM_MODELS: Dict[Language, np.ndarray] = {}
_FIVEGRAM_MODELS: Dict[Language, np.ndarray] = {}
_CACHE: Dict[Language, Dict[str, Optional[float]]] = {}
_HIGH_ACCURACY_MODE_MAX_TEXT_LENGTH = 120


@dataclass
class LanguageDetector:
    """This class detects the language of text."""

    _languages: FrozenSet[Language]
    _minimum_relative_distance: float
    _is_low_accuracy_mode_enabled: bool
    _languages_with_unique_characters: FrozenSet[Language]
    _one_language_alphabets: Dict[_Alphabet, Language]
    _unigram_language_models: Dict[Language, np.ndarray]
    _bigram_language_models: Dict[Language, np.ndarray]
    _trigram_language_models: Dict[Language, np.ndarray]
    _quadrigram_language_models: Dict[Language, np.ndarray]
    _fivegram_language_models: Dict[Language, np.ndarray]
    _cache: Dict[Language, Dict[str, Optional[float]]]

    def __repr__(self):
        languages = sorted([language.name for language in self._languages])
        return (
            "LanguageDetector("
            f"_languages={languages}, "
            f"_minimum_relative_distance={self._minimum_relative_distance})"
        )

    @classmethod
    def _from(
        cls,
        languages: FrozenSet[Language],
        minimum_relative_distance: float,
        is_every_language_model_preloaded: bool,
        is_low_accuracy_mode_enabled: bool,
    ) -> "LanguageDetector":
        languages_with_unique_characters = frozenset(
            {
                language
                for language in languages
                if language._unique_characters is not None
            }
        )
        one_language_alphabets = {
            alphabet: language
            for alphabet, language in _Alphabet.all_supporting_single_language().items()
            if language in languages
        }
        detector = LanguageDetector(
            languages,
            minimum_relative_distance,
            is_low_accuracy_mode_enabled,
            languages_with_unique_characters,
            one_language_alphabets,
            _UNIGRAM_MODELS,
            _BIGRAM_MODELS,
            _TRIGRAM_MODELS,
            _QUADRIGRAM_MODELS,
            _FIVEGRAM_MODELS,
            _CACHE,
        )

        if is_every_language_model_preloaded:
            detector._preload_language_models()

        return detector

    def _preload_language_models(self):
        trigram_models = [
            self._load_language_models(language, 3) for language in self._languages
        ]

        for trigram_model in trigram_models:
            if trigram_model is not None:
                self._trigram_language_models.update(trigram_model)

        if not self._is_low_accuracy_mode_enabled:
            (unigram_models, bigram_models, quadrigram_models, fivegram_models,) = [
                [
                    self._load_language_models(language, ngram_length)
                    for language in self._languages
                ]
                for ngram_length in (1, 2, 4, 5)
            ]

            for unigram_model in unigram_models:
                if unigram_model is not None:
                    self._unigram_language_models.update(unigram_model)

            for bigram_model in bigram_models:
                if bigram_model is not None:
                    self._bigram_language_models.update(bigram_model)

            for quadrigram_model in quadrigram_models:
                if quadrigram_model is not None:
                    self._quadrigram_language_models.update(quadrigram_model)

            for fivegram_model in fivegram_models:
                if fivegram_model is not None:
                    self._fivegram_language_models.update(fivegram_model)

    def detect_language_of(self, text: str) -> Optional[Language]:
        """Detect the language of text.

        Args:
            text (str): The text whose language should be identified.

        Returns:
            The identified language. If the language cannot be
            reliably detected, None is returned.
        """
        confidence_values = self.compute_language_confidence_values(text)

        if len(confidence_values) == 0:
            return None

        most_likely_language, most_likely_language_probability = confidence_values[0]

        if len(confidence_values) == 1:
            return most_likely_language

        second_most_likely_language_probability = confidence_values[1][1]

        if most_likely_language_probability == second_most_likely_language_probability:
            return None
        if (
            most_likely_language_probability - second_most_likely_language_probability
            < self._minimum_relative_distance
        ):
            return None

        return most_likely_language

    def compute_language_confidence_values(
        self, text: str
    ) -> List[Tuple[Language, float]]:
        """Compute confidence values for each language considered
        possible for the given text.

        A list of all possible languages is returned, sorted by
        their confidence value in descending order. The values
        that this method computes are part of a relative
        confidence metric, not of an absolute one. Each value
        is a number between 0.0 and 1.0. The most likely language
        is always returned with value 1.0. All other languages get
        values assigned which are lower than 1.0, denoting how less
        likely those languages are in comparison to the most likely
        language.

        The list returned by this method does not necessarily
        contain all languages which this LanguageDetector instance
        was built from. If the rule-based engine decides that a
        specific language is truly impossible, then it will not be
        part of the returned list. Likewise, if no ngram probabilities
        can be found within the detector's languages for the given
        text, the returned list will be empty. The confidence value for
        each language not being part of the returned list is assumed to
        be 0.0.

        Args:
            text (str): The text for which to compute confidence values.

        Returns:
            A list of 2-element tuples. Each tuple contains a language
            and the associated confidence value.
        """
        cleaned_up_text = self._clean_up_input_text(text)
        if (
            len(cleaned_up_text) == 0
            or NO_LETTER.fullmatch(cleaned_up_text) is not None
        ):
            return []
        words = self._split_text_into_words(cleaned_up_text)
        language_detected_by_rules = self._detect_language_with_rules(words)

        if language_detected_by_rules is not None:
            return [(language_detected_by_rules, 1.0)]

        filtered_languages = self._filter_languages_by_rules(words)

        if len(filtered_languages) == 1:
            filtered_language = next(iter(filtered_languages))
            return [(filtered_language, 1.0)]

        if self._is_low_accuracy_mode_enabled and len(cleaned_up_text) < 3:
            return []

        character_count = len(cleaned_up_text)
        ngram_length_range = (
            range(3, 4)
            if character_count >= _HIGH_ACCURACY_MODE_MAX_TEXT_LENGTH
            or self._is_low_accuracy_mode_enabled
            else range(1, 6)
        )
        unigram_counts = None
        all_probabilities = []

        for ngram_length in ngram_length_range:
            if character_count >= ngram_length:
                if ngram_length == 1:
                    unigram_counts = self._count_unigrams(
                        cleaned_up_text, filtered_languages
                    )

                probabilities = self._look_up_language_models(
                    cleaned_up_text, ngram_length, filtered_languages
                )
                all_probabilities.append(probabilities)

        summed_up_probabilities = self._sum_up_probabilities(
            all_probabilities, unigram_counts, filtered_languages
        )

        if len(summed_up_probabilities) == 0:
            return []

        highest_probability = sorted(summed_up_probabilities.values())[-1]

        return sorted(
            [
                (language, highest_probability / probability)
                for language, probability in summed_up_probabilities.items()
            ],
            key=operator.itemgetter(1, 0),
            reverse=True,
        )

    def _clean_up_input_text(self, text: str) -> str:
        trimmed = text.strip().lower()
        without_punctuation = PUNCTUATION.sub("", trimmed)
        without_numbers = NUMBERS.sub("", without_punctuation)
        normalized_whitespace = MULTIPLE_WHITESPACE.sub(" ", without_numbers)
        return normalized_whitespace

    def _split_text_into_words(self, text: str) -> List[str]:
        normalized_text = "".join(
            (char + " " if self._is_logogram(char) else char for char in text)
        )
        if " " in normalized_text:
            return [char for char in normalized_text.split(" ") if len(char) > 0]
        return [normalized_text]

    def _is_logogram(self, char: str) -> bool:
        if char.isspace():
            return False
        for language in LANGUAGES_SUPPORTING_LOGOGRAMS:
            for alphabet in language._alphabets:
                if alphabet.matches(char):
                    return True
        return False

    def _detect_language_with_rules(self, words: List[str]) -> Optional[Language]:
        total_language_counts: TypedCounter[Optional[Language]] = Counter()
        half_word_count = len(words) * 0.5
        for word in words:
            word_language_counts: TypedCounter[Language] = Counter()
            for char in word:
                is_match = False
                for alphabet, language in self._one_language_alphabets.items():
                    if alphabet.matches(char):
                        word_language_counts[language] += 1
                        is_match = True
                        break
                if not is_match:
                    if _Alphabet.HAN.matches(char):
                        word_language_counts[Language.CHINESE] += 1
                    elif JAPANESE_CHARACTER_SET.fullmatch(char) is not None:
                        word_language_counts[Language.JAPANESE] += 1
                    elif (
                        _Alphabet.LATIN.matches(char)
                        or _Alphabet.CYRILLIC.matches(char)
                        or _Alphabet.DEVANAGARI.matches(char)
                    ):
                        for language in self._languages_with_unique_characters:
                            if (
                                language._unique_characters is not None
                                and char in language._unique_characters
                            ):
                                word_language_counts[language] += 1

            if len(word_language_counts) == 0:
                total_language_counts[None] += 1
            elif len(word_language_counts) == 1:
                language = list(word_language_counts.elements())[0]
                if language in self._languages:
                    total_language_counts[language] += 1
                else:
                    total_language_counts[None] += 1
            elif (
                Language.CHINESE in word_language_counts
                and Language.JAPANESE in word_language_counts
            ):
                total_language_counts[Language.JAPANESE] += 1
            else:
                most_frequent_word_languages = word_language_counts.most_common(2)
                (
                    most_frequent_word_language,
                    first_count,
                ) = most_frequent_word_languages[0]
                (_, second_count) = most_frequent_word_languages[1]
                if (
                    first_count > second_count
                    and most_frequent_word_language in self._languages
                ):
                    total_language_counts[most_frequent_word_language] += 1
                else:
                    total_language_counts[None] += 1

        if total_language_counts[None] < half_word_count:
            del total_language_counts[None]

        if len(total_language_counts) == 0:
            return None
        if len(total_language_counts) == 1:
            return list(total_language_counts)[0]
        if (
            len(total_language_counts) == 2
            and Language.CHINESE in total_language_counts
            and Language.JAPANESE in total_language_counts
        ):
            return Language.JAPANESE

        most_frequent_total_languages = total_language_counts.most_common(2)
        (most_frequent_total_language, first_count) = most_frequent_total_languages[0]
        (_, second_count) = most_frequent_total_languages[1]

        if first_count == second_count:
            return None

        return most_frequent_total_language

    def _filter_languages_by_rules(self, words: List[str]) -> FrozenSet[Language]:
        detected_alphabets: TypedCounter[_Alphabet] = Counter()
        half_word_count = len(words) * 0.5
        for word in words:
            for alphabet in _Alphabet:
                if alphabet.matches(word):
                    detected_alphabets[alphabet] += 1
                    break

        if len(detected_alphabets) == 0:
            return self._languages
        if len(detected_alphabets) > 1:
            distinct_alphabets = {count for count in detected_alphabets.values()}
            if len(distinct_alphabets) == 1:
                return self._languages

        most_frequent_alphabet = detected_alphabets.most_common(1)[0][0]
        filtered_languages = {
            language
            for language in self._languages
            if most_frequent_alphabet in language._alphabets
        }
        language_counts: TypedCounter[Language] = Counter()

        for characters, languages in CHARS_TO_LANGUAGES_MAPPING.items():
            relevant_languages = languages.intersection(filtered_languages)

            for word in words:
                for character in characters:
                    if character in word:
                        for language in relevant_languages:
                            language_counts[language] += 1

        languages_subset = {
            language
            for language, count in language_counts.items()
            if count >= half_word_count
        }

        if len(languages_subset) > 0:
            return frozenset(languages_subset)

        return frozenset(filtered_languages)

    def _look_up_language_models(
        self, text: str, ngram_length: int, filtered_languages: FrozenSet[Language]
    ) -> Dict[Language, float]:
        test_data_model = _TestDataLanguageModel.from_text(text, ngram_length)
        probabilities = self._compute_language_probabilities(
            test_data_model, filtered_languages
        )
        return probabilities

    def _compute_language_probabilities(
        self, model: _TestDataLanguageModel, filtered_languages: FrozenSet[Language]
    ) -> Dict[Language, float]:
        probabilities = {}
        for language in filtered_languages:
            result = self._compute_sum_of_ngram_probabilities(language, model.ngrams)
            if result < 0:
                probabilities[language] = result
        return probabilities

    def _compute_sum_of_ngram_probabilities(
        self, language: Language, ngrams: FrozenSet[str]
    ) -> float:
        result = 0.0
        for ngram in ngrams:
            for elem in _range_of_lower_order_ngrams(ngram):
                probability = self._look_up_ngram_probability(language, elem)
                if probability is not None:
                    result += probability
                    break
        return result

    def _look_up_ngram_probability(
        self, language: Language, ngram: str
    ) -> Optional[float]:
        if language not in self._cache:
            self._cache[language] = {}

        if ngram in self._cache[language]:
            return self._cache[language][ngram]

        ngram_length = len(ngram)
        if ngram_length == 5:
            language_models = self._fivegram_language_models
        elif ngram_length == 4:
            language_models = self._quadrigram_language_models
        elif ngram_length == 3:
            language_models = self._trigram_language_models
        elif ngram_length == 2:
            language_models = self._bigram_language_models
        elif ngram_length == 1:
            language_models = self._unigram_language_models
        elif ngram_length == 0:
            raise ValueError("zerogram detected")
        else:
            raise ValueError(f"unsupported ngram length detected: {ngram_length}")

        probability = None

        if language not in language_models:
            models = self._load_language_models(language, ngram_length)
            if models is None:
                self._cache[language][ngram] = probability
                return probability
            language_models.update(models)

        mask = np.isin(language_models[language]["ngram"], ngram)

        try:
            probability = language_models[language]["frequency"][mask][0]
        except IndexError:
            pass

        self._cache[language][ngram] = probability

        return probability

    def _count_unigrams(
        self,
        text: str,
        filtered_languages: FrozenSet[Language],
    ) -> TypedCounter[Language]:
        unigram_model = _TestDataLanguageModel.from_text(text, ngram_length=1)
        unigram_counts: TypedCounter[Language] = Counter()
        for language in filtered_languages:
            for unigram in unigram_model.ngrams:
                if self._look_up_ngram_probability(language, unigram) is not None:
                    unigram_counts[language] += 1
        return unigram_counts

    def _sum_up_probabilities(
        self,
        probabilities: List[Dict[Language, float]],
        unigram_counts: Optional[TypedCounter[Language]],
        filtered_languages: FrozenSet[Language],
    ) -> Dict[Language, float]:
        summed_up_probabilities = {}
        for language in filtered_languages:
            result = 0.0
            for dct in probabilities:
                if language in dct:
                    result += dct[language]
            if unigram_counts is not None and language in unigram_counts:
                result /= unigram_counts[language]
            if result != 0:
                summed_up_probabilities[language] = result
        return summed_up_probabilities

    def _load_language_models(
        self,
        language: Language,
        ngram_length: int,
    ) -> Optional[Dict[Language, np.ndarray]]:
        loaded_model = _TrainingDataLanguageModel.from_numpy_binary_file(
            language, ngram_length
        )
        if loaded_model is None:
            return None
        return {language: loaded_model}
