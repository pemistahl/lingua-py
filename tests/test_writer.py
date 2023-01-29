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

import numpy as np
import os
import pytest

from math import log
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

from lingua.language import Language
from lingua.writer import LanguageModelFilesWriter, TestDataFilesWriter


@pytest.fixture
def language_model_files_text():
    return (
        "These sentences are intended for testing purposes.\n"
        "Do not use them in production!\n"
        "By the way, they consist of 23 words in total."
    )


@pytest.fixture
def test_data_files_text():
    return (
        "There are many attributes associated with good software.\n"
        "Some of these can be mutually contradictory, and different customers and participants may have different priorities.\n"
        "Weinberg provides an example of how different goals can have a dramatic effect on both effort required and efficiency.\n"
        "Furthermore, he notes that programmers will generally aim to achieve any explicit goals which may be set, probably at the expense of any other quality attributes.\n"
        "Sommerville has identified four generalised attributes which are not concerned with what a program does, but how well the program does it:\n"
        "Maintainability, Dependability, Efficiency, Usability\n"
    )


@pytest.fixture
def expected_unigram_model():
    return np.array(
        [
            ("a", log(3 / 100)),
            ("b", log(1 / 100)),
            ("c", log(3 / 100)),
            ("d", log(1 / 20)),
            ("e", log(7 / 50)),
            ("f", log(1 / 50)),
            ("g", log(1 / 100)),
            ("h", log(1 / 25)),
            ("i", log(3 / 50)),
            ("l", log(1 / 100)),
            ("m", log(1 / 100)),
            ("n", log(1 / 10)),
            ("o", log(1 / 10)),
            ("p", log(3 / 100)),
            ("r", log(1 / 20)),
            ("s", log(1 / 10)),
            ("t", log(13 / 100)),
            ("u", log(3 / 100)),
            ("w", log(1 / 50)),
            ("y", log(3 / 100)),
        ],
        dtype=[("ngram", "U1"), ("frequency", "f2")],
    )


@pytest.fixture
def expected_bigram_model():
    return np.array(
        [
            ("al", log(1 / 3)),
            ("ar", log(1 / 3)),
            ("ay", log(1 / 3)),
            ("by", log(1 / 1)),
            ("ce", log(1 / 3)),
            ("co", log(1 / 3)),
            ("ct", log(1 / 3)),
            ("de", log(1 / 5)),
            ("do", log(1 / 5)),
            ("ds", log(1 / 5)),
            ("du", log(1 / 5)),
            ("ed", log(1 / 14)),
            ("em", log(1 / 14)),
            ("en", log(3 / 14)),
            ("es", log(2 / 7)),
            ("ey", log(1 / 14)),
            ("fo", log(1 / 2)),
            ("he", log(1 / 1)),
            ("in", log(2 / 3)),
            ("io", log(1 / 6)),
            ("is", log(1 / 6)),
            ("nc", log(1 / 10)),
            ("nd", log(1 / 10)),
            ("ng", log(1 / 10)),
            ("no", log(1 / 10)),
            ("ns", log(1 / 10)),
            ("nt", log(1 / 5)),
            ("od", log(1 / 10)),
            ("of", log(1 / 10)),
            ("on", log(1 / 5)),
            ("or", log(1 / 5)),
            ("os", log(1 / 10)),
            ("ot", log(1 / 5)),
            ("po", log(1 / 3)),
            ("pr", log(1 / 3)),
            ("pu", log(1 / 3)),
            ("rd", log(1 / 5)),
            ("re", log(1 / 5)),
            ("ro", log(1 / 5)),
            ("rp", log(1 / 5)),
            ("se", log(2 / 5)),
            ("si", log(1 / 10)),
            ("st", log(1 / 5)),
            ("ta", log(1 / 13)),
            ("te", log(3 / 13)),
            ("th", log(4 / 13)),
            ("ti", log(2 / 13)),
            ("to", log(1 / 13)),
            ("uc", log(1 / 3)),
            ("ur", log(1 / 3)),
            ("us", log(1 / 3)),
            ("wa", log(1 / 2)),
            ("wo", log(1 / 2)),
        ],
        dtype=[("ngram", "U2"), ("frequency", "f2")],
    )


@pytest.fixture
def expected_trigram_model():
    return np.array(
        [
            ("are", log(1 / 1)),
            ("ces", log(1 / 1)),
            ("con", log(1 / 1)),
            ("cti", log(1 / 1)),
            ("ded", log(1 / 1)),
            ("duc", log(1 / 1)),
            ("enc", log(1 / 3)),
            ("end", log(1 / 3)),
            ("ent", log(1 / 3)),
            ("ese", log(1 / 4)),
            ("est", log(1 / 4)),
            ("for", log(1 / 1)),
            ("hem", log(1 / 4)),
            ("hes", log(1 / 4)),
            ("hey", log(1 / 4)),
            ("ing", log(1 / 4)),
            ("int", log(1 / 4)),
            ("ion", log(1 / 1)),
            ("ist", log(1 / 1)),
            ("nce", log(1 / 1)),
            ("nde", log(1 / 1)),
            ("not", log(1 / 1)),
            ("nsi", log(1 / 1)),
            ("nte", log(1 / 1)),
            ("odu", log(1 / 1)),
            ("ons", log(1 / 2)),
            ("ord", log(1 / 2)),
            ("ose", log(1 / 1)),
            ("ota", log(1 / 2)),
            ("pos", log(1 / 1)),
            ("pro", log(1 / 1)),
            ("pur", log(1 / 1)),
            ("rds", log(1 / 1)),
            ("rod", log(1 / 1)),
            ("rpo", log(1 / 1)),
            ("sen", log(1 / 4)),
            ("ses", log(1 / 4)),
            ("sis", log(1 / 1)),
            ("sti", log(1 / 2)),
            ("tal", log(1 / 1)),
            ("ten", log(2 / 3)),
            ("tes", log(1 / 3)),
            ("the", log(1 / 1)),
            ("tin", log(1 / 2)),
            ("tio", log(1 / 2)),
            ("tot", log(1 / 1)),
            ("uct", log(1 / 1)),
            ("urp", log(1 / 1)),
            ("use", log(1 / 1)),
            ("way", log(1 / 1)),
            ("wor", log(1 / 1)),
        ],
        dtype=[("ngram", "U3"), ("frequency", "f2")],
    )


@pytest.fixture
def expected_quadrigram_model():
    return np.array(
        [
            ("cons", log(1 / 1)),
            ("ctio", log(1 / 1)),
            ("duct", log(1 / 1)),
            ("ence", log(1 / 1)),
            ("ende", log(1 / 1)),
            ("ente", log(1 / 1)),
            ("esti", log(1 / 1)),
            ("hese", log(1 / 1)),
            ("inte", log(1 / 1)),
            ("nces", log(1 / 1)),
            ("nded", log(1 / 1)),
            ("nsis", log(1 / 1)),
            ("nten", log(1 / 1)),
            ("oduc", log(1 / 1)),
            ("onsi", log(1 / 1)),
            ("ords", log(1 / 1)),
            ("oses", log(1 / 1)),
            ("otal", log(1 / 1)),
            ("pose", log(1 / 1)),
            ("prod", log(1 / 1)),
            ("purp", log(1 / 1)),
            ("rodu", log(1 / 1)),
            ("rpos", log(1 / 1)),
            ("sent", log(1 / 1)),
            ("sist", log(1 / 1)),
            ("stin", log(1 / 1)),
            ("tenc", log(1 / 2)),
            ("tend", log(1 / 2)),
            ("test", log(1 / 1)),
            ("them", log(1 / 4)),
            ("thes", log(1 / 4)),
            ("they", log(1 / 4)),
            ("ting", log(1 / 1)),
            ("tion", log(1 / 1)),
            ("tota", log(1 / 1)),
            ("ucti", log(1 / 1)),
            ("urpo", log(1 / 1)),
            ("word", log(1 / 1)),
        ],
        dtype=[("ngram", "U4"), ("frequency", "f2")],
    )


@pytest.fixture
def expected_fivegram_model():
    return np.array(
        [
            ("consi", log(1 / 1)),
            ("ction", log(1 / 1)),
            ("ducti", log(1 / 1)),
            ("ences", log(1 / 1)),
            ("ended", log(1 / 1)),
            ("enten", log(1 / 1)),
            ("estin", log(1 / 1)),
            ("inten", log(1 / 1)),
            ("nsist", log(1 / 1)),
            ("ntenc", log(1 / 2)),
            ("ntend", log(1 / 2)),
            ("oduct", log(1 / 1)),
            ("onsis", log(1 / 1)),
            ("poses", log(1 / 1)),
            ("produ", log(1 / 1)),
            ("purpo", log(1 / 1)),
            ("roduc", log(1 / 1)),
            ("rpose", log(1 / 1)),
            ("sente", log(1 / 1)),
            ("sting", log(1 / 1)),
            ("tence", log(1 / 1)),
            ("tende", log(1 / 1)),
            ("testi", log(1 / 1)),
            ("these", log(1 / 1)),
            ("total", log(1 / 1)),
            ("uctio", log(1 / 1)),
            ("urpos", log(1 / 1)),
            ("words", log(1 / 1)),
        ],
        dtype=[("ngram", "U5"), ("frequency", "f2")],
    )


@pytest.fixture
def expected_sentences_file_content():
    return (
        "There are many attributes associated with good software.\n"
        "Some of these can be mutually contradictory, and different customers and participants may have different priorities.\n"
        "Weinberg provides an example of how different goals can have a dramatic effect on both effort required and efficiency.\n"
        "Furthermore, he notes that programmers will generally aim to achieve any explicit goals which may be set, probably at the expense of any other quality attributes.\n"
    )


@pytest.fixture
def expected_single_words_file_content():
    return "there\n" "attributes\n" "associated\n" "software\n"


@pytest.fixture
def expected_word_pairs_file_content():
    return (
        "there attributes\n"
        "associated software\n"
        "these mutually\n"
        "contradictory different\n"
    )


def test_language_model_files_writer(
    language_model_files_text,
    expected_unigram_model,
    expected_bigram_model,
    expected_trigram_model,
    expected_quadrigram_model,
    expected_fivegram_model,
):
    input_file = create_temp_input_file(language_model_files_text)
    input_file_path = Path(input_file.name)

    output_directory = TemporaryDirectory()
    output_directory_path = Path(output_directory.name)

    LanguageModelFilesWriter.create_and_write_language_model_files(
        input_file_path=input_file_path,
        output_directory_path=output_directory_path,
        language=Language.ENGLISH,
        char_class="\\p{L}",
    )

    files = read_directory_content(output_directory_path)

    assert len(files) == 5
    assert files[4] == "unigrams.npz"
    assert files[0] == "bigrams.npz"
    assert files[3] == "trigrams.npz"
    assert files[2] == "quadrigrams.npz"
    assert files[1] == "fivegrams.npz"

    unigrams_file_path = output_directory_path / files[4]
    bigrams_file_path = output_directory_path / files[0]
    trigrams_file_path = output_directory_path / files[3]
    quadrigrams_file_path = output_directory_path / files[2]
    fivegrams_file_path = output_directory_path / files[1]

    check_npz_file_content(unigrams_file_path, expected_unigram_model)
    check_npz_file_content(bigrams_file_path, expected_bigram_model)
    check_npz_file_content(trigrams_file_path, expected_trigram_model)
    check_npz_file_content(quadrigrams_file_path, expected_quadrigram_model)
    check_npz_file_content(fivegrams_file_path, expected_fivegram_model)


def test_test_data_files_writer(
    test_data_files_text,
    expected_sentences_file_content,
    expected_single_words_file_content,
    expected_word_pairs_file_content,
):
    input_file = create_temp_input_file(test_data_files_text)
    input_file_path = Path(input_file.name)

    output_directory = TemporaryDirectory()
    output_directory_path = Path(output_directory.name)

    TestDataFilesWriter.create_and_write_test_data_files(
        input_file_path=input_file_path,
        output_directory_path=output_directory_path,
        char_class="\\p{L}",
        maximum_lines=4,
    )

    files = read_directory_content(output_directory_path)
    assert len(files) == 3

    sentences_file_path = output_directory_path / files[0]
    single_words_file_path = output_directory_path / files[1]
    word_pairs_file_path = output_directory_path / files[2]

    check_file_content(
        sentences_file_path, "sentences.txt", expected_sentences_file_content
    )
    check_file_content(
        single_words_file_path, "single-words.txt", expected_single_words_file_content
    )
    check_file_content(
        word_pairs_file_path, "word-pairs.txt", expected_word_pairs_file_content
    )


def test_relative_input_file_path_raises_exception():
    relative_input_file_path = Path("some/relative/path/file.txt")
    expected_error_message = (
        f"input file path '{relative_input_file_path}' is not absolute"
    )

    with pytest.raises(Exception) as exception_info1:
        LanguageModelFilesWriter.create_and_write_language_model_files(
            input_file_path=relative_input_file_path,
            output_directory_path=Path("/some/output/directory"),
            language=Language.ENGLISH,
            char_class="\\p{L}",
        )
    assert exception_info1.value.args[0] == expected_error_message

    with pytest.raises(Exception) as exception_info2:
        TestDataFilesWriter.create_and_write_test_data_files(
            input_file_path=relative_input_file_path,
            output_directory_path=Path("/some/output/directory"),
            char_class="\\p{L}",
            maximum_lines=4,
        )
    assert exception_info2.value.args[0] == expected_error_message


def test_non_existing_input_file_raises_exception():
    non_existing_input_file_path = Path("/some/non-existing/path/file.txt")
    expected_error_message = (
        f"Input file '{non_existing_input_file_path}' does not exist"
    )

    with pytest.raises(Exception) as exception_info1:
        LanguageModelFilesWriter.create_and_write_language_model_files(
            input_file_path=non_existing_input_file_path,
            output_directory_path=Path("/some/output/directory"),
            language=Language.ENGLISH,
            char_class="\\p{L}",
        )
    assert exception_info1.value.args[0] == expected_error_message

    with pytest.raises(Exception) as exception_info2:
        TestDataFilesWriter.create_and_write_test_data_files(
            input_file_path=non_existing_input_file_path,
            output_directory_path=Path("/some/output/directory"),
            char_class="\\p{L}",
            maximum_lines=4,
        )
    assert exception_info2.value.args[0] == expected_error_message


def test_directory_as_input_file_raises_exception():
    input_file = TemporaryDirectory()
    input_file_path = Path(input_file.name)
    expected_error_message = (
        f"Input file path '{input_file_path}' does not represent a regular file"
    )

    with pytest.raises(Exception) as exception_info1:
        LanguageModelFilesWriter.create_and_write_language_model_files(
            input_file_path=input_file_path,
            output_directory_path=Path("/some/output/directory"),
            language=Language.ENGLISH,
            char_class="\\p{L}",
        )
    assert exception_info1.value.args[0] == expected_error_message

    with pytest.raises(Exception) as exception_info2:
        TestDataFilesWriter.create_and_write_test_data_files(
            input_file_path=input_file_path,
            output_directory_path=Path("/some/output/directory"),
            char_class="\\p{L}",
            maximum_lines=4,
        )
    assert exception_info2.value.args[0] == expected_error_message


def test_relative_output_directory_path_raises_exception():
    input_file = create_temp_input_file("some content")
    input_file_path = Path(input_file.name)

    relative_output_directory_path = Path("some/relative/path")
    expected_error_message = (
        f"Output directory path '{relative_output_directory_path}' is not absolute"
    )

    with pytest.raises(Exception) as exception_info1:
        LanguageModelFilesWriter.create_and_write_language_model_files(
            input_file_path=input_file_path,
            output_directory_path=relative_output_directory_path,
            language=Language.ENGLISH,
            char_class="\\p{L}",
        )
    assert exception_info1.value.args[0] == expected_error_message

    with pytest.raises(Exception) as exception_info2:
        TestDataFilesWriter.create_and_write_test_data_files(
            input_file_path=input_file_path,
            output_directory_path=relative_output_directory_path,
            char_class="\\p{L}",
            maximum_lines=4,
        )
    assert exception_info2.value.args[0] == expected_error_message


def test_non_existing_output_directory_path_raises_exception():
    input_file = create_temp_input_file("some content")
    input_file_path = Path(input_file.name)

    non_existing_output_directory_path = Path("/some/non-existing/directory")
    expected_error_message = (
        f"Output directory path '{non_existing_output_directory_path}' does not exist"
    )

    with pytest.raises(Exception) as exception_info1:
        LanguageModelFilesWriter.create_and_write_language_model_files(
            input_file_path=input_file_path,
            output_directory_path=non_existing_output_directory_path,
            language=Language.ENGLISH,
            char_class="\\p{L}",
        )
    assert exception_info1.value.args[0] == expected_error_message

    with pytest.raises(Exception) as exception_info2:
        TestDataFilesWriter.create_and_write_test_data_files(
            input_file_path=input_file_path,
            output_directory_path=non_existing_output_directory_path,
            char_class="\\p{L}",
            maximum_lines=4,
        )
    assert exception_info2.value.args[0] == expected_error_message


def test_file_as_output_directory_raises_exception():
    input_file = create_temp_input_file("some content")
    input_file_path = Path(input_file.name)
    expected_error_message = (
        f"Output directory path '{input_file_path}' does not represent a directory"
    )

    with pytest.raises(Exception) as exception_info1:
        LanguageModelFilesWriter.create_and_write_language_model_files(
            input_file_path=input_file_path,
            output_directory_path=input_file_path,
            language=Language.ENGLISH,
            char_class="\\p{L}",
        )
    assert exception_info1.value.args[0] == expected_error_message

    with pytest.raises(Exception) as exception_info2:
        TestDataFilesWriter.create_and_write_test_data_files(
            input_file_path=input_file_path,
            output_directory_path=input_file_path,
            char_class="\\p{L}",
            maximum_lines=4,
        )
    assert exception_info2.value.args[0] == expected_error_message


def check_npz_file_content(file_path: Path, expected_numpy_array: np.ndarray):
    with np.load(file_path) as data:
        assert "arr" in data
        assert np.array_equal(data["arr"], expected_numpy_array)


def check_file_content(
    file_path: Path, expected_file_name: str, expected_file_content: str
):
    assert file_path.is_file()
    assert file_path.name == expected_file_name

    with file_path.open() as txt_file:
        assert txt_file.read() == expected_file_content


def create_temp_input_file(content: str):
    input_file = NamedTemporaryFile()
    input_file.write(bytes(content, "utf-8"))
    input_file.seek(0)
    return input_file


def read_directory_content(directory):
    files = os.listdir(directory)
    files.sort()
    return files
