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

import argparse
import fastspell
import fasttext
import gcld3
import langdetect
import langid
import numpy as np
import os
import pandas as pd
import pycld2
import time
import urllib.request

from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Counter as TypedCounter, Dict, List, Optional, Tuple

from simplemma.langdetect import lang_detector as simplemma_detector
from lingua import IsoCode639_1, Language, LanguageDetectorBuilder


class Category(Enum):
    AVERAGE = auto()
    SINGLE_WORDS = auto()
    WORD_PAIRS = auto()
    SENTENCES = auto()

    def folder_name(self) -> str:
        return self.name.lower().replace("_", "-")


@dataclass
class DetectorStatistics:
    _detector_name: str
    _is_single_language_detector: bool
    _language: Language
    _single_word_statistic: "Statistic"
    _word_pair_statistic: "Statistic"
    _sentence_statistic: "Statistic"
    _single_word_accuracy: float
    _word_pair_accuracy: float
    _sentence_accuracy: float
    _average_accuracy: float

    @classmethod
    def new(
        cls, detector_name: str, is_single_language_detector: bool, language: Language
    ) -> "DetectorStatistics":
        return DetectorStatistics(
            _detector_name=detector_name,
            _is_single_language_detector=is_single_language_detector,
            _language=language,
            _single_word_statistic=Statistic.new(),
            _word_pair_statistic=Statistic.new(),
            _sentence_statistic=Statistic.new(),
            _single_word_accuracy=0.0,
            _word_pair_accuracy=0.0,
            _sentence_accuracy=0.0,
            _average_accuracy=0.0,
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

    def create_report_data(self) -> Optional[str]:
        language = (
            None
            if self._is_single_language_detector
            and self._language.name.lower() not in self._detector_name
            else self._language
        )
        (
            self._single_word_accuracy,
            single_word_report,
        ) = self._single_word_statistic.create_report_data(language, "single words")
        (
            self._word_pair_accuracy,
            word_pair_report,
        ) = self._word_pair_statistic.create_report_data(language, "word pairs")
        (
            self._sentence_accuracy,
            sentence_report,
        ) = self._sentence_statistic.create_report_data(language, "sentences")

        self._average_accuracy = (
            self._single_word_accuracy
            + self._word_pair_accuracy
            + self._sentence_accuracy
        ) / 3

        if self._average_accuracy == 0:
            return None

        return (
            f"##### {self._language.name.title()} #####\n\n"
            f">>> Accuracy on average: {format_accuracy(self._average_accuracy)}%\n\n"
            f"{single_word_report}"
            f"{word_pair_report}"
            f"{sentence_report}"
        )

    def to_dataframe(self, category: Category) -> pd.DataFrame:
        accuracy = np.nan

        if category == Category.AVERAGE and self._average_accuracy > 0:
            accuracy = self._average_accuracy
        elif category == Category.SINGLE_WORDS and self._single_word_accuracy > 0:
            accuracy = self._single_word_accuracy
        elif category == Category.WORD_PAIRS and self._word_pair_accuracy > 0:
            accuracy = self._word_pair_accuracy
        elif category == Category.SENTENCES and self._sentence_accuracy > 0:
            accuracy = self._sentence_accuracy

        return pd.DataFrame(
            {
                self._detector_name: [accuracy * 100],
            },
            index=[self._language.name.title()],
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
        self, language: Optional[Language], description: str
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

    def format_language_accuracies(self, language: Optional[Language]) -> str:
        sorted_accuracies = []
        for lang, accuracy in self._language_accuracies.items():
            if lang != language:
                sorted_accuracies.append((lang, accuracy))

        sorted_accuracies.sort(key=lambda elem: (-elem[1], elem[0]))

        substrs = [
            (
                f"{language.name.title()}: {format_accuracy(accuracy)}%"
                if language is not None
                else f"Unknown: {format_accuracy(accuracy)}%"
            )
            for language, accuracy in sorted_accuracies
        ]
        return ", ".join(substrs)


class AbstractLanguageDetector:
    def __init__(
        self,
        detector_name: str,
        is_single_language_detector: bool,
        languages: List[Language],
    ):
        accuracy_reports_directory = Path(__file__).parent / "../accuracy-reports"
        self.detector_name = detector_name
        self.is_single_language_detector = is_single_language_detector
        self.languages = languages
        self.reports_directory = accuracy_reports_directory / detector_name
        self.single_words = self._get_file_content(Category.SINGLE_WORDS.folder_name())
        self.word_pairs = self._get_file_content(Category.WORD_PAIRS.folder_name())
        self.sentences = self._get_file_content(Category.SENTENCES.folder_name())

    def _setup(self, language: Language) -> None:
        pass

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return []

    def _get_file_content(self, subdirectory: str) -> Dict[Language, List[str]]:
        file_content = {}
        test_data_directory = Path(__file__).parent / "../language-testdata"

        for language in self.languages:
            test_data_file_name = f"{language.iso_code_639_1.name.lower()}.txt"
            test_data_file_path = (
                test_data_directory / subdirectory / test_data_file_name
            )

            with test_data_file_path.open(mode="r") as test_data_file:
                file_content[language] = [
                    line.rstrip() for line in test_data_file if len(line.rstrip()) > 0
                ]

        return file_content

    def collect_statistics(self) -> List[DetectorStatistics]:
        if not self.reports_directory.is_dir():
            os.makedirs(self.reports_directory)

        total_language_count = len(self.languages)
        all_statistics = []

        for idx, language in enumerate(self.languages):
            name = language.name.title()
            step = f"({idx+1}/{total_language_count})"

            print(f"Collecting {self.detector_name} statistics for {name}... {step}")

            self._setup(language)

            statistics = DetectorStatistics.new(
                self.detector_name, self.is_single_language_detector, language
            )

            detected_languages = self._detect(self.single_words[language])
            for single_word, detected_language in zip(
                self.single_words[language], detected_languages
            ):
                statistics.add_single_word_counts(detected_language, single_word)

            detected_languages = self._detect(self.word_pairs[language])
            for word_pair, detected_language in zip(
                self.word_pairs[language], detected_languages
            ):
                statistics.add_word_pair_counts(detected_language, word_pair)

            detected_languages = self._detect(self.sentences[language])
            for sentence, detected_language in zip(
                self.sentences[language], detected_languages
            ):
                statistics.add_sentence_counts(detected_language, sentence)

            statistics.compute_accuracy_values()

            all_statistics.append(statistics)

        return all_statistics

    def write_reports(self, statistics: List[DetectorStatistics]):
        for stat in statistics:
            report = stat.create_report_data()
            if report is not None:
                report_file_name = f"{stat._language.name.title()}.txt"
                report_file_path = self.reports_directory / report_file_name
                with report_file_path.open(mode="w") as report_file:
                    report_file.write(report)


class CLD2Detector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(CLD2Detector, self).__init__("cld2", False, languages)

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        results = []
        for text in texts:
            try:
                results.append(map_detector_to_lingua(pycld2.detect(text)[2][0][1]))
            except pycld2.error:
                results.append(None)
        return results


class CLD3Detector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(CLD3Detector, self).__init__("cld3", False, languages)
        self.detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=512)

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [
            map_detector_to_lingua(self.detector.FindLanguage(text).language)
            for text in texts
        ]


class FastspellDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language], mode: str):
        super(FastspellDetector, self).__init__(f"fastspell-{mode}", False, languages)
        self.mode = mode

    def _setup(self, language: Language) -> None:
        self.fastspell_obj = fastspell.FastSpell(
            language.iso_code_639_1.name.lower(), mode=self.mode
        )

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [
            map_detector_to_lingua(self.fastspell_obj.getlang(text)) for text in texts
        ]


class FasttextDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(FasttextDetector, self).__init__("fasttext", False, languages)
        fasttext_model_url = (
            "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
        )
        fasttext_model_file = str(Path(__file__).parent / "fasttext_model.bin")
        if not os.path.isfile(fasttext_model_file):
            fasttext_model_file = urllib.request.urlretrieve(
                fasttext_model_url, fasttext_model_file
            )[0]
        self.detector = fasttext.load_model(fasttext_model_file)

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [
            map_detector_to_lingua(
                self.detector.predict(text)[0][0].split("__label__")[1]
            )
            for text in texts
        ]


class LangdetectDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(LangdetectDetector, self).__init__("langdetect", False, languages)

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        results = []
        for text in texts:
            try:
                results.append(map_detector_to_lingua(langdetect.detect(text)))
            except langdetect.lang_detect_exception.LangDetectException:
                results.append(None)
        return results


class LangidDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(LangidDetector, self).__init__("langid", False, languages)

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [map_detector_to_lingua(langid.classify(text)[0]) for text in texts]


class LinguaLowAccuracyDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(LinguaLowAccuracyDetector, self).__init__(
            "lingua-low-accuracy", False, languages
        )
        self.detector = (
            LanguageDetectorBuilder.from_all_languages()
            .with_low_accuracy_mode()
            .with_preloaded_language_models()
            .build()
        )

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [self.detector.detect_language_of(text) for text in texts]


class LinguaHighAccuracyDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(LinguaHighAccuracyDetector, self).__init__(
            "lingua-high-accuracy", False, languages
        )
        self.detector = (
            LanguageDetectorBuilder.from_all_languages()
            .with_preloaded_language_models()
            .build()
        )

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [self.detector.detect_language_of(text) for text in texts]


class LinguaSingleLanguageDetector(AbstractLanguageDetector):
    def __init__(self, language: Language, languages: List[Language]):
        super(LinguaSingleLanguageDetector, self).__init__(
            f"lingua-{language.name.lower()}-detector", True, languages
        )
        self.detector = LanguageDetectorBuilder.from_languages(language).build()

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [self.detector.detect_language_of(text) for text in texts]


class SimplemmaDetector(AbstractLanguageDetector):
    def __init__(self, languages: List[Language]):
        super(SimplemmaDetector, self).__init__("simplemma", False, languages)
        self.iso_codes = tuple(
            language.iso_code_639_1.name.lower()
            for language in [
                Language.BULGARIAN,
                Language.CATALAN,
                Language.CZECH,
                Language.WELSH,
                Language.DANISH,
                Language.GERMAN,
                Language.GREEK,
                Language.ENGLISH,
                Language.SPANISH,
                Language.ESTONIAN,
                Language.PERSIAN,
                Language.FINNISH,
                Language.FRENCH,
                Language.IRISH,
                Language.HINDI,
                Language.HUNGARIAN,
                Language.ARMENIAN,
                Language.INDONESIAN,
                Language.ICELANDIC,
                Language.ITALIAN,
                Language.GEORGIAN,
                Language.LATIN,
                Language.LITHUANIAN,
                Language.LATVIAN,
                Language.MACEDONIAN,
                Language.MALAY,
                Language.BOKMAL,
                Language.NYNORSK,
                Language.DUTCH,
                Language.POLISH,
                Language.PORTUGUESE,
                Language.ROMANIAN,
                Language.RUSSIAN,
                Language.SLOVAK,
                Language.SLOVENE,
                Language.ALBANIAN,
                Language.SWEDISH,
                Language.SWAHILI,
                Language.TAGALOG,
                Language.TURKISH,
                Language.UKRAINIAN,
            ]
        )

    def _detect(self, texts: List[str]) -> List[Optional[Language]]:
        return [
            map_detector_to_lingua(simplemma_detector(text, self.iso_codes)[0][0])  # type: ignore
            for text in texts
        ]


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


def parse_command_line_args() -> Tuple[List[str], List[str]]:
    default_languages = [language.name.lower() for language in Language]
    default_detectors = [
        "cld2",
        "cld3",
        "fastspell-aggr",
        "fastspell-cons",
        "fasttext",
        "langdetect",
        "langid",
        "lingua-high-accuracy",
        "lingua-low-accuracy",
        "simplemma",
    ]
    default_detectors.extend(
        [f"lingua-{language}-detector" for language in default_languages]
    )
    detector_choices = default_detectors.copy()
    detector_choices.append("lingua-all-single-language-detectors")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--detectors", nargs="+", choices=detector_choices, default=default_detectors
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        choices=default_languages,
        default=default_languages,
    )
    args = parser.parse_args()
    return args.detectors, args.languages


def create_detector_instance(
    detector_name: str, languages: List[Language]
) -> Optional[AbstractLanguageDetector]:
    if detector_name == "cld2":
        return CLD2Detector(languages)
    if detector_name == "cld3":
        return CLD3Detector(languages)
    if detector_name == "fastspell-aggr":
        return FastspellDetector(languages, mode="aggr")
    if detector_name == "fastspell-cons":
        return FastspellDetector(languages, mode="cons")
    if detector_name == "fasttext":
        return FasttextDetector(languages)
    if detector_name == "langdetect":
        return LangdetectDetector(languages)
    if detector_name == "langid":
        return LangidDetector(languages)
    if detector_name == "lingua-high-accuracy":
        return LinguaHighAccuracyDetector(languages)
    if detector_name == "lingua-low-accuracy":
        return LinguaLowAccuracyDetector(languages)
    if detector_name.startswith("lingua-") and detector_name.endswith("-detector"):
        language_name = detector_name.split("-")[1]
        language = Language[language_name.upper()]
        return LinguaSingleLanguageDetector(language, languages)
    if detector_name == "simplemma":
        return SimplemmaDetector(languages)
    return None


def main():
    total_start = time.perf_counter()
    detector_names, language_names = parse_command_line_args()
    languages = sorted([Language[name.upper()] for name in language_names])
    all_statistics = {}
    all_single_language_detectors_name = "lingua-all-single-language-detectors"

    if all_single_language_detectors_name in detector_names:
        detector_names.remove(all_single_language_detectors_name)
        for language_name in language_names:
            detector_name = f"lingua-{language_name}-detector"
            if detector_name not in detector_names:
                detector_names.append(detector_name)

    for detector_name in detector_names:
        detector = create_detector_instance(detector_name, languages)
        if detector is not None:
            start = time.perf_counter()
            statistics = detector.collect_statistics()
            detector.write_reports(statistics)
            stop = time.perf_counter()
            print(f"{detector_name} statistics written in {stop - start:.2f} seconds\n")
            all_statistics[detector_name] = statistics

    print("Updating aggregated reports...")
    start = time.perf_counter()

    for category in Category:
        report_file_path = (
            Path(__file__).parent
            / f"../accuracy-reports/{category.folder_name()}-accuracy-values.csv"
        )

        try:
            dataframe = pd.read_csv(report_file_path, index_col="language")
        except FileNotFoundError:
            dataframe = pd.DataFrame()

        for detector_name in detector_names:
            statistics = all_statistics[detector_name]
            for stat in statistics:
                df = stat.to_dataframe(category)

                # Update values in existing columns
                if df.columns.isin(dataframe.columns).all():
                    row = stat._language.name.title()
                    for column in df.columns:
                        dataframe.at[row, column] = df.at[row, column]

                # Add new columns
                else:
                    dataframe = pd.concat([dataframe, df], axis=1)

        # Sort dataframe columns alphabetically
        dataframe = dataframe.reindex(sorted(dataframe.columns), axis=1)

        dataframe.to_csv(report_file_path, index_label="language", na_rep="NaN")

    total_stop = time.perf_counter()
    total_time = total_stop - total_start
    total_minutes = int(total_time / 60)
    total_seconds = total_time - total_minutes * 60
    print(f"Aggregated reports updated in {total_stop - start:.2f} seconds\n")
    print(
        f"All reports written in {total_minutes} minutes, {total_seconds:.2f} seconds"
    )


if __name__ == "__main__":
    main()
