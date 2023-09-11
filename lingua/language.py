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

from enum import Enum
from functools import total_ordering
from typing import Dict, FrozenSet, List, Optional, Pattern

from .isocode import IsoCode639_1, IsoCode639_3


def _pattern(char_class: str) -> Pattern[str]:
    return regex.compile(r"^\p{{Is{}}}+$".format(char_class))


class _Alphabet(Enum):
    ARABIC = (1, _pattern("Arabic"))
    ARMENIAN = (2, _pattern("Armenian"))
    BENGALI = (3, _pattern("Bengali"))
    CYRILLIC = (4, _pattern("Cyrillic"))
    DEVANAGARI = (5, _pattern("Devanagari"))
    GEORGIAN = (6, _pattern("Georgian"))
    GREEK = (7, _pattern("Greek"))
    GUJARATI = (8, _pattern("Gujarati"))
    GURMUKHI = (9, _pattern("Gurmukhi"))
    HAN = (10, _pattern("Han"))
    HANGUL = (11, _pattern("Hangul"))
    HEBREW = (12, _pattern("Hebrew"))
    HIRAGANA = (13, _pattern("Hiragana"))
    KATAKANA = (14, _pattern("Katakana"))
    LATIN = (15, _pattern("Latin"))
    TAMIL = (16, _pattern("Tamil"))
    TELUGU = (17, _pattern("Telugu"))
    THAI = (18, _pattern("Thai"))

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, _: int, pattern: Pattern[str]):
        self._pattern = pattern

    def matches(self, text: str) -> bool:
        return self._pattern.match(text) is not None

    @classmethod
    def all_supporting_single_language(cls) -> Dict["_Alphabet", "Language"]:
        alphabets = {}
        for alphabet in _Alphabet:
            supported_languages = alphabet._supported_languages()
            if len(supported_languages) == 1:
                alphabets[alphabet] = supported_languages[0]
        return alphabets

    def _supported_languages(self) -> List["Language"]:
        languages = []
        for language in Language:
            if self in language._alphabets:
                languages.append(language)
        return languages


@total_ordering
class Language(Enum):
    """This enum specifies the so far 75 supported languages which can be
    detected by *Lingua*.
    """

    AFRIKAANS = (
        1,
        IsoCode639_1.AF,
        IsoCode639_3.AFR,
        frozenset([_Alphabet.LATIN]),
    )
    ALBANIAN = (2, IsoCode639_1.SQ, IsoCode639_3.SQI, frozenset([_Alphabet.LATIN]))
    ARABIC = (3, IsoCode639_1.AR, IsoCode639_3.ARA, frozenset([_Alphabet.ARABIC]))
    ARMENIAN = (
        4,
        IsoCode639_1.HY,
        IsoCode639_3.HYE,
        frozenset([_Alphabet.ARMENIAN]),
    )
    AZERBAIJANI = (
        5,
        IsoCode639_1.AZ,
        IsoCode639_3.AZE,
        frozenset([_Alphabet.LATIN]),
        "Əə",
    )
    BASQUE = (6, IsoCode639_1.EU, IsoCode639_3.EUS, frozenset([_Alphabet.LATIN]))
    BELARUSIAN = (
        7,
        IsoCode639_1.BE,
        IsoCode639_3.BEL,
        frozenset([_Alphabet.CYRILLIC]),
    )
    BENGALI = (
        8,
        IsoCode639_1.BN,
        IsoCode639_3.BEN,
        frozenset([_Alphabet.BENGALI]),
    )
    BOKMAL = (9, IsoCode639_1.NB, IsoCode639_3.NOB, frozenset([_Alphabet.LATIN]))
    BOSNIAN = (10, IsoCode639_1.BS, IsoCode639_3.BOS, frozenset([_Alphabet.LATIN]))
    BULGARIAN = (
        11,
        IsoCode639_1.BG,
        IsoCode639_3.BUL,
        frozenset([_Alphabet.CYRILLIC]),
    )
    CATALAN = (
        12,
        IsoCode639_1.CA,
        IsoCode639_3.CAT,
        frozenset([_Alphabet.LATIN]),
        "Ïï",
    )
    CHINESE = (13, IsoCode639_1.ZH, IsoCode639_3.ZHO, frozenset([_Alphabet.HAN]))
    CROATIAN = (14, IsoCode639_1.HR, IsoCode639_3.HRV, frozenset([_Alphabet.LATIN]))
    CZECH = (
        15,
        IsoCode639_1.CS,
        IsoCode639_3.CES,
        frozenset([_Alphabet.LATIN]),
        "ĚěŘřŮů",
    )
    DANISH = (16, IsoCode639_1.DA, IsoCode639_3.DAN, frozenset([_Alphabet.LATIN]))
    DUTCH = (17, IsoCode639_1.NL, IsoCode639_3.NLD, frozenset([_Alphabet.LATIN]))
    ENGLISH = (18, IsoCode639_1.EN, IsoCode639_3.ENG, frozenset([_Alphabet.LATIN]))
    ESPERANTO = (
        19,
        IsoCode639_1.EO,
        IsoCode639_3.EPO,
        frozenset([_Alphabet.LATIN]),
        "ĈĉĜĝĤĥĴĵŜŝŬŭ",
    )
    ESTONIAN = (20, IsoCode639_1.ET, IsoCode639_3.EST, frozenset([_Alphabet.LATIN]))
    FINNISH = (21, IsoCode639_1.FI, IsoCode639_3.FIN, frozenset([_Alphabet.LATIN]))
    FRENCH = (22, IsoCode639_1.FR, IsoCode639_3.FRA, frozenset([_Alphabet.LATIN]))
    GANDA = (23, IsoCode639_1.LG, IsoCode639_3.LUG, frozenset([_Alphabet.LATIN]))
    GEORGIAN = (
        24,
        IsoCode639_1.KA,
        IsoCode639_3.KAT,
        frozenset([_Alphabet.GEORGIAN]),
    )
    GERMAN = (
        25,
        IsoCode639_1.DE,
        IsoCode639_3.DEU,
        frozenset([_Alphabet.LATIN]),
        "ß",
    )
    GREEK = (26, IsoCode639_1.EL, IsoCode639_3.ELL, frozenset([_Alphabet.GREEK]))
    GUJARATI = (
        27,
        IsoCode639_1.GU,
        IsoCode639_3.GUJ,
        frozenset([_Alphabet.GUJARATI]),
    )
    HEBREW = (28, IsoCode639_1.HE, IsoCode639_3.HEB, frozenset([_Alphabet.HEBREW]))
    HINDI = (
        29,
        IsoCode639_1.HI,
        IsoCode639_3.HIN,
        frozenset([_Alphabet.DEVANAGARI]),
    )
    HUNGARIAN = (
        30,
        IsoCode639_1.HU,
        IsoCode639_3.HUN,
        frozenset([_Alphabet.LATIN]),
        "ŐőŰű",
    )
    ICELANDIC = (
        31,
        IsoCode639_1.IS,
        IsoCode639_3.ISL,
        frozenset([_Alphabet.LATIN]),
    )
    INDONESIAN = (
        32,
        IsoCode639_1.ID,
        IsoCode639_3.IND,
        frozenset([_Alphabet.LATIN]),
    )
    IRISH = (33, IsoCode639_1.GA, IsoCode639_3.GLE, frozenset([_Alphabet.LATIN]))
    ITALIAN = (34, IsoCode639_1.IT, IsoCode639_3.ITA, frozenset([_Alphabet.LATIN]))
    JAPANESE = (
        35,
        IsoCode639_1.JA,
        IsoCode639_3.JPN,
        frozenset([_Alphabet.HIRAGANA, _Alphabet.KATAKANA, _Alphabet.HAN]),
    )
    KAZAKH = (
        36,
        IsoCode639_1.KK,
        IsoCode639_3.KAZ,
        frozenset([_Alphabet.CYRILLIC]),
        "ӘәҒғҚқҢңҰұ",
    )
    KOREAN = (37, IsoCode639_1.KO, IsoCode639_3.KOR, frozenset([_Alphabet.HANGUL]))
    LATIN = (38, IsoCode639_1.LA, IsoCode639_3.LAT, frozenset([_Alphabet.LATIN]))
    LATVIAN = (
        39,
        IsoCode639_1.LV,
        IsoCode639_3.LAV,
        frozenset([_Alphabet.LATIN]),
        "ĢģĶķĻļŅņ",
    )
    LITHUANIAN = (
        40,
        IsoCode639_1.LT,
        IsoCode639_3.LIT,
        frozenset([_Alphabet.LATIN]),
        "ĖėĮįŲų",
    )
    MACEDONIAN = (
        41,
        IsoCode639_1.MK,
        IsoCode639_3.MKD,
        frozenset([_Alphabet.CYRILLIC]),
        "ЃѓЅѕЌќЏџ",
    )
    MALAY = (42, IsoCode639_1.MS, IsoCode639_3.MSA, frozenset([_Alphabet.LATIN]))
    MAORI = (43, IsoCode639_1.MI, IsoCode639_3.MRI, frozenset([_Alphabet.LATIN]))
    MARATHI = (
        44,
        IsoCode639_1.MR,
        IsoCode639_3.MAR,
        frozenset([_Alphabet.DEVANAGARI]),
        "ळ",
    )
    MONGOLIAN = (
        45,
        IsoCode639_1.MN,
        IsoCode639_3.MON,
        frozenset([_Alphabet.CYRILLIC]),
    )
    NYNORSK = (46, IsoCode639_1.NN, IsoCode639_3.NNO, frozenset([_Alphabet.LATIN]))
    PERSIAN = (47, IsoCode639_1.FA, IsoCode639_3.FAS, frozenset([_Alphabet.ARABIC]))
    POLISH = (
        48,
        IsoCode639_1.PL,
        IsoCode639_3.POL,
        frozenset([_Alphabet.LATIN]),
        "ŁłŃńŚśŹź",
    )
    PORTUGUESE = (
        49,
        IsoCode639_1.PT,
        IsoCode639_3.POR,
        frozenset([_Alphabet.LATIN]),
    )
    PUNJABI = (
        50,
        IsoCode639_1.PA,
        IsoCode639_3.PAN,
        frozenset([_Alphabet.GURMUKHI]),
    )
    ROMANIAN = (
        51,
        IsoCode639_1.RO,
        IsoCode639_3.RON,
        frozenset([_Alphabet.LATIN]),
        "Țţ",
    )
    RUSSIAN = (
        52,
        IsoCode639_1.RU,
        IsoCode639_3.RUS,
        frozenset([_Alphabet.CYRILLIC]),
    )
    SERBIAN = (
        53,
        IsoCode639_1.SR,
        IsoCode639_3.SRP,
        frozenset([_Alphabet.CYRILLIC]),
        "ЂђЋћ",
    )
    SHONA = (54, IsoCode639_1.SN, IsoCode639_3.SNA, frozenset([_Alphabet.LATIN]))
    SLOVAK = (
        55,
        IsoCode639_1.SK,
        IsoCode639_3.SLK,
        frozenset([_Alphabet.LATIN]),
        "ĹĺĽľŔŕ",
    )
    SLOVENE = (56, IsoCode639_1.SL, IsoCode639_3.SLV, frozenset([_Alphabet.LATIN]))
    SOMALI = (57, IsoCode639_1.SO, IsoCode639_3.SOM, frozenset([_Alphabet.LATIN]))
    SOTHO = (58, IsoCode639_1.ST, IsoCode639_3.SOT, frozenset([_Alphabet.LATIN]))
    SPANISH = (
        59,
        IsoCode639_1.ES,
        IsoCode639_3.SPA,
        frozenset([_Alphabet.LATIN]),
        "¿¡",
    )
    SWAHILI = (60, IsoCode639_1.SW, IsoCode639_3.SWA, frozenset([_Alphabet.LATIN]))
    SWEDISH = (61, IsoCode639_1.SV, IsoCode639_3.SWE, frozenset([_Alphabet.LATIN]))
    TAGALOG = (62, IsoCode639_1.TL, IsoCode639_3.TGL, frozenset([_Alphabet.LATIN]))
    TAMIL = (63, IsoCode639_1.TA, IsoCode639_3.TAM, frozenset([_Alphabet.TAMIL]))
    TELUGU = (64, IsoCode639_1.TE, IsoCode639_3.TEL, frozenset([_Alphabet.TELUGU]))
    THAI = (65, IsoCode639_1.TH, IsoCode639_3.THA, frozenset([_Alphabet.THAI]))
    TSONGA = (66, IsoCode639_1.TS, IsoCode639_3.TSO, frozenset([_Alphabet.LATIN]))
    TSWANA = (67, IsoCode639_1.TN, IsoCode639_3.TSN, frozenset([_Alphabet.LATIN]))
    TURKISH = (68, IsoCode639_1.TR, IsoCode639_3.TUR, frozenset([_Alphabet.LATIN]))
    UKRAINIAN = (
        69,
        IsoCode639_1.UK,
        IsoCode639_3.UKR,
        frozenset([_Alphabet.CYRILLIC]),
        "ҐґЄєЇї",
    )
    URDU = (70, IsoCode639_1.UR, IsoCode639_3.URD, frozenset([_Alphabet.ARABIC]))
    VIETNAMESE = (
        71,
        IsoCode639_1.VI,
        IsoCode639_3.VIE,
        frozenset([_Alphabet.LATIN]),
        "ẰằẦầẲẳẨẩẴẵẪẫẮắẤấẠạẶặẬậỀềẺẻỂểẼẽỄễẾếỆệỈỉĨĩỊị"
        + "ƠơỒồỜờỎỏỔổỞởỖỗỠỡỐốỚớỘộỢợƯưỪừỦủỬửŨũỮữỨứỤụỰựỲỳỶỷỸỹỴỵ",
    )
    WELSH = (72, IsoCode639_1.CY, IsoCode639_3.CYM, frozenset([_Alphabet.LATIN]))
    XHOSA = (73, IsoCode639_1.XH, IsoCode639_3.XHO, frozenset([_Alphabet.LATIN]))
    YORUBA = (
        74,
        IsoCode639_1.YO,
        IsoCode639_3.YOR,
        frozenset([_Alphabet.LATIN]),
        "Ṣṣ",
    )
    ZULU = (75, IsoCode639_1.ZU, IsoCode639_3.ZUL, frozenset([_Alphabet.LATIN]))

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(
        self,
        _: int,
        iso_code639_1: IsoCode639_1,
        iso_code639_3: IsoCode639_3,
        alphabets: FrozenSet[_Alphabet],
        unique_characters: Optional[str] = None,
    ):
        self.iso_code_639_1 = iso_code639_1
        self.iso_code_639_3 = iso_code639_3
        self._alphabets = alphabets
        self._unique_characters = unique_characters

    def __lt__(self, other):
        if self is None and other is not None:
            return False
        if self is not None and other is None:
            return True
        if not isinstance(other, Language):
            return NotImplemented
        return self.value < other.value

    def __repr__(self):
        return str(self)

    @classmethod
    def all(cls) -> FrozenSet["Language"]:
        """Return a set of all supported languages."""
        return frozenset(language for language in Language)

    @classmethod
    def all_spoken_ones(cls) -> FrozenSet["Language"]:
        """Return a set of all supported spoken languages."""
        return frozenset(
            language for language in Language if language is not Language.LATIN
        )

    @classmethod
    def all_with_arabic_script(cls) -> FrozenSet["Language"]:
        """Return a set of all languages supporting the Arabic script."""
        return frozenset(
            language for language in Language if _Alphabet.ARABIC in language._alphabets
        )

    @classmethod
    def all_with_cyrillic_script(cls) -> FrozenSet["Language"]:
        """Return a set of all languages supporting the Cyrillic script."""
        return frozenset(
            language
            for language in Language
            if _Alphabet.CYRILLIC in language._alphabets
        )

    @classmethod
    def all_with_devanagari_script(cls) -> FrozenSet["Language"]:
        """Return a set of all languages supporting the Devanagari script."""
        return frozenset(
            language
            for language in Language
            if _Alphabet.DEVANAGARI in language._alphabets
        )

    @classmethod
    def all_with_latin_script(cls) -> FrozenSet["Language"]:
        """Return a set of all languages supporting the Latin script."""
        return frozenset(
            language for language in Language if _Alphabet.LATIN in language._alphabets
        )

    @classmethod
    def from_iso_code_639_1(cls, iso_code: IsoCode639_1) -> "Language":
        """Return the language associated with the ISO 639-1 code
        passed to this method.

        Raises:
            ValueError: if there is no language for the given ISO code
        """
        for language in Language:
            if language.iso_code_639_1 == iso_code:
                return language
        raise ValueError(f"There is no language for ISO 639-1 code {iso_code}")

    @classmethod
    def from_iso_code_639_3(cls, iso_code: IsoCode639_3) -> "Language":
        """Return the language associated with the ISO 639-3 code
        passed to this method.

        Raises:
            ValueError: if there is no language for the given ISO code
        """
        for language in Language:
            if language.iso_code_639_3 == iso_code:
                return language
        raise ValueError(f"There is no language for ISO 639-3 code {iso_code}")
