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

from typing import FrozenSet, Iterable

from .detector import LanguageDetector
from .isocode import IsoCode639_1, IsoCode639_3
from .language import Language

_MISSING_LANGUAGE_MESSAGE: str = (
    "LanguageDetector needs at least 2 languages to choose from"
)


class LanguageDetectorBuilder:
    """This class configures and creates an instance of LanguageDetector."""

    def __init__(self, languages: FrozenSet[Language]):
        self._languages = languages
        self._minimum_relative_distance = 0.0
        self._is_every_language_model_preloaded = False
        self._is_low_accuracy_mode_enabled = False

    def __repr__(self):
        languages = sorted([language.name for language in self._languages])
        return (
            "LanguageDetectorBuilder("
            f"_languages={languages}, "
            f"_minimum_relative_distance={self._minimum_relative_distance}, "
            f"_is_every_language_model_preloaded={self._is_every_language_model_preloaded}), "
            f"_is_low_accuracy_mode_enabled={self._is_low_accuracy_mode_enabled}"
        )

    @classmethod
    def from_all_languages(cls) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in languages.
        """
        return cls._from(Language.all())

    @classmethod
    def from_all_spoken_languages(cls) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in spoken languages.
        """
        return cls._from(Language.all_spoken_ones())

    @classmethod
    def from_all_languages_with_arabic_script(cls) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in languages supporting the Arabic script.
        """
        return cls._from(Language.all_with_arabic_script())

    @classmethod
    def from_all_languages_with_cyrillic_script(cls) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in languages supporting the Cyrillic script.
        """
        return cls._from(Language.all_with_cyrillic_script())

    @classmethod
    def from_all_languages_with_devanagari_script(cls) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in languages supporting the Devanagari script.
        """
        return cls._from(Language.all_with_devanagari_script())

    @classmethod
    def from_all_languages_with_latin_script(cls) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in languages supporting the Latin script.
        """
        return cls._from(Language.all_with_latin_script())

    @classmethod
    def from_all_languages_without(
        cls, *languages: Language
    ) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with all built-in languages except those passed to this method.
        """
        languages_to_load = Language.all().difference(languages)
        if len(languages_to_load) < 2:
            raise ValueError(_MISSING_LANGUAGE_MESSAGE)
        return cls._from(languages_to_load)

    @classmethod
    def from_languages(cls, *languages: Language) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with the languages passed to this method.
        """
        if len(languages) < 2:
            raise ValueError(_MISSING_LANGUAGE_MESSAGE)
        return cls._from(languages)

    @classmethod
    def from_iso_codes_639_1(
        cls, *iso_codes: IsoCode639_1
    ) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with the languages specified by the ISO 639-1 codes passed
        to this method.

        Raises:
            ValueError: if less than two ISO codes are specified
        """
        if len(iso_codes) < 2:
            raise ValueError(_MISSING_LANGUAGE_MESSAGE)
        languages = set()
        for iso_code in iso_codes:
            language = Language.from_iso_code_639_1(iso_code)
            languages.add(language)
        return cls._from(languages)

    @classmethod
    def from_iso_codes_639_3(
        cls, *iso_codes: IsoCode639_3
    ) -> "LanguageDetectorBuilder":
        """Create and return an instance of LanguageDetectorBuilder
        with the languages specified by the ISO 639-3 codes passed
        to this method.

        Raises:
            ValueError: if less than two ISO codes are specified
        """
        if len(iso_codes) < 2:
            raise ValueError(_MISSING_LANGUAGE_MESSAGE)
        languages = set()
        for iso_code in iso_codes:
            language = Language.from_iso_code_639_3(iso_code)
            languages.add(language)
        return cls._from(languages)

    def with_minimum_relative_distance(
        self, distance: float
    ) -> "LanguageDetectorBuilder":
        """Set the desired value for the minimum relative distance measure.

        By default, Lingua returns the most likely language for a given
        input text. However, there are certain words that are spelled the
        same in more than one language. The word 'prologue', for instance,
        is both a valid English and French word. Lingua would output either
        English or French which might be wrong in the given context.
        For cases like that, it is possible to specify a minimum relative
        distance that the logarithmized and summed up probabilities for
        each possible language have to satisfy.

        Be aware that the distance between the language probabilities is
        dependent on the length of the input text. The longer the input
        text, the larger the distance between the languages. So if you
        want to classify very short text phrases, do not set the minimum
        relative distance too high. Otherwise you will get most results
        returned as None which is the return value for cases where
        language detection is not reliably possible.

        Raises:
            ValueError: if distance is smaller than 0.0 or greater than 0.99
        """
        if not 0 <= distance < 1:
            raise ValueError(
                "Minimum relative distance must lie in between 0.0 and 0.99"
            )
        self._minimum_relative_distance = distance
        return self

    def with_preloaded_language_models(self) -> "LanguageDetectorBuilder":
        """Preload all language models when creating the LanguageDetector
        instance.

        By default, Lingua uses lazy-loading to load only those language
        models on demand which are considered relevant by the rule-based
        filter engine. For web services, for instance, it is rather
        beneficial to preload all language models into memory to avoid
        unexpected latency while waiting for the service response. This
        method allows to switch between these two loading modes.
        """
        self._is_every_language_model_preloaded = True
        return self

    def with_low_accuracy_mode(self) -> "LanguageDetectorBuilder":
        """Disables the high accuracy mode in order to save memory
        and increase performance.

        By default, Lingua's high detection accuracy comes at the cost
        of loading large language models into memory which might not be
        feasible for systems running low on resources.

        This method disables the high accuracy mode so that only a small
        subset of language models is loaded into memory. The downside of
        this approach is that detection accuracy for short texts consisting
        of less than 120 characters will drop significantly. However,
        detection accuracy for texts which are longer than 120 characters
        will remain mostly unaffected.
        """
        self._is_low_accuracy_mode_enabled = True
        return self

    def build(self) -> LanguageDetector:
        """Create and return the configured LanguageDetector instance."""
        return LanguageDetector._from(
            self._languages,
            self._minimum_relative_distance,
            self._is_every_language_model_preloaded,
            self._is_low_accuracy_mode_enabled,
        )

    @classmethod
    def _from(cls, languages: Iterable[Language]) -> "LanguageDetectorBuilder":
        if not isinstance(languages, frozenset):
            return LanguageDetectorBuilder(frozenset(languages))
        return LanguageDetectorBuilder(languages)
