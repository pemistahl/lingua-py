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

from collections import defaultdict
from pathlib import Path

from lingua import Language
from lingua._model import _load_ngram_probability_model
from lingua._ngram import _get_ngram_name_by_length


def load_ngrams(ngram_length: int) -> dict[Language, frozenset[str]]:
    result = {}
    for language in Language:
        model = _load_ngram_probability_model(language, ngram_length)
        if model is not None:
            result[model.language] = frozenset(model.ngrams)
    return result


def identify_unique_ngrams(
    ngrams: dict[Language, frozenset[str]]
) -> dict[Language, set[str]]:
    unique_ngrams: set[str] = set()
    for ngrams_i in ngrams.values():
        current = ngrams_i
        for ngrams_j in ngrams.values():
            if ngrams_j is not ngrams_i:
                current = current - ngrams_j
        unique_ngrams = unique_ngrams.union(current)

    result = defaultdict(set)
    for unique_ngram in unique_ngrams:
        for language in ngrams:
            if unique_ngram in ngrams[language]:
                result[language].add(unique_ngram)
                break
    return result


def store_unique_ngrams(unique_ngrams: dict[Language, set[str]], ngram_length: int):
    ngram_name = _get_ngram_name_by_length(ngram_length)
    for language, ngrams in unique_ngrams.items():
        obj = {"language": language.name, "ngrams": list(ngrams)}
        json_data = json.dumps(obj, ensure_ascii=False)
        compressed_json = brotli.compress(
            json_data.encode("utf-8"), mode=brotli.MODE_TEXT
        )
        iso_code = language.iso_code_639_1.name.lower()
        relative_brotli_file_path = (
            f"../lingua/language-models/{iso_code}/unique_{ngram_name}s.json.br"
        )
        absolute_brotli_file_path = Path(__file__).parent / relative_brotli_file_path
        with open(absolute_brotli_file_path, mode="wb") as brotli_file:
            brotli_file.write(compressed_json)


if __name__ == "__main__":
    for ngram_length in range(1, 6):
        ngram_name = _get_ngram_name_by_length(ngram_length)
        print(f"Storing unique {ngram_name}s...")
        ngrams = load_ngrams(ngram_length)
        unique_ngrams = identify_unique_ngrams(ngrams)
        store_unique_ngrams(unique_ngrams, ngram_length)
        print("Done\n")
