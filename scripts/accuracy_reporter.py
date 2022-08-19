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

import csv
import fasttext
import gcld3
import langdetect
import langid
import os
import pycld2
import time
import urllib.request

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Counter as TypedCounter, Dict, List, Optional, Tuple

from lingua import IsoCode639_1, Language, LanguageDetectorBuilder


@dataclass
class DetectorStatistics:
    _single_word_statistic: "Statistic"
    _word_pair_statistic: "Statistic"
    _sentence_statistic: "Statistic"
    _average_accuracies: Dict[Language, float]

    @classmethod
    def new(cls) -> "DetectorStatistics":
        return DetectorStatistics(
            _single_word_statistic=Statistic.new(),
            _word_pair_statistic=Statistic.new(),
            _sentence_statistic=Statistic.new(),
            _average_accuracies={},
        )

    def add_single_word_counts(self, language: Optional[Language], single_word: str):
        self._single_word_statistic.add_language_count(language)
        self._single_word_statistic.add_entity_count()
        self._single_word_statistic.add_entity_length_count(single_word)

    def add_word_pair_counts(self, language: Optional[Language], word_pair: str):
        self._word_pair_statistic.add_language_count(language)
        self._word_pair_statistic.add_entity_count()
        self._word_pair_statistic.add_entity_length_count(word_pair)

    def add_sentence_counts(self, language: Optional[Language], sentence: str):
        self._sentence_statistic.add_language_count(language)
        self._sentence_statistic.add_entity_count()
        self._sentence_statistic.add_entity_length_count(sentence)

    def compute_accuracy_values(self):
        self._single_word_statistic.map_counts_to_accuracy_values()
        self._word_pair_statistic.map_counts_to_accuracy_values()
        self._sentence_statistic.map_counts_to_accuracy_values()

    def create_report_data(self, language: Language) -> Optional[str]:
        (
            single_word_accuracy,
            single_word_report,
        ) = self._single_word_statistic.create_report_data(language, "single words")
        (
            word_pair_accuracy,
            word_pair_report,
        ) = self._word_pair_statistic.create_report_data(language, "word pairs")
        (
            sentence_accuracy,
            sentence_report,
        ) = self._sentence_statistic.create_report_data(language, "sentences")
        average_accuracy = (
            single_word_accuracy + word_pair_accuracy + sentence_accuracy
        ) / 3

        self._average_accuracies[language] = average_accuracy

        if average_accuracy == 0:
            return None

        return (
            f"##### {language.name.title()} #####\n\n"
            f">>> Accuracy on average: {format_accuracy(average_accuracy)}%\n\n"
            f"{single_word_report}"
            f"{word_pair_report}"
            f"{sentence_report}"
        )

    def create_aggregated_report_row(self, language: Language) -> str:
        if language in self._average_accuracies:
            accuracy = self._average_accuracies[language]
            if accuracy > 0:
                average_accuracy_column = format_accuracy(accuracy, digits=0)
            else:
                average_accuracy_column = "NaN"
        else:
            average_accuracy_column = "NaN"

        if language in self._single_word_statistic._language_accuracies:
            single_words_accuracy_column = format_accuracy(
                self._single_word_statistic._language_accuracies[language], digits=0
            )
        else:
            single_words_accuracy_column = "NaN"

        if language in self._word_pair_statistic._language_accuracies:
            word_pairs_accuracy_column = format_accuracy(
                self._word_pair_statistic._language_accuracies[language], digits=0
            )
        else:
            word_pairs_accuracy_column = "NaN"

        if language in self._sentence_statistic._language_accuracies:
            sentences_accuracy_column = format_accuracy(
                self._sentence_statistic._language_accuracies[language], digits=0
            )
        else:
            sentences_accuracy_column = "NaN"

        return (
            f"{average_accuracy_column},"
            f"{single_words_accuracy_column},"
            f"{word_pairs_accuracy_column},"
            f"{sentences_accuracy_column}"
        )


@dataclass
class Statistic:
    _language_counts: TypedCounter[Optional[Language]]
    _language_accuracies: Dict[Optional[Language], float]
    _entity_count: int
    _entity_length_count: int

    @classmethod
    def new(cls) -> "Statistic":
        return Statistic(
            _language_counts=Counter(),
            _language_accuracies={},
            _entity_count=0,
            _entity_length_count=0,
        )

    def add_language_count(self, language: Optional[Language]):
        self._language_counts[language] += 1

    def add_entity_count(self):
        self._entity_count += 1

    def add_entity_length_count(self, entity: str):
        self._entity_length_count += len(entity)

    def map_counts_to_accuracy_values(self):
        sum_of_counts = sum(self._language_counts.values())
        for language, count in self._language_counts.items():
            self._language_accuracies[language] = count / sum_of_counts

    def create_report_data(
        self, language: Language, description: str
    ) -> Tuple[float, str]:
        if language in self._language_accuracies:
            accuracy = self._language_accuracies[language]
        else:
            accuracy = 0.0

        average_length = round(self._entity_length_count / self._entity_count)
        report = (
            f">> Detection of {self._entity_count} {description} (average length: {average_length} chars)\n"
            f"Accuracy: {format_accuracy(accuracy)}%\n"
            f"Erroneously classified as {self.format_language_accuracies(language)}\n\n"
        )
        return accuracy, report

    def format_language_accuracies(self, language: Language) -> str:
        sorted_accuracies = []
        for lang, accuracy in self._language_accuracies.items():
            if lang != language:
                sorted_accuracies.append((lang, accuracy))

        sorted_accuracies.sort(key=lambda elem: (-elem[1], elem[0]))

        substrs = [
            f"{language.name.title()}: {format_accuracy(accuracy)}%"
            if language is not None
            else f"Unknown: {format_accuracy(accuracy)}%"
            for language, accuracy in sorted_accuracies
        ]
        return ", ".join(substrs)


def main():
    start = time.perf_counter()
    lingua_detector_with_high_accuracy = (
        LanguageDetectorBuilder.from_all_languages()
        .with_preloaded_language_models()
        .build()
    )

    lingua_detector_with_low_accuracy = (
        LanguageDetectorBuilder.from_all_languages()
        .with_low_accuracy_mode()
        .with_preloaded_language_models()
        .build()
    )

    fasttext_model_url = (
        "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
    )
    fasttext_model_file = str(Path(__file__).parent / "fasttext_model.bin")
    if not os.path.isfile(fasttext_model_file):
        fasttext_model_file = urllib.request.urlretrieve(
            fasttext_model_url, fasttext_model_file
        )[0]
    fasttext_detector = fasttext.load_model(fasttext_model_file)

    cld3_detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=512)

    test_data_directory = Path(__file__).parent / "../language-testdata"
    accuracy_reports_directory = Path(__file__).parent / "../accuracy-reports"
    lingua_high_accuracy_reports_directory = (
        accuracy_reports_directory / "lingua-high-accuracy"
    )
    lingua_low_accuracy_reports_directory = (
        accuracy_reports_directory / "lingua-low-accuracy"
    )
    langdetect_reports_directory = accuracy_reports_directory / "langdetect"
    fasttext_reports_directory = accuracy_reports_directory / "fasttext"
    langid_reports_directory = accuracy_reports_directory / "langid"
    cld3_reports_directory = accuracy_reports_directory / "cld3"
    cld2_reports_directory = accuracy_reports_directory / "cld2"

    if not lingua_high_accuracy_reports_directory.is_dir():
        os.makedirs(lingua_high_accuracy_reports_directory)

    if not lingua_low_accuracy_reports_directory.is_dir():
        os.makedirs(lingua_low_accuracy_reports_directory)

    if not langdetect_reports_directory.is_dir():
        os.makedirs(langdetect_reports_directory)

    if not fasttext_reports_directory.is_dir():
        os.makedirs(fasttext_reports_directory)

    if not langid_reports_directory.is_dir():
        os.makedirs(langid_reports_directory)

    if not cld3_reports_directory.is_dir():
        os.makedirs(cld3_reports_directory)

    if not cld2_reports_directory.is_dir():
        os.makedirs(cld2_reports_directory)

    aggregated_report_file = (
        accuracy_reports_directory / "aggregated-accuracy-values.csv"
    )

    with aggregated_report_file.open(mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            [
                "language",
                "average-cld2",
                "single-words-cld2",
                "word-pairs-cld2",
                "sentences-cld2",
                "average-cld3",
                "single-words-cld3",
                "word-pairs-cld3",
                "sentences-cld3",
                "average-langid",
                "single-words-langid",
                "word-pairs-langid",
                "sentences-langid",
                "average-fasttext",
                "single-words-fasttext",
                "word-pairs-fasttext",
                "sentences-fasttext",
                "average-langdetect",
                "single-words-langdetect",
                "word-pairs-langdetect",
                "sentences-langdetect",
                "average-lingua-low",
                "single-words-lingua-low",
                "word-pairs-lingua-low",
                "sentences-lingua-low",
                "average-lingua-high",
                "single-words-lingua-high",
                "word-pairs-lingua-high",
                "sentences-lingua-high",
            ]
        )

        total_language_count = len(Language)

        for idx, language in enumerate(Language):
            print(
                f"Writing reports for {language.name.title()}... ({idx+1}/{total_language_count})"
            )

            single_words = get_file_content(
                test_data_directory, "single-words", language
            )
            word_pairs = get_file_content(test_data_directory, "word-pairs", language)
            sentences = get_file_content(test_data_directory, "sentences", language)

            lingua_high_accuracy_statistics = DetectorStatistics.new()
            lingua_low_accuracy_statistics = DetectorStatistics.new()
            langdetect_statistics = DetectorStatistics.new()
            fasttext_statistics = DetectorStatistics.new()
            langid_statistics = DetectorStatistics.new()
            cld3_statistics = DetectorStatistics.new()
            cld2_statistics = DetectorStatistics.new()

            for single_word in single_words:
                lingua_language_in_high_accuracy_mode = (
                    lingua_detector_with_high_accuracy.detect_language_of(single_word)
                )
                lingua_high_accuracy_statistics.add_single_word_counts(
                    lingua_language_in_high_accuracy_mode, single_word
                )

                lingua_language_in_low_accuracy_mode = (
                    lingua_detector_with_low_accuracy.detect_language_of(single_word)
                )
                lingua_low_accuracy_statistics.add_single_word_counts(
                    lingua_language_in_low_accuracy_mode, single_word
                )

                try:
                    langdetect_language = map_detector_to_lingua(
                        langdetect.detect(single_word)
                    )
                except langdetect.lang_detect_exception.LangDetectException:
                    langdetect_language = None
                langdetect_statistics.add_single_word_counts(
                    langdetect_language, single_word
                )

                fasttext_language = map_detector_to_lingua(
                    fasttext_detector.predict(single_word)[0][0].split("__label__")[1]
                )
                fasttext_statistics.add_single_word_counts(
                    fasttext_language, single_word
                )

                langid_language = map_detector_to_lingua(
                    langid.classify(single_word)[0]
                )
                langid_statistics.add_single_word_counts(langid_language, single_word)

                cld3_language = map_detector_to_lingua(
                    cld3_detector.FindLanguage(single_word).language
                )
                cld3_statistics.add_single_word_counts(cld3_language, single_word)

                try:
                    cld2_language = map_detector_to_lingua(
                        pycld2.detect(single_word)[2][0][1]
                    )
                except pycld2.error:
                    cld2_language = None
                cld2_statistics.add_single_word_counts(cld2_language, single_word)

            for word_pair in word_pairs:
                lingua_language_in_high_accuracy_mode = (
                    lingua_detector_with_high_accuracy.detect_language_of(word_pair)
                )
                lingua_high_accuracy_statistics.add_word_pair_counts(
                    lingua_language_in_high_accuracy_mode, word_pair
                )

                lingua_language_in_low_accuracy_mode = (
                    lingua_detector_with_low_accuracy.detect_language_of(word_pair)
                )
                lingua_low_accuracy_statistics.add_word_pair_counts(
                    lingua_language_in_low_accuracy_mode, word_pair
                )

                try:
                    langdetect_language = map_detector_to_lingua(
                        langdetect.detect(word_pair)
                    )
                except langdetect.lang_detect_exception.LangDetectException:
                    langdetect_language = None
                langdetect_statistics.add_word_pair_counts(
                    langdetect_language, word_pair
                )

                fasttext_language = map_detector_to_lingua(
                    fasttext_detector.predict(word_pair)[0][0].split("__label__")[1]
                )
                fasttext_statistics.add_word_pair_counts(fasttext_language, word_pair)

                langid_language = map_detector_to_lingua(langid.classify(word_pair)[0])
                langid_statistics.add_word_pair_counts(langid_language, word_pair)

                cld3_language = map_detector_to_lingua(
                    cld3_detector.FindLanguage(word_pair).language
                )
                cld3_statistics.add_word_pair_counts(cld3_language, word_pair)

                try:
                    cld2_language = map_detector_to_lingua(
                        pycld2.detect(word_pair)[2][0][1]
                    )
                except pycld2.error:
                    cld2_language = None
                cld2_statistics.add_word_pair_counts(cld2_language, word_pair)

            for sentence in sentences:
                lingua_language_in_high_accuracy_mode = (
                    lingua_detector_with_high_accuracy.detect_language_of(sentence)
                )
                lingua_high_accuracy_statistics.add_sentence_counts(
                    lingua_language_in_high_accuracy_mode, sentence
                )

                lingua_language_in_low_accuracy_mode = (
                    lingua_detector_with_low_accuracy.detect_language_of(sentence)
                )
                lingua_low_accuracy_statistics.add_sentence_counts(
                    lingua_language_in_low_accuracy_mode, sentence
                )

                try:
                    langdetect_language = map_detector_to_lingua(
                        langdetect.detect(sentence)
                    )
                except langdetect.lang_detect_exception.LangDetectException:
                    langdetect_language = None
                langdetect_statistics.add_sentence_counts(langdetect_language, sentence)

                fasttext_language = map_detector_to_lingua(
                    fasttext_detector.predict(sentence)[0][0].split("__label__")[1]
                )
                fasttext_statistics.add_sentence_counts(fasttext_language, sentence)

                langid_language = map_detector_to_lingua(langid.classify(sentence)[0])
                langid_statistics.add_sentence_counts(langid_language, sentence)

                cld3_language = map_detector_to_lingua(
                    cld3_detector.FindLanguage(sentence).language
                )
                cld3_statistics.add_sentence_counts(cld3_language, sentence)

                try:
                    cld2_language = map_detector_to_lingua(
                        pycld2.detect(sentence)[2][0][1]
                    )
                except pycld2.error:
                    cld2_language = None
                cld2_statistics.add_sentence_counts(cld2_language, sentence)

            lingua_high_accuracy_statistics.compute_accuracy_values()
            lingua_low_accuracy_statistics.compute_accuracy_values()
            langdetect_statistics.compute_accuracy_values()
            fasttext_statistics.compute_accuracy_values()
            langid_statistics.compute_accuracy_values()
            cld3_statistics.compute_accuracy_values()
            cld2_statistics.compute_accuracy_values()

            lingua_high_accuracy_report = (
                lingua_high_accuracy_statistics.create_report_data(language)
            )
            lingua_low_accuracy_report = (
                lingua_low_accuracy_statistics.create_report_data(language)
            )
            langdetect_report = langdetect_statistics.create_report_data(language)
            fasttext_report = fasttext_statistics.create_report_data(language)
            langid_report = langid_statistics.create_report_data(language)
            cld3_report = cld3_statistics.create_report_data(language)
            cld2_report = cld2_statistics.create_report_data(language)

            lingua_high_accuracy_aggregated_report_row = (
                lingua_high_accuracy_statistics.create_aggregated_report_row(language)
            )
            lingua_low_accuracy_aggregated_report_row = (
                lingua_low_accuracy_statistics.create_aggregated_report_row(language)
            )
            langdetect_aggregated_report_row = (
                langdetect_statistics.create_aggregated_report_row(language)
            )
            fasttext_aggregated_report_row = (
                fasttext_statistics.create_aggregated_report_row(language)
            )
            langid_aggregated_report_row = (
                langid_statistics.create_aggregated_report_row(language)
            )
            cld3_aggregated_report_row = cld3_statistics.create_aggregated_report_row(
                language
            )
            cld2_aggregated_report_row = cld2_statistics.create_aggregated_report_row(
                language
            )
            total_aggregated_report_row = (
                f"{language.name.title()},"
                f"{cld2_aggregated_report_row},"
                f"{cld3_aggregated_report_row},"
                f"{langid_aggregated_report_row},"
                f"{fasttext_aggregated_report_row},"
                f"{langdetect_aggregated_report_row},"
                f"{lingua_low_accuracy_aggregated_report_row},"
                f"{lingua_high_accuracy_aggregated_report_row}"
            )
            csv_writer.writerow(total_aggregated_report_row.split(","))

            report_file_name = f"{language.name.title()}.txt"
            lingua_high_accuracy_reports_file_path = (
                lingua_high_accuracy_reports_directory / report_file_name
            )
            lingua_low_accuracy_reports_file_path = (
                lingua_low_accuracy_reports_directory / report_file_name
            )
            langdetect_reports_file_path = (
                langdetect_reports_directory / report_file_name
            )
            fasttext_reports_file_path = fasttext_reports_directory / report_file_name
            langid_reports_file_path = langid_reports_directory / report_file_name
            cld3_reports_file_path = cld3_reports_directory / report_file_name
            cld2_reports_file_path = cld2_reports_directory / report_file_name

            if lingua_high_accuracy_report is not None:
                with lingua_high_accuracy_reports_file_path.open(
                    mode="w"
                ) as lingua_high_accuracy_reports_file:
                    lingua_high_accuracy_reports_file.write(lingua_high_accuracy_report)

            if lingua_low_accuracy_report is not None:
                with lingua_low_accuracy_reports_file_path.open(
                    mode="w"
                ) as lingua_low_accuracy_reports_file:
                    lingua_low_accuracy_reports_file.write(lingua_low_accuracy_report)

            if langdetect_report is not None:
                with langdetect_reports_file_path.open(
                    mode="w"
                ) as langdetect_reports_file:
                    langdetect_reports_file.write(langdetect_report)

            if fasttext_report is not None:
                with fasttext_reports_file_path.open(mode="w") as fasttext_reports_file:
                    fasttext_reports_file.write(fasttext_report)

            if langid_report is not None:
                with langid_reports_file_path.open(mode="w") as langid_reports_file:
                    langid_reports_file.write(langid_report)

            if cld3_report is not None:
                with cld3_reports_file_path.open(mode="w") as cld3_reports_file:
                    cld3_reports_file.write(cld3_report)

            if cld2_report is not None:
                with cld2_reports_file_path.open(mode="w") as cld2_reports_file:
                    cld2_reports_file.write(cld2_report)

            print("Done\n")

    elapsed = time.perf_counter() - start
    print(f"All accuracy reports successfully written in {elapsed:.2f} seconds")


def get_file_content(
    test_data_directory: Path, subdirectory: str, language: Language
) -> List[str]:
    test_data_file_name = f"{language.iso_code_639_1.name.lower()}.txt"
    test_data_file_path = test_data_directory / subdirectory / test_data_file_name
    with test_data_file_path.open(mode="r") as test_data_file:
        lines = []
        for line in test_data_file:
            stripped_line = line.rstrip()
            if len(stripped_line) > 0:
                lines.append(stripped_line)
        return lines


def format_accuracy(accuracy: float, digits: int = 2) -> str:
    return f"{accuracy*100:.{digits}f}"


def map_detector_to_lingua(iso_code: str) -> Optional[Language]:
    if iso_code in ["zh-cn", "zh-tw"]:
        iso_code = "zh"
    try:
        lingua_iso_code = IsoCode639_1[iso_code.upper()]
        for language in Language:
            if language.iso_code_639_1 == lingua_iso_code:
                return language
        return None
    except KeyError:
        return None


if __name__ == "__main__":
    main()
