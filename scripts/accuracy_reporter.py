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

import csv
import fastspell
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
from typing import Callable, Counter as TypedCounter, Dict, List, Optional, Tuple

from simplemma.langdetect import lang_detector as simplemma_detector
from lingua import IsoCode639_1, Language, LanguageDetectorBuilder  # type: ignore


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
                if lang is None:
                    lng = "Unknown"
                else:
                    lng = lang.name.title()
                sorted_accuracies.append((lng, accuracy))

        sorted_accuracies.sort(key=lambda elem: (-elem[1], elem[0]))

        substrs = [
            f"{language}: {format_accuracy(accuracy)}%"
            for language, accuracy in sorted_accuracies
        ]
        return ", ".join(substrs)


def format_accuracy(accuracy: float, digits: int = 2) -> str:
    return f"{accuracy*100:.{digits}f}"


def map_detector_to_lingua(iso_code: str) -> Optional[Language]:
    if iso_code in ["zh-cn", "zh-tw"]:
        iso_code = "zh"
    try:
        for language in Language.all():
            if language.iso_code_639_1.name.lower() == iso_code:
                return language
        return None
    except KeyError:
        return None


def simplemma_detect(texts: List[str]) -> List[Optional[Language]]:
    iso_codes = tuple(
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

    return [
        map_detector_to_lingua(simplemma_detector(text, iso_codes)[0][0])
        for text in texts
    ]


def cld2_detect(texts: List[str]) -> List[Optional[Language]]:
    results = []
    for text in texts:
        try:
            results.append(map_detector_to_lingua(pycld2.detect(text)[2][0][1]))
        except pycld2.error:
            results.append(None)
    return results


cld3_detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=512)


def cld3_detect(texts: List[str]) -> List[Optional[Language]]:
    return [
        map_detector_to_lingua(cld3_detector.FindLanguage(text).language)
        for text in texts
    ]


def langid_detect(texts: List[str]) -> List[Optional[Language]]:
    return [map_detector_to_lingua(langid.classify(text)[0]) for text in texts]


fasttext_model_url = (
    "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
)
fasttext_model_file = str(Path(__file__).parent / "fasttext_model.bin")
if not os.path.isfile(fasttext_model_file):
    fasttext_model_file = urllib.request.urlretrieve(
        fasttext_model_url, fasttext_model_file
    )[0]
fasttext_detector = fasttext.load_model(fasttext_model_file)


def fasttext_detect(texts: List[str]) -> List[Optional[Language]]:
    return [
        map_detector_to_lingua(
            fasttext_detector.predict(text)[0][0].split("__label__")[1]
        )
        for text in texts
    ]


fastspell_obj = None


def fastspell_setup(language: Language) -> None:
    global fastspell_obj
    fastspell_obj = fastspell.FastSpell(language.iso_code_639_1.name.lower())


def fastspell_cons_detect(texts: List[str]) -> List[Optional[Language]]:
    assert fastspell_obj is not None
    fastspell_obj.mode = "cons"
    return [map_detector_to_lingua(fastspell_obj.getlang(text)) for text in texts]


def fastspell_aggr_detect(texts: List[str]) -> List[Optional[Language]]:
    assert fastspell_obj is not None
    fastspell_obj.mode = "aggr"
    return [map_detector_to_lingua(fastspell_obj.getlang(text)) for text in texts]


def langdetect_detect(texts: List[str]) -> List[Optional[Language]]:
    results = []
    for text in texts:
        try:
            results.append(map_detector_to_lingua(langdetect.detect(text)))
        except langdetect.lang_detect_exception.LangDetectException:
            results.append(None)
    return results


lingua_detector_with_low_accuracy = (
    LanguageDetectorBuilder.from_all_languages()
    .with_low_accuracy_mode()
    .with_preloaded_language_models()
    .build()
)


def lingua_low_accuracy_detect(texts: List[str]) -> List[Optional[Language]]:
    return lingua_detector_with_low_accuracy.detect_languages_in_parallel_of(texts)


lingua_detector_with_high_accuracy = (
    LanguageDetectorBuilder.from_all_languages()
    .with_preloaded_language_models()
    .build()
)


def lingua_high_accuracy_detect(texts: List[str]) -> List[Optional[Language]]:
    return lingua_detector_with_high_accuracy.detect_languages_in_parallel_of(texts)


def get_file_content(subdirectory: str) -> Dict[Language, List[str]]:
    file_content = {}
    test_data_directory = Path(__file__).parent / "../language-testdata"

    for language in Language.all():
        test_data_file_name = f"{language.iso_code_639_1.name.lower()}.txt"
        test_data_file_path = test_data_directory / subdirectory / test_data_file_name

        with test_data_file_path.open(mode="r") as test_data_file:
            file_content[language] = [
                line.rstrip() for line in test_data_file if len(line.rstrip()) > 0
            ]

    return file_content


single_words = get_file_content("single-words")
word_pairs = get_file_content("word-pairs")
sentences = get_file_content("sentences")


def collect_statistics(
    detector_name: str,
    reports_directory: Path,
    detector_fn: Callable[[List[str]], List[Optional[Language]]],
    setup_detector_fn: Optional[Callable[[Language], None]] = None,
) -> List[DetectorStatistics]:
    start = time.perf_counter()
    language_statistics = []

    if not reports_directory.is_dir():
        os.makedirs(reports_directory)

    total_language_count = len(Language.all())

    for idx, language in enumerate(sorted(Language.all())):
        print(
            f"Writing {detector_name} reports for {language.name.title()}... ({idx+1}/{total_language_count})"
        )

        if setup_detector_fn is not None:
            setup_detector_fn(language)

        statistics = DetectorStatistics.new()

        detected_languages = detector_fn(single_words[language])
        for single_word, detected_language in zip(
            single_words[language], detected_languages
        ):
            statistics.add_single_word_counts(detected_language, single_word)

        detected_languages = detector_fn(word_pairs[language])
        for word_pair, detected_language in zip(
            word_pairs[language], detected_languages
        ):
            statistics.add_word_pair_counts(detected_language, word_pair)

        detected_languages = detector_fn(sentences[language])
        for sentence, detected_language in zip(sentences[language], detected_languages):
            statistics.add_sentence_counts(detected_language, sentence)

        statistics.compute_accuracy_values()

        reports_file_path = reports_directory / f"{language.name.title()}.txt"
        report = statistics.create_report_data(language)

        if report is not None:
            with reports_file_path.open(mode="w") as reports_file:
                reports_file.write(report)

        language_statistics.append(statistics)

    stop = time.perf_counter()
    print(f"{detector_name} reports written in {stop - start:.2f} seconds\n")

    return language_statistics


def main():
    start = time.perf_counter()

    accuracy_reports_directory = Path(__file__).parent / "../accuracy-reports"

    simplemma_reports_directory = accuracy_reports_directory / "simplemma"
    simplemma_statistics = collect_statistics(
        "simplemma", simplemma_reports_directory, simplemma_detect
    )

    cld2_reports_directory = accuracy_reports_directory / "cld2"
    cld2_statistics = collect_statistics("CLD2", cld2_reports_directory, cld2_detect)

    cld3_reports_directory = accuracy_reports_directory / "cld3"
    cld3_statistics = collect_statistics("CLD3", cld3_reports_directory, cld3_detect)

    langid_reports_directory = accuracy_reports_directory / "langid"
    langid_statistics = collect_statistics(
        "langid", langid_reports_directory, langid_detect
    )

    fasttext_reports_directory = accuracy_reports_directory / "fasttext"
    fasttext_statistics = collect_statistics(
        "fasttext", fasttext_reports_directory, fasttext_detect
    )

    fastspell_cons_reports_directory = accuracy_reports_directory / "fastspell_cons"
    fastspell_cons_statistics = collect_statistics(
        "fastspell_cons",
        fastspell_cons_reports_directory,
        fastspell_cons_detect,
        fastspell_setup,
    )

    fastspell_aggr_reports_directory = accuracy_reports_directory / "fastspell_aggr"
    fastspell_aggr_statistics = collect_statistics(
        "fastspell_aggr",
        fastspell_aggr_reports_directory,
        fastspell_aggr_detect,
        fastspell_setup,
    )

    langdetect_reports_directory = accuracy_reports_directory / "langdetect"
    langdetect_statistics = collect_statistics(
        "langdetect", langdetect_reports_directory, langdetect_detect
    )

    lingua_low_accuracy_reports_directory = (
        accuracy_reports_directory / "lingua-low-accuracy"
    )
    lingua_low_accuracy_statistics = collect_statistics(
        "lingua-low-accuracy",
        lingua_low_accuracy_reports_directory,
        lingua_low_accuracy_detect,
    )

    lingua_high_accuracy_reports_directory = (
        accuracy_reports_directory / "lingua-high-accuracy"
    )
    lingua_high_accuracy_statistics = collect_statistics(
        "lingua-high-accuracy",
        lingua_high_accuracy_reports_directory,
        lingua_high_accuracy_detect,
    )

    aggregated_report_file_path = (
        accuracy_reports_directory / "aggregated-accuracy-values.csv"
    )

    with aggregated_report_file_path.open(
        mode="w", newline=""
    ) as aggregated_report_file:
        csv_writer = csv.writer(aggregated_report_file)
        csv_writer.writerow(
            [
                "language",
                "average-simplemma",
                "single-words-simplemma",
                "word-pairs-simplemma",
                "sentences-simplemma",
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
                "average-fastspell-cons",
                "single-words-fastspell-cons",
                "word-pairs-fastspell-cons",
                "sentences-fastspell-cons",
                "average-fastspell-aggr",
                "single-words-fastspell-aggr",
                "word-pairs-fastspell-aggr",
                "sentences-fastspell-aggr",
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

        for idx, language in enumerate(sorted(Language.all())):
            simplemma_aggregated_report_row = simplemma_statistics[
                idx
            ].create_aggregated_report_row(language)

            cld2_aggregated_report_row = cld2_statistics[
                idx
            ].create_aggregated_report_row(language)

            cld3_aggregated_report_row = cld3_statistics[
                idx
            ].create_aggregated_report_row(language)

            langid_aggregated_report_row = langid_statistics[
                idx
            ].create_aggregated_report_row(language)

            fasttext_aggregated_report_row = fasttext_statistics[
                idx
            ].create_aggregated_report_row(language)

            fastspell_cons_aggregated_report_row = fastspell_cons_statistics[
                idx
            ].create_aggregated_report_row(language)

            fastspell_aggr_aggregated_report_row = fastspell_aggr_statistics[
                idx
            ].create_aggregated_report_row(language)

            langdetect_aggregated_report_row = langdetect_statistics[
                idx
            ].create_aggregated_report_row(language)

            lingua_low_accuracy_aggregated_report_row = lingua_low_accuracy_statistics[
                idx
            ].create_aggregated_report_row(language)

            lingua_high_accuracy_aggregated_report_row = (
                lingua_high_accuracy_statistics[idx].create_aggregated_report_row(
                    language
                )
            )

            total_aggregated_report_row = (
                f"{language.name.title()},"
                f"{simplemma_aggregated_report_row},"
                f"{cld2_aggregated_report_row},"
                f"{cld3_aggregated_report_row},"
                f"{langid_aggregated_report_row},"
                f"{fasttext_aggregated_report_row},"
                f"{fastspell_cons_aggregated_report_row},"
                f"{fastspell_aggr_aggregated_report_row},"
                f"{langdetect_aggregated_report_row},"
                f"{lingua_low_accuracy_aggregated_report_row},"
                f"{lingua_high_accuracy_aggregated_report_row}"
            )
            csv_writer.writerow(total_aggregated_report_row.split(","))

    elapsed = time.perf_counter() - start
    print(f"All accuracy reports successfully written in {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
