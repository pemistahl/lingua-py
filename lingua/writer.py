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

from pathlib import Path
from typing import Dict, List, Optional

import regex

from ._constant import MULTIPLE_WHITESPACE, NUMBERS, PUNCTUATION
from .language import Language
from ._model import _TrainingDataLanguageModel


class LanguageModelFilesWriter:
    """This class creates language model files and writes them to a directory."""

    @classmethod
    def create_and_write_language_model_files(
        cls,
        input_file_path: Path,
        output_directory_path: Path,
        language: Language,
        char_class: str,
    ):
        """Create language model files for accuracy report generation and
        write them to a directory.

        Args:
            input_file_path: The path to a txt file used for language
                model creation. The assumed encoding of the txt file is UTF-8.
            output_directory_path: The path to an existing directory where the
                language model files are to be written.
            language: The language for which to create language models.
            char_class: A regex character class such as \\p{L} to restrict the
                set of characters that the language models are built from.

        Raises:
            Exception: if the input file path is not absolute or does not point
                to an existing txt file; if the input file's encoding is not
                UTF-8; if the output directory path is not absolute or does not
                point to an existing directory; if the character class cannot
                be compiled to a valid regular expression
        """
        check_input_file_path(input_file_path)
        check_output_directory_path(output_directory_path)

        unigram_model = cls._create_language_model(
            input_file_path=input_file_path,
            language=language,
            ngram_length=1,
            char_class=char_class,
            lower_ngram_absolute_frequencies={},
        )
        bigram_model = cls._create_language_model(
            input_file_path=input_file_path,
            language=language,
            ngram_length=2,
            char_class=char_class,
            lower_ngram_absolute_frequencies=unigram_model.absolute_frequencies,
        )
        trigram_model = cls._create_language_model(
            input_file_path=input_file_path,
            language=language,
            ngram_length=3,
            char_class=char_class,
            lower_ngram_absolute_frequencies=bigram_model.absolute_frequencies,
        )
        quadrigram_model = cls._create_language_model(
            input_file_path=input_file_path,
            language=language,
            ngram_length=4,
            char_class=char_class,
            lower_ngram_absolute_frequencies=trigram_model.absolute_frequencies,
        )
        fivegram_model = cls._create_language_model(
            input_file_path=input_file_path,
            language=language,
            ngram_length=5,
            char_class=char_class,
            lower_ngram_absolute_frequencies=quadrigram_model.absolute_frequencies,
        )

        cls._write_compressed_language_model(
            unigram_model, 1, output_directory_path, "unigrams.npz"
        )
        cls._write_compressed_language_model(
            bigram_model, 2, output_directory_path, "bigrams.npz"
        )
        cls._write_compressed_language_model(
            trigram_model, 3, output_directory_path, "trigrams.npz"
        )
        cls._write_compressed_language_model(
            quadrigram_model, 4, output_directory_path, "quadrigrams.npz"
        )
        cls._write_compressed_language_model(
            fivegram_model, 5, output_directory_path, "fivegrams.npz"
        )

    @classmethod
    def _create_language_model(
        cls,
        input_file_path: Path,
        language: Language,
        ngram_length: int,
        char_class: str,
        lower_ngram_absolute_frequencies: Optional[Dict[str, int]],
    ) -> _TrainingDataLanguageModel:
        with input_file_path.open() as input_file:
            input_file_lines = [
                line for line in input_file if not line.strip().isspace()
            ]
            return _TrainingDataLanguageModel.from_text(
                text=input_file_lines,
                language=language,
                ngram_length=ngram_length,
                char_class=char_class,
                lower_ngram_absolute_frequencies=lower_ngram_absolute_frequencies,
            )

    @classmethod
    def _write_compressed_language_model(
        cls,
        model: _TrainingDataLanguageModel,
        ngram_length: int,
        output_directory_path: Path,
        file_name: str,
    ):
        file_path = output_directory_path / file_name
        model.to_numpy_binary_file(file_path, ngram_length)


class TestDataFilesWriter:
    """This class creates test data files for accuracy report generation
    and writes them to a directory.
    """

    @classmethod
    def create_and_write_test_data_files(
        cls,
        input_file_path: Path,
        output_directory_path: Path,
        char_class: str,
        maximum_lines: int,
    ):
        """Create test data files for accuracy report generation and
        write them to a directory.

        Args:
            input_file_path: The path to a txt file used for test data
                creation. The assumed encoding of the txt file is UTF-8.
            output_directory_path: The path to an existing directory where
                the test data files are to be written.
            char_class: A regex character class such as \\p{L} to restrict
                the set of characters that the test data are built from.
            maximum_lines: The maximum number of lines each test data file
                should have.

        Raises:
            Exception: if the input file path is not absolute or does not point
                to an existing txt file; if the input file's encoding is not
                UTF-8; if the output directory path is not absolute or does not
                point to an existing directory; if the character class cannot
                be compiled to a valid regular expression
        """
        check_input_file_path(input_file_path)
        check_output_directory_path(output_directory_path)

        cls._create_and_write_sentences_file(
            input_file_path, output_directory_path, maximum_lines
        )

        single_words = cls._create_and_write_single_words_file(
            input_file_path, output_directory_path, char_class, maximum_lines
        )

        cls._create_and_write_word_pairs_file(
            single_words, output_directory_path, maximum_lines
        )

    @classmethod
    def _create_and_write_sentences_file(
        cls, input_file_path: Path, output_directory_path: Path, maximum_lines: int
    ):
        sentences_file_path = output_directory_path / "sentences.txt"
        if sentences_file_path.is_file():
            sentences_file_path.unlink()
        with input_file_path.open() as input_file:
            with sentences_file_path.open(mode="w") as sentences_file:
                line_counter = 0
                for line in input_file:
                    normalized_whitespace = MULTIPLE_WHITESPACE.sub(" ", line.strip())
                    removed_quotes = normalized_whitespace.replace('"', "")
                    if line_counter < maximum_lines:
                        sentences_file.write(removed_quotes)
                        sentences_file.write("\n")
                        line_counter += 1
                    else:
                        break

    @classmethod
    def _create_and_write_single_words_file(
        cls,
        input_file_path: Path,
        output_directory_path: Path,
        char_class: str,
        maximum_lines: int,
    ) -> List[str]:
        single_words_file_path = output_directory_path / "single-words.txt"
        word_regex = regex.compile(f"[{char_class}]{{5,}}")
        words = []
        if single_words_file_path.is_file():
            single_words_file_path.unlink()
        with input_file_path.open() as input_file:
            with single_words_file_path.open(mode="w") as single_words_file:
                line_counter = 0
                for line in input_file:
                    removed_punctuation = PUNCTUATION.sub("", line)
                    removed_numbers = NUMBERS.sub("", removed_punctuation)
                    normalized_whitespace = MULTIPLE_WHITESPACE.sub(
                        " ", removed_numbers
                    )
                    removed_quotes = normalized_whitespace.replace('"', "")
                    single_words = [
                        word.strip().lower()
                        for word in removed_quotes.split(" ")
                        if word_regex.fullmatch(word) is not None
                    ]
                    words.extend(single_words)

                for word in words:
                    if line_counter < maximum_lines:
                        single_words_file.write(word)
                        single_words_file.write("\n")
                        line_counter += 1
                    else:
                        break
        return words

    @classmethod
    def _create_and_write_word_pairs_file(
        cls, words: List[str], output_directory_path: Path, maximum_lines: int
    ):
        word_pairs_file_path = output_directory_path / "word-pairs.txt"
        word_pairs = []
        if word_pairs_file_path.is_file():
            word_pairs_file_path.unlink()
        for i in range(0, len(words) - 2 + 1, 2):
            sublst = words[i : i + 2]
            word_pairs.append(" ".join(sublst))
        with word_pairs_file_path.open(mode="w") as word_pairs_file:
            line_counter = 0
            for word_pair in word_pairs:
                if line_counter < maximum_lines:
                    word_pairs_file.write(word_pair)
                    word_pairs_file.write("\n")
                    line_counter += 1
                else:
                    break


def check_input_file_path(input_file_path: Path):
    if not input_file_path.is_absolute():
        raise Exception(f"input file path '{input_file_path}' is not absolute")

    if not input_file_path.exists():
        raise Exception(f"Input file '{input_file_path}' does not exist")

    if not input_file_path.is_file():
        raise Exception(
            f"Input file path '{input_file_path}' does not represent a regular file"
        )


def check_output_directory_path(output_directory_path: Path):
    if not output_directory_path.is_absolute():
        raise Exception(
            f"Output directory path '{output_directory_path}' is not absolute"
        )

    if not output_directory_path.exists():
        raise Exception(
            f"Output directory path '{output_directory_path}' does not exist"
        )

    if not output_directory_path.is_dir():
        raise Exception(
            f"Output directory path '{output_directory_path}' does not represent a directory"
        )
