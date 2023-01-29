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

from enum import Enum


class IsoCode639_1(Enum):
    """This enum specifies the ISO 639-1 code representations for the
    supported languages.

    ISO 639 is a standardized nomenclature used to classify languages.
    """

    #: The ISO 639-1 code for Afrikaans
    AF = 1, "Afrikaans"

    #: The ISO 639-1 code for Arabic
    AR = 2, "Arabic"

    #: The ISO 639-1 code for Azerbaijani
    AZ = 3, "Azerbaijani"

    #: The ISO 639-1 code for Belarusian
    BE = 4, "Belarusian"

    #: The ISO 639-1 code for Bulgarian
    BG = 5, "Bulgarian"

    #: The ISO 639-1 code for Bengali
    BN = 6, "Bengali"

    #: The ISO 639-1 code for Bosnian
    BS = 7, "Bosnian"

    #: The ISO 639-1 code for Catalan
    CA = 8, "Catalan"

    #: The ISO 639-1 code for Czech
    CS = 9, "Czech"

    #: The ISO 639-1 code for Welsh
    CY = 10, "Welsh"

    #: The ISO 639-1 code for Danish
    DA = 11, "Danish"

    #: The ISO 639-1 code for German
    DE = 12, "German"

    #: The ISO 639-1 code for Greek
    EL = 13, "Greek"

    #: The ISO 639-1 code for English
    EN = 14, "English"

    #: The ISO 639-1 code for Esperanto
    EO = 15, "Esperanto"

    #: The ISO 639-1 code for Spanish
    ES = 16, "Spanish"

    #: The ISO 639-1 code for Estonian
    ET = 17, "Estonian"

    #: The ISO 639-1 code for Basque
    EU = 18, "Basque"

    #: The ISO 639-1 code for Persian
    FA = 19, "Persian"

    #: The ISO 639-1 code for Finnish
    FI = 20, "Finnish"

    #: The ISO 639-1 code for French
    FR = 21, "French"

    #: The ISO 639-1 code for Irish
    GA = 22, "Irish"

    #: The ISO 639-1 code for Gujarati
    GU = 23, "Gujarati"

    #: The ISO 639-1 code for Hebrew
    HE = 24, "Hebrew"

    #: The ISO 639-1 code for Hindi
    HI = 25, "Hindi"

    #: The ISO 639-1 code for Croatian
    HR = 26, "Croatian"

    #: The ISO 639-1 code for Hungarian
    HU = 27, "Hungarian"

    #: The ISO 639-1 code for Armenian
    HY = 28, "Armenian"

    #: The ISO 639-1 code for Indonesian
    ID = 29, "Indonesian"

    #: The ISO 639-1 code for Icelandic
    IS = 30, "Icelandic"

    #: The ISO 639-1 code for Italian
    IT = 31, "Italian"

    #: The ISO 639-1 code for Japanese
    JA = 32, "Japanese"

    #: The ISO 639-1 code for Georgian
    KA = 33, "Georgian"

    #: The ISO 639-1 code for Kazakh
    KK = 34, "Kazakh"

    #: The ISO 639-1 code for Korean
    KO = 35, "Korean"

    #: The ISO 639-1 code for Latin
    LA = 36, "Latin"

    #: The ISO 639-1 code for Ganda
    LG = 37, "Ganda"

    #: The ISO 639-1 code for Lithuanian
    LT = 38, "Lithuanian"

    #: The ISO 639-1 code for Latvian
    LV = 39, "Latvian"

    #: The ISO 639-1 code for Maori
    MI = 40, "Maori"

    #: The ISO 639-1 code for Macedonian
    MK = 41, "Macedonian"

    #: The ISO 639-1 code for Mongolian
    MN = 42, "Mongolian"

    #: The ISO 639-1 code for Marathi
    MR = 43, "Marathi"

    #: The ISO 639-1 code for Malay
    MS = 44, "Malay"

    #: The ISO 639-1 code for Norwegian Bokmal
    NB = 45, "Norwegian Bokmal"

    #: The ISO 639-1 code for Dutch
    NL = 46, "Dutch"

    #: The ISO 639-1 code for Norwegian Nynorsk
    NN = 47, "Norwegian Nynorsk"

    #: The ISO 639-1 code for Punjabi
    PA = 48, "Punjabi"

    #: The ISO 639-1 code for Polish
    PL = 49, "Polish"

    #: The ISO 639-1 code for Portuguese
    PT = 50, "Portuguese"

    #: The ISO 639-1 code for Romanian
    RO = 51, "Romanian"

    #: The ISO 639-1 code for Russian
    RU = 52, "Russian"

    #: The ISO 639-1 code for Slovak
    SK = 53, "Slovak"

    #: The ISO 639-1 code for Slovene
    SL = 54, "Slovene"

    #: The ISO 639-1 code for Shona
    SN = 55, "Shona"

    #: The ISO 639-1 code for Somali
    SO = 56, "Somali"

    #: The ISO 639-1 code for Albanian
    SQ = 57, "Albanian"

    #: The ISO 639-1 code for Serbian
    SR = 58, "Serbian"

    #: The ISO 639-1 code for Sotho
    ST = 59, "Sotho"

    #: The ISO 639-1 code for Swedish
    SV = 60, "Swedish"

    #: The ISO 639-1 code for Swahili
    SW = 61, "Swahili"

    #: The ISO 639-1 code for Tamil
    TA = 62, "Tamil"

    #: The ISO 639-1 code for Telugu
    TE = 63, "Telugu"

    #: The ISO 639-1 code for Thai
    TH = 64, "Thai"

    #: The ISO 639-1 code for Tagalog
    TL = 65, "Tagalog"

    #: The ISO 639-1 code for Tswana
    TN = 66, "Tswana"

    #: The ISO 639-1 code for Turkish
    TR = 67, "Turkish"

    #: The ISO 639-1 code for Tsonga
    TS = 68, "Tsonga"

    #: The ISO 639-1 code for Ukrainian
    UK = 69, "Ukrainian"

    #: The ISO 639-1 code for Urdu
    UR = 70, "Urdu"

    #: The ISO 639-1 code for Vietnamese
    VI = 71, "Vietnamese"

    #: The ISO 639-1 code for Xhosa
    XH = 72, "Xhosa"

    #: The ISO 639-1 code for Yoruba
    YO = 73, "Yoruba"

    #: The ISO 639-1 code for Chinese
    ZH = 74, "Chinese"

    #: The ISO 639-1 code for Zulu
    ZU = 75, "Zulu"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        obj.__doc__ = " ".join(["The ISO 639-1 code for", args[1]])
        return obj

    def __repr__(self):
        return str(self)


class IsoCode639_3(Enum):
    """This enum specifies the ISO 639-3 code representations for the
    supported languages.

    ISO 639 is a standardized nomenclature used to classify languages.
    """

    #: The ISO 639-3 code for Afrikaans
    AFR = 1, "Afrikaans"

    #: The ISO 639-3 code for Arabic
    ARA = 2, "Arabic"

    #: The ISO 639-3 code for Azerbaijani
    AZE = 3, "Azerbaijani"

    #: The ISO 639-3 code for Belarusian
    BEL = 4, "Belarusian"

    #: The ISO 639-3 code for Bengali
    BEN = 5, "Bengali"

    #: The ISO 639-3 code for Bosnian
    BOS = 6, "Bosnian"

    #: The ISO 639-3 code for Bulgarian
    BUL = 7, "Bulgarian"

    #: The ISO 639-3 code for Catalan
    CAT = 8, "Catalan"

    #: The ISO 639-3 code for Czech
    CES = 9, "Czech"

    #: The ISO 639-3 code for Welsh
    CYM = 10, "Welsh"

    #: The ISO 639-3 code for Danish
    DAN = 11, "Danish"

    #: The ISO 639-3 code for German
    DEU = 12, "German"

    #: The ISO 639-3 code for Greek
    ELL = 13, "Greek"

    #: The ISO 639-3 code for English
    ENG = 14, "English"

    #: The ISO 639-3 code for Esperanto
    EPO = 15, "Esperanto"

    #: The ISO 639-3 code for Estonian
    EST = 16, "Estonian"

    #: The ISO 639-3 code for Basque
    EUS = 17, "Basque"

    #: The ISO 639-3 code for Persian
    FAS = 18, "Persian"

    #: The ISO 639-3 code for Finnish
    FIN = 19, "Finnish"

    #: The ISO 639-3 code for French
    FRA = 20, "French"

    #: The ISO 639-3 code for Irish
    GLE = 21, "Irish"

    #: The ISO 639-3 code for Gujarati
    GUJ = 22, "Gujarati"

    #: The ISO 639-3 code for Hebrew
    HEB = 23, "Hebrew"

    #: The ISO 639-3 code for Hindi
    HIN = 24, "Hindi"

    #: The ISO 639-3 code for Croatian
    HRV = 25, "Croatian"

    #: The ISO 639-3 code for Hungarian
    HUN = 26, "Hungarian"

    #: The ISO 639-3 code for Armenian
    HYE = 27, "Armenian"

    #: The ISO 639-3 code for Indonesian
    IND = 28, "Indonesian"

    #: The ISO 639-3 code for Icelandic
    ISL = 29, "Icelandic"

    #: The ISO 639-3 code for Italian
    ITA = 30, "Italian"

    #: The ISO 639-3 code for Japanese
    JPN = 31, "Japanese"

    #: The ISO 639-3 code for Georgian
    KAT = 32, "Georgian"

    #: The ISO 639-3 code for Kazakh
    KAZ = 33, "Kazakh"

    #: The ISO 639-3 code for Korean
    KOR = 34, "Korean"

    #: The ISO 639-3 code for Latin
    LAT = 35, "Latin"

    #: The ISO 639-3 code for Latvian
    LAV = 36, "Latvian"

    #: The ISO 639-3 code for Lithuanian
    LIT = 37, "Lithuanian"

    #: The ISO 639-3 code for Ganda
    LUG = 38, "Ganda"

    #: The ISO 639-3 code for Marathi
    MAR = 39, "Marathi"

    #: The ISO 639-3 code for Macedonian
    MKD = 40, "Macedonian"

    #: The ISO 639-3 code for Mongolian
    MON = 41, "Mongolian"

    #: The ISO 639-3 code for Maori
    MRI = 42, "Maori"

    #: The ISO 639-3 code for Malay
    MSA = 43, "Malay"

    #: The ISO 639-3 code for Dutch
    NLD = 44, "Dutch"

    #: The ISO 639-3 code for Norwegian Nynorsk
    NNO = 45, "Norwegian Nynorsk"

    #: The ISO 639-3 code for Norwegian Bokmal
    NOB = 46, "Norwegian Bokmal"

    #: The ISO 639-3 code for Punjabi
    PAN = 47, "Punjabi"

    #: The ISO 639-3 code for Polish
    POL = 48, "Polish"

    #: The ISO 639-3 code for Portuguese
    POR = 49, "Portuguese"

    #: The ISO 639-3 code for Romanian
    RON = 50, "Romanian"

    #: The ISO 639-3 code for Russian
    RUS = 51, "Russian"

    #: The ISO 639-3 code for Slovak
    SLK = 52, "Slovak"

    #: The ISO 639-3 code for Slovene
    SLV = 53, "Slovene"

    #: The ISO 639-3 code for Shona
    SNA = 54, "Shona"

    #: The ISO 639-3 code for Somali
    SOM = 55, "Somali"

    #: The ISO 639-3 code for Sotho
    SOT = 56, "Sotho"

    #: The ISO 639-3 code for Spanish
    SPA = 57, "Spanish"

    #: The ISO 639-3 code for Albanian
    SQI = 58, "Albanian"

    #: The ISO 639-3 code for Serbian
    SRP = 59, "Serbian"

    #: The ISO 639-3 code for Swahili
    SWA = 60, "Swahili"

    #: The ISO 639-3 code for Swedish
    SWE = 61, "Swedish"

    #: The ISO 639-3 code for Tamil
    TAM = 62, "Tamil"

    #: The ISO 639-3 code for Telugu
    TEL = 63, "Telugu"

    #: The ISO 639-3 code for Tagalog
    TGL = 64, "Tagalog"

    #: The ISO 639-3 code for Thai
    THA = 65, "Thai"

    #: The ISO 639-3 code for Tswana
    TSN = 66, "Tswana"

    #: The ISO 639-3 code for Tsonga
    TSO = 67, "Tsonga"

    #: The ISO 639-3 code for Turkish
    TUR = 68, "Turkish"

    #: The ISO 639-3 code for Ukrainian
    UKR = 69, "Ukrainian"

    #: The ISO 639-3 code for Urdu
    URD = 70, "Urdu"

    #: The ISO 639-3 code for Vietnamese
    VIE = 71, "Vietnamese"

    #: The ISO 639-3 code for Xhosa
    XHO = 72, "Xhosa"

    #: The ISO 639-3 code for Yoruba
    YOR = 73, "Yoruba"

    #: The ISO 639-3 code for Chinese
    ZHO = 74, "Chinese"

    #: The ISO 639-3 code for Zulu
    ZUL = 75, "Zulu"

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        obj.__doc__ = " ".join(["The ISO 639-3 code for", args[1]])
        return obj

    def __repr__(self):
        return str(self)
