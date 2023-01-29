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

import math
import numpy as np
import regex

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Counter as TypedCounter, Dict, List, Optional

from .language import Language
from ._ngram import _get_ngram_name_by_length, _NgramRange


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

    @classmethod
    def from_numpy_binary_file(
        cls, language: Language, ngram_length: int
    ) -> Optional[np.ndarray]:
        ngram_name = _get_ngram_name_by_length(ngram_length)
        iso_code = language.iso_code_639_1.name.lower()
        relative_file_path = f"./language-models/{iso_code}/{ngram_name}s.npz"
        absolute_file_path = Path(__file__).parent / relative_file_path
        try:
            with np.load(absolute_file_path) as data:
                return data["arr"]
        except OSError:
            return None

    def to_numpy_binary_file(self, file_path: Path, ngram_length: int):
        frequencies = []
        if self.relative_frequencies is not None:
            for ngram, fraction in self.relative_frequencies.items():
                frequency = math.log(fraction.numerator / fraction.denominator)
                frequencies.append((ngram, frequency))

        dtype = [("ngram", f"U{ngram_length}"), ("frequency", "f2")]
        arr = np.array(frequencies, dtype=dtype)
        arr.sort()

        np.savez_compressed(file_path, arr=arr)

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


@dataclass
class _TestDataLanguageModel:
    ngrams: List[List[str]]

    @classmethod
    def from_text(cls, words: List[str], ngram_length: int) -> "_TestDataLanguageModel":
        if ngram_length not in range(1, 6):
            raise ValueError(f"ngram length {ngram_length} is not in range 1..6")
        ngrams = set()
        for word in words:
            chars_count = len(word)
            if chars_count >= ngram_length:
                for i in range(0, chars_count - ngram_length + 1):
                    substr = word[i : i + ngram_length]
                    ngrams.add(substr)

        lower_order_ngrams = [list(_NgramRange(ngram)) for ngram in ngrams]
        return _TestDataLanguageModel(lower_order_ngrams)
