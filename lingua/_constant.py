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

import regex
from regex import Pattern
from typing import Dict, FrozenSet

from .language import Language

JAPANESE_CHARACTER_SET: Pattern = regex.compile(r"^[\p{Hiragana}\p{Katakana}\p{Han}]+$")
MULTIPLE_WHITESPACE: Pattern = regex.compile(r"\s+")
NUMBERS: Pattern = regex.compile(r"\p{N}")
PUNCTUATION: Pattern = regex.compile(r"\p{P}")
LETTERS: Pattern = regex.compile(r"\p{Han}|\p{Hangul}|\p{Hiragana}|\p{Katakana}|\p{L}+")
TOKENS_WITH_OPTIONAL_WHITESPACE = regex.compile(
    r"\s*(?:\p{Han}|\p{Hangul}|\p{Hiragana}|\p{Katakana}|[\p{L}'-]+)[\p{N}\p{P}]*\s*"
)
TOKENS_WITHOUT_WHITESPACE = regex.compile(
    r"\p{Han}|\p{Hangul}|\p{Hiragana}|\p{Katakana}|\p{L}+"
)

CHARS_TO_LANGUAGES_MAPPING: Dict[str, FrozenSet[Language]] = {
    "Ãã": frozenset([Language.PORTUGUESE, Language.VIETNAMESE]),
    "ĄąĘę": frozenset([Language.LITHUANIAN, Language.POLISH]),
    "Żż": frozenset([Language.POLISH, Language.ROMANIAN]),
    "Îî": frozenset([Language.FRENCH, Language.ROMANIAN]),
    "Ññ": frozenset([Language.BASQUE, Language.SPANISH]),
    "ŇňŤť": frozenset([Language.CZECH, Language.SLOVAK]),
    "Ăă": frozenset([Language.ROMANIAN, Language.VIETNAMESE]),
    "İıĞğ": frozenset([Language.AZERBAIJANI, Language.TURKISH]),
    "ЈјЉљЊњ": frozenset([Language.MACEDONIAN, Language.SERBIAN]),
    "ẸẹỌọ": frozenset([Language.VIETNAMESE, Language.YORUBA]),
    "ÐðÞþ": frozenset([Language.ICELANDIC, Language.TURKISH]),
    "Ûû": frozenset([Language.FRENCH, Language.HUNGARIAN]),
    "Ōō": frozenset([Language.MAORI, Language.YORUBA]),
    "ӨөҮү": frozenset([Language.KAZAKH, Language.MONGOLIAN]),
    "ĀāĒēĪī": frozenset([Language.LATVIAN, Language.MAORI, Language.YORUBA]),
    "Şş": frozenset([Language.AZERBAIJANI, Language.ROMANIAN, Language.TURKISH]),
    "Ďď": frozenset([Language.CZECH, Language.ROMANIAN, Language.SLOVAK]),
    "Ćć": frozenset([Language.BOSNIAN, Language.CROATIAN, Language.POLISH]),
    "Đđ": frozenset([Language.BOSNIAN, Language.CROATIAN, Language.VIETNAMESE]),
    "Іі": frozenset([Language.BELARUSIAN, Language.KAZAKH, Language.UKRAINIAN]),
    "Ìì": frozenset([Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA]),
    "Øø": frozenset([Language.BOKMAL, Language.DANISH, Language.NYNORSK]),
    "Ūū": frozenset(
        [Language.LATVIAN, Language.LITHUANIAN, Language.MAORI, Language.YORUBA]
    ),
    "Ëë": frozenset(
        [Language.AFRIKAANS, Language.ALBANIAN, Language.DUTCH, Language.FRENCH]
    ),
    "ÈèÙù": frozenset(
        [Language.FRENCH, Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA]
    ),
    "Êê": frozenset(
        [Language.AFRIKAANS, Language.FRENCH, Language.PORTUGUESE, Language.VIETNAMESE]
    ),
    "Õõ": frozenset(
        [
            Language.ESTONIAN,
            Language.HUNGARIAN,
            Language.PORTUGUESE,
            Language.VIETNAMESE,
        ]
    ),
    "Ôô": frozenset(
        [Language.FRENCH, Language.PORTUGUESE, Language.SLOVAK, Language.VIETNAMESE]
    ),
    "ЁёЫыЭэ": frozenset(
        [Language.BELARUSIAN, Language.KAZAKH, Language.MONGOLIAN, Language.RUSSIAN]
    ),
    "ЩщЪъ": frozenset(
        [Language.BULGARIAN, Language.KAZAKH, Language.MONGOLIAN, Language.RUSSIAN]
    ),
    "Òò": frozenset(
        [Language.CATALAN, Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA]
    ),
    "Ææ": frozenset(
        [Language.BOKMAL, Language.DANISH, Language.ICELANDIC, Language.NYNORSK]
    ),
    "Åå": frozenset(
        [Language.BOKMAL, Language.DANISH, Language.NYNORSK, Language.SWEDISH]
    ),
    "Ââ": frozenset(
        [
            Language.FRENCH,
            Language.PORTUGUESE,
            Language.ROMANIAN,
            Language.TURKISH,
            Language.VIETNAMESE,
        ]
    ),
    "Ýý": frozenset(
        [
            Language.CZECH,
            Language.ICELANDIC,
            Language.SLOVAK,
            Language.TURKISH,
            Language.VIETNAMESE,
        ]
    ),
    "Ää": frozenset(
        [
            Language.ESTONIAN,
            Language.FINNISH,
            Language.GERMAN,
            Language.SLOVAK,
            Language.SWEDISH,
        ]
    ),
    "Àà": frozenset(
        [
            Language.CATALAN,
            Language.FRENCH,
            Language.ITALIAN,
            Language.PORTUGUESE,
            Language.VIETNAMESE,
        ]
    ),
    "Üü": frozenset(
        [
            Language.AZERBAIJANI,
            Language.CATALAN,
            Language.ESTONIAN,
            Language.GERMAN,
            Language.HUNGARIAN,
            Language.SPANISH,
            Language.TURKISH,
        ]
    ),
    "ČčŠšŽž": frozenset(
        [
            Language.BOSNIAN,
            Language.CZECH,
            Language.CROATIAN,
            Language.LATVIAN,
            Language.LITHUANIAN,
            Language.SLOVAK,
            Language.SLOVENE,
        ]
    ),
    "Çç": frozenset(
        [
            Language.ALBANIAN,
            Language.AZERBAIJANI,
            Language.BASQUE,
            Language.CATALAN,
            Language.FRENCH,
            Language.GERMAN,
            Language.PORTUGUESE,
            Language.TURKISH,
        ]
    ),
    "Öö": frozenset(
        [
            Language.AZERBAIJANI,
            Language.ESTONIAN,
            Language.FINNISH,
            Language.GERMAN,
            Language.HUNGARIAN,
            Language.ICELANDIC,
            Language.SWEDISH,
            Language.TURKISH,
        ]
    ),
    "Óó": frozenset(
        [
            Language.CATALAN,
            Language.GERMAN,
            Language.HUNGARIAN,
            Language.ICELANDIC,
            Language.IRISH,
            Language.POLISH,
            Language.PORTUGUESE,
            Language.SLOVAK,
            Language.SPANISH,
            Language.VIETNAMESE,
            Language.YORUBA,
        ]
    ),
    "ÁáÍíÚú": frozenset(
        [
            Language.CATALAN,
            Language.CZECH,
            Language.GERMAN,
            Language.ICELANDIC,
            Language.IRISH,
            Language.HUNGARIAN,
            Language.PORTUGUESE,
            Language.SLOVAK,
            Language.SPANISH,
            Language.VIETNAMESE,
            Language.YORUBA,
        ]
    ),
    "Éé": frozenset(
        [
            Language.CATALAN,
            Language.CZECH,
            Language.FRENCH,
            Language.GERMAN,
            Language.HUNGARIAN,
            Language.ICELANDIC,
            Language.IRISH,
            Language.ITALIAN,
            Language.PORTUGUESE,
            Language.SLOVAK,
            Language.SPANISH,
            Language.VIETNAMESE,
            Language.YORUBA,
        ]
    ),
}
