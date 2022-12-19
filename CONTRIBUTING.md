## You want to contribute to Lingua? That's great!

In case you want to contribute something to *Lingua*, then I encourage you to do so. Do you have ideas for
improving the API? Are there some specific languages that you want to have supported early? Or have you
found any bugs so far? Feel free to open an issue or send a pull request. It's very much appreciated.

For pull requests, please make sure that all unit tests pass and that the code is formatted according to
the rules of the [Python code formatter *Black*](https://github.com/psf/black).

All kinds of pull requests are welcome. The pull requests I favor the most are new language additions. If you want
to contribute new languages to *Lingua*, here comes a detailed manual explaining how to accomplish that.

Thank you very much in advance for all contributions, however small they may be.

### How to add new languages?

1. Clone *Lingua's* repository to your own computer.
2. Open enums [`IsoCode639_1`][isocode639_1 url] and [`IsoCode639_3`][isocode639_3 url] and add the
language's iso codes. Among other sites, Wikipedia provides a [comprehensive list][wikipedia isocodes list].
3. Open enum [`Language`][language url] and add a new entry for your language. If the language is written
with a script that is not yet supported by *Lingua's* [`Alphabet`][alphabet url] enum, then add a new entry
for it there as well.
4. If your language's script contains characters that are completely unique to it, then add them to the
property tuples in the `Language` enum. However, if the characters occur in more
than one language **but** not in all languages, then add them to the
[`CHARS_TO_LANGUAGES_MAPPING`][chars to languages mapping url] constant instead.
5. Use [`LanguageModelFilesWriter`][language model files writer url] to create the language model files.
The training data file used for ngram probability estimation is not required to have a specific format
other than to be a valid txt file with UTF-8 encoding. Do **not** rename the language model files.
6. Use [`TestDataFilesWriter`][test data files writer url] to create the test data files used for
accuracy report generation. The input file from which to create the test data should have each
sentence on a separate line. Do **not** rename the test data files.
7. Create a new directory in [`/lingua/language-models`][language models directory url] named after the new
language's ISO 639-1 code and put the language model files into it.
8. Put the generated test data files in [`/language-testdata`][test data directory url].
9. Fix the existing unit tests by adding your new language.
10. For accuracy report generation, run `poetry run python3 scripts/accuracy_reporter.py`.
11. Be happy! :-) You have successfully contributed a new language and have thereby significantly widened
this library's fields of application.

[isocode639_1 url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/isocode.py#L19
[isocode639_3 url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/isocode.py#L261
[wikipedia isocodes list]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[language url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/language.py#L78
[alphabet url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/language.py#L29
[chars to languages mapping url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/_constant.py#L34
[language model files writer url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/writer.py#L26
[test data files writer url]: https://github.com/pemistahl/lingua-py/blob/main/lingua/writer.py#L144
[language models directory url]: https://github.com/pemistahl/lingua-py/tree/main/lingua/language-models
[test data directory url]: https://github.com/pemistahl/lingua-py/tree/main/language-testdata
