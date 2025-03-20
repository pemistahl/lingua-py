## Lingua 2.1.0 (released on 20 Mar 2025)

### Features

- This release introduces an absolute confidence metric based on unique and most
  common ngrams for each supported language. It allows to build
  a language detector from a single language only. Such a detector serves as
  a binary classifier, telling you whether some text is written in your selected
  language or not. (#235)

### Improvements

- The new absolute confidence metric helps to improve accuracy in low accuracy mode.
  The mean of average detection accuracy (single words, word pairs and sentences combined)
  increases from 77% to 80%.

- The rule-based algorithm for the recognition of Japanese texts has been improved.
  Texts including both Japanese and Chinese characters are now classified more often
  correctly as Japanese instead of Chinese.

- The characters `Щщ` are now correctly identified as possible indicators for
  the Ukrainian language, leading to slightly higher accuracy when identifying
  Ukrainian texts.

- The enums provided by this library can now be copied and pickled. (#199)

- Members of the enums provided by this library can now be created dynamically
  with the function `from_str()`. (#225)

- The library can now be used with Azure Artifacts. (#209)

### Bug Fixes

- Text spans created by `LanguageDetector.detect_multiple_languages_of()`
  sometimes skipped characters in the last span. This has been fixed.

- The tokenization of texts written in the Devanagari alphabet was flawed.
  This has been fixed, leading to better detection accuracy for Hindi and Marathi.

- The classes provided by this library are not part of the `builtins` module anymore
  but of the correct `lingua` module. (#255)

### Compatibility

- The newest Python 3.13 is now officially supported.
- Support for Python 3.8 and 3.9 has been dropped. The lowest supported Python version is 3.10 now.

## Lingua 1.4.1 (released on 07 Mar 2025)

### Improvements

- The rule-based algorithm for the recognition of Japanese texts has been improved.
  Texts including both Japanese and Chinese characters are now classified more often
  correctly as Japanese instead of Chinese.

### Bug Fixes

- Text spans created by `LanguageDetector.detect_multiple_languages_of()`
  sometimes skipped characters in the last span. This has been fixed. (#247)

## Lingua 1.4.0 (released on 29 Oct 2024)

### Features

- This release introduces an absolute confidence metric based on unique and most
  common ngrams for each supported language. It allows to build
  a language detector from a single language only. Such a detector serves as
  a binary classifier, telling you whether some text is written in your selected
  language or not. (#235)

### Improvements

- The new absolute confidence metric helps to improve accuracy in low accuracy mode.
  The mean of average detection accuracy (single words, word pairs and sentences combined)
  increases from 77% to 80%.

### Bug Fixes

- The tokenization of texts written in the Devanagari alphabet was flawed.
  This has been fixed, leading to better detection accuracy for Hindi and Marathi.

### Compatibility

- The newest Python 3.13 is now officially supported.
- Support for Python 3.8 and 3.9 has been dropped. The lowest supported Python version is 3.10 now.

## Lingua 1.3.5 (released on 03 Apr 2024)

### Improvements

- The language models are now stored in dictionaries instead of NumPy arrays.
  This change leads to significantly improved runtime performance at the cost
  of higher memory consumption (up to 3 GB for all models). As the runtime
  performance was much too slow with the former approach, this change makes
  sense because adding more memory is quite cheap.

- The language model files are now compressed with the Brotli algorithm which
  reduces the file size by 15 %, on average.

- The characters `Щщ` are now correctly identified as possible indicators for
  the Ukrainian language, leading to slightly higher accuracy when identifying
  Ukrainian texts.

### Miscellaneous

- All dependencies have been updated to their latest versions.

## Lingua 2.0.2 (released on 12 Dec 2023)

### Improvements

- Type stubs for the Python bindings are now available, allowing better static code
  analysis, better code completion in supported IDEs and easier understanding of
  the library's API. (#197)

### Bug Fixes

- The method `LanguageDetector.detect_multiple_languages_of` still returned character
  indices instead of byte indices when only a single `DetectionResult` was produced.
  This has been fixed. (#203, #205)

## Lingua 2.0.1 (released on 23 Nov 2023)

### Bug Fixes

- The method `LanguageDetector.detect_multiple_languages_of` returns byte indices.
  For creating string slices in Python and JavaScript, character indices are needed
  but were not provided. This resulted in incorrect `DetectionResult`s for Python
  and JavaScript. This has been fixed now by converting the byte indices to
  character indices. (#192)

- Some minor bugs in the WASM module have been fixed to prepare the first release
  of [Lingua for JavaScript](https://github.com/pemistahl/lingua-js).

## Lingua 2.0.0 (released on 14 Nov 2023)

### Features

- Python bindings for the Rust implementation of Lingua have now replaced the
  pure Python implementation in order to benefit from Rust's performance in any
  Python software.

- Parallel equivalents for all methods in `LanguageDetector` have been added
  to give the user the choice of using the library single-threaded or
  multi-threaded.

## Lingua 1.3.4 (released on 07 Nov 2023)

### Miscellaneous

- This release resolves some dependency issues so that the latest versions
  of dependencies NumPy, Pandas and Matplotib can be used with Python >= 3.9
  while older versions are used with Python 3.8.

- All dependencies have been updated to their latest versions.

## Lingua 1.3.3 (released on 27 Sep 2023)

### Improvements

- Processing the language models now performs a little faster by performing binary
  search on the language model NumPy arrays.

### Bug Fixes

- Several bugs in multiple languages detection have been fixed that caused
  incomplete results to be returned in several cases. (#143, #154)

- A significant amount of Kazakh texts were incorrectly classified as Mongolian.
  This has been fixed. (#160)

### Miscellaneous

- A new section on [performance tips](https://github.com/pemistahl/lingua-py#10-performance-tips)
  has been added to the README.

- All dependencies have been updated to their latest versions.

## Lingua 1.3.2 (released on 29 Jan 2023)

### Improvements

- After applying some internal optimizations, language detection is now
  faster, at least between 20% and 30%, approximately. For long input texts,
  the speed improvement is greater than for short input texts.

## Lingua 1.3.1 (released on 04 Jan 2023)

### Bug Fixes

- For long input texts, an error occurred whiled computing the confidence values
  due to numerical underflow when converting probabilities. This has been fixed.
  Thanks to @jordimas for reporting this bug. (#102)

## Lingua 1.3.0 (released on 30 Dec 2022)

### Improvements

- The min-max normalization method for the confidence values has been
  replaced with applying the softmax function. This gives more realistic
  probabilities. Big thanks to @Alex-Kopylov for proposing and implementing
  this change. (#99)

## Lingua 1.2.1 (released on 27 Dec 2022)

### Bug Fixes

- Under certain circumstances, calling the method
  `LanguageDetector.detect_multiple_languages_of()` raised an `IndexError`.
  This has been fixed. Thanks to @Saninsusanin for reporting this bug. (#98)

## Lingua 1.2.0 (released on 19 Dec 2022)

### Features

- The new method `LanguageDetector.detect_multiple_languages_of()` has been
  introduced. It allows to detect multiple languages in mixed-language text. (#4)

- The new method `LanguageDetector.compute_language_confidence()` has been
  introduced. It allows to retrieve the confidence value for one specific
  language only, given the input text. (#86)

### Improvements

- The computation of the confidence values has been revised and the min-max
  normalization algorithm is now applied to the values, making them better
  comparable by behaving more like real probabilities. (#78)

### Miscellaneous

- The library now has a fresh and colorful new logo. Why? Well, why not? (-:

## Lingua 1.1.3 (released on 29 Sep 2022)

### Improvements

- An `__all__` variable has been added indicating which types are exported
  by the library. This helps with type checking programs using Lingua. Big
  thanks to @bscan for the pull request. (#76)
- The rule-based language filter has been improved for German texts. (#71)
- A further bottleneck in the code has been removed, making language detection
  30 % faster compared to version 1.1.2, approximately.

## Lingua 1.1.2 (released on 06 Sep 2022)

### Improvements

- The language models are now stored on disk as serialized NumPy arrays instead
  of JSON. This reduces the preloading time of the language models significantly.
- A bottleneck in the language detection code has been removed, making language
  detection 40 % faster, approximately.

### Bug Fixes

- The `py.typed` file that actives static type checking was missing.
  Big thanks to @Vasniktel for reporting this problem. (#63)
- The ISO 639-3 code for Urdu was wrong. Big thanks to @pluiez for reporting
  this bug. (#64)

## Lingua 1.1.1 (released on 26 Aug 2022)

### Bug Fixes

- For certain ngrams, wrong probabilities were returned. This has been fixed.
  Big thanks to @3a77 for reporting this bug. (#62)

## Lingua 1.1.0 (released on 22 Aug 2022)

### Features

- The new method `LanguageDetectorBuilder.with_low_accuracy_mode()` has been
  introduced. By activating it, detection accuracy for short text is reduced
  in favor of a smaller memory footprint and faster detection performance.

### Improvements

- The memory footprint has been reduced significantly by storing the
  language models in structured NumPy arrays instead of dictionaries.
  This reduces memory consumption from 2600 MB to 800 MB, approximately.
- Several language model files have become obsolete and could be deleted
  without decreasing detection accuracy. This results in a smaller memory
  footprint.

### Compatibility

- The lowest supported Python version is 3.8 now. Python 3.7 is no longer
  compatible with this library.

## Lingua 1.0.1 (released on 24 Jan 2022)

### Compatibility

- This patch release makes the library compatible with Python >= 3.7.1.
  Previously, it could be installed from PyPI only with Python >= 3.9.

### Lingua 1.0.0 (released on 10 Jan 2022)

- The very first release of *Lingua*. Enjoy!
