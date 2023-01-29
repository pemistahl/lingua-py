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

from lingua.builder import LanguageDetectorBuilder
from lingua.detector import (
    ConfidenceValue,
    LanguageDetector,
    _UNIGRAM_MODELS,
    _BIGRAM_MODELS,
    _TRIGRAM_MODELS,
    _QUADRIGRAM_MODELS,
    _FIVEGRAM_MODELS,
    _collect_languages_with_unique_characters,
    _collect_one_language_alphabets,
    _split_text_into_words,
)
from lingua.language import Language
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
                # ("w", 0.0),
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
                # ("aq", 0.0),
                # ("wx", 0.0),
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
                # ("aqu", 0.0),
                # ("tez", 0.0),
                # ("wxy", 0.0),
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
                # ("aqua", 0.0),
                # ("wxyz", 0.0),
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
                # ("aquas", 0.0),
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
                # ("w", 0.0),
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
                # ("wx", 0.0),
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
                # ("wxy", 0.0),
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
                # ("wxyz", 0.0),
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
    languages = frozenset([Language.ENGLISH, Language.GERMAN])
    return LanguageDetector(
        _languages=languages,
        _minimum_relative_distance=0.0,
        _is_low_accuracy_mode_enabled=False,
        _languages_with_unique_characters=_collect_languages_with_unique_characters(
            languages
        ),
        _one_language_alphabets=_collect_one_language_alphabets(languages),
        _unigram_language_models=unigram_models,
        _bigram_language_models=bigram_models,
        _trigram_language_models=trigram_models,
        _quadrigram_language_models=quadrigram_models,
        _fivegram_language_models=fivegram_models,
        _cache={},
    )


detector_for_all_languages = (
    LanguageDetectorBuilder.from_all_languages()
    .with_preloaded_language_models()
    .build()
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
        pytest.param(
            "Weltweit    gibt es ungefähr 6.000 Sprachen.",
            ["weltweit", "gibt", "es", "ungefähr", "sprachen"],
        ),
    ],
)
def test_text_is_split_into_words_correctly(text, expected_words):
    assert _split_text_into_words(text) == expected_words


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
def test_language_detection_with_rules(word, expected_language):
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
                Language.GERMAN,
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
                Language.GERMAN,
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
                Language.GERMAN,
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
                Language.GERMAN,
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
            ],
        ),
        pytest.param(
            "només",
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
def test_language_filtering_with_rules(word, expected_languages):
    filtered_languages = detector_for_all_languages._filter_languages_by_rules([word])
    assert filtered_languages == frozenset(expected_languages)


@pytest.mark.parametrize("invalid_str", ["", " \n  \t;", "3<856%)§"])
def test_strings_without_letters_return_no_language(invalid_str):
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
        # unknown ngrams
        pytest.param(Language.GERMAN, "xyz", None),
        pytest.param(Language.ENGLISH, "ab", None),
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
    "ngram_model, expected_sum_of_probabilities",
    [
        pytest.param(
            _TestDataLanguageModel([["a"], ["l"], ["t"], ["e"], ["r"]]),
            f(log(0.01)) + f(log(0.02)) + f(log(0.03)) + f(log(0.04)) + f(log(0.05)),
        ),
        pytest.param(
            # back off unknown Trigram("tez") to known Bigram("te")
            _TestDataLanguageModel(
                [["alt", "al", "a"], ["lte", "lt", "l"], ["tez", "te", "t"]]
            ),
            f(log(0.19)) + f(log(0.2)) + f(log(0.13)),
        ),
        pytest.param(
            # back off unknown Fivegram("aquas") to known Unigram("a")
            _TestDataLanguageModel([["aquas", "aqua", "aqu", "aq", "a"]]),
            f(log(0.01)),
        ),
    ],
)
def test_summation_of_ngram_probabilities(
    detector_for_english_and_german, ngram_model, expected_sum_of_probabilities
):
    sum_of_probabilities = (
        detector_for_english_and_german._compute_sum_of_ngram_probabilities(
            Language.ENGLISH, ngram_model
        )
    )
    assert isclose(sum_of_probabilities, expected_sum_of_probabilities, rel_tol=0.001)


@pytest.mark.parametrize(
    "ngram_model,expected_probabilities",
    [
        pytest.param(
            _TestDataLanguageModel([["a"], ["l"], ["t"], ["e"], ["r"]]),
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
            _TestDataLanguageModel(
                [
                    ["alt", "al", "a"],
                    ["lte", "lt", "l"],
                    ["ter", "te", "t"],
                    ["wxy", "wx", "w"],
                ]
            ),
            {
                Language.ENGLISH: f(log(0.19)) + f(log(0.2)) + f(log(0.21)),
                Language.GERMAN: f(log(0.22)) + f(log(0.23)) + f(log(0.24)),
            },
        ),
        pytest.param(
            _TestDataLanguageModel(
                [
                    ["alte", "alt", "al", "a"],
                    ["lter", "lte", "lt", "l"],
                    ["wxyz", "wxy", "wx", "w"],
                ]
            ),
            {
                Language.ENGLISH: f(log(0.25)) + f(log(0.26)),
                Language.GERMAN: f(log(0.27)) + f(log(0.28)),
            },
        ),
    ],
)
def test_computation_of_language_probabilities(
    detector_for_english_and_german, ngram_model, expected_probabilities
):
    probabilities = detector_for_english_and_german._compute_language_probabilities(
        ngram_model, frozenset([Language.ENGLISH, Language.GERMAN])
    )
    for language, probability in probabilities.items():
        expected_probability = expected_probabilities[language]
        assert isclose(probability, expected_probability, rel_tol=0.001)


def test_detect_language(detector_for_english_and_german):
    assert (
        detector_for_english_and_german.detect_language_of("Alter") == Language.GERMAN
    )


def test_no_language_is_returned(detector_for_english_and_german):
    assert detector_for_english_and_german.detect_language_of("проарплап") is None


@pytest.mark.parametrize(
    "text,expected_confidence_values",
    [
        pytest.param(
            "groß",
            [
                ConfidenceValue(Language.GERMAN, 1.0),
                ConfidenceValue(Language.ENGLISH, 0.0),
            ],
        ),
        pytest.param(
            "Alter",
            [
                ConfidenceValue(Language.GERMAN, 0.81),
                ConfidenceValue(Language.ENGLISH, 0.19),
            ],
        ),
        pytest.param(
            "проарплап",
            [
                ConfidenceValue(Language.ENGLISH, 0.0),
                ConfidenceValue(Language.GERMAN, 0.0),
            ],
        ),
    ],
)
def test_compute_language_confidence_values(
    detector_for_english_and_german, text, expected_confidence_values
):
    confidence_values = (
        detector_for_english_and_german.compute_language_confidence_values(text)
    )
    assert len(confidence_values) == 2

    first, second = confidence_values
    expected_first, expected_second = expected_confidence_values

    assert first.language == expected_first.language
    assert round(first.value, 2) == expected_first.value

    assert second.language == expected_second.language
    assert round(second.value, 2) == expected_second.value


@pytest.mark.parametrize(
    "text,expected_confidence_for_german,expected_confidence_for_english",
    [
        pytest.param("groß", 1.0, 0.0),
        pytest.param("Alter", 0.81, 0.19),
        pytest.param("проарплап", 0.0, 0.0),
    ],
)
def test_compute_language_confidence(
    detector_for_english_and_german,
    text,
    expected_confidence_for_german,
    expected_confidence_for_english,
):
    confidence_for_german = detector_for_english_and_german.compute_language_confidence(
        text, Language.GERMAN
    )
    assert round(confidence_for_german, 2) == expected_confidence_for_german

    confidence_for_english = (
        detector_for_english_and_german.compute_language_confidence(
            text, Language.ENGLISH
        )
    )
    assert round(confidence_for_english, 2) == expected_confidence_for_english

    confidence_for_french = detector_for_english_and_german.compute_language_confidence(
        text, Language.FRENCH
    )
    assert confidence_for_french == 0.0


def test_detect_multiple_languages_for_empty_string():
    assert detector_for_all_languages.detect_multiple_languages_of("") == []


def test_detect_multiple_languages_english():
    sentence = "I'm really not sure whether multi-language detection is a good idea."

    results = detector_for_all_languages.detect_multiple_languages_of(sentence)
    assert len(results) == 1

    result = results[0]
    substring = sentence[result.start_index : result.end_index]
    assert substring == sentence
    assert result.language == Language.ENGLISH


def test_detect_multiple_languages_english_and_german():
    sentence = (
        "  He   turned around and asked: "
        + '"Entschuldigen Sie, sprechen Sie Deutsch?"'
    )
    results = detector_for_all_languages.detect_multiple_languages_of(sentence)
    assert len(results) == 2

    first_result = results[0]
    first_substring = sentence[first_result.start_index : first_result.end_index]
    assert first_substring == "  He   turned around and asked: "
    assert first_result.language == Language.ENGLISH

    second_result = results[1]
    second_substring = sentence[second_result.start_index : second_result.end_index]
    assert second_substring == '"Entschuldigen Sie, sprechen Sie Deutsch?"'
    assert second_result.language == Language.GERMAN


def test_detect_multiple_languages_chinese_english():
    sentence = "上海大学是一个好大学. It is such a great university."

    results = detector_for_all_languages.detect_multiple_languages_of(sentence)
    assert len(results) == 2

    first_result = results[0]
    first_substring = sentence[first_result.start_index : first_result.end_index]
    assert first_substring == "上海大学是一个好大学. "
    assert first_result.language == Language.CHINESE

    second_result = results[1]
    second_substring = sentence[second_result.start_index : second_result.end_index]
    assert second_substring == "It is such a great university."
    assert second_result.language == Language.ENGLISH


def test_detect_multiple_languages_french_german_english():
    sentence = (
        "Parlez-vous français? "
        + "Ich spreche Französisch nur ein bisschen. "
        + "A little bit is better than nothing."
    )

    results = detector_for_all_languages.detect_multiple_languages_of(sentence)
    assert len(results) == 3

    first_result = results[0]
    first_substring = sentence[first_result.start_index : first_result.end_index]
    assert first_substring == "Parlez-vous français? "
    assert first_result.language == Language.FRENCH

    second_result = results[1]
    second_substring = sentence[second_result.start_index : second_result.end_index]
    assert second_substring == "Ich spreche Französisch nur ein bisschen. "
    assert second_result.language == Language.GERMAN

    third_result = results[2]
    third_substring = sentence[third_result.start_index : third_result.end_index]
    assert third_substring == "A little bit is better than nothing."
    assert third_result.language == Language.ENGLISH


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
def test_deterministic_language_detection(text, languages):
    detected_languages = set()
    for i in range(0, 50):
        language = detector_for_all_languages.detect_language_of(text)
        detected_languages.add(language)
    assert len(detected_languages) == 1


def test_low_accuracy_mode():
    remove_language_models_from_detector()

    assert_all_language_models_are_unloaded()

    detector = (
        LanguageDetectorBuilder.from_languages(Language.ENGLISH, Language.GERMAN)
        .with_preloaded_language_models()
        .with_low_accuracy_mode()
        .build()
    )

    assert_only_trigram_language_models_are_loaded()

    assert detector.detect_language_of("bed") == Language.ENGLISH
    assert detector.detect_language_of("be") is None
    assert detector.detect_language_of("b") is None
    assert detector.detect_language_of("") is None

    assert_only_trigram_language_models_are_loaded()


def test_two_detectors_share_same_language_models():
    remove_language_models_from_detector()

    assert_all_language_models_are_unloaded()

    first_detector = (
        LanguageDetectorBuilder.from_languages(Language.ENGLISH, Language.GERMAN)
        .with_preloaded_language_models()
        .with_low_accuracy_mode()
        .build()
    )

    second_detector = (
        LanguageDetectorBuilder.from_languages(Language.SWEDISH, Language.ENGLISH)
        .with_preloaded_language_models()
        .with_low_accuracy_mode()
        .build()
    )

    assert len(first_detector._trigram_language_models) == 3
    assert len(second_detector._trigram_language_models) == 3
    assert (
        first_detector._trigram_language_models
        is second_detector._trigram_language_models
    )


def assert_all_language_models_are_unloaded():
    assert len(_UNIGRAM_MODELS) == 0
    assert len(_BIGRAM_MODELS) == 0
    assert len(_TRIGRAM_MODELS) == 0
    assert len(_QUADRIGRAM_MODELS) == 0
    assert len(_FIVEGRAM_MODELS) == 0


def assert_only_trigram_language_models_are_loaded():
    assert len(_UNIGRAM_MODELS) == 0
    assert len(_BIGRAM_MODELS) == 0
    assert len(_TRIGRAM_MODELS) > 0
    assert len(_QUADRIGRAM_MODELS) == 0
    assert len(_FIVEGRAM_MODELS) == 0


def remove_language_models_from_detector():
    _UNIGRAM_MODELS.clear()
    _BIGRAM_MODELS.clear()
    _TRIGRAM_MODELS.clear()
    _QUADRIGRAM_MODELS.clear()
    _FIVEGRAM_MODELS.clear()
