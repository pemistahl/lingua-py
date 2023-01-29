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


class _NgramRange(object):
    def __init__(self, start: str):
        self.start = start

    def __iter__(self):
        return self

    def __next__(self) -> str:
        value = self.start
        length = len(value)
        if length == 0:
            raise StopIteration()
        result = self.start
        new_value = value[: length - 1]
        self.start = new_value
        return result


def _get_ngram_name_by_length(ngram_length: int) -> str:
    if ngram_length == 1:
        return "unigram"
    elif ngram_length == 2:
        return "bigram"
    elif ngram_length == 3:
        return "trigram"
    elif ngram_length == 4:
        return "quadrigram"
    elif ngram_length == 5:
        return "fivegram"
    else:
        raise ValueError(f"ngram length {ngram_length} is not in range 1..6")
