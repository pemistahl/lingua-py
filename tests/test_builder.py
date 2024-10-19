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

from lingua.builder import LanguageDetectorBuilder
from lingua.isocode import IsoCode639_1, IsoCode639_3
from lingua.language import Language


def test_build_from_all_languages():
    builder = LanguageDetectorBuilder.from_all_languages()
    assert builder._languages == Language.all()


def test_build_from_spoken_languages():
    builder = LanguageDetectorBuilder.from_all_spoken_languages()
    assert builder._languages == Language.all_spoken_ones()


def test_build_from_languages_with_arabic_script():
    builder = LanguageDetectorBuilder.from_all_languages_with_arabic_script()
    assert builder._languages == Language.all_with_arabic_script()


def test_build_from_languages_with_cyrillic_script():
    builder = LanguageDetectorBuilder.from_all_languages_with_cyrillic_script()
    assert builder._languages == Language.all_with_cyrillic_script()


def test_build_from_languages_with_devanagari_script():
    builder = LanguageDetectorBuilder.from_all_languages_with_devanagari_script()
    assert builder._languages == Language.all_with_devanagari_script()


def test_build_from_languages_with_latin_script():
    builder = LanguageDetectorBuilder.from_all_languages_with_latin_script()
    assert builder._languages == Language.all_with_latin_script()


def test_build_from_blacklist():
    languages = {Language.TURKISH, Language.ROMANIAN}
    builder = LanguageDetectorBuilder.from_all_languages_without(*languages)
    expected_languages = Language.all().difference(languages)
    assert builder._languages == expected_languages


def test_cannot_build_from_blacklist():
    with pytest.raises(ValueError) as exception_info:
        LanguageDetectorBuilder.from_all_languages_without(*Language.all())
    assert (
        exception_info.value.args[0]
        == "LanguageDetector needs at least 1 language to choose from"
    )


def test_build_from_whitelist():
    language_sets = [{Language.GERMAN}, {Language.GERMAN, Language.ENGLISH}]
    for languages in language_sets:
        builder = LanguageDetectorBuilder.from_languages(*languages)
        assert builder._languages == languages


def test_cannot_build_from_whitelist():
    with pytest.raises(ValueError) as exception_info:
        LanguageDetectorBuilder.from_languages()
    assert (
        exception_info.value.args[0]
        == "LanguageDetector needs at least 1 language to choose from"
    )


def test_build_from_iso_639_1_codes():
    builder = LanguageDetectorBuilder.from_iso_codes_639_1(IsoCode639_1.DE)
    assert builder._languages == {Language.GERMAN}

    builder = LanguageDetectorBuilder.from_iso_codes_639_1(
        IsoCode639_1.DE, IsoCode639_1.SV
    )
    assert builder._languages == {Language.GERMAN, Language.SWEDISH}


def test_cannot_build_from_iso_639_1_codes():
    with pytest.raises(ValueError) as exception_info:
        LanguageDetectorBuilder.from_iso_codes_639_1()
    assert (
        exception_info.value.args[0]
        == "LanguageDetector needs at least 1 language to choose from"
    )


def test_build_from_iso_639_3_codes():
    builder = LanguageDetectorBuilder.from_iso_codes_639_3(
        IsoCode639_3.DEU, IsoCode639_3.SWE
    )
    assert builder._languages == {Language.GERMAN, Language.SWEDISH}


def test_cannot_build_from_iso_639_3_codes():
    with pytest.raises(ValueError) as exception_info:
        LanguageDetectorBuilder.from_iso_codes_639_3()
    assert (
        exception_info.value.args[0]
        == "LanguageDetector needs at least 1 language to choose from"
    )


def test_build_with_minimum_relative_distance():
    builder = LanguageDetectorBuilder.from_all_languages()
    assert builder._minimum_relative_distance == 0.0
    builder.with_minimum_relative_distance(0.2)
    assert builder._minimum_relative_distance == 0.2


def test_cannot_build_with_minimum_relative_distance():
    builder = LanguageDetectorBuilder.from_all_languages()
    for value in (-0.01, -2.3, 1.0, 1.7):
        with pytest.raises(ValueError) as exception_info:
            builder.with_minimum_relative_distance(value)
        assert (
            exception_info.value.args[0]
            == "Minimum relative distance must lie in between 0.0 and 0.99"
        )


def test_build_with_low_accuracy_mode():
    builder = LanguageDetectorBuilder.from_all_languages()
    assert builder._is_low_accuracy_mode_enabled is False
    builder.with_low_accuracy_mode()
    assert builder._is_low_accuracy_mode_enabled is True
