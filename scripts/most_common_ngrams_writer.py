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

from collections import Counter
from pathlib import Path
from typing import Counter as TypedCounter, Dict, List

from lingua import Language, IsoCode639_1
from lingua._constant import LETTERS
from lingua._ngram import _get_ngram_name_by_length


def identify_most_common_ngrams(
    ngram_length: int, most_common: int
) -> Dict[Language, List[str]]:
    result = {}
    relative_directory_path = "../language-testdata/sentences"
    absolute_directory_path = Path(__file__).parent / relative_directory_path

    for sentence_file in absolute_directory_path.iterdir():
        iso_code = sentence_file.parts[-1][:2]
        language = Language.from_iso_code_639_1(IsoCode639_1[iso_code.upper()])
        words = LETTERS.findall(sentence_file.read_text().lower())
        counter: TypedCounter[str] = Counter()

        for word in words:
            for i in range(0, len(word) - ngram_length + 1):
                substr = word[i : i + ngram_length]
                for alphabet in language._alphabets:
                    if alphabet.matches(substr):
                        counter.update([substr])

        most_common_ngrams = [tup[0] for tup in counter.most_common(most_common)]
        result[language] = most_common_ngrams

    return result


def store_most_common_ngrams(
    most_common_ngrams: Dict[Language, List[str]], ngram_length: int
):
    ngram_name = _get_ngram_name_by_length(ngram_length)
    for language, ngrams in most_common_ngrams.items():
        obj = {"language": language.name, "ngrams": ngrams}
        json_data = json.dumps(obj, ensure_ascii=False)
        compressed_json = brotli.compress(
            json_data.encode("utf-8"), mode=brotli.MODE_TEXT
        )
        iso_code = language.iso_code_639_1.name.lower()
        relative_brotli_file_path = (
            f"../lingua/language-models/{iso_code}/mostcommon_{ngram_name}s.json.br"
        )
        absolute_brotli_file_path = Path(__file__).parent / relative_brotli_file_path
        with open(absolute_brotli_file_path, mode="wb") as brotli_file:
            brotli_file.write(compressed_json)


if __name__ == "__main__":
    for ngram_length in range(1, 6):
        ngram_name = _get_ngram_name_by_length(ngram_length)
        print(f"Storing most common {ngram_name}s...")
        ngrams = identify_most_common_ngrams(ngram_length, most_common=25)
        store_most_common_ngrams(ngrams, ngram_length)
        print("Done\n")
