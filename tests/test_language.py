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

from lingua.isocode import IsoCode639_1, IsoCode639_3
from lingua.language import Language


def test_all_languages_are_available():
    assert Language.all() == frozenset(
        [
            Language.AFRIKAANS,
            Language.ALBANIAN,
            Language.ARABIC,
            Language.ARMENIAN,
            Language.AZERBAIJANI,
            Language.BASQUE,
            Language.BELARUSIAN,
            Language.BENGALI,
            Language.BOKMAL,
            Language.BOSNIAN,
            Language.BULGARIAN,
            Language.CATALAN,
            Language.CHINESE,
            Language.CROATIAN,
            Language.CZECH,
            Language.DANISH,
            Language.DUTCH,
            Language.ENGLISH,
            Language.ESPERANTO,
            Language.ESTONIAN,
            Language.FINNISH,
            Language.FRENCH,
            Language.GANDA,
            Language.GEORGIAN,
            Language.GERMAN,
            Language.GREEK,
            Language.GUJARATI,
            Language.HEBREW,
            Language.HINDI,
            Language.HUNGARIAN,
            Language.ICELANDIC,
            Language.INDONESIAN,
            Language.IRISH,
            Language.ITALIAN,
            Language.JAPANESE,
            Language.KAZAKH,
            Language.KOREAN,
            Language.LATIN,
            Language.LATVIAN,
            Language.LITHUANIAN,
            Language.MACEDONIAN,
            Language.MALAY,
            Language.MAORI,
            Language.MARATHI,
            Language.MONGOLIAN,
            Language.NYNORSK,
            Language.PERSIAN,
            Language.POLISH,
            Language.PORTUGUESE,
            Language.PUNJABI,
            Language.ROMANIAN,
            Language.RUSSIAN,
            Language.SERBIAN,
            Language.SHONA,
            Language.SLOVAK,
            Language.SLOVENE,
            Language.SOMALI,
            Language.SOTHO,
            Language.SPANISH,
            Language.SWAHILI,
            Language.SWEDISH,
            Language.TAGALOG,
            Language.TAMIL,
            Language.TELUGU,
            Language.THAI,
            Language.TSONGA,
            Language.TSWANA,
            Language.TURKISH,
            Language.UKRAINIAN,
            Language.URDU,
            Language.VIETNAMESE,
            Language.WELSH,
            Language.XHOSA,
            Language.YORUBA,
            Language.ZULU,
        ]
    )


def test_all_spoken_languages_are_available():
    assert Language.all_spoken_ones() == frozenset(
        [
            Language.AFRIKAANS,
            Language.ALBANIAN,
            Language.ARABIC,
            Language.ARMENIAN,
            Language.AZERBAIJANI,
            Language.BASQUE,
            Language.BELARUSIAN,
            Language.BENGALI,
            Language.BOKMAL,
            Language.BOSNIAN,
            Language.BULGARIAN,
            Language.CATALAN,
            Language.CHINESE,
            Language.CROATIAN,
            Language.CZECH,
            Language.DANISH,
            Language.DUTCH,
            Language.ENGLISH,
            Language.ESPERANTO,
            Language.ESTONIAN,
            Language.FINNISH,
            Language.FRENCH,
            Language.GANDA,
            Language.GEORGIAN,
            Language.GERMAN,
            Language.GREEK,
            Language.GUJARATI,
            Language.HEBREW,
            Language.HINDI,
            Language.HUNGARIAN,
            Language.ICELANDIC,
            Language.INDONESIAN,
            Language.IRISH,
            Language.ITALIAN,
            Language.JAPANESE,
            Language.KAZAKH,
            Language.KOREAN,
            Language.LATVIAN,
            Language.LITHUANIAN,
            Language.MACEDONIAN,
            Language.MALAY,
            Language.MAORI,
            Language.MARATHI,
            Language.MONGOLIAN,
            Language.NYNORSK,
            Language.PERSIAN,
            Language.POLISH,
            Language.PORTUGUESE,
            Language.PUNJABI,
            Language.ROMANIAN,
            Language.RUSSIAN,
            Language.SERBIAN,
            Language.SHONA,
            Language.SLOVAK,
            Language.SLOVENE,
            Language.SOMALI,
            Language.SOTHO,
            Language.SPANISH,
            Language.SWAHILI,
            Language.SWEDISH,
            Language.TAGALOG,
            Language.TAMIL,
            Language.TELUGU,
            Language.THAI,
            Language.TSONGA,
            Language.TSWANA,
            Language.TURKISH,
            Language.UKRAINIAN,
            Language.URDU,
            Language.VIETNAMESE,
            Language.WELSH,
            Language.XHOSA,
            Language.YORUBA,
            Language.ZULU,
        ]
    )


def test_languages_support_arabic_script():
    assert Language.all_with_arabic_script() == frozenset(
        [Language.ARABIC, Language.PERSIAN, Language.URDU]
    )


def test_languages_support_cyrillic_alphabet():
    assert Language.all_with_cyrillic_script() == frozenset(
        [
            Language.BELARUSIAN,
            Language.BULGARIAN,
            Language.KAZAKH,
            Language.MACEDONIAN,
            Language.MONGOLIAN,
            Language.RUSSIAN,
            Language.SERBIAN,
            Language.UKRAINIAN,
        ]
    )


def test_languages_support_devanagari_script():
    assert Language.all_with_devanagari_script() == frozenset(
        [Language.HINDI, Language.MARATHI]
    )


def test_languages_support_latin_script():
    assert Language.all_with_latin_script() == frozenset(
        [
            Language.AFRIKAANS,
            Language.ALBANIAN,
            Language.AZERBAIJANI,
            Language.BASQUE,
            Language.BOKMAL,
            Language.BOSNIAN,
            Language.CATALAN,
            Language.CROATIAN,
            Language.CZECH,
            Language.DANISH,
            Language.DUTCH,
            Language.ENGLISH,
            Language.ESPERANTO,
            Language.ESTONIAN,
            Language.FINNISH,
            Language.FRENCH,
            Language.GANDA,
            Language.GERMAN,
            Language.HUNGARIAN,
            Language.ICELANDIC,
            Language.INDONESIAN,
            Language.IRISH,
            Language.ITALIAN,
            Language.LATIN,
            Language.LATVIAN,
            Language.LITHUANIAN,
            Language.MALAY,
            Language.MAORI,
            Language.NYNORSK,
            Language.POLISH,
            Language.PORTUGUESE,
            Language.ROMANIAN,
            Language.SHONA,
            Language.SLOVAK,
            Language.SLOVENE,
            Language.SOMALI,
            Language.SOTHO,
            Language.SPANISH,
            Language.SWAHILI,
            Language.SWEDISH,
            Language.TAGALOG,
            Language.TSONGA,
            Language.TSWANA,
            Language.TURKISH,
            Language.VIETNAMESE,
            Language.WELSH,
            Language.XHOSA,
            Language.YORUBA,
            Language.ZULU,
        ]
    )


def test_language_from_iso_code_639_1():
    assert Language.from_iso_code_639_1(IsoCode639_1.DE) == Language.GERMAN


def test_language_from_iso_code_639_3():
    assert Language.from_iso_code_639_3(IsoCode639_3.DEU) == Language.GERMAN
