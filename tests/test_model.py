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

from fractions import Fraction
from math import isclose

from lingua.detector import _split_text_into_words
from lingua.language import Language
from lingua._model import (
    _load_ngram_probability_model,
    _load_ngram_count_model,
    _create_lower_order_ngrams,
    _NgramModelType,
    _TrainingDataLanguageModel,
)
from tests import minify

TEXT: str = """These sentences are intended for testing purposes.
    ⚠ Do not use them in production
    By the way, they consist of 23 words in total."""


def map_values_to_fractions(dct: dict[str, str]) -> dict[str, Fraction]:
    ngrams = {}
    for key, value in dct.items():
        numerator, denominator = value.split("/")
        ngrams[key] = Fraction(int(numerator), int(denominator))
    return ngrams


def expected_unigrams() -> list[list[str]]:
    return [
        ["a"],
        ["b"],
        ["c"],
        ["d"],
        ["e"],
        ["f"],
        ["g"],
        ["h"],
        ["i"],
        ["l"],
        ["m"],
        ["n"],
        ["o"],
        ["p"],
        ["r"],
        ["s"],
        ["t"],
        ["u"],
        ["w"],
        ["y"],
    ]


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


def expected_unigram_model_json():
    return """
    {
        "language":"ENGLISH",
        "ngrams":{
            "3/100":"a c p u y",
            "1/100":"b g l m",
            "1/20":"d r",
            "7/50":"e",
            "1/50":"f w",
            "1/25":"h",
            "3/50":"i",
            "1/10":"n o s",
            "13/100":"t"
        }
    }
    """


def expected_bigrams() -> list[list[str]]:
    return [
        ["al", "a"],
        ["ar", "a"],
        ["ay", "a"],
        ["by", "b"],
        ["ce", "c"],
        ["co", "c"],
        ["ct", "c"],
        ["de", "d"],
        ["do", "d"],
        ["ds", "d"],
        ["du", "d"],
        ["ed", "e"],
        ["em", "e"],
        ["en", "e"],
        ["es", "e"],
        ["ey", "e"],
        ["fo", "f"],
        ["he", "h"],
        ["in", "i"],
        ["io", "i"],
        ["is", "i"],
        ["nc", "n"],
        ["nd", "n"],
        ["ng", "n"],
        ["no", "n"],
        ["ns", "n"],
        ["nt", "n"],
        ["od", "o"],
        ["of", "o"],
        ["on", "o"],
        ["or", "o"],
        ["os", "o"],
        ["ot", "o"],
        ["po", "p"],
        ["pr", "p"],
        ["pu", "p"],
        ["rd", "r"],
        ["re", "r"],
        ["ro", "r"],
        ["rp", "r"],
        ["se", "s"],
        ["si", "s"],
        ["st", "s"],
        ["ta", "t"],
        ["te", "t"],
        ["th", "t"],
        ["ti", "t"],
        ["to", "t"],
        ["uc", "u"],
        ["ur", "u"],
        ["us", "u"],
        ["wa", "w"],
        ["wo", "w"],
    ]


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


def expected_trigrams() -> list[list[str]]:
    return [
        ["are", "ar", "a"],
        ["ces", "ce", "c"],
        ["con", "co", "c"],
        ["cti", "ct", "c"],
        ["ded", "de", "d"],
        ["duc", "du", "d"],
        ["enc", "en", "e"],
        ["end", "en", "e"],
        ["ent", "en", "e"],
        ["ese", "es", "e"],
        ["est", "es", "e"],
        ["for", "fo", "f"],
        ["hem", "he", "h"],
        ["hes", "he", "h"],
        ["hey", "he", "h"],
        ["ing", "in", "i"],
        ["int", "in", "i"],
        ["ion", "io", "i"],
        ["ist", "is", "i"],
        ["nce", "nc", "n"],
        ["nde", "nd", "n"],
        ["not", "no", "n"],
        ["nsi", "ns", "n"],
        ["nte", "nt", "n"],
        ["odu", "od", "o"],
        ["ons", "on", "o"],
        ["ord", "or", "o"],
        ["ose", "os", "o"],
        ["ota", "ot", "o"],
        ["pos", "po", "p"],
        ["pro", "pr", "p"],
        ["pur", "pu", "p"],
        ["rds", "rd", "r"],
        ["rod", "ro", "r"],
        ["rpo", "rp", "r"],
        ["sen", "se", "s"],
        ["ses", "se", "s"],
        ["sis", "si", "s"],
        ["sti", "st", "s"],
        ["tal", "ta", "t"],
        ["ten", "te", "t"],
        ["tes", "te", "t"],
        ["the", "th", "t"],
        ["tin", "ti", "t"],
        ["tio", "ti", "t"],
        ["tot", "to", "t"],
        ["uct", "uc", "u"],
        ["urp", "ur", "u"],
        ["use", "us", "u"],
        ["way", "wa", "w"],
        ["wor", "wo", "w"],
    ]


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


def expected_quadrigrams() -> list[list[str]]:
    return [
        ["cons", "con", "co", "c"],
        ["ctio", "cti", "ct", "c"],
        ["duct", "duc", "du", "d"],
        ["ence", "enc", "en", "e"],
        ["ende", "end", "en", "e"],
        ["ente", "ent", "en", "e"],
        ["esti", "est", "es", "e"],
        ["hese", "hes", "he", "h"],
        ["inte", "int", "in", "i"],
        ["nces", "nce", "nc", "n"],
        ["nded", "nde", "nd", "n"],
        ["nsis", "nsi", "ns", "n"],
        ["nten", "nte", "nt", "n"],
        ["oduc", "odu", "od", "o"],
        ["onsi", "ons", "on", "o"],
        ["ords", "ord", "or", "o"],
        ["oses", "ose", "os", "o"],
        ["otal", "ota", "ot", "o"],
        ["pose", "pos", "po", "p"],
        ["prod", "pro", "pr", "p"],
        ["purp", "pur", "pu", "p"],
        ["rodu", "rod", "ro", "r"],
        ["rpos", "rpo", "rp", "r"],
        ["sent", "sen", "se", "s"],
        ["sist", "sis", "si", "s"],
        ["stin", "sti", "st", "s"],
        ["tenc", "ten", "te", "t"],
        ["tend", "ten", "te", "t"],
        ["test", "tes", "te", "t"],
        ["them", "the", "th", "t"],
        ["thes", "the", "th", "t"],
        ["they", "the", "th", "t"],
        ["ting", "tin", "ti", "t"],
        ["tion", "tio", "ti", "t"],
        ["tota", "tot", "to", "t"],
        ["ucti", "uct", "uc", "u"],
        ["urpo", "urp", "ur", "u"],
        ["word", "wor", "wo", "w"],
    ]


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


def expected_fivegrams() -> list[list[str]]:
    return [
        ["consi", "cons", "con", "co", "c"],
        ["ction", "ctio", "cti", "ct", "c"],
        ["ducti", "duct", "duc", "du", "d"],
        ["ences", "ence", "enc", "en", "e"],
        ["ended", "ende", "end", "en", "e"],
        ["enten", "ente", "ent", "en", "e"],
        ["estin", "esti", "est", "es", "e"],
        ["inten", "inte", "int", "in", "i"],
        ["nsist", "nsis", "nsi", "ns", "n"],
        ["ntenc", "nten", "nte", "nt", "n"],
        ["ntend", "nten", "nte", "nt", "n"],
        ["oduct", "oduc", "odu", "od", "o"],
        ["onsis", "onsi", "ons", "on", "o"],
        ["poses", "pose", "pos", "po", "p"],
        ["produ", "prod", "pro", "pr", "p"],
        ["purpo", "purp", "pur", "pu", "p"],
        ["roduc", "rodu", "rod", "ro", "r"],
        ["rpose", "rpos", "rpo", "rp", "r"],
        ["sente", "sent", "sen", "se", "s"],
        ["sting", "stin", "sti", "st", "s"],
        ["tence", "tenc", "ten", "te", "t"],
        ["tende", "tend", "ten", "te", "t"],
        ["testi", "test", "tes", "te", "t"],
        ["these", "thes", "the", "th", "t"],
        ["total", "tota", "tot", "to", "t"],
        ["uctio", "ucti", "uct", "uc", "u"],
        ["urpos", "urpo", "urp", "ur", "u"],
        ["words", "word", "wor", "wo", "w"],
    ]


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
def test_training_data_model_from_text(
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
    "language," "absolute_frequencies," "relative_frequencies," "expected_json",
    [
        pytest.param(
            Language.ENGLISH,
            expected_unigram_absolute_frequencies(),
            expected_unigram_relative_frequencies(),
            expected_unigram_model_json(),
        )
    ],
)
def test_training_data_model_to_json(
    language, absolute_frequencies, relative_frequencies, expected_json
):
    model = _TrainingDataLanguageModel(
        language, absolute_frequencies, relative_frequencies
    )
    assert model.to_json() == minify(expected_json)


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
    ngrams = _create_lower_order_ngrams(_split_text_into_words(TEXT), ngram_length)
    assert sorted(ngrams) == expected_ngrams


def test_load_ngram_probability_model():
    ngram_model = _load_ngram_probability_model(Language.ENGLISH, 1)
    assert ngram_model.language == Language.ENGLISH
    assert "a" in ngram_model.ngrams
    assert isclose(ngram_model.ngrams["a"], -2.470391707934208, rel_tol=0.001)


def test_load_ngram_model():
    unique_ngram_model = _load_ngram_count_model(
        Language.ENGLISH, 1, _NgramModelType.UNIQUE
    )
    assert unique_ngram_model.language == Language.ENGLISH
    assert unique_ngram_model.ngrams == frozenset(["ɦ", "ƅ", "ﬀ", "ƴ", "ｍ", "ȼ"])
