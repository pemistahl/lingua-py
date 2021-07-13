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

import json
import pytest

from fractions import Fraction
from typing import Final

from lingua.language import Language
from lingua._model import (
    _TrainingDataLanguageModel,
    _TestDataLanguageModel,
    _JSONLanguageModel,
    _LinguaJSONDecoder,
    _LinguaJSONEncoder,
)

TEXT: Final = """These sentences are intended for testing purposes.
    ⚠ Do not use them in production
    By the way, they consist of 23 words in total."""


def map_values_to_fractions(dct: dict[str, str]) -> dict[str, Fraction]:
    ngrams = {}
    for key, value in dct.items():
        numerator, denominator = value.split("/")
        ngrams[key] = Fraction(int(numerator), int(denominator))
    return ngrams


def expected_unigrams() -> frozenset[str]:
    return frozenset(
        {
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "l",
            "m",
            "n",
            "o",
            "p",
            "r",
            "s",
            "t",
            "u",
            "w",
            "y",
        }
    )


def expected_unigram_absolute_frequencies() -> dict[str, int]:
    return {
        "a": 3,
        "b": 1,
        "c": 3,
        "d": 5,
        "e": 14,
        "f": 2,
        "g": 1,
        "h": 4,
        "i": 6,
        "l": 1,
        "m": 1,
        "n": 10,
        "o": 10,
        "p": 3,
        "r": 5,
        "s": 10,
        "t": 13,
        "u": 3,
        "w": 2,
        "y": 3,
    }


def expected_unigram_relative_frequencies() -> dict[str, Fraction]:
    return map_values_to_fractions(
        {
            "a": "3/100",
            "b": "1/100",
            "c": "3/100",
            "d": "1/20",
            "e": "7/50",
            "f": "1/50",
            "g": "1/100",
            "h": "1/25",
            "i": "3/50",
            "l": "1/100",
            "m": "1/100",
            "n": "1/10",
            "o": "1/10",
            "p": "3/100",
            "r": "1/20",
            "s": "1/10",
            "t": "13/100",
            "u": "3/100",
            "w": "1/50",
            "y": "3/100",
        }
    )


def expected_bigrams() -> frozenset[str]:
    return frozenset(
        {
            "de",
            "pr",
            "pu",
            "do",
            "uc",
            "ds",
            "du",
            "ur",
            "us",
            "ed",
            "in",
            "io",
            "em",
            "en",
            "is",
            "al",
            "es",
            "ar",
            "rd",
            "re",
            "ey",
            "nc",
            "nd",
            "ay",
            "ng",
            "ro",
            "rp",
            "no",
            "ns",
            "nt",
            "fo",
            "wa",
            "se",
            "od",
            "si",
            "by",
            "of",
            "wo",
            "on",
            "st",
            "ce",
            "or",
            "os",
            "ot",
            "co",
            "ta",
            "te",
            "ct",
            "th",
            "ti",
            "to",
            "he",
            "po",
        }
    )


def expected_unigram_json_relative_frequencies() -> dict[str, float]:
    return {
        ngram: frac.numerator / frac.denominator
        for ngram, frac in expected_unigram_relative_frequencies().items()
    }


def expected_bigram_absolute_frequencies() -> dict[str, int]:
    return {
        "de": 1,
        "pr": 1,
        "pu": 1,
        "do": 1,
        "uc": 1,
        "ds": 1,
        "du": 1,
        "ur": 1,
        "us": 1,
        "ed": 1,
        "in": 4,
        "io": 1,
        "em": 1,
        "en": 3,
        "is": 1,
        "al": 1,
        "es": 4,
        "ar": 1,
        "rd": 1,
        "re": 1,
        "ey": 1,
        "nc": 1,
        "nd": 1,
        "ay": 1,
        "ng": 1,
        "ro": 1,
        "rp": 1,
        "no": 1,
        "ns": 1,
        "nt": 2,
        "fo": 1,
        "wa": 1,
        "se": 4,
        "od": 1,
        "si": 1,
        "of": 1,
        "by": 1,
        "wo": 1,
        "on": 2,
        "st": 2,
        "ce": 1,
        "or": 2,
        "os": 1,
        "ot": 2,
        "co": 1,
        "ta": 1,
        "ct": 1,
        "te": 3,
        "th": 4,
        "ti": 2,
        "to": 1,
        "he": 4,
        "po": 1,
    }


def expected_bigram_relative_frequencies() -> dict[str, Fraction]:
    return map_values_to_fractions(
        {
            "de": "1/5",
            "pr": "1/3",
            "pu": "1/3",
            "do": "1/5",
            "uc": "1/3",
            "ds": "1/5",
            "du": "1/5",
            "ur": "1/3",
            "us": "1/3",
            "ed": "1/14",
            "in": "2/3",
            "io": "1/6",
            "em": "1/14",
            "en": "3/14",
            "is": "1/6",
            "al": "1/3",
            "es": "2/7",
            "ar": "1/3",
            "rd": "1/5",
            "re": "1/5",
            "ey": "1/14",
            "nc": "1/10",
            "nd": "1/10",
            "ay": "1/3",
            "ng": "1/10",
            "ro": "1/5",
            "rp": "1/5",
            "no": "1/10",
            "ns": "1/10",
            "nt": "1/5",
            "fo": "1/2",
            "wa": "1/2",
            "se": "2/5",
            "od": "1/10",
            "si": "1/10",
            "of": "1/10",
            "by": "1/1",
            "wo": "1/2",
            "on": "1/5",
            "st": "1/5",
            "ce": "1/3",
            "or": "1/5",
            "os": "1/10",
            "ot": "1/5",
            "co": "1/3",
            "ta": "1/13",
            "ct": "1/3",
            "te": "3/13",
            "th": "4/13",
            "ti": "2/13",
            "to": "1/13",
            "he": "1/1",
            "po": "1/3",
        }
    )


def expected_trigrams() -> frozenset[str]:
    return frozenset(
        {
            "rds",
            "ose",
            "ded",
            "con",
            "use",
            "est",
            "ion",
            "ist",
            "pur",
            "hem",
            "hes",
            "tin",
            "cti",
            "tio",
            "wor",
            "ten",
            "hey",
            "ota",
            "tal",
            "tes",
            "uct",
            "sti",
            "pro",
            "odu",
            "nsi",
            "rod",
            "for",
            "ces",
            "nce",
            "not",
            "are",
            "pos",
            "tot",
            "end",
            "enc",
            "sis",
            "sen",
            "nte",
            "ses",
            "ord",
            "ing",
            "ent",
            "int",
            "nde",
            "way",
            "the",
            "rpo",
            "urp",
            "duc",
            "ons",
            "ese",
        }
    )


def expected_trigram_absolute_frequencies() -> dict[str, int]:
    return {
        "rds": 1,
        "ose": 1,
        "ded": 1,
        "con": 1,
        "use": 1,
        "est": 1,
        "ion": 1,
        "ist": 1,
        "pur": 1,
        "hem": 1,
        "hes": 1,
        "tin": 1,
        "cti": 1,
        "wor": 1,
        "tio": 1,
        "ten": 2,
        "ota": 1,
        "hey": 1,
        "tal": 1,
        "tes": 1,
        "uct": 1,
        "sti": 1,
        "pro": 1,
        "odu": 1,
        "nsi": 1,
        "rod": 1,
        "for": 1,
        "ces": 1,
        "nce": 1,
        "not": 1,
        "pos": 1,
        "are": 1,
        "tot": 1,
        "end": 1,
        "enc": 1,
        "sis": 1,
        "sen": 1,
        "nte": 2,
        "ord": 1,
        "ses": 1,
        "ing": 1,
        "ent": 1,
        "way": 1,
        "nde": 1,
        "int": 1,
        "rpo": 1,
        "the": 4,
        "urp": 1,
        "duc": 1,
        "ons": 1,
        "ese": 1,
    }


def expected_trigram_relative_frequencies() -> dict[str, Fraction]:
    return map_values_to_fractions(
        {
            "rds": "1/1",
            "ose": "1/1",
            "ded": "1/1",
            "con": "1/1",
            "use": "1/1",
            "est": "1/4",
            "ion": "1/1",
            "ist": "1/1",
            "pur": "1/1",
            "hem": "1/4",
            "hes": "1/4",
            "tin": "1/2",
            "cti": "1/1",
            "wor": "1/1",
            "tio": "1/2",
            "ten": "2/3",
            "ota": "1/2",
            "hey": "1/4",
            "tal": "1/1",
            "tes": "1/3",
            "uct": "1/1",
            "sti": "1/2",
            "pro": "1/1",
            "odu": "1/1",
            "nsi": "1/1",
            "rod": "1/1",
            "for": "1/1",
            "ces": "1/1",
            "nce": "1/1",
            "not": "1/1",
            "pos": "1/1",
            "are": "1/1",
            "tot": "1/1",
            "end": "1/3",
            "enc": "1/3",
            "sis": "1/1",
            "sen": "1/4",
            "nte": "1/1",
            "ord": "1/2",
            "ses": "1/4",
            "ing": "1/4",
            "ent": "1/3",
            "way": "1/1",
            "nde": "1/1",
            "int": "1/4",
            "rpo": "1/1",
            "the": "1/1",
            "urp": "1/1",
            "duc": "1/1",
            "ons": "1/2",
            "ese": "1/4",
        }
    )


def expected_quadrigrams() -> frozenset[str]:
    return frozenset(
        {
            "onsi",
            "sist",
            "ende",
            "ords",
            "esti",
            "tenc",
            "nces",
            "oduc",
            "tend",
            "thes",
            "rpos",
            "ting",
            "nten",
            "nsis",
            "they",
            "tota",
            "cons",
            "tion",
            "prod",
            "ence",
            "test",
            "otal",
            "pose",
            "nded",
            "oses",
            "inte",
            "urpo",
            "them",
            "sent",
            "duct",
            "stin",
            "ente",
            "ucti",
            "purp",
            "ctio",
            "rodu",
            "word",
            "hese",
        }
    )


def expected_quadrigram_absolute_frequencies() -> dict[str, int]:
    return {
        "onsi": 1,
        "sist": 1,
        "ende": 1,
        "ords": 1,
        "esti": 1,
        "oduc": 1,
        "nces": 1,
        "tenc": 1,
        "tend": 1,
        "thes": 1,
        "rpos": 1,
        "ting": 1,
        "nsis": 1,
        "nten": 2,
        "tota": 1,
        "they": 1,
        "cons": 1,
        "tion": 1,
        "prod": 1,
        "otal": 1,
        "test": 1,
        "ence": 1,
        "pose": 1,
        "oses": 1,
        "nded": 1,
        "inte": 1,
        "them": 1,
        "urpo": 1,
        "duct": 1,
        "sent": 1,
        "stin": 1,
        "ucti": 1,
        "ente": 1,
        "purp": 1,
        "ctio": 1,
        "rodu": 1,
        "word": 1,
        "hese": 1,
    }


def expected_quadrigram_relative_frequencies() -> dict[str, Fraction]:
    return map_values_to_fractions(
        {
            "onsi": "1/1",
            "sist": "1/1",
            "ende": "1/1",
            "ords": "1/1",
            "esti": "1/1",
            "oduc": "1/1",
            "nces": "1/1",
            "tenc": "1/2",
            "tend": "1/2",
            "thes": "1/4",
            "rpos": "1/1",
            "ting": "1/1",
            "nsis": "1/1",
            "nten": "1/1",
            "tota": "1/1",
            "they": "1/4",
            "cons": "1/1",
            "tion": "1/1",
            "prod": "1/1",
            "otal": "1/1",
            "test": "1/1",
            "ence": "1/1",
            "pose": "1/1",
            "oses": "1/1",
            "nded": "1/1",
            "inte": "1/1",
            "them": "1/4",
            "urpo": "1/1",
            "duct": "1/1",
            "sent": "1/1",
            "stin": "1/1",
            "ucti": "1/1",
            "ente": "1/1",
            "purp": "1/1",
            "ctio": "1/1",
            "rodu": "1/1",
            "word": "1/1",
            "hese": "1/1",
        }
    )


def expected_fivegrams() -> frozenset[str]:
    return frozenset(
        {
            "testi",
            "sente",
            "ences",
            "tende",
            "these",
            "ntenc",
            "ducti",
            "ntend",
            "onsis",
            "total",
            "uctio",
            "enten",
            "poses",
            "ction",
            "produ",
            "inten",
            "nsist",
            "words",
            "sting",
            "tence",
            "purpo",
            "estin",
            "roduc",
            "urpos",
            "ended",
            "rpose",
            "oduct",
            "consi",
        }
    )


def expected_fivegram_absolute_frequencies() -> dict[str, int]:
    return {
        "testi": 1,
        "sente": 1,
        "ences": 1,
        "tende": 1,
        "ducti": 1,
        "ntenc": 1,
        "these": 1,
        "onsis": 1,
        "ntend": 1,
        "total": 1,
        "uctio": 1,
        "enten": 1,
        "poses": 1,
        "ction": 1,
        "produ": 1,
        "inten": 1,
        "nsist": 1,
        "words": 1,
        "sting": 1,
        "purpo": 1,
        "tence": 1,
        "estin": 1,
        "roduc": 1,
        "urpos": 1,
        "rpose": 1,
        "ended": 1,
        "oduct": 1,
        "consi": 1,
    }


def expected_fivegram_relative_frequencies() -> dict[str, Fraction]:
    return map_values_to_fractions(
        {
            "testi": "1/1",
            "sente": "1/1",
            "ences": "1/1",
            "tende": "1/1",
            "ducti": "1/1",
            "ntenc": "1/2",
            "these": "1/1",
            "onsis": "1/1",
            "ntend": "1/2",
            "total": "1/1",
            "uctio": "1/1",
            "enten": "1/1",
            "poses": "1/1",
            "ction": "1/1",
            "produ": "1/1",
            "inten": "1/1",
            "nsist": "1/1",
            "words": "1/1",
            "sting": "1/1",
            "purpo": "1/1",
            "tence": "1/1",
            "estin": "1/1",
            "roduc": "1/1",
            "urpos": "1/1",
            "rpose": "1/1",
            "ended": "1/1",
            "oduct": "1/1",
            "consi": "1/1",
        }
    )


def test_json_language_model_serializer_and_deserializer():
    model = _JSONLanguageModel(Language.ENGLISH, {"3/5": "a b c d e"})

    serialized = json.dumps(model, cls=_LinguaJSONEncoder)
    assert serialized == '{"language": "ENGLISH", "ngrams": {"3/5": "a b c d e"}}'

    deserialized = json.loads(serialized, cls=_LinguaJSONDecoder)
    assert deserialized == model


@pytest.mark.parametrize(
    "ngram_length,"
    "expected_absolute_frequencies,"
    "expected_relative_frequencies,"
    "lower_ngram_absolute_frequencies",
    [
        pytest.param(
            1,
            expected_unigram_absolute_frequencies(),
            expected_unigram_relative_frequencies(),
            {},
            id="unigram_model",
        ),
        pytest.param(
            2,
            expected_bigram_absolute_frequencies(),
            expected_bigram_relative_frequencies(),
            expected_unigram_absolute_frequencies(),
            id="bigram_model",
        ),
        pytest.param(
            3,
            expected_trigram_absolute_frequencies(),
            expected_trigram_relative_frequencies(),
            expected_bigram_absolute_frequencies(),
            id="trigram_model",
        ),
        pytest.param(
            4,
            expected_quadrigram_absolute_frequencies(),
            expected_quadrigram_relative_frequencies(),
            expected_trigram_absolute_frequencies(),
            id="quadrigram_model",
        ),
        pytest.param(
            5,
            expected_fivegram_absolute_frequencies(),
            expected_fivegram_relative_frequencies(),
            expected_quadrigram_absolute_frequencies(),
            id="fivegram_model",
        ),
    ],
)
def test_training_data_model_creation(
    ngram_length,
    expected_absolute_frequencies,
    expected_relative_frequencies,
    lower_ngram_absolute_frequencies,
):
    model = _TrainingDataLanguageModel.from_text(
        TEXT.strip().lower().splitlines(),
        Language.ENGLISH,
        ngram_length,
        "\\p{L}&&\\p{Latin}",
        lower_ngram_absolute_frequencies,
    )
    assert model.language == Language.ENGLISH
    assert model.absolute_frequencies == expected_absolute_frequencies
    assert model.relative_frequencies == expected_relative_frequencies


@pytest.mark.parametrize(
    "ngram_length,expected_ngrams",
    [
        pytest.param(1, expected_unigrams(), id="unigram_model"),
        pytest.param(2, expected_bigrams(), id="bigram_model"),
        pytest.param(3, expected_trigrams(), id="trigram_model"),
        pytest.param(4, expected_quadrigrams(), id="quadrigram_model"),
        pytest.param(5, expected_fivegrams(), id="fivegram_model"),
    ],
)
def test_test_data_model_creation(ngram_length, expected_ngrams):
    model = _TestDataLanguageModel.from_text(TEXT.lower(), ngram_length)
    assert model.ngrams == expected_ngrams
