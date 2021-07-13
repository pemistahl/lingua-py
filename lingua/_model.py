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

import json
import math
import regex

from collections import defaultdict, Counter, OrderedDict
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Any

from ._constant import LETTER
from .language import Language


class _LinguaJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, _JSONLanguageModel):
            return {"language": obj.language.name, "ngrams": obj.ngrams}
        return json.JSONEncoder.default(self, obj)


class _LinguaJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: Any) -> Any:
        if isinstance(obj, dict) and "language" in obj and "ngrams" in obj:
            language = Language[obj["language"]]
            ngrams = self.object_hook(obj["ngrams"])
            return _JSONLanguageModel(language, ngrams)
        return obj


@dataclass
class _JSONLanguageModel:
    language: Language
    ngrams: dict[str, str]


@dataclass
class _TrainingDataLanguageModel:
    language: Language
    absolute_frequencies: Optional[dict[str, int]]
    relative_frequencies: Optional[dict[str, Fraction]]
    json_relative_frequencies: Optional[dict[str, float]]

    @classmethod
    def from_text(
        cls,
        text: list[str],
        language: Language,
        ngram_length: int,
        char_class: str,
        lower_ngram_absolute_frequencies: Optional[dict[str, int]],
    ) -> "_TrainingDataLanguageModel":
        absolute_frequencies = cls.compute_absolute_frequencies(
            text, ngram_length, char_class
        )
        relative_frequencies = cls.compute_relative_frequencies(
            ngram_length, absolute_frequencies, lower_ngram_absolute_frequencies
        )
        return _TrainingDataLanguageModel(
            language=language,
            absolute_frequencies=absolute_frequencies,
            relative_frequencies=relative_frequencies,
            json_relative_frequencies=None,
        )

    @classmethod
    def from_json(cls, serialized_json: str) -> "_TrainingDataLanguageModel":
        json_language_model: _JSONLanguageModel = json.loads(
            serialized_json, cls=_LinguaJSONDecoder
        )
        json_relative_frequencies = {}

        for fraction, ngrams in json_language_model.ngrams.items():
            numerator, denominator = fraction.split("/")
            frequency = math.log(int(numerator) / int(denominator))
            for ngram in ngrams.split(" "):
                json_relative_frequencies[ngram] = frequency

        return _TrainingDataLanguageModel(
            language=json_language_model.language,
            absolute_frequencies=None,
            relative_frequencies=None,
            json_relative_frequencies=json_relative_frequencies,
        )

    def to_json(self) -> str:
        fractions_to_ngrams = defaultdict(list)
        if self.relative_frequencies is not None:
            for ngram, fraction in self.relative_frequencies.items():
                fractions_to_ngrams[fraction].append(ngram)

        fractions_to_joined_ngrams = OrderedDict()
        for fraction, ngrams in fractions_to_ngrams.items():
            fraction_str = f"{fraction.numerator}/{fraction.denominator}"
            fractions_to_joined_ngrams[fraction_str] = " ".join(
                sorted(map(lambda n: n, ngrams))
            )

        model = _JSONLanguageModel(self.language, fractions_to_joined_ngrams)
        return regex.sub(r"([:,])\s*", r"\1", json.dumps(model, cls=_LinguaJSONEncoder))

    def get_relative_frequency(self, ngram: str) -> float:
        if (
            self.json_relative_frequencies is None
            or ngram not in self.json_relative_frequencies
        ):
            return 0.0
        return self.json_relative_frequencies[ngram]

    @classmethod
    def compute_absolute_frequencies(
        cls, text: list[str], ngram_length: int, char_class: str
    ) -> dict[str, int]:
        absolute_frequencies = Counter[str]()
        regexp = regex.compile(r"^[{}]+$".format(char_class))
        for line in text:
            lowercased_line = line.lower()
            for i in range(0, len(lowercased_line) - ngram_length + 1):
                substr = lowercased_line[i : i + ngram_length]
                if regexp.match(substr) is not None:
                    absolute_frequencies.update([substr])
        return absolute_frequencies

    @classmethod
    def compute_relative_frequencies(
        cls,
        ngram_length: int,
        absolute_frequencies: dict[str, int],
        lower_ngram_absolute_frequencies: Optional[dict[str, int]],
    ) -> dict[str, Fraction]:
        if lower_ngram_absolute_frequencies is None:
            return {}
        ngram_probabilities = {}
        total_ngram_frequency = sum(absolute_frequencies.values())
        for ngram, frequency in absolute_frequencies.items():
            if ngram_length == 1 or len(lower_ngram_absolute_frequencies) == 0:
                denominator = total_ngram_frequency
            else:
                substr = ngram[: ngram_length - 1]
                denominator = lower_ngram_absolute_frequencies[substr]
            ngram_probabilities[ngram] = Fraction(frequency, denominator)
        return ngram_probabilities


@dataclass
class _TestDataLanguageModel:
    ngrams: frozenset[str]

    @classmethod
    def from_text(cls, text: str, ngram_length: int) -> "_TestDataLanguageModel":
        if ngram_length not in range(1, 6):
            raise ValueError(f"ngram length {ngram_length} is not in range 1..6")
        ngrams = set()
        text_length = len(text)
        if text_length >= ngram_length:
            for i in range(0, text_length - ngram_length + 1):
                substr = text[i : i + ngram_length]
                if LETTER.fullmatch(substr) is not None:
                    ngrams.add(substr)
        return _TestDataLanguageModel(frozenset(ngrams))
