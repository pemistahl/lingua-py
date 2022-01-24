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

import regex

from lingua._json import _load_json
from lingua.language import Language


EXPECTED_UNIGRAM_MODEL: str = """
{
    "language":"ENGLISH",
    "ngrams":{
        "2/93616591":"ﬀ ċ ė ĩ ȼ ɔ ţ ũ ʔ ơ ả ộ ù",
        "36/93616591":"ā",
        "16/93616591":"ﬁ",
        "7/93616591":"ă ệ",
        "5/93616591":"ą ħ ś",
        "26/93616591":"ć",
        "49/93616591":"č",
        "8/93616591":"đ ě ź",
        "1/93616591":"ē ț ġ ḵ ņ ɑ ə ɛ ɦ ű ƅ ạ ƴ ặ ế ỉ ờ ủ ứ",
        "4/93616591":"ș ÿ",
        "9/93616591":"ę ż",
        "40/93616591":"ğ",
        "13/93616591":"ī ß",
        "31/93616591":"ı",
        "39/93616591":"ł",
        "25/93616591":"ń",
        "3/93616591":"ň ｍ ů ư ị",
        "10/93616591":"ō",
        "60/93616591":"œ",
        "11/93616591":"ř ì",
        "18/93616591":"ş",
        "52/93616591":"š ô",
        "7915445/93616591":"a",
        "1461095/93616591":"b",
        "3003229/93616591":"c",
        "3622548/93616591":"d",
        "11308892/93616591":"e",
        "2006896/93616591":"f",
        "1963483/93616591":"g",
        "234603/4927189":"h",
        "6800966/93616591":"i",
        "207477/93616591":"j",
        "14/93616591":"ū û",
        "760186/93616591":"k",
        "3928800/93616591":"l",
        "2358339/93616591":"m",
        "6698842/93616591":"n",
        "7137868/93616591":"o",
        "1994813/93616591":"p",
        "82818/93616591":"q",
        "5939665/93616591":"r",
        "6234570/93616591":"s",
        "8431167/93616591":"t",
        "2559048/93616591":"u",
        "1024914/93616591":"v",
        "1751793/93616591":"w",
        "172448/93616591":"x",
        "1683314/93616591":"y",
        "103267/93616591":"z",
        "20/93616591":"ž",
        "37/93616591":"º ë",
        "4/4927189":"à",
        "539/93616591":"á",
        "913/93616591":"â",
        "28/93616591":"ã",
        "118/93616591":"ä",
        "42/93616591":"å",
        "6/93616591":"æ",
        "126/93616591":"ç",
        "136/93616591":"è",
        "2259/93616591":"é",
        "45/93616591":"ê",
        "428/93616591":"í",
        "1/4927189":"î",
        "77/93616591":"ï",
        "21/93616591":"ð",
        "478/93616591":"ñ",
        "48/93616591":"ò",
        "490/93616591":"ó",
        "93/93616591":"õ",
        "200/93616591":"ö",
        "32/93616591":"ø",
        "142/93616591":"ú",
        "149/93616591":"ü",
        "23/93616591":"ý"
    }
}"""


def test_load_json():
    assert _load_json(Language.ENGLISH, ngram_length=1) == minify(
        EXPECTED_UNIGRAM_MODEL
    )


def minify(strng):
    r = regex.compile(r"\n\s*")
    return r.sub("", strng)
