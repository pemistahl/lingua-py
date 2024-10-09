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

import brotli
import json
import regex

from collections import Counter, defaultdict, OrderedDict
from dataclasses import dataclass
from enum import Enum, auto
from fractions import Fraction
from math import log
from pathlib import Path
from typing import Any, Counter as TypedCounter, Dict, FrozenSet, List, Optional

from .language import Language
from ._ngram import _NgramRange, _get_ngram_name_by_length


class _NgramProbabilitiesJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, _TrainingDataLanguageModel):
            language = obj.language.name
            ngrams = self.encode_frequencies(obj.relative_frequencies)
            return {"language": language, "ngrams": ngrams}
        return json.JSONEncoder.default(self, obj)

    def encode_frequencies(self, obj: Optional[Dict[str, Fraction]]) -> Dict[str, str]:
        fractions_to_ngrams = defaultdict(list)
        if obj is not None:
            for ngram, fraction in obj.items():
                fractions_to_ngrams[fraction].append(ngram)

        fractions_to_joined_ngrams = OrderedDict()
        for fraction, ngrams in fractions_to_ngrams.items():
            fraction_str = f"{fraction.numerator}/{fraction.denominator}"
            fractions_to_joined_ngrams[fraction_str] = " ".join(
                sorted(map(lambda n: n, ngrams))
            )
        return fractions_to_joined_ngrams


class _NgramProbabilitiesJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: Any) -> Any:
        if isinstance(obj, dict) and "language" in obj and "ngrams" in obj:
            language = Language[obj["language"]]
            ngrams = self.parse_frequencies(obj["ngrams"])
            return _NgramProbabilityModel(language, ngrams)
        return obj

    def parse_frequencies(self, obj: Dict[str, str]) -> Dict[str, float]:
        frequencies = {}
        for fraction, ngrams in obj.items():
            numerator, denominator = fraction.split("/")
            frequency = log(int(numerator) / int(denominator))
            for ngram in ngrams.split(" "):
                frequencies[ngram] = frequency
        return frequencies


class _NgramsJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: Any) -> Any:
        if isinstance(obj, dict) and "language" in obj and "ngrams" in obj:
            language = Language[obj["language"]]
            ngrams = self.object_hook(obj["ngrams"])
            return _NgramModel(language, frozenset(ngrams))
        return obj


@dataclass
class _NgramProbabilityModel:
    language: Language
    ngrams: Dict[str, float]


@dataclass
class _NgramModel:
    language: Language
    ngrams: FrozenSet[str]


class _NgramModelType(Enum):
    UNIQUE = auto()
    MOSTCOMMON = auto()


def _load_ngram_probability_model(
    language: Language, ngram_length: int
) -> Optional[_NgramProbabilityModel]:
    ngram_name = _get_ngram_name_by_length(ngram_length)
    iso_code = language.iso_code_639_1.name.lower()
    relative_file_path = f"./language-models/{iso_code}/{ngram_name}s.json.br"
    absolute_file_path = Path(__file__).parent / relative_file_path
    try:
        with open(absolute_file_path, mode="rb") as ngrams_file:
            ngrams_json = brotli.decompress(ngrams_file.read()).decode("utf-8")
            return json.loads(ngrams_json, cls=_NgramProbabilitiesJSONDecoder)
    except FileNotFoundError:
        return None


def _load_ngram_model(
    language: Language, ngram_length: int, model_type: _NgramModelType
) -> Optional[_NgramModel]:
    ngram_name = _get_ngram_name_by_length(ngram_length)
    iso_code = language.iso_code_639_1.name.lower()
    relative_file_path = (
        f"./language-models/{iso_code}/{model_type.name.lower()}_{ngram_name}s.json.br"
    )
    absolute_file_path = Path(__file__).parent / relative_file_path
    try:
        with open(absolute_file_path, mode="rb") as unique_ngrams_file:
            unique_ngrams_json = brotli.decompress(unique_ngrams_file.read()).decode(
                "utf-8"
            )
            return json.loads(unique_ngrams_json, cls=_NgramsJSONDecoder)
    except FileNotFoundError:
        return None


@dataclass
class _TrainingDataLanguageModel:
    language: Language
    absolute_frequencies: Optional[Dict[str, int]]
    relative_frequencies: Optional[Dict[str, Fraction]]

    @classmethod
    def from_text(
        cls,
        text: List[str],
        language: Language,
        ngram_length: int,
        char_class: str,
        lower_ngram_absolute_frequencies: Optional[Dict[str, int]],
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
        )

    def to_json(self) -> str:
        return regex.sub(
            r"([:,])\s*",
            r"\1",
            json.dumps(self, ensure_ascii=False, cls=_NgramProbabilitiesJSONEncoder),
        )

    @classmethod
    def compute_absolute_frequencies(
        cls, text: List[str], ngram_length: int, char_class: str
    ) -> Dict[str, int]:
        absolute_frequencies: TypedCounter[str] = Counter()
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
        absolute_frequencies: Dict[str, int],
        lower_ngram_absolute_frequencies: Optional[Dict[str, int]],
    ) -> Dict[str, Fraction]:
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


def _create_ngrams(words: List[str], ngram_length: int) -> FrozenSet[str]:
    if ngram_length not in range(1, 6):
        raise ValueError(f"ngram length {ngram_length} is not in range 1..6")
    ngrams = set()
    for word in words:
        chars_count = len(word)
        if chars_count >= ngram_length:
            for i in range(0, chars_count - ngram_length + 1):
                substr = word[i : i + ngram_length]
                ngrams.add(substr)
    return frozenset(ngrams)


def _create_lower_order_ngrams(words: List[str], ngram_length: int) -> List[List[str]]:
    ngrams = _create_ngrams(words, ngram_length)
    return [list(_NgramRange(ngram)) for ngram in ngrams]
