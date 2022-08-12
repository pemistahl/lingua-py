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

import os
import pytest
import regex

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from zipfile import ZipFile

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
    return """
    {
        "language":"ENGLISH",
        "ngrams":{
            "13/100":"t",
            "1/25":"h",
            "7/50":"e",
            "1/10":"n o s",
            "3/100":"a c p u y",
            "1/20":"d r",
            "3/50":"i",
            "1/50":"f w",
            "1/100":"b g l m"
        }
    }
    """


@pytest.fixture
def expected_bigram_model():
    return """
    {
        "language":"ENGLISH",
        "ngrams":{
            "4/13":"th",
            "1/1":"by he",
            "2/7":"es",
            "2/5":"se",
            "3/14":"en",
            "1/5":"de do ds du nt on or ot rd re ro rp st",
            "3/13":"te",
            "1/10":"nc nd ng no ns od of os si",
            "1/3":"al ar ay ce co ct po pr pu uc ur us",
            "2/3":"in",
            "1/14":"ed em ey",
            "1/2":"fo wa wo",
            "2/13":"ti",
            "1/6":"io is",
            "1/13":"ta to"
        }
    }
    """


@pytest.fixture
def expected_trigram_model():
    return """
    {
        "language":"ENGLISH",
        "ngrams":{
            "1/1":"are ces con cti ded duc for ion ist nce nde not nsi nte odu ose pos pro pur rds rod rpo sis tal the tot uct urp use way wor",
            "1/4":"ese est hem hes hey ing int sen ses",
            "1/3":"enc end ent tes",
            "2/3":"ten",
            "1/2":"ons ord ota sti tin tio"
        }
    }
    """


@pytest.fixture
def expected_quadrigram_model():
    return """
    {
        "language":"ENGLISH",
        "ngrams":{
            "1/4":"them thes they",
            "1/1":"cons ctio duct ence ende ente esti hese inte nces nded nsis nten oduc onsi ords oses otal pose prod purp rodu rpos sent sist stin test ting tion tota ucti urpo word",
            "1/2":"tenc tend"
        }
    }
    """


@pytest.fixture
def expected_fivegram_model():
    return """
    {
        "language":"ENGLISH",
        "ngrams":{
            "1/1":"consi ction ducti ences ended enten estin inten nsist oduct onsis poses produ purpo roduc rpose sente sting tence tende testi these total uctio urpos words",
            "1/2":"ntenc ntend"
        }
    }
    """


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
    assert files[4] == "unigrams.json.zip"
    assert files[0] == "bigrams.json.zip"
    assert files[3] == "trigrams.json.zip"
    assert files[2] == "quadrigrams.json.zip"
    assert files[1] == "fivegrams.json.zip"

    unigrams_file_path = output_directory_path / files[4]
    bigrams_file_path = output_directory_path / files[0]
    trigrams_file_path = output_directory_path / files[3]
    quadrigrams_file_path = output_directory_path / files[2]
    fivegrams_file_path = output_directory_path / files[1]

    check_zip_file_content(unigrams_file_path, "unigrams.json", expected_unigram_model)
    check_zip_file_content(bigrams_file_path, "bigrams.json", expected_bigram_model)
    check_zip_file_content(trigrams_file_path, "trigrams.json", expected_trigram_model)
    check_zip_file_content(
        quadrigrams_file_path, "quadrigrams.json", expected_quadrigram_model
    )
    check_zip_file_content(
        fivegrams_file_path, "fivegrams.json", expected_fivegram_model
    )


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


def check_zip_file_content(
    file_path: Path, expected_file_name: str, expected_file_content: str
):
    with ZipFile(file_path) as zip_file:
        name_list = zip_file.namelist()
        assert len(name_list) == 1
        assert name_list[0] == expected_file_name

        with zip_file.open(expected_file_name) as json_file:
            json_content = json_file.read().decode("utf-8")
            assert json_content == minify(expected_file_content)


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


def minify(json: str):
    return regex.sub(r"\n\s*", "", json)
