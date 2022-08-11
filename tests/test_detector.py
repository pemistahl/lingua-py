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

import numpy as np
import pytest

from math import isclose, log

from lingua.detector import LanguageDetector
from lingua.language import Language, _Alphabet
from lingua._model import _TestDataLanguageModel


def f(num):
    return np.float16(num)


# ##############################
# LANGUAGE MODELS FOR ENGLISH
# ##############################


@pytest.fixture
def unigram_model_for_english():
    return np.sort(
        np.array(
            [
                ("a", log(0.01)),
                ("l", log(0.02)),
                ("t", log(0.03)),
                ("e", log(0.04)),
                ("r", log(0.05)),
                # unknown unigrams
                ("w", 0.0),
            ],
            dtype=[("ngram", "U1"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def bigram_model_for_english():
    return np.sort(
        np.array(
            [
                ("al", log(0.11)),
                ("lt", log(0.12)),
                ("te", log(0.13)),
                ("er", log(0.14)),
                # unknown bigrams
                ("aq", 0.0),
                ("wx", 0.0),
            ],
            dtype=[("ngram", "U2"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def trigram_model_for_english():
    return np.sort(
        np.array(
            [
                ("alt", log(0.19)),
                ("lte", log(0.2)),
                ("ter", log(0.21)),
                # unknown trigrams
                ("aqu", 0.0),
                ("tez", 0.0),
                ("wxy", 0.0),
            ],
            dtype=[("ngram", "U3"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def quadrigram_model_for_english():
    return np.sort(
        np.array(
            [
                ("alte", log(0.25)),
                ("lter", log(0.26)),
                # unknown quadrigrams
                ("aqua", 0.0),
                ("wxyz", 0.0),
            ],
            dtype=[("ngram", "U4"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def fivegram_model_for_english():
    return np.sort(
        np.array(
            [
                ("alter", log(0.29)),
                # unknown fivegrams
                ("aquas", 0.0),
            ],
            dtype=[("ngram", "U5"), ("frequency", "f2")],
        )
    )


# ##############################
# LANGUAGE MODELS FOR GERMAN
# ##############################


@pytest.fixture
def unigram_model_for_german():
    return np.sort(
        np.array(
            [
                ("a", log(0.06)),
                ("l", log(0.07)),
                ("t", log(0.08)),
                ("e", log(0.09)),
                ("r", log(0.1)),
                # unknown unigrams
                ("w", 0.0),
            ],
            dtype=[("ngram", "U1"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def bigram_model_for_german():
    return np.sort(
        np.array(
            [
                ("al", log(0.15)),
                ("lt", log(0.16)),
                ("te", log(0.17)),
                ("er", log(0.18)),
                # unknown bigrams
                ("wx", 0.0),
            ],
            dtype=[("ngram", "U2"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def trigram_model_for_german():
    return np.sort(
        np.array(
            [
                ("alt", log(0.22)),
                ("lte", log(0.23)),
                ("ter", log(0.24)),
                # unknown trigrams
                ("wxy", 0.0),
            ],
            dtype=[("ngram", "U3"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def quadrigram_model_for_german():
    return np.sort(
        np.array(
            [
                ("alte", log(0.27)),
                ("lter", log(0.28)),
                # unknown quadrigrams
                ("wxyz", 0.0),
            ],
            dtype=[("ngram", "U4"), ("frequency", "f2")],
        )
    )


@pytest.fixture
def fivegram_model_for_german():
    return np.sort(
        np.array(
            [
                ("alter", log(0.3)),
            ],
            dtype=[("ngram", "U5"), ("frequency", "f2")],
        )
    )


# ##############################
# NGRAM MODELS
# ##############################


@pytest.fixture
def unigram_models(unigram_model_for_english, unigram_model_for_german):
    return {
        Language.ENGLISH: unigram_model_for_english,
        Language.GERMAN: unigram_model_for_german,
    }


@pytest.fixture
def bigram_models(bigram_model_for_english, bigram_model_for_german):
    return {
        Language.ENGLISH: bigram_model_for_english,
        Language.GERMAN: bigram_model_for_german,
    }


@pytest.fixture
def trigram_models(trigram_model_for_english, trigram_model_for_german):
    return {
        Language.ENGLISH: trigram_model_for_english,
        Language.GERMAN: trigram_model_for_german,
    }


@pytest.fixture
def quadrigram_models(quadrigram_model_for_english, quadrigram_model_for_german):
    return {
        Language.ENGLISH: quadrigram_model_for_english,
        Language.GERMAN: quadrigram_model_for_german,
    }


@pytest.fixture
def fivegram_models(fivegram_model_for_english, fivegram_model_for_german):
    return {
        Language.ENGLISH: fivegram_model_for_english,
        Language.GERMAN: fivegram_model_for_german,
    }


# ##############################
# DETECTORS
# ##############################


@pytest.fixture
def detector_for_english_and_german(
    unigram_models, bigram_models, trigram_models, quadrigram_models, fivegram_models
):
    return LanguageDetector(
        _languages=frozenset([Language.ENGLISH, Language.GERMAN]),
        _minimum_relative_distance=0.0,
        _is_low_accuracy_mode_enabled=False,
        _languages_with_unique_characters=frozenset(),
        _one_language_alphabets={},
        _unigram_language_models=unigram_models,
        _bigram_language_models=bigram_models,
        _trigram_language_models=trigram_models,
        _quadrigram_language_models=quadrigram_models,
        _fivegram_language_models=fivegram_models,
        _cache={},
    )


@pytest.fixture
def detector_for_all_languages():
    languages = Language.all()
    languages_with_unique_characters = frozenset(
        {language for language in languages if language._unique_characters is not None}
    )
    one_language_alphabets = {
        alphabet: language
        for alphabet, language in _Alphabet.all_supporting_single_language().items()
        if language in languages
    }

    return LanguageDetector(
        _languages=languages,
        _minimum_relative_distance=0.0,
        _is_low_accuracy_mode_enabled=False,
        _languages_with_unique_characters=languages_with_unique_characters,
        _one_language_alphabets=one_language_alphabets,
        _unigram_language_models={},
        _bigram_language_models={},
        _trigram_language_models={},
        _quadrigram_language_models={},
        _fivegram_language_models={},
        _cache={},
    )


def test_text_is_cleaned_up_properly(detector_for_all_languages):
    text = """Weltweit    gibt es ungefähr 6.000 Sprachen,
    wobei laut Schätzungen zufolge ungefähr 90  Prozent davon
    am Ende dieses Jahrhunderts verdrängt sein werden."""

    expected_cleaned_text = (
        "weltweit gibt es ungefähr sprachen wobei laut schätzungen zufolge ungefähr "
        "prozent davon am ende dieses jahrhunderts verdrängt sein werden"
    )

    assert (
        detector_for_all_languages._clean_up_input_text(text) == expected_cleaned_text
    )


@pytest.mark.parametrize(
    "text,expected_words",
    [
        pytest.param("this is a sentence", ["this", "is", "a", "sentence"]),
        pytest.param("sentence", ["sentence"]),
        pytest.param(
            "上海大学是一个好大学 this is a sentence",
            [
                "上",
                "海",
                "大",
                "学",
                "是",
                "一",
                "个",
                "好",
                "大",
                "学",
                "this",
                "is",
                "a",
                "sentence",
            ],
        ),
    ],
)
def test_text_is_split_into_words_correctly(
    detector_for_all_languages, text, expected_words
):
    assert detector_for_all_languages._split_text_into_words(text) == expected_words


@pytest.mark.parametrize(
    "word,expected_language",
    [
        # words with unique characters
        pytest.param("məhərrəm", Language.AZERBAIJANI),
        pytest.param("substituïts", Language.CATALAN),
        pytest.param("rozdělit", Language.CZECH),
        pytest.param("tvořen", Language.CZECH),
        pytest.param("subjektů", Language.CZECH),
        pytest.param("nesufiĉecon", Language.ESPERANTO),
        pytest.param("intermiksiĝis", Language.ESPERANTO),
        pytest.param("monaĥinoj", Language.ESPERANTO),
        pytest.param("kreitaĵoj", Language.ESPERANTO),
        pytest.param("ŝpinante", Language.ESPERANTO),
        pytest.param("apenaŭ", Language.ESPERANTO),
        pytest.param("groß", Language.GERMAN),
        pytest.param("σχέδια", Language.GREEK),
        pytest.param("fekvő", Language.HUNGARIAN),
        pytest.param("meggyűrűzni", Language.HUNGARIAN),
        pytest.param("ヴェダイヤモンド", Language.JAPANESE),
        pytest.param("әлем", Language.KAZAKH),
        pytest.param("шаруашылығы", Language.KAZAKH),
        pytest.param("ақын", Language.KAZAKH),
        pytest.param("оның", Language.KAZAKH),
        pytest.param("шұрайлы", Language.KAZAKH),
        pytest.param("teoloģiska", Language.LATVIAN),
        pytest.param("blaķene", Language.LATVIAN),
        pytest.param("ceļojumiem", Language.LATVIAN),
        pytest.param("numuriņu", Language.LATVIAN),
        pytest.param("mergelės", Language.LITHUANIAN),
        pytest.param("įrengus", Language.LITHUANIAN),
        pytest.param("slegiamų", Language.LITHUANIAN),
        pytest.param("припаѓа", Language.MACEDONIAN),
        pytest.param("ѕидови", Language.MACEDONIAN),
        pytest.param("ќерка", Language.MACEDONIAN),
        pytest.param("џамиите", Language.MACEDONIAN),
        pytest.param("मिळते", Language.MARATHI),
        pytest.param("үндсэн", Language.MONGOLIAN),
        pytest.param("дөхөж", Language.MONGOLIAN),
        pytest.param("zmieniły", Language.POLISH),
        pytest.param("państwowych", Language.POLISH),
        pytest.param("mniejszości", Language.POLISH),
        pytest.param("groźne", Language.POLISH),
        pytest.param("ialomiţa", Language.ROMANIAN),
        pytest.param("наслеђивања", Language.SERBIAN),
        pytest.param("неисквареношћу", Language.SERBIAN),
        pytest.param("podĺa", Language.SLOVAK),
        pytest.param("pohľade", Language.SLOVAK),
        pytest.param("mŕtvych", Language.SLOVAK),
        pytest.param("ґрунтовому", Language.UKRAINIAN),
        pytest.param("пропонує", Language.UKRAINIAN),
        pytest.param("пристрої", Language.UKRAINIAN),
        pytest.param("cằm", Language.VIETNAMESE),
        pytest.param("thần", Language.VIETNAMESE),
        pytest.param("chẳng", Language.VIETNAMESE),
        pytest.param("quẩy", Language.VIETNAMESE),
        pytest.param("sẵn", Language.VIETNAMESE),
        pytest.param("nhẫn", Language.VIETNAMESE),
        pytest.param("dắt", Language.VIETNAMESE),
        pytest.param("chất", Language.VIETNAMESE),
        pytest.param("đạp", Language.VIETNAMESE),
        pytest.param("mặn", Language.VIETNAMESE),
        pytest.param("hậu", Language.VIETNAMESE),
        pytest.param("hiền", Language.VIETNAMESE),
        pytest.param("lẻn", Language.VIETNAMESE),
        pytest.param("biểu", Language.VIETNAMESE),
        pytest.param("kẽm", Language.VIETNAMESE),
        pytest.param("diễm", Language.VIETNAMESE),
        pytest.param("phế", Language.VIETNAMESE),
        pytest.param("việc", Language.VIETNAMESE),
        pytest.param("chỉnh", Language.VIETNAMESE),
        pytest.param("trĩ", Language.VIETNAMESE),
        pytest.param("ravị", Language.VIETNAMESE),
        pytest.param("thơ", Language.VIETNAMESE),
        pytest.param("nguồn", Language.VIETNAMESE),
        pytest.param("thờ", Language.VIETNAMESE),
        pytest.param("sỏi", Language.VIETNAMESE),
        pytest.param("tổng", Language.VIETNAMESE),
        pytest.param("nhở", Language.VIETNAMESE),
        pytest.param("mỗi", Language.VIETNAMESE),
        pytest.param("bỡi", Language.VIETNAMESE),
        pytest.param("tốt", Language.VIETNAMESE),
        pytest.param("giới", Language.VIETNAMESE),
        pytest.param("một", Language.VIETNAMESE),
        pytest.param("hợp", Language.VIETNAMESE),
        pytest.param("hưng", Language.VIETNAMESE),
        pytest.param("từng", Language.VIETNAMESE),
        pytest.param("của", Language.VIETNAMESE),
        pytest.param("sử", Language.VIETNAMESE),
        pytest.param("cũng", Language.VIETNAMESE),
        pytest.param("những", Language.VIETNAMESE),
        pytest.param("chức", Language.VIETNAMESE),
        pytest.param("dụng", Language.VIETNAMESE),
        pytest.param("thực", Language.VIETNAMESE),
        pytest.param("kỳ", Language.VIETNAMESE),
        pytest.param("kỷ", Language.VIETNAMESE),
        pytest.param("mỹ", Language.VIETNAMESE),
        pytest.param("mỵ", Language.VIETNAMESE),
        pytest.param("aṣiwèrè", Language.YORUBA),
        pytest.param("ṣaaju", Language.YORUBA),
        pytest.param("والموضوع", None),
        pytest.param("сопротивление", None),
        pytest.param("house", None),
        # words with unique alphabet
        pytest.param("ունենա", Language.ARMENIAN),
        pytest.param("জানাতে", Language.BENGALI),
        pytest.param("გარეუბან", Language.GEORGIAN),
        pytest.param("σταμάτησε", Language.GREEK),
        pytest.param("ઉપકરણોની", Language.GUJARATI),
        pytest.param("בתחרויות", Language.HEBREW),
        pytest.param("びさ", Language.JAPANESE),
        pytest.param("대결구도가", Language.KOREAN),
        pytest.param("ਮੋਟਰਸਾਈਕਲਾਂ", Language.PUNJABI),
        pytest.param("துன்பங்களை", Language.TAMIL),
        pytest.param("కృష్ణదేవరాయలు", Language.TELUGU),
        pytest.param("ในทางหลวงหมายเลข", Language.THAI),
    ],
)
def test_language_detection_with_rules(
    detector_for_all_languages, word, expected_language
):
    detected_language = detector_for_all_languages._detect_language_with_rules([word])
    assert detected_language == expected_language


@pytest.mark.parametrize(
    "word,expected_languages",
    [
        pytest.param("والموضوع", [Language.ARABIC, Language.PERSIAN, Language.URDU]),
        pytest.param(
            "сопротивление",
            [
                Language.BELARUSIAN,
                Language.BULGARIAN,
                Language.KAZAKH,
                Language.MACEDONIAN,
                Language.MONGOLIAN,
                Language.RUSSIAN,
                Language.SERBIAN,
                Language.UKRAINIAN,
            ],
        ),
        pytest.param(
            "раскрывае",
            [
                Language.BELARUSIAN,
                Language.KAZAKH,
                Language.MONGOLIAN,
                Language.RUSSIAN,
            ],
        ),
        pytest.param(
            "этот",
            [
                Language.BELARUSIAN,
                Language.KAZAKH,
                Language.MONGOLIAN,
                Language.RUSSIAN,
            ],
        ),
        pytest.param(
            "огнём",
            [
                Language.BELARUSIAN,
                Language.KAZAKH,
                Language.MONGOLIAN,
                Language.RUSSIAN,
            ],
        ),
        pytest.param(
            "плаваща",
            [Language.BULGARIAN, Language.KAZAKH, Language.MONGOLIAN, Language.RUSSIAN],
        ),
        pytest.param(
            "довършат",
            [Language.BULGARIAN, Language.KAZAKH, Language.MONGOLIAN, Language.RUSSIAN],
        ),
        pytest.param(
            "павінен", [Language.BELARUSIAN, Language.KAZAKH, Language.UKRAINIAN]
        ),
        pytest.param("затоплување", [Language.MACEDONIAN, Language.SERBIAN]),
        pytest.param("ректасцензија", [Language.MACEDONIAN, Language.SERBIAN]),
        pytest.param("набљудувач", [Language.MACEDONIAN, Language.SERBIAN]),
        pytest.param("aizklātā", [Language.LATVIAN, Language.MAORI, Language.YORUBA]),
        pytest.param("sistēmas", [Language.LATVIAN, Language.MAORI, Language.YORUBA]),
        pytest.param("palīdzi", [Language.LATVIAN, Language.MAORI, Language.YORUBA]),
        pytest.param("nhẹn", [Language.VIETNAMESE, Language.YORUBA]),
        pytest.param("chọn", [Language.VIETNAMESE, Language.YORUBA]),
        pytest.param(
            "prihvaćanju", [Language.BOSNIAN, Language.CROATIAN, Language.POLISH]
        ),
        pytest.param(
            "nađete", [Language.BOSNIAN, Language.CROATIAN, Language.VIETNAMESE]
        ),
        pytest.param("visão", [Language.PORTUGUESE, Language.VIETNAMESE]),
        pytest.param("wystąpią", [Language.LITHUANIAN, Language.POLISH]),
        pytest.param("budowę", [Language.LITHUANIAN, Language.POLISH]),
        pytest.param(
            "nebūsime",
            [Language.LATVIAN, Language.LITHUANIAN, Language.MAORI, Language.YORUBA],
        ),
        pytest.param(
            "afişate", [Language.AZERBAIJANI, Language.ROMANIAN, Language.TURKISH]
        ),
        pytest.param("kradzieżami", [Language.POLISH, Language.ROMANIAN]),
        pytest.param("înviat", [Language.FRENCH, Language.ROMANIAN]),
        pytest.param(
            "venerdì", [Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA]
        ),
        pytest.param("años", [Language.BASQUE, Language.SPANISH]),
        pytest.param("rozohňuje", [Language.CZECH, Language.SLOVAK]),
        pytest.param("rtuť", [Language.CZECH, Language.SLOVAK]),
        pytest.param("pregătire", [Language.ROMANIAN, Language.VIETNAMESE]),
        pytest.param("jeďte", [Language.CZECH, Language.ROMANIAN, Language.SLOVAK]),
        pytest.param("minjaverðir", [Language.ICELANDIC, Language.TURKISH]),
        pytest.param("þagnarskyldu", [Language.ICELANDIC, Language.TURKISH]),
        pytest.param("nebûtu", [Language.FRENCH, Language.HUNGARIAN]),
        pytest.param(
            "hashemidëve",
            [Language.AFRIKAANS, Language.ALBANIAN, Language.DUTCH, Language.FRENCH],
        ),
        pytest.param(
            "forêt",
            [
                Language.AFRIKAANS,
                Language.FRENCH,
                Language.PORTUGUESE,
                Language.VIETNAMESE,
            ],
        ),
        pytest.param(
            "succèdent",
            [Language.FRENCH, Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA],
        ),
        pytest.param(
            "où",
            [Language.FRENCH, Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA],
        ),
        pytest.param(
            "tõeliseks",
            [
                Language.ESTONIAN,
                Language.HUNGARIAN,
                Language.PORTUGUESE,
                Language.VIETNAMESE,
            ],
        ),
        pytest.param(
            "viòiem",
            [Language.CATALAN, Language.ITALIAN, Language.VIETNAMESE, Language.YORUBA],
        ),
        pytest.param(
            "contrôle",
            [
                Language.FRENCH,
                Language.PORTUGUESE,
                Language.SLOVAK,
                Language.VIETNAMESE,
            ],
        ),
        pytest.param("direktør", [Language.BOKMAL, Language.DANISH, Language.NYNORSK]),
        pytest.param(
            "vývoj",
            [
                Language.CZECH,
                Language.ICELANDIC,
                Language.SLOVAK,
                Language.TURKISH,
                Language.VIETNAMESE,
            ],
        ),
        pytest.param(
            "päralt",
            [
                Language.ESTONIAN,
                Language.FINNISH,
                Language.GERMAN,
                Language.SLOVAK,
                Language.SWEDISH,
            ],
        ),
        pytest.param(
            "labâk",
            [
                Language.FRENCH,
                Language.PORTUGUESE,
                Language.ROMANIAN,
                Language.TURKISH,
                Language.VIETNAMESE,
            ],
        ),
        pytest.param(
            "pràctiques",
            [
                Language.CATALAN,
                Language.FRENCH,
                Language.ITALIAN,
                Language.PORTUGUESE,
                Language.VIETNAMESE,
            ],
        ),
        pytest.param(
            "überrascht",
            [
                Language.AZERBAIJANI,
                Language.CATALAN,
                Language.ESTONIAN,
                Language.GERMAN,
                Language.HUNGARIAN,
                Language.SPANISH,
                Language.TURKISH,
            ],
        ),
        pytest.param(
            "indebærer",
            [Language.BOKMAL, Language.DANISH, Language.ICELANDIC, Language.NYNORSK],
        ),
        pytest.param(
            "måned",
            [Language.BOKMAL, Language.DANISH, Language.NYNORSK, Language.SWEDISH],
        ),
        pytest.param(
            "zaručen",
            [
                Language.BOSNIAN,
                Language.CZECH,
                Language.CROATIAN,
                Language.LATVIAN,
                Language.LITHUANIAN,
                Language.SLOVAK,
                Language.SLOVENE,
            ],
        ),
        pytest.param(
            "zkouškou",
            [
                Language.BOSNIAN,
                Language.CZECH,
                Language.CROATIAN,
                Language.LATVIAN,
                Language.LITHUANIAN,
                Language.SLOVAK,
                Language.SLOVENE,
            ],
        ),
        pytest.param(
            "navržen",
            [
                Language.BOSNIAN,
                Language.CZECH,
                Language.CROATIAN,
                Language.LATVIAN,
                Language.LITHUANIAN,
                Language.SLOVAK,
                Language.SLOVENE,
            ],
        ),
        pytest.param(
            "façonnage",
            [
                Language.ALBANIAN,
                Language.AZERBAIJANI,
                Language.BASQUE,
                Language.CATALAN,
                Language.FRENCH,
                Language.PORTUGUESE,
                Language.TURKISH,
            ],
        ),
        pytest.param(
            "höher",
            [
                Language.AZERBAIJANI,
                Language.ESTONIAN,
                Language.FINNISH,
                Language.GERMAN,
                Language.HUNGARIAN,
                Language.ICELANDIC,
                Language.SWEDISH,
                Language.TURKISH,
            ],
        ),
        pytest.param(
            "catedráticos",
            [
                Language.CATALAN,
                Language.CZECH,
                Language.ICELANDIC,
                Language.IRISH,
                Language.HUNGARIAN,
                Language.PORTUGUESE,
                Language.SLOVAK,
                Language.SPANISH,
                Language.VIETNAMESE,
                Language.YORUBA,
            ],
        ),
        pytest.param(
            "política",
            [
                Language.CATALAN,
                Language.CZECH,
                Language.ICELANDIC,
                Language.IRISH,
                Language.HUNGARIAN,
                Language.PORTUGUESE,
                Language.SLOVAK,
                Language.SPANISH,
                Language.VIETNAMESE,
                Language.YORUBA,
            ],
        ),
        pytest.param(
            "música",
            [
                Language.CATALAN,
                Language.CZECH,
                Language.ICELANDIC,
                Language.IRISH,
                Language.HUNGARIAN,
                Language.PORTUGUESE,
                Language.SLOVAK,
                Language.SPANISH,
                Language.VIETNAMESE,
                Language.YORUBA,
            ],
        ),
        pytest.param(
            "contradicció",
            [
                Language.CATALAN,
                Language.HUNGARIAN,
                Language.ICELANDIC,
                Language.IRISH,
                Language.POLISH,
                Language.PORTUGUESE,
                Language.SLOVAK,
                Language.SPANISH,
                Language.VIETNAMESE,
                Language.YORUBA,
            ],
        ),
        pytest.param(
            "només",
            [
                Language.CATALAN,
                Language.CZECH,
                Language.FRENCH,
                Language.HUNGARIAN,
                Language.ICELANDIC,
                Language.IRISH,
                Language.ITALIAN,
                Language.PORTUGUESE,
                Language.SLOVAK,
                Language.SPANISH,
                Language.VIETNAMESE,
                Language.YORUBA,
            ],
        ),
        pytest.param(
            "house",
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
            ],
        ),
    ],
)
def test_language_filtering_with_rules(
    detector_for_all_languages, word, expected_languages
):
    filtered_languages = detector_for_all_languages._filter_languages_by_rules([word])
    assert filtered_languages == frozenset(expected_languages)


@pytest.mark.parametrize("invalid_str", ["", " \n  \t;", "3<856%)§"])
def test_strings_without_letters_return_no_language(
    detector_for_all_languages, invalid_str
):
    assert detector_for_all_languages.detect_language_of(invalid_str) is None


@pytest.mark.parametrize(
    "language,ngram,expected_probability",
    [
        pytest.param(Language.ENGLISH, "a", f(log(0.01))),
        pytest.param(Language.ENGLISH, "lt", f(log(0.12))),
        pytest.param(Language.ENGLISH, "ter", f(log(0.21))),
        pytest.param(Language.ENGLISH, "alte", f(log(0.25))),
        pytest.param(Language.ENGLISH, "alter", f(log(0.29))),
        pytest.param(Language.GERMAN, "t", f(log(0.08))),
        pytest.param(Language.GERMAN, "er", f(log(0.18))),
        pytest.param(Language.GERMAN, "alt", f(log(0.22))),
        pytest.param(Language.GERMAN, "lter", f(log(0.28))),
        pytest.param(Language.GERMAN, "alter", f(log(0.3))),
    ],
)
def test_ngram_probability_lookup(
    detector_for_english_and_german, language, ngram, expected_probability
):
    probability = detector_for_english_and_german._look_up_ngram_probability(
        language, ngram
    )
    assert probability == expected_probability


@pytest.mark.parametrize(
    "ngrams, expected_sum_of_probabilities",
    [
        pytest.param(
            frozenset(["a", "l", "t", "e", "r"]),
            f(log(0.01)) + f(log(0.02)) + f(log(0.03)) + f(log(0.04)) + f(log(0.05)),
        ),
        pytest.param(
            # back off unknown Trigram("tez") to known Bigram("te")
            frozenset(["alt", "lte", "tez"]),
            f(log(0.19)) + f(log(0.2)) + f(log(0.13)),
        ),
        pytest.param(
            # back off unknown Fivegram("aquas") to known Unigram("a")
            frozenset(["aquas"]),
            f(log(0.01)),
        ),
    ],
)
def test_summation_of_ngram_probabilities(
    detector_for_english_and_german, ngrams, expected_sum_of_probabilities
):
    sum_of_probabilities = (
        detector_for_english_and_german._compute_sum_of_ngram_probabilities(
            Language.ENGLISH, ngrams
        )
    )
    assert isclose(sum_of_probabilities, expected_sum_of_probabilities, rel_tol=0.001)


@pytest.mark.parametrize(
    "test_data_model,expected_probabilities",
    [
        pytest.param(
            _TestDataLanguageModel(frozenset(["a", "l", "t", "e", "r"])),
            {
                Language.ENGLISH: f(log(0.01))
                + f(log(0.02))
                + f(log(0.03))
                + f(log(0.04))
                + f(log(0.05)),
                Language.GERMAN: f(log(0.06))
                + f(log(0.07))
                + f(log(0.08))
                + f(log(0.09))
                + f(log(0.1)),
            },
        ),
        pytest.param(
            _TestDataLanguageModel(frozenset(["alt", "lte", "ter", "wxy"])),
            {
                Language.ENGLISH: f(log(0.19)) + f(log(0.2)) + f(log(0.21)),
                Language.GERMAN: f(log(0.22)) + f(log(0.23)) + f(log(0.24)),
            },
        ),
        pytest.param(
            _TestDataLanguageModel(frozenset(["alte", "lter", "wxyz"])),
            {
                Language.ENGLISH: f(log(0.25)) + f(log(0.26)),
                Language.GERMAN: f(log(0.27)) + f(log(0.28)),
            },
        ),
    ],
)
def test_computation_of_language_probabilities(
    detector_for_english_and_german, test_data_model, expected_probabilities
):
    probabilities = detector_for_english_and_german._compute_language_probabilities(
        test_data_model, frozenset([Language.ENGLISH, Language.GERMAN])
    )
    for language, probability in probabilities.items():
        expected_probability = expected_probabilities[language]
        assert isclose(probability, expected_probability, rel_tol=0.001)


def test_detect_language(detector_for_english_and_german):
    assert (
        detector_for_english_and_german.detect_language_of("Alter") == Language.GERMAN
    )


def test_compute_language_confidence_values(detector_for_english_and_german):
    unigram_count_for_both_languages = 5
    english_probabilities = [
        # unigrams
        0.01,
        0.02,
        0.03,
        0.04,
        0.05,
        # bigrams
        0.11,
        0.12,
        0.13,
        0.14,
        # trigrams
        0.19,
        0.2,
        0.21,
        # quadrigrams
        0.25,
        0.26,
        # fivegrams
        0.29,
    ]
    german_probabilities = [
        # unigrams
        0.06,
        0.07,
        0.08,
        0.09,
        0.1,
        # bigrams
        0.15,
        0.16,
        0.17,
        0.18,
        # trigrams
        0.22,
        0.23,
        0.24,
        # quadrigrams
        0.27,
        0.28,
        # fivegrams
        0.3,
    ]
    total_probability_for_english = (
        sum([f(log(probability)) for probability in english_probabilities])
        / unigram_count_for_both_languages
    )
    total_probability_for_german = (
        sum([f(log(probability)) for probability in german_probabilities])
        / unigram_count_for_both_languages
    )
    expected_confidence_value_for_english = (
        total_probability_for_german / total_probability_for_english
    )
    confidence_values = (
        detector_for_english_and_german.compute_language_confidence_values("Alter")
    )

    assert len(confidence_values) == 2
    assert confidence_values[0] == (Language.GERMAN, 1.0)
    assert confidence_values[1][0] == Language.ENGLISH
    assert isclose(
        confidence_values[1][1], expected_confidence_value_for_english, rel_tol=0.001
    )


def test_no_language_is_returned(detector_for_english_and_german):
    assert detector_for_english_and_german.detect_language_of("проарплап") is None


def test_no_confidence_values_are_returned(detector_for_english_and_german):
    assert (
        detector_for_english_and_german.compute_language_confidence_values("проарплап")
        == []
    )


@pytest.mark.parametrize(
    "text,languages",
    [
        pytest.param(
            "ام وی با نیکی میناج تیزر داشت؟؟؟؟؟؟ i vote for bts ( _ ) as the _ via ( _ )",
            [Language.ENGLISH, Language.URDU],
        ),
        pytest.param(
            "Az elmúlt hétvégén 12-re emelkedett az elhunyt koronavírus-fertőzöttek száma Szlovákiában. Mindegyik szociális otthon dolgozóját letesztelik, Matovič szerint az ingázóknak még várniuk kellene a teszteléssel",
            [Language.HUNGARIAN, Language.SLOVAK],
        ),
    ],
)
def test_deterministic_language_detection(detector_for_all_languages, text, languages):
    detected_languages = set()
    for i in range(0, 50):
        language = detector_for_all_languages.detect_language_of(text)
        detected_languages.add(language)
    assert len(detected_languages) == 1
