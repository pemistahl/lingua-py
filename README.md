<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/logo.png" alt="Lingua Logo" />

<br>

[![build](https://github.com/pemistahl/lingua-py/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/pemistahl/lingua-py/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/pemistahl/lingua-py/branch/main/graph/badge.svg)](https://codecov.io/gh/pemistahl/lingua-py)
[![supported languages](https://img.shields.io/badge/supported%20languages-75-green.svg)](#supported-languages)
[![docs](https://img.shields.io/badge/docs-API-yellowgreen)](https://pemistahl.github.io/lingua-py)
[![pypi](https://img.shields.io/badge/PYPI-v1.0.0-blue)](https://pypi.org/project/lingua-language-detector)
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

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
[*langid*](https://github.com/saffsd/langid.py) and
[*langdetect*](https://github.com/Mimino666/langdetect).
Unfortunately, except for the last one they have two major drawbacks:

1. Detection only works with quite lengthy text fragments. For very short
   text snippets such as Twitter messages, they do not provide adequate results.
2. The more languages take part in the decision process, the less accurate are
   the detection results.

*Lingua* aims at eliminating these problems. She nearly does not need any
configuration and yields pretty accurate results on both long and short text,
even on single words and phrases. She draws on both rule-based and statistical
methods but does not use any dictionaries of words. She does not need a
connection to any external API or service either. Once the library has been
downloaded, it can be used completely offline.

## 3. Which languages are supported?

Compared to other language detection libraries, *Lingua's* focus is on
*quality over quantity*, that is, getting detection right for a small set of
languages first before adding new ones. Currently, the following 75 languages
are supported:

- A
    - Afrikaans
    - Albanian
    - Arabic
    - Armenian
    - Azerbaijani
- B
    - Basque
    - Belarusian
    - Bengali
    - Norwegian Bokmal
    - Bosnian
    - Bulgarian
- C
    - Catalan
    - Chinese
    - Croatian
    - Czech
- D
    - Danish
    - Dutch
- E
    - English
    - Esperanto
    - Estonian
- F
    - Finnish
    - French
- G
    - Ganda
    - Georgian
    - German
    - Greek
    - Gujarati
- H
    - Hebrew
    - Hindi
    - Hungarian
- I
    - Icelandic
    - Indonesian
    - Irish
    - Italian
- J
    - Japanese
- K
    - Kazakh
    - Korean
- L
    - Latin
    - Latvian
    - Lithuanian
- M
    - Macedonian
    - Malay
    - Maori
    - Marathi
    - Mongolian
- N
    - Norwegian Nynorsk
- P
    - Persian
    - Polish
    - Portuguese
    - Punjabi
- R
    - Romanian
    - Russian
- S
    - Serbian
    - Shona
    - Slovak
    - Slovene
    - Somali
    - Sotho
    - Spanish
    - Swahili
    - Swedish
- T
    - Tagalog
    - Tamil
    - Telugu
    - Thai
    - Tsonga
    - Tswana
    - Turkish
- U
    - Ukrainian
    - Urdu
- V
    - Vietnamese
- W
    - Welsh
- X
    - Xhosa
- Y
    - Yoruba
- Z
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
*Lingua*, *langdetect*, *langid*, *CLD 2* and *CLD 3* running over the data of
*Lingua's* supported 75 languages. Languages that are not supported by the other
detectors are simply ignored for them during the detection process.

The box plots below illustrate the distributions of the accuracy values for
each classifier. The boxes themselves represent the areas which the middle
50 % of data lie within. Within the colored boxes, the horizontal lines mark
the median of the distributions. All these plots demonstrate that *Lingua*
clearly outperforms its contenders. Bar plots for each language can be found
in the file
[ACCURACY_PLOTS.md](https://github.com/pemistahl/lingua-py/blob/main/ACCURACY_PLOTS.md).
Detailed statistics including mean, median and standard deviation values for
each language and classifier are available in the file
[ACCURACY_TABLE.md](https://github.com/pemistahl/lingua-py/blob/main/ACCURACY_TABLE.md).

### 4.1 Single word detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-single-words.png" alt="Single Word Detection Performance" />

<br/><br/>

### 4.2 Word pair detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-word-pairs.png" alt="Word Pair Detection Performance" />

<br/><br/>

### 4.3 Sentence detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-sentences.png" alt="Sentence Detection Performance" />

<br/><br/>

### 4.4 Average detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/main/images/plots/boxplot-average.png" alt="Average Detection Performance" />

<br/><br/>

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

## 6. Test report generation

If you want to reproduce the accuracy results above, you can generate the test
reports yourself for all classifiers and languages by executing:

    poetry install --extras "langdetect langid gcld3 pycld2"
    poetry run python3 scripts/accuracy_reporter.py

For each detector and language, a test report file is then written into
[`/accuracy-reports`](https://github.com/pemistahl/lingua-py/tree/main/accuracy-reports).
As an example, here is the current output of the *Lingua* German report:

```
##### German #####

>>> Accuracy on average: 89.27%

>> Detection of 1000 single words (average length: 9 chars)
Accuracy: 74.20%
Erroneously classified as Dutch: 2.30%, Danish: 2.20%, English: 2.20%, Latin: 1.80%, Bokmal: 1.60%, Italian: 1.30%, Basque: 1.20%, Esperanto: 1.20%, French: 1.20%, Swedish: 0.90%, Afrikaans: 0.70%, Finnish: 0.60%, Nynorsk: 0.60%, Portuguese: 0.60%, Yoruba: 0.60%, Sotho: 0.50%, Tsonga: 0.50%, Welsh: 0.50%, Estonian: 0.40%, Irish: 0.40%, Polish: 0.40%, Spanish: 0.40%, Tswana: 0.40%, Albanian: 0.30%, Icelandic: 0.30%, Tagalog: 0.30%, Bosnian: 0.20%, Catalan: 0.20%, Croatian: 0.20%, Indonesian: 0.20%, Lithuanian: 0.20%, Romanian: 0.20%, Swahili: 0.20%, Zulu: 0.20%, Latvian: 0.10%, Malay: 0.10%, Maori: 0.10%, Slovak: 0.10%, Slovene: 0.10%, Somali: 0.10%, Turkish: 0.10%, Xhosa: 0.10%

>> Detection of 1000 word pairs (average length: 18 chars)
Accuracy: 93.90%
Erroneously classified as Dutch: 0.90%, Latin: 0.90%, English: 0.70%, Swedish: 0.60%, Danish: 0.50%, French: 0.40%, Bokmal: 0.30%, Irish: 0.20%, Tagalog: 0.20%, Tsonga: 0.20%, Afrikaans: 0.10%, Esperanto: 0.10%, Estonian: 0.10%, Finnish: 0.10%, Italian: 0.10%, Maori: 0.10%, Nynorsk: 0.10%, Somali: 0.10%, Swahili: 0.10%, Turkish: 0.10%, Welsh: 0.10%, Zulu: 0.10%

>> Detection of 1000 sentences (average length: 111 chars)
Accuracy: 99.70%
Erroneously classified as Dutch: 0.20%, Latin: 0.10%
```

## 7. How to add it to your project?

*Lingua* is available in the [Python Package Index](https://pypi.org/project/lingua-language-detector)
and can be installed with:

    pip install lingua-language-detector

## 8. How to build?

*Lingua* requires Python >= 3.9 and uses [Poetry](https://python-poetry.org) for packaging and
dependency management. You need to install it first if you have not done so yet.
Afterwards, clone the repository and install the project dependencies:

```
git clone https://github.com/pemistahl/lingua-py.git
cd lingua-py
poetry install
```

The library makes uses of type annotations which allow for static type checking with
[Mypy](http://mypy-lang.org). Run the following command for checking the types:

    poetry run mypy

The source code is accompanied by an extensive unit test suite. To run the tests, simply say:

    poetry run pytest

## 9. How to use?

### 9.1 Basic usage

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> detector.detect_language_of("languages are awesome")
Language.ENGLISH
```

### 9.2 Minimum relative distance

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
.with_minimum_relative_distance(0.25)\
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

### 9.3 Confidence values

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
ENGLISH: 1.00
FRENCH: 0.79
GERMAN: 0.75
SPANISH: 0.70
```

In the example above, a list of all possible languages is returned, sorted by
their confidence value in descending order. The values that the detector
computes are part of a **relative** confidence metric, not of an absolute one.
Each value is a number between 0.0 and 1.0. The most likely language is always
returned with value 1.0. All other languages get values assigned which are
lower than 1.0, denoting how less likely those languages are in comparison to
the most likely language.

The list returned by this method does not necessarily contain all languages
which this LanguageDetector instance was built from. If the rule-based engine
decides that a specific language is truly impossible, then it will not be part
of the returned list. Likewise, if no ngram probabilities can be found within
the detector's languages for the given input text, the returned list will be
empty. The confidence value for each language not being part of the returned
list is assumed to be 0.0.

## 9.4 Eager loading versus lazy loading

By default, *Lingua* uses lazy-loading to load only those language models on
demand which are considered relevant by the rule-based filter engine. For web
services, for instance, it is rather beneficial to preload all language models
into memory to avoid unexpected latency while waiting for the service response.
If you want to enable the eager-loading mode, you can do it like this:

    LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()

Multiple instances of `LanguageDetector` share the same language models in
memory which are accessed asynchronously by the instances.

## 9.5 Methods to build the LanguageDetector

There might be classification tasks where you know beforehand that your
language data is definitely not written in Latin, for instance. The detection
accuracy can become better in such cases if you exclude certain languages from
the decision process or just explicitly include relevant languages:

```python
from lingua import LanguageDetectorBuilder, Language, IsoCode639_1, IsoCode639_3

# Including all languages available in the library
# consumes approximately 3GB of memory and might
# lead to slow runtime performance.
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

## 10. What's next for version 1.1.0?

Take a look at the [planned issues](https://github.com/pemistahl/lingua-py/milestone/1).

## 11. Contributions

Any contributions to *Lingua* are very much appreciated. Please read the instructions
in [`CONTRIBUTING.md`](https://github.com/pemistahl/lingua-py/blob/main/CONTRIBUTING.md)
for how to add new languages to the library.
