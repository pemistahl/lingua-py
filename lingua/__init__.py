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

"""
## 1. What does this library do?

Its task is simple: It tells you which language some provided textual data is
written in. This is very useful as a preprocessing step for linguistic data
in natural language processing applications such as text classification and
spell checking. Other use cases, for instance, might include routing e-mails
to the right geographically located customer service department, based on the
e-mails' languages.

## 2. Why does this library exist?

Language detection is often done as part of large machine learning frameworks
or natural language processing applications. In cases where you don't need
the full-fledged functionality of those systems or don't want to learn the
ropes of those, a small flexible library comes in handy.

Python is widely used in natural language processing, so there are a couple
of comprehensive open source libraries for this task, such as Google's
[*CLD 2*](https://github.com/CLD2Owners/cld2) and
[*CLD 3*](https://github.com/google/cld3),
[*langid*](https://github.com/saffsd/langid.py),
[*fastText*](https://fasttext.cc/docs/en/language-identification.html) and
[*langdetect*](https://github.com/Mimino666/langdetect).
Unfortunately, except for the last one they have two major drawbacks:

1. Detection only works with quite lengthy text fragments. For very short
text snippets such as Twitter messages, it does not provide adequate results.
2. The more languages take part in the decision process, the less accurate are
the detection results.

*Lingua* aims at eliminating these problems. It nearly does not need any
configuration and yields pretty accurate results on both long and short text,
even on single words and phrases. It draws on both rule-based and statistical
methods but does not use any dictionaries of words. It does not need a
connection to any external API or service either. Once the library has been
downloaded, it can be used completely offline.

## 3. Which languages are supported?

Compared to other language detection libraries, *Lingua's* focus is on
*quality over quantity*, that is, getting detection right for a small set of
languages first before adding new ones. Currently, the following 75 languages
are supported:

- Afrikaans
- Albanian
- Arabic
- Armenian
- Azerbaijani
- Basque
- Belarusian
- Bengali
- Norwegian Bokmal
- Bosnian
- Bulgarian
- Catalan
- Chinese
- Croatian
- Czech
- Danish
- Dutch
- English
- Esperanto
- Estonian
- Finnish
- French
- Ganda
- Georgian
- German
- Greek
- Gujarati
- Hebrew
- Hindi
- Hungarian
- Icelandic
- Indonesian
- Irish
- Italian
- Japanese
- Kazakh
- Korean
- Latin
- Latvian
- Lithuanian
- Macedonian
- Malay
- Maori
- Marathi
- Mongolian
- Norwegian Nynorsk
- Persian
- Polish
- Portuguese
- Punjabi
- Romanian
- Russian
- Serbian
- Shona
- Slovak
- Slovene
- Somali
- Sotho
- Spanish
- Swahili
- Swedish
- Tagalog
- Tamil
- Telugu
- Thai
- Tsonga
- Tswana
- Turkish
- Ukrainian
- Urdu
- Vietnamese
- Welsh
- Xhosa
- Yoruba
- Zulu

## 4. How good is it?

*Lingua* is able to report accuracy statistics for some bundled test data
available for each supported language. The test data for each language is split
into three parts:

1. a list of single words with a minimum length of 5 characters
2. a list of word pairs with a minimum length of 10 characters
3. a list of complete grammatical sentences of various lengths

Both the language models and the test data have been created from separate
documents of the [Wortschatz corpora](https://wortschatz.uni-leipzig.de)
offered by Leipzig University, Germany. Data crawled from various news websites
have been used for training, each corpus comprising one million sentences.
For testing, corpora made of arbitrarily chosen websites have been used, each
comprising ten thousand sentences. From each test corpus, a random unsorted
subset of 1000 single words, 1000 word pairs and 1000 sentences has been
extracted, respectively.

Given the generated test data, I have compared the detection results of
*Lingua*, *fastText*, *langdetect*, *langid*, *CLD 2* and *CLD 3* running over the data
of *Lingua's* supported 75 languages. Languages that are not supported by the other
detectors are simply ignored for them during the detection process.

Each of the following sections contains two plots. The bar plot shows the detailed accuracy
results for each supported language. The box plot illustrates the distributions of the
accuracy values for each classifier. The boxes themselves represent the areas which the
middle 50 % of data lie within. Within the colored boxes, the horizontal lines mark the
median of the distributions.

### 4.1 Single word detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-single-words.png" alt="Single Word Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/barplot-single-words.png" alt="Single Word Detection Performance" />
</details>

<br/><br/>

### 4.2 Word pair detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-word-pairs.png" alt="Word Pair Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/barplot-word-pairs.png" alt="Word Pair Detection Performance" />
</details>

<br/><br/>

### 4.3 Sentence detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-sentences.png" alt="Sentence Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/barplot-sentences.png" alt="Sentence Detection Performance" />
</details>

<br/><br/>

### 4.4 Average detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-average.png" alt="Average Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/barplot-average.png" alt="Average Detection Performance" />
</details>

## 5. Why is it better than other libraries?

Every language detector uses a probabilistic
[n-gram](https://en.wikipedia.org/wiki/N-gram) model trained on the character
distribution in some training corpus. Most libraries only use n-grams of size 3
(trigrams) which is satisfactory for detecting the language of longer text
fragments consisting of multiple sentences. For short phrases or single words,
however, trigrams are not enough. The shorter the input text is, the less
n-grams are available. The probabilities estimated from such few n-grams are not
reliable. This is why *Lingua* makes use of n-grams of sizes 1 up to 5 which
results in much more accurate prediction of the correct language.

A second important difference is that *Lingua* does not only use such a
statistical model, but also a rule-based engine. This engine first determines
the alphabet of the input text and searches for characters which are unique
in one or more languages. If exactly one language can be reliably chosen this
way, the statistical model is not necessary anymore. In any case, the
rule-based engine filters out languages that do not satisfy the conditions of
the input text. Only then, in a second step, the probabilistic n-gram model is
taken into consideration. This makes sense because loading less language models
means less memory consumption and better runtime performance.

In general, it is always a good idea to restrict the set of languages to be
considered in the classification process using the respective api methods.
If you know beforehand that certain languages are never to occur in an input
text, do not let those take part in the classifcation process. The filtering
mechanism of the rule-based engine is quite good, however, filtering based on
your own knowledge of the input text is always preferable.

## 6. How to add it to your project?

*Lingua* is available in the
[Python Package Index](https://pypi.org/project/lingua-language-detector)
and can be installed with:

```shell
pip install lingua-language-detector
```

## 7. How to use?

### 7.1 Basic usage

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> detector.detect_language_of("languages are awesome")
Language.ENGLISH

```

### 7.2 Minimum relative distance

By default, *Lingua* returns the most likely language for a given input text.
However, there are certain words that are spelled the same in more than one
language. The word *prologue*, for instance, is both a valid English and French
word. *Lingua* would output either English or French which might be wrong in
the given context. For cases like that, it is possible to specify a minimum
relative distance that the logarithmized and summed up probabilities for
each possible language have to satisfy. It can be stated in the following way:

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
>>> detector = LanguageDetectorBuilder.from_languages(*languages)\
.with_minimum_relative_distance(0.9)\
.build()
>>> print(detector.detect_language_of("languages are awesome"))
None

```

Be aware that the distance between the language probabilities is dependent on
the length of the input text. The longer the input text, the larger the
distance between the languages. So if you want to classify very short text
phrases, do not set the minimum relative distance too high. Otherwise, `None`
will be returned most of the time as in the example above. This is the return
value for cases where language detection is not reliably possible.

### 7.3 Confidence values

Knowing about the most likely language is nice but how reliable is the computed
likelihood? And how less likely are the other examined languages in comparison
to the most likely one? These questions can be answered as well:

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> confidence_values = detector.compute_language_confidence_values("languages are awesome")
>>> for language, value in confidence_values:
...     print(f"{language.name}: {value:.2f}")
ENGLISH: 0.93
FRENCH: 0.04
GERMAN: 0.02
SPANISH: 0.01

```

In the example above, a list is returned containing those languages which the
calling instance of LanguageDetector has been built from, sorted by
their confidence value in descending order. Each value is a probability between
0.0 and 1.0. The probabilities of all languages will sum to 1.0.
If the language is unambiguously identified by the rule engine, the value 1.0
will always be returned for this language. The other languages will receive a
value of 0.0.

There is also a method for returning the confidence value for one specific
language only:

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> confidence_value = detector.compute_language_confidence("languages are awesome", Language.FRENCH)
>>> print(f"{confidence_value:.2f}")
0.04

```

The value that this method computes is a number between 0.0 and 1.0. If the
language is unambiguously identified by the rule engine, the value 1.0 will
always be returned. If the given language is not supported by this detector
instance, the value 0.0 will always be returned.

### 7.4 Eager loading versus lazy loading

By default, *Lingua* uses lazy-loading to load only those language models on
demand which are considered relevant by the rule-based filter engine. For web
services, for instance, it is rather beneficial to preload all language models
into memory to avoid unexpected latency while waiting for the service response.
If you want to enable the eager-loading mode, you can do it like this:

```python
LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
```

Multiple instances of `LanguageDetector` share the same language models in
memory which are accessed asynchronously by the instances.

### 7.5 Low accuracy mode versus high accuracy mode

*Lingua's* high detection accuracy comes at the cost of being noticeably slower
than other language detectors. The large language models also consume significant
amounts of memory. These requirements might not be feasible for systems running low
on resources. If you want to classify mostly long texts or need to save resources,
you can enable a *low accuracy mode* that loads only a small subset of the language
models into memory:

```python
LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()
```

The downside of this approach is that detection accuracy for short texts consisting
of less than 120 characters will drop significantly. However, detection accuracy for
texts which are longer than 120 characters will remain mostly unaffected.

In high accuracy mode (the default), the language detector consumes approximately
800 MB of memory if all language models are loaded. In low accuracy mode, memory
consumption is reduced to approximately 60 MB.

An alternative for a smaller memory footprint and faster performance is to reduce the set
of languages when building the language detector. In most cases, it is not advisable to
build the detector from all supported languages. When you have knowledge about
the texts you want to classify you can almost always rule out certain languages as impossible
or unlikely to occur.

### 7.6 Detection of multiple languages in mixed-language texts

In contrast to most other language detectors, *Lingua* is able to detect multiple
languages in mixed-language texts. This feature can yield quite reasonable results but
it is still in an experimental state and therefore the detection result is highly
dependent on the input text. It works best in high-accuracy mode with multiple long
words for each language. The shorter the phrases and their words are, the less
accurate are the results. Reducing the set of languages when building the language
detector can also improve accuracy for this task if the languages occurring in the
text are equal to the languages supported by the respective language detector instance.

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> sentence = "Parlez-vous français? " + \\
...            "Ich spreche Französisch nur ein bisschen. " + \\
...            "A little bit is better than nothing."
>>> for result in detector.detect_multiple_languages_of(sentence):
...     print(f"{result.language.name}: '{sentence[result.start_index:result.end_index]}'")
FRENCH: 'Parlez-vous français? '
GERMAN: 'Ich spreche Französisch nur ein bisschen. '
ENGLISH: 'A little bit is better than nothing.'

```

In the example above, a list of
[`DetectionResult`](https://github.com/pemistahl/lingua-py/blob/main/lingua/detector.py#L144)
is returned. Each entry in the list describes a contiguous single-language text section,
providing start and end indices of the respective substring.

### 7.7 Methods to build the LanguageDetector

There might be classification tasks where you know beforehand that your
language data is definitely not written in Latin, for instance. The detection
accuracy can become better in such cases if you exclude certain languages from
the decision process or just explicitly include relevant languages:

```python
from lingua import LanguageDetectorBuilder, Language, IsoCode639_1, IsoCode639_3

# Include all languages available in the library.
LanguageDetectorBuilder.from_all_languages()

# Include only languages that are not yet extinct (= currently excludes Latin).
LanguageDetectorBuilder.from_all_spoken_languages()

# Include only languages written with Cyrillic script.
LanguageDetectorBuilder.from_all_languages_with_cyrillic_script()

# Exclude only the Spanish language from the decision algorithm.
LanguageDetectorBuilder.from_all_languages_without(Language.SPANISH)

# Only decide between English and German.
LanguageDetectorBuilder.from_languages(Language.ENGLISH, Language.GERMAN)

# Select languages by ISO 639-1 code.
LanguageDetectorBuilder.from_iso_codes_639_1(IsoCode639_1.EN, IsoCode639_1.DE)

# Select languages by ISO 639-3 code.
LanguageDetectorBuilder.from_iso_codes_639_3(IsoCode639_3.ENG, IsoCode639_3.DEU)
```
"""

__all__ = (
    "ConfidenceValue",
    "DetectionResult",
    "LanguageDetectorBuilder",
    "LanguageDetector",
    "IsoCode639_1",
    "IsoCode639_3",
    "Language",
    "LanguageModelFilesWriter",
    "TestDataFilesWriter",
)

from .builder import LanguageDetectorBuilder
from .detector import ConfidenceValue, DetectionResult, LanguageDetector
from .isocode import IsoCode639_1, IsoCode639_3
from .language import Language
from .writer import LanguageModelFilesWriter, TestDataFilesWriter
