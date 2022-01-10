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

from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from .language import Language
from ._ngram import _get_ngram_name_by_length


def _load_json(language: Language, ngram_length: int) -> Optional[str]:
    ngram_name = _get_ngram_name_by_length(ngram_length)
    iso_code = language.iso_code_639_1.name.lower()
    relative_zip_file_path = f"./language-models/{iso_code}/{ngram_name}s.json.zip"
    absolute_zip_file_path = Path(__file__).parent / relative_zip_file_path
    json_file_name = f"{ngram_name}s.json"
    try:
        with ZipFile(absolute_zip_file_path) as zip_file:
            with zip_file.open(json_file_name) as json_file:
                return json_file.read().decode("utf-8")
    except FileNotFoundError:
        return None
