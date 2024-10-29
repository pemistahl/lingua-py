<div align="center">

![lingua](https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/logo.png)

[![build](https://github.com/pemistahl/lingua-py/actions/workflows/build.yml/badge.svg?branch=pure-python-impl)](https://github.com/pemistahl/lingua-py/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/pemistahl/lingua-py/branch/pure-python-impl/graph/badge.svg)](https://codecov.io/gh/pemistahl/lingua-py)
[![supported languages](https://img.shields.io/badge/supported%20languages-75-green.svg)](#4-which-languages-are-supported)
![supported Python versions](https://img.shields.io/badge/Python-%3E%3D%203.10-blue)
[![pypi](https://img.shields.io/badge/PYPI-v1.4.0-blue)](https://pypi.org/project/lingua-language-detector/1.4.0/)
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
</div>

<br>

## 1. What does this library do?

Its task is simple: It tells you which language some text is written in.
This is very useful as a preprocessing step for linguistic data
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
[*Langid*](https://github.com/saffsd/langid.py),
[*fastText*](https://fasttext.cc/docs/en/language-identification.html),
[*fastspell*](https://github.com/mbanon/fastspell),
[*Simplemma*](https://github.com/adbar/simplemma) and
[*Langdetect*](https://github.com/Mimino666/langdetect).
Unfortunately, most of them have two major drawbacks:

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

## 3. A short history of this library

This library started as a pure Python implementation. Python's quick prototyping
capabilities made an important contribution to its improvements. Unfortunately,
there was always a tradeoff between performance and memory consumption. At first,
*Lingua's* language models were stored in dictionaries during runtime. This led
to quick performance at the cost of large memory consumption (more than 3 GB).
Because of that, the language models were then stored in NumPy arrays instead of
dictionaries. Memory consumption reduced to approximately 800 MB but CPU
performance dropped significantly. Both approaches were not satisfying.

Starting from version 2.0.0, the pure Python implementation is complemented by
compiled Python bindings to the native
[Rust implementation](https://github.com/pemistahl/lingua-rs) of *Lingua*.
This decision has led to both quick performance and a small memory
footprint of less than 1 GB. The pure Python implementation is still available
in a [separate branch](https://github.com/pemistahl/lingua-py/tree/pure-python-impl)
in this repository and will be kept up-to-date in subsequent 1.* releases.
There are environments that do not support native Python extensions such as
[Juno](https://juno.sh/), so a pure Python implementation is still useful.
Both 1.* and 2.* versions are available on the Python package index (PyPI).

## 4. Which languages are supported?

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

## 5. How accurate is it?

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
*Lingua*, *fastText*, *langdetect*, *langid*, *CLD 2* and *CLD 3* running over the data of
*Lingua's* supported 75 languages. Languages that are not supported by the other
detectors are simply ignored for them during the detection process.

Each of the following sections contains three plots. The bar plot shows the detailed accuracy
results for each supported language. The box plots illustrate the distributions of the
accuracy values for each classifier. The boxes themselves represent the areas which the
middle 50 % of data lie within. Within the colored boxes, the horizontal lines mark the
median of the distributions.

### 5.1 Single word detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-single-words.png" alt="Single Word Detection Performance" />

<br/><br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-single-language-mode-single-words.png" alt="Single Word Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/barplot-single-words.png" alt="Single Word Detection Performance" />
</details>

<br/><br/>

### 5.2 Word pair detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-word-pairs.png" alt="Word Pair Detection Performance" />

<br/><br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-single-language-mode-word-pairs.png" alt="Word Pair Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/barplot-word-pairs.png" alt="Word Pair Detection Performance" />
</details>

<br/><br/>

### 5.3 Sentence detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-sentences.png" alt="Sentence Detection Performance" />

<br/><br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-single-language-mode-sentences.png" alt="Sentence Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/barplot-sentences.png" alt="Sentence Detection Performance" />
</details>

<br/><br/>

### 5.4 Average detection

<br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-average.png" alt="Average Detection Performance" />

<br/><br/>

<img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/boxplot-single-language-mode-average.png" alt="Average Detection Performance" />

<br/>

<details>
    <summary>Bar plot</summary>
    <img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/plots/barplot-average.png" alt="Average Detection Performance" />
</details>

<br/><br/>

### 5.5 Mean, median and standard deviation

The tables found [here](https://github.com/pemistahl/lingua-py/tree/pure-python-impl/tables)
show detailed statistics for each language and classifier including mean, median and standard deviation.


## 6. How fast is it?

The accuracy reporter script measures the time each language detector needs
to classify 3000 input texts for each of the supported 75 languages. The results
below have been produced on an iMac 3.6 Ghz 8-Core Intel Core i9 with 40 GB RAM.

CLD 2 and 3, FastText and FastSpell have at least partially been implemented
in C or C++, that is why they are the most performant ones. The others have been
implemented in pure Python including Lingua.

| Detector                                     |             Time |
|----------------------------------------------|-----------------:|
| CLD 2                                        |         8.65 sec |
| FastText                                     |        10.50 sec |
| CLD 3                                        |        16.77 sec |
| FastSpell (aggressive mode)                  |        51.92 sec |
| FastSpell (conservative mode)                |        52.32 sec |
| Simplemma                                    |  2 min 36.44 sec |
| Langid                                       |  3 min 50.40 sec |
| Lingua (low accuracy mode)                   |  4 min 05.53 sec |
| Lingua (high accuracy mode)                  |  8 min 09.52 sec |
| Langdetect                                   | 10 min 43.96 sec |

## 7. Why is it better than other libraries?

Every language detector compared here uses a probabilistic
[n-gram](https://en.wikipedia.org/wiki/N-gram) model trained on the character
distribution in some training corpus. Most libraries only use n-grams of size 3
(trigrams) which is satisfactory for detecting the language of longer text
fragments consisting of multiple sentences. For short phrases or single words,
however, trigrams are not enough. The shorter the input text is, the less
n-grams are available. The probabilities estimated from such few n-grams are not
reliable. This is why *Lingua* makes use of a Naive Bayes classifier with n-grams
of sizes 1 up to 5 which results in much more accurate prediction of the correct language.

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
text, do not let those take part in the classification process. The filtering
mechanism of the rule-based engine is quite good, however, filtering based on
your own knowledge of the input text is always preferable.

## 8. Test report generation

If you want to reproduce the accuracy results above, you can generate the test
reports yourself for all classifiers and languages by executing:

    poetry install --only script
    poetry run python3 scripts/accuracy_reporter.py

Accuracy reports for only a subset of classifiers and / or languages can be created by
passing command line arguments:

    poetry run python3 scripts/accuracy_reporter.py --detectors cld2 lingua-high-accuracy --languages bulgarian german

For each detector and language, a test report file is then written into
[`/accuracy-reports`](https://github.com/pemistahl/lingua-py/tree/pure-python-impl/accuracy-reports).
As an example, here is the current output of the *Lingua* German report
(high accuracy mode):

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

## 9. How to add it to your project?

*Lingua* is available in the [Python Package Index](https://pypi.org/project/lingua-language-detector/1.3.5)
and can be installed with:

    pip install lingua-language-detector==1.4.0

## 10. How to build?

*Lingua* requires Python >= 3.10 and uses [Poetry](https://python-poetry.org) for packaging and
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

## 11. How to use?

### 11.1 Basic usage

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> language = detector.detect_language_of("languages are awesome")
>>> language
Language.ENGLISH
>>> language.iso_code_639_1
IsoCode639_1.EN
>>> language.iso_code_639_1.name
'EN'
>>> language.iso_code_639_3
IsoCode639_3.ENG
>>> language.iso_code_639_3.name
'ENG'
```

### 11.2 Minimum relative distance

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

### 11.3 Confidence values

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

### 11.4 Eager loading versus lazy loading

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

### 11.5 Low accuracy mode versus high accuracy mode

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

### 11.6 Single language mode

If you build a `LanguageDetector` from one language only it will operate in single language mode.
This means the detector will try to find out whether a given text has been written in the given language or not.
If not, then `None` will be returned, otherwise the given language.

In single language mode, the detector decides based on a set of unique and most common n-grams which
have been collected beforehand for every supported language. It turns out that unique and most common
n-grams help to improve accuracy in low accuracy mode, so they are used for that mode as well. In high
accuracy mode, however, they do not make a significant difference, that's why they are left out.

### 11.7 Detection of multiple languages in mixed-language texts

In contrast to most other language detectors, *Lingua* is able to detect multiple languages
in mixed-language texts. This feature can yield quite reasonable results but it is still
in an experimental state and therefore the detection result is highly dependent on the input
text. It works best in high-accuracy mode with multiple long words for each language.
The shorter the phrases and their words are, the less accurate are the results. Reducing the
set of languages when building the language detector can also improve accuracy for this task
if the languages occurring in the text are equal to the languages supported by the respective
language detector instance.

```python
>>> from lingua import Language, LanguageDetectorBuilder
>>> languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN]
>>> detector = LanguageDetectorBuilder.from_languages(*languages).build()
>>> sentence = "Parlez-vous français? " + \
...            "Ich spreche Französisch nur ein bisschen. " + \
...            "A little bit is better than nothing."
>>> for result in detector.detect_multiple_languages_of(sentence):
...     print(f"{result.language.name}: '{sentence[result.start_index:result.end_index]}'")
FRENCH: 'Parlez-vous français? '
GERMAN: 'Ich spreche Französisch nur ein bisschen. '
ENGLISH: 'A little bit is better than nothing.'
```

In the example above, a list of
[`DetectionResult`](https://github.com/pemistahl/lingua-py/blob/pure-python-impl/lingua/detector.py#L148)
is returned. Each entry in the list describes a contiguous single-language text section,
providing start and end indices of the respective substring.

### 11.8 Methods to build the LanguageDetector

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

## 12. Performance tips

If you find that Lingua is too slow for your purposes, e.g. when you classify
a large amount of texts, a sensible option is to make use of process-based
parallelism via the [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
module. This allows to distribute the workload over multiple CPU cores which improves
speed of execution at the cost of higher memory consumption.

The easiest way to implement it is by making use of
[`ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor):

```python
from concurrent.futures import ProcessPoolExecutor
from lingua import LanguageDetectorBuilder

detector = (
  LanguageDetectorBuilder.from_all_languages()
  .with_preloaded_language_models()
  .build()
)

def classify(text):
    return detector.detect_language_of(text)

n = 4 # Set n to the number of CPU cores in your machine
texts = ["huge amount", "of texts", ...]

with ProcessPoolExecutor(max_workers=n) as executor:
    results = executor.map(classify, texts)
    for detected_language in results:
        # process the results
        ...
```

Be aware that starting n processes will consume n times more memory for the
language models. In a single process, all language models consume around 3 GB
of memory. So when starting 4 processes, memory consumption will increase up to
12 GB!

## 13. What's next for version 1.5.0?

Take a look at the [planned issues](https://github.com/pemistahl/lingua-py/milestone/10).
