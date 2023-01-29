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

import pytest
from lingua._ngram import _NgramRange


def test_ngram_iterator():
    ngram = "äbcde"
    ngram_range = _NgramRange(ngram)

    assert next(ngram_range) == "äbcde"
    assert next(ngram_range) == "äbcd"
    assert next(ngram_range) == "äbc"
    assert next(ngram_range) == "äb"
    assert next(ngram_range) == "ä"

    with pytest.raises(StopIteration):
        next(ngram_range)
