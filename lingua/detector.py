#
# Copyright © 2022-present Peter M. Stahl pemistahl@gmail.com
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

from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from math import exp
from typing import NamedTuple, Optional


from ._constant import (
    CHARS_TO_LANGUAGES_MAPPING,
    JAPANESE_CHARACTER_SET,
    TOKENS_WITHOUT_WHITESPACE,
    TOKENS_WITH_OPTIONAL_WHITESPACE,
)
from .language import Language, _Alphabet
from ._model import (
    _load_ngram_probability_model,
    _load_ngram_model,
    _create_ngrams,
    _create_lower_order_ngrams,
    _NgramModelType,
)

_UNIGRAM_MODELS: dict[Language, dict[str, float]] = {}
_BIGRAM_MODELS: dict[Language, dict[str, float]] = {}
_TRIGRAM_MODELS: dict[Language, dict[str, float]] = {}
_QUADRIGRAM_MODELS: dict[Language, dict[str, float]] = {}
_FIVEGRAM_MODELS: dict[Language, dict[str, float]] = {}
_UNIQUE_UNIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_UNIQUE_BIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_UNIQUE_TRIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_UNIQUE_QUADRIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_UNIQUE_FIVEGRAM_MODELS: dict[Language, frozenset[str]] = {}
_MOST_COMMON_UNIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_MOST_COMMON_BIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_MOST_COMMON_TRIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_MOST_COMMON_QUADRIGRAM_MODELS: dict[Language, frozenset[str]] = {}
_MOST_COMMON_FIVEGRAM_MODELS: dict[Language, frozenset[str]] = {}
_LANGUAGES_WITH_SINGLE_UNIQUE_SCRIPT: frozenset[Language] = (
    Language.all_with_single_unique_script()
)
_HIGH_ACCURACY_MODE_MAX_TEXT_LENGTH = 120


def _split_text_into_words(text: str) -> list[str]:
    return TOKENS_WITHOUT_WHITESPACE.findall(text.lower())


def _sum_up_probabilities(
    probabilities: list[dict[Language, float]],
    unigram_counts: Optional[Counter[Language]],
    filtered_languages: frozenset[Language],
) -> dict[Language, Decimal]:
    summed_up_probabilities = {}
    for language in filtered_languages:
        result = 0.0
        for dct in probabilities:
            if language in dct:
                result += dct[language]
        if unigram_counts is not None and language in unigram_counts:
            result /= unigram_counts[language]
        if result != 0:
            # Use Decimal instead of float to prevent numerical underflow
            summed_up_probabilities[language] = _compute_exponent(result)
    return summed_up_probabilities


def _compute_exponent(value: float) -> Decimal:
    exponent = exp(value)
    if exponent > 0:
        return Decimal(exponent)
    return Decimal(value).exp()


def _sort_confidence_values(values: list["ConfidenceValue"]):
    values.sort(key=lambda tup: (-tup[1], tup[0]))


def _collect_languages_with_unique_characters(
    languages: frozenset[Language],
) -> frozenset[Language]:
    return frozenset(
        {language for language in languages if language._unique_characters is not None}
    )


def _collect_single_language_alphabets(
    languages: frozenset[Language],
) -> dict[_Alphabet, Language]:
    return {
        alphabet: language
        for alphabet, language in _Alphabet.all_supporting_single_language().items()
        if language in languages
    }


def _merge_adjacent_results(
    results: list["DetectionResult"], mergeable_result_indices: list[int]
):
    mergeable_result_indices.sort(reverse=True)

    for i in mergeable_result_indices:
        if i == 0:
            results[i + 1] = DetectionResult(
                start_index=results[i].start_index,
                end_index=results[i + 1].end_index,
                word_count=results[i].word_count + results[i + 1].word_count,
                language=results[i + 1].language,
            )
        else:
            results[i - 1] = DetectionResult(
                start_index=results[i - 1].start_index,
                end_index=results[i].end_index,
                word_count=results[i - 1].word_count + results[i].word_count,
                language=results[i - 1].language,
            )

        del results[i]

        if len(results) == 1:
            break


class ConfidenceValue(NamedTuple):
    """This class describes a language's confidence value.

    Attributes:
        language (Language):
            The language associated with this confidence value.

        value (float):
            The language's confidence value which lies between 0.0 and 1.0.
    """

    language: Language
    value: float


class DetectionResult(NamedTuple):
    """This class describes a contiguous single-language
    text section within a possibly mixed-language text.

    Attributes:
        start_index (int):
            The start index of the identified single-language substring.

        end_index (int):
            The end index of the identified single-language substring.

        word_count (int):
            The number of words being part of the identified
            single-language substring.

        language (Language):
            The detected language of the identified single-language substring.
    """

    start_index: int
    end_index: int
    word_count: int
    language: Language


@dataclass
class LanguageDetector:
    """This class detects the language of text."""

    _languages: frozenset[Language]
    _minimum_relative_distance: float
    _is_low_accuracy_mode_enabled: bool
    _is_built_from_one_language: bool
    _languages_with_unique_characters: frozenset[Language]
    _one_language_alphabets: dict[_Alphabet, Language]
    _unigram_language_models: dict[Language, dict[str, float]]
    _bigram_language_models: dict[Language, dict[str, float]]
    _trigram_language_models: dict[Language, dict[str, float]]
    _quadrigram_language_models: dict[Language, dict[str, float]]
    _fivegram_language_models: dict[Language, dict[str, float]]
    _unique_unigram_language_models: dict[Language, frozenset[str]]
    _unique_bigram_language_models: dict[Language, frozenset[str]]
    _unique_trigram_language_models: dict[Language, frozenset[str]]
    _unique_quadrigram_language_models: dict[Language, frozenset[str]]
    _unique_fivegram_language_models: dict[Language, frozenset[str]]
    _most_common_unigram_language_models: dict[Language, frozenset[str]]
    _most_common_bigram_language_models: dict[Language, frozenset[str]]
    _most_common_trigram_language_models: dict[Language, frozenset[str]]
    _most_common_quadrigram_language_models: dict[Language, frozenset[str]]
    _most_common_fivegram_language_models: dict[Language, frozenset[str]]

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
        languages: frozenset[Language],
        minimum_relative_distance: float,
        is_every_language_model_preloaded: bool,
        is_low_accuracy_mode_enabled: bool,
    ) -> "LanguageDetector":
        is_built_from_one_language = len(languages) == 1
        languages_with_unique_characters = _collect_languages_with_unique_characters(
            languages
        )
        one_language_alphabets = _collect_single_language_alphabets(languages)
        detector = LanguageDetector(
            languages,
            minimum_relative_distance,
            is_low_accuracy_mode_enabled,
            is_built_from_one_language,
            languages_with_unique_characters,
            one_language_alphabets,
            _UNIGRAM_MODELS,
            _BIGRAM_MODELS,
            _TRIGRAM_MODELS,
            _QUADRIGRAM_MODELS,
            _FIVEGRAM_MODELS,
            _UNIQUE_UNIGRAM_MODELS,
            _UNIQUE_BIGRAM_MODELS,
            _UNIQUE_TRIGRAM_MODELS,
            _UNIQUE_QUADRIGRAM_MODELS,
            _UNIQUE_FIVEGRAM_MODELS,
            _MOST_COMMON_UNIGRAM_MODELS,
            _MOST_COMMON_BIGRAM_MODELS,
            _MOST_COMMON_TRIGRAM_MODELS,
            _MOST_COMMON_QUADRIGRAM_MODELS,
            _MOST_COMMON_FIVEGRAM_MODELS,
        )

        if is_every_language_model_preloaded:
            detector._preload_language_models()

        if is_built_from_one_language or is_low_accuracy_mode_enabled:
            detector._preload_unique_ngram_models()

        if is_built_from_one_language:
            detector._preload_most_common_ngram_models()

        return detector

    def _preload_unique_ngram_models(self):
        unique_unigram_models = [
            _load_ngram_model(language, 1, model_type=_NgramModelType.UNIQUE)
            for language in self._languages
            if language not in self._unique_unigram_language_models
        ]

        unique_bigram_models = [
            _load_ngram_model(language, 2, model_type=_NgramModelType.UNIQUE)
            for language in self._languages
            if language not in self._unique_bigram_language_models
        ]

        unique_trigram_models = [
            _load_ngram_model(language, 3, model_type=_NgramModelType.UNIQUE)
            for language in self._languages
            if language not in self._unique_trigram_language_models
        ]

        unique_quadrigram_models = [
            _load_ngram_model(language, 4, model_type=_NgramModelType.UNIQUE)
            for language in self._languages
            if language not in self._unique_quadrigram_language_models
        ]

        unique_fivegram_models = [
            _load_ngram_model(language, 5, model_type=_NgramModelType.UNIQUE)
            for language in self._languages
            if language not in self._unique_fivegram_language_models
        ]

        for unique_unigram_model in unique_unigram_models:
            if unique_unigram_model is not None:
                self._unique_unigram_language_models[unique_unigram_model.language] = (
                    unique_unigram_model.ngrams
                )

        for unique_bigram_model in unique_bigram_models:
            if unique_bigram_model is not None:
                self._unique_bigram_language_models[unique_bigram_model.language] = (
                    unique_bigram_model.ngrams
                )

        for unique_trigram_model in unique_trigram_models:
            if unique_trigram_model is not None:
                self._unique_trigram_language_models[unique_trigram_model.language] = (
                    unique_trigram_model.ngrams
                )

        for unique_quadrigram_model in unique_quadrigram_models:
            if unique_quadrigram_model is not None:
                self._unique_quadrigram_language_models[
                    unique_quadrigram_model.language
                ] = unique_quadrigram_model.ngrams

        for unique_fivegram_model in unique_fivegram_models:
            if unique_fivegram_model is not None:
                self._unique_fivegram_language_models[
                    unique_fivegram_model.language
                ] = unique_fivegram_model.ngrams

    def _preload_most_common_ngram_models(self):
        most_common_unigram_models = [
            _load_ngram_model(language, 1, model_type=_NgramModelType.MOSTCOMMON)
            for language in self._languages
            if language not in self._most_common_unigram_language_models
        ]

        most_common_bigram_models = [
            _load_ngram_model(language, 2, model_type=_NgramModelType.MOSTCOMMON)
            for language in self._languages
            if language not in self._most_common_bigram_language_models
        ]

        most_common_trigram_models = [
            _load_ngram_model(language, 3, model_type=_NgramModelType.MOSTCOMMON)
            for language in self._languages
            if language not in self._most_common_trigram_language_models
        ]

        most_common_quadrigram_models = [
            _load_ngram_model(language, 4, model_type=_NgramModelType.MOSTCOMMON)
            for language in self._languages
            if language not in self._most_common_quadrigram_language_models
        ]

        most_common_fivegram_models = [
            _load_ngram_model(language, 5, model_type=_NgramModelType.MOSTCOMMON)
            for language in self._languages
            if language not in self._most_common_fivegram_language_models
        ]

        for most_common_unigram_model in most_common_unigram_models:
            if most_common_unigram_model is not None:
                self._most_common_unigram_language_models[
                    most_common_unigram_model.language
                ] = most_common_unigram_model.ngrams

        for most_common_bigram_model in most_common_bigram_models:
            if most_common_bigram_model is not None:
                self._most_common_bigram_language_models[
                    most_common_bigram_model.language
                ] = most_common_bigram_model.ngrams

        for most_common_trigram_model in most_common_trigram_models:
            if most_common_trigram_model is not None:
                self._most_common_trigram_language_models[
                    most_common_trigram_model.language
                ] = most_common_trigram_model.ngrams

        for most_common_quadrigram_model in most_common_quadrigram_models:
            if most_common_quadrigram_model is not None:
                self._most_common_quadrigram_language_models[
                    most_common_quadrigram_model.language
                ] = most_common_quadrigram_model.ngrams

        for most_common_fivegram_model in most_common_fivegram_models:
            if most_common_fivegram_model is not None:
                self._most_common_fivegram_language_models[
                    most_common_fivegram_model.language
                ] = most_common_fivegram_model.ngrams

    def _preload_language_models(self):
        trigram_models = [
            _load_ngram_probability_model(language, 3)
            for language in self._languages
            if language not in self._trigram_language_models
        ]

        for trigram_model in trigram_models:
            if trigram_model is not None:
                self._trigram_language_models[trigram_model.language] = (
                    trigram_model.ngrams
                )

        if not self._is_low_accuracy_mode_enabled:
            unigram_models = [
                _load_ngram_probability_model(language, 1)
                for language in self._languages
                if language not in self._unigram_language_models
            ]

            bigram_models = [
                _load_ngram_probability_model(language, 2)
                for language in self._languages
                if language not in self._bigram_language_models
            ]

            quadrigram_models = [
                _load_ngram_probability_model(language, 4)
                for language in self._languages
                if language not in self._quadrigram_language_models
            ]

            fivegram_models = [
                _load_ngram_probability_model(language, 5)
                for language in self._languages
                if language not in self._fivegram_language_models
            ]

            for unigram_model in unigram_models:
                if unigram_model is not None:
                    self._unigram_language_models[unigram_model.language] = (
                        unigram_model.ngrams
                    )

            for bigram_model in bigram_models:
                if bigram_model is not None:
                    self._bigram_language_models[bigram_model.language] = (
                        bigram_model.ngrams
                    )

            for quadrigram_model in quadrigram_models:
                if quadrigram_model is not None:
                    self._quadrigram_language_models[quadrigram_model.language] = (
                        quadrigram_model.ngrams
                    )

            for fivegram_model in fivegram_models:
                if fivegram_model is not None:
                    self._fivegram_language_models[fivegram_model.language] = (
                        fivegram_model.ngrams
                    )

    def unload_language_models(self):
        """Clear all language models loaded by this LanguageDetector instance.

        This helps to free allocated memory previously consumed by the models.
        """
        for language in self._languages:
            try:
                self._trigram_language_models.pop(language)

                if not self._is_low_accuracy_mode_enabled:
                    self._unigram_language_models.pop(language)
                    self._bigram_language_models.pop(language)
                    self._quadrigram_language_models.pop(language)
                    self._fivegram_language_models.pop(language)

                if (
                    self._is_built_from_one_language
                    or self._is_low_accuracy_mode_enabled
                ):
                    self._unique_unigram_language_models.pop(language)
                    self._unique_bigram_language_models.pop(language)
                    self._unique_trigram_language_models.pop(language)
                    self._unique_quadrigram_language_models.pop(language)
                    self._unique_fivegram_language_models.pop(language)

                if self._is_built_from_one_language:
                    self._most_common_unigram_language_models.pop(language)
                    self._most_common_bigram_language_models.pop(language)
                    self._most_common_trigram_language_models.pop(language)
                    self._most_common_quadrigram_language_models.pop(language)
                    self._most_common_fivegram_language_models.pop(language)

            except KeyError:
                pass

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
            if most_likely_language_probability == 0.0:
                return None
            return most_likely_language

        second_most_likely_language_probability = confidence_values[1].value

        if most_likely_language_probability == second_most_likely_language_probability:
            return None
        if (
            most_likely_language_probability - second_most_likely_language_probability
            < self._minimum_relative_distance
        ):
            return None

        return most_likely_language

    def detect_multiple_languages_of(self, text: str) -> list[DetectionResult]:
        """Attempt to detect multiple languages in mixed-language text.

        This feature is experimental and under continuous development.

        A list of DetectionResult is returned containing an entry for each
        contiguous single-language text section as identified by the library.
        Each entry consists of the identified language, a start index and an
        end index. The indices denote the substring that has been identified
        as a contiguous single-language text section.

        Args:
            text (str): The text whose language should be identified.

        Returns:
            A list of detection results. Each result contains the
            identified language, the start index and end index of
            the identified single-language substring.
        """
        if len(text) == 0:
            return []

        tokens_without_whitespace = TOKENS_WITHOUT_WHITESPACE.findall(text)
        if len(tokens_without_whitespace) == 0:
            return []

        results = []
        language_counts: Counter[Language] = Counter()

        language = self.detect_language_of(text)
        if language is not None:
            language_counts[language] += 1

        for word in tokens_without_whitespace:
            if len(word) < 5:
                continue
            language = self.detect_language_of(word)
            if language is not None:
                language_counts[language] += 1

        languages = frozenset(language_counts.keys())

        if len(languages) == 1:
            result = DetectionResult(
                start_index=0,
                end_index=len(text),
                word_count=len(tokens_without_whitespace),
                language=next(iter(languages)),
            )
            results.append(result)
        else:
            previous_detector_languages = self._languages.copy()
            self._languages = languages

            current_start_index = 0
            current_end_index = 0
            word_count = 0
            current_language = None
            token_matches = list(TOKENS_WITH_OPTIONAL_WHITESPACE.finditer(text))
            last_index = len(token_matches) - 1

            for i, token_match in enumerate(token_matches):
                word = token_match.group(0)
                language = self.detect_language_of(word)

                if i == 0 or (current_language is None and language is not None):
                    current_language = language

                if (
                    language != current_language
                    and language is not None
                    and current_language is not None
                ):
                    result = DetectionResult(
                        start_index=current_start_index,
                        end_index=current_end_index,
                        word_count=word_count,
                        language=current_language,
                    )
                    results.append(result)
                    current_start_index = current_end_index
                    current_language = language
                    word_count = 0

                current_end_index = token_match.end()
                word_count += 1

                if i == last_index and current_language is not None:
                    result = DetectionResult(
                        start_index=current_start_index,
                        end_index=current_end_index,
                        word_count=word_count,
                        language=current_language,
                    )
                    results.append(result)

            if len(results) > 1:
                mergeable_result_indices = []

                for i, result in enumerate(results):
                    if result.word_count == 1:
                        mergeable_result_indices.append(i)

                _merge_adjacent_results(results, mergeable_result_indices)

                if len(results) > 1:
                    mergeable_result_indices.clear()

                    for i in range(len(results) - 1):
                        if results[i].language == results[i + 1].language:
                            mergeable_result_indices.append(i + 1)

                    _merge_adjacent_results(results, mergeable_result_indices)

            self._languages = previous_detector_languages

        return results

    def compute_language_confidence_values(self, text: str) -> list[ConfidenceValue]:
        """Compute confidence values for each language supported
        by this detector for the given text.

        The confidence values denote how likely it is that the
        given text has been written in any of the languages
        supported by this detector.

        A list is returned containing those languages which the
        calling instance of LanguageDetector has been built from.
        The entries are sorted by their confidence value in
        descending order. Each value is a probability between
        0.0 and 1.0. The probabilities of all languages will sum to 1.0.
        If the language is unambiguously identified by the rule engine,
        the value 1.0 will always be returned for this language. The
        other languages will receive a value of 0.0.

        Args:
            text (str): The text for which to compute confidence values.

        Returns:
            A list of 2-element tuples. Each tuple contains a language
            and the associated confidence value.
        """
        values = [ConfidenceValue(language, 0.0) for language in self._languages]

        words = _split_text_into_words(text)
        if len(words) == 0:
            return values

        if self._is_built_from_one_language or self._is_low_accuracy_mode_enabled:
            language_detected_by_ngrams = (
                self._detect_language_with_unique_and_common_ngrams(words)
            )
            if language_detected_by_ngrams is not None:
                for i in range(len(values)):
                    if values[i].language == language_detected_by_ngrams:
                        values[i] = ConfidenceValue(language_detected_by_ngrams, 1.0)
                        break
                _sort_confidence_values(values)
                return values

        language_detected_by_rules = self._detect_language_with_rules(words)

        if language_detected_by_rules is not None:
            for i in range(len(values)):
                if values[i].language == language_detected_by_rules:
                    values[i] = ConfidenceValue(language_detected_by_rules, 1.0)
                    break
            _sort_confidence_values(values)
            return values

        if self._is_built_from_one_language:
            return values

        filtered_languages = self._filter_languages_by_rules(words)

        if len(filtered_languages) == 1:
            language_detected_by_filter = next(iter(filtered_languages))
            for i in range(len(values)):
                if values[i].language == language_detected_by_filter:
                    values[i] = ConfidenceValue(language_detected_by_filter, 1.0)
                    break
            _sort_confidence_values(values)
            return values

        character_count = sum(len(word) for word in words)

        if self._is_low_accuracy_mode_enabled and character_count < 3:
            _sort_confidence_values(values)
            return values

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
                ngram_model = _create_lower_order_ngrams(words, ngram_length)

                if ngram_length == 1:
                    unigram_counts = self._count_unigrams(
                        ngram_model, filtered_languages
                    )

                probabilities = self._compute_language_probabilities(
                    ngram_model, filtered_languages
                )
                all_probabilities.append(probabilities)

        summed_up_probabilities = _sum_up_probabilities(
            all_probabilities, unigram_counts, filtered_languages
        )

        if len(summed_up_probabilities) == 0:
            _sort_confidence_values(values)
            return values

        denominator = sum(summed_up_probabilities.values())

        for language, probability in summed_up_probabilities.items():
            for i in range(len(values)):
                if values[i].language == language:
                    # apply softmax function
                    normalized_probability = probability / denominator
                    values[i] = ConfidenceValue(language, float(normalized_probability))
                    break

        _sort_confidence_values(values)
        return values

    def compute_language_confidence(self, text: str, language: Language) -> float:
        """Compute the confidence value for the given language and input text.

        The confidence value denotes how likely it is that the given text
        has been written in the given language. The value that this method
        computes is a number between 0.0 and 1.0. If the language is
        unambiguously identified by the rule engine, the value 1.0 will
        always be returned. If the given language is not supported by this
        detector instance, the value 0.0 will always be returned.

        Args:
            text (str): The text for which to compute the confidence value.

            language (Language):
                The language for which to compute the confidence value.

        Returns:
            A float value between 0.0 and 1.0.
        """
        confidence_values = self.compute_language_confidence_values(text)
        for value in confidence_values:
            if value.language == language:
                return value.value
        return 0.0

    def _detect_language_with_unique_and_common_ngrams(
        self, words: list[str]
    ) -> Optional[Language]:
        fivegrams = _create_ngrams(words, ngram_length=5)

        for language in self._languages:
            if language in self._unique_fivegram_language_models:
                for fivegram in fivegrams:
                    if fivegram in self._unique_fivegram_language_models[language]:
                        return language

            if (
                self._is_built_from_one_language
                and language in self._most_common_fivegram_language_models
            ):
                for fivegram in fivegrams:
                    if fivegram in self._most_common_fivegram_language_models[language]:
                        return language

        quadrigrams = _create_ngrams(words, ngram_length=4)

        for language in self._languages:
            if language in self._unique_quadrigram_language_models:
                for quadrigram in quadrigrams:
                    if quadrigram in self._unique_quadrigram_language_models[language]:
                        return language

            if (
                self._is_built_from_one_language
                and language in self._most_common_quadrigram_language_models
            ):
                for quadrigram in quadrigrams:
                    if (
                        quadrigram
                        in self._most_common_quadrigram_language_models[language]
                    ):
                        return language

        trigrams = _create_ngrams(words, ngram_length=3)

        for language in self._languages:
            if language in self._unique_trigram_language_models:
                for trigram in trigrams:
                    if trigram in self._unique_trigram_language_models[language]:
                        return language

            if (
                self._is_built_from_one_language
                and language in self._most_common_trigram_language_models
            ):
                for trigram in trigrams:
                    if trigram in self._most_common_trigram_language_models[language]:
                        return language

        bigrams = _create_ngrams(words, ngram_length=2)

        for language in self._languages:
            if language in self._unique_bigram_language_models:
                for bigram in bigrams:
                    if bigram in self._unique_bigram_language_models[language]:
                        return language

            if (
                language == Language.HINDI
                or language == Language.MARATHI
                or (language == Language.JAPANESE and self._is_built_from_one_language)
                or language in _LANGUAGES_WITH_SINGLE_UNIQUE_SCRIPT
            ):
                unigrams = _create_ngrams(words, ngram_length=1)

                if language in self._unique_unigram_language_models:
                    for unigram in unigrams:
                        if unigram in self._unique_unigram_language_models[language]:
                            return language

                if (
                    self._is_built_from_one_language
                    and language in self._most_common_unigram_language_models
                ):
                    for unigram in unigrams:
                        if (
                            unigram
                            in self._most_common_unigram_language_models[language]
                        ):
                            return language

        return None

    def _detect_language_with_rules(self, words: list[str]) -> Optional[Language]:
        total_language_counts: Counter[Optional[Language]] = Counter()
        half_word_count = len(words) * 0.5
        for word in words:
            word_language_counts: Counter[Language] = Counter()
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

    def _filter_languages_by_rules(self, words: list[str]) -> frozenset[Language]:
        detected_alphabets: Counter[_Alphabet] = Counter()
        half_word_count = len(words) * 0.5

        for word in words:
            for alphabet in _Alphabet:
                if alphabet.matches(word):
                    detected_alphabets[alphabet] += len(word)
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
        language_counts: Counter[Language] = Counter()

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

    def _compute_language_probabilities(
        self,
        ngram_model: list[list[str]],
        filtered_languages: frozenset[Language],
    ) -> dict[Language, float]:
        probabilities = {}
        for language in filtered_languages:
            result = self._compute_sum_of_ngram_probabilities(language, ngram_model)
            if result < 0:
                probabilities[language] = result
        return probabilities

    def _compute_sum_of_ngram_probabilities(
        self, language: Language, ngram_model: list[list[str]]
    ) -> float:
        result = 0.0
        for ngrams in ngram_model:
            for ngram in ngrams:
                probability = self._look_up_ngram_probability(language, ngram)
                if probability is not None:
                    result += probability
                    break
        return result

    def _look_up_ngram_probability(
        self, language: Language, ngram: str
    ) -> Optional[float]:
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

        if language not in language_models:
            model = _load_ngram_probability_model(language, ngram_length)
            if model is None:
                return None
            language_models[model.language] = model.ngrams

        return language_models[language].get(ngram, None)

    def _count_unigrams(
        self,
        unigram_model: list[list[str]],
        filtered_languages: frozenset[Language],
    ) -> Counter[Language]:
        unigram_counts: Counter[Language] = Counter()
        for language in filtered_languages:
            for unigrams in unigram_model:
                if self._look_up_ngram_probability(language, unigrams[0]) is not None:
                    unigram_counts[language] += 1
        return unigram_counts
