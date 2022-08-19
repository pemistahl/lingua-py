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
import psutil
import sys

from lingua import LanguageDetectorBuilder, Language


def report_memory_usage_of_low_accuracy_mode():
    LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().with_preloaded_language_models().build()
    process = psutil.Process(os.getpid())
    process_size = process.memory_info().rss
    print(
        f"Entire Python process in low accuracy mode: {process_size / 1000000:.2f} MB"
    )


def report_memory_usage_of_high_accuracy_mode():
    unigrams_size = 0
    bigrams_size = 0
    trigrams_size = 0
    quadrigrams_size = 0
    fivegrams_size = 0

    detector = (
        LanguageDetectorBuilder.from_all_languages()
        .with_preloaded_language_models()
        .build()
    )

    for language in Language:
        if language in detector._unigram_language_models:
            unigrams_size += sys.getsizeof(detector._unigram_language_models[language])

        if language in detector._bigram_language_models:
            bigrams_size += sys.getsizeof(detector._bigram_language_models[language])

        if language in detector._trigram_language_models:
            trigrams_size += sys.getsizeof(detector._trigram_language_models[language])

        if language in detector._quadrigram_language_models:
            quadrigrams_size += sys.getsizeof(
                detector._quadrigram_language_models[language]
            )

        if language in detector._fivegram_language_models:
            fivegrams_size += sys.getsizeof(
                detector._fivegram_language_models[language]
            )

    process = psutil.Process(os.getpid())
    process_size = process.memory_info().rss

    print(
        f"Entire Python process in high accuracy mode: {process_size / 1000000:.2f} MB"
    )
    print(f"Unigrams: {unigrams_size / 1000000:.2f} MB")
    print(f"Bigrams: {bigrams_size / 1000000:.2f} MB")
    print(f"Trigrams: {trigrams_size / 1000000:.2f} MB")
    print(f"Quadrigrams: {quadrigrams_size / 1000000:.2f} MB")
    print(f"Fivegrams: {fivegrams_size / 1000000:.2f} MB")


if __name__ == "__main__":
    report_memory_usage_of_low_accuracy_mode()
    report_memory_usage_of_high_accuracy_mode()
