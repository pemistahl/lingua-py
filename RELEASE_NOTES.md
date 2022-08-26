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
