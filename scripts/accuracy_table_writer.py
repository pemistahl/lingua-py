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

import math
import pandas as pd

from pathlib import Path


class AccuracyTableWriter:
    _columns = (
        "average-lingua",
        "average-langdetect",
        "average-langid",
        "average-cld3",
        "average-cld2",
        "single-words-lingua",
        "single-words-langdetect",
        "single-words-langid",
        "single-words-cld3",
        "single-words-cld2",
        "word-pairs-lingua",
        "word-pairs-langdetect",
        "word-pairs-langid",
        "word-pairs-cld3",
        "word-pairs-cld2",
        "sentences-lingua",
        "sentences-langdetect",
        "sentences-langid",
        "sentences-cld3",
        "sentences-cld2",
    )
    _table = """<table>
    <tr>
        <th>Language</th>
        <th colspan="5">Average</th>
        <th colspan="5">Single Words</th>
        <th colspan="5">Word Pairs</th>
        <th colspan="5">Sentences</th>
    </tr>
    <tr>
        <th></th>
        <th>Lingua</th>
        <th>Langdetect</th>
        <th>Langid</th>
        <th>&nbsp;&nbsp;CLD3&nbsp;&nbsp;</th>
        <th>&nbsp;&nbsp;CLD2&nbsp;&nbsp;</th>
        <th>Lingua</th>
        <th>Langdetect</th>
        <th>Langid</th>
        <th>&nbsp;&nbsp;CLD3&nbsp;&nbsp;</th>
        <th>&nbsp;&nbsp;CLD2&nbsp;&nbsp;</th>
        <th>Lingua</th>
        <th>Langdetect</th>
        <th>Langid</th>
        <th>&nbsp;&nbsp;CLD3&nbsp;&nbsp;</th>
        <th>&nbsp;&nbsp;CLD2&nbsp;&nbsp;</th>
        <th>Lingua</th>
        <th>Langdetect</th>
        <th>Langid</th>
        <th>&nbsp;&nbsp;CLD3&nbsp;&nbsp;</th>
        <th>&nbsp;&nbsp;CLD2&nbsp;&nbsp;</th>
    </tr>
    """

    def __init__(self, file_path):
        self._dataframe = self._read_into_dataframe(file_path)

    def write_accuracy_table(self, file_name):
        mean = self._dataframe.mean().round().astype(int)
        median = self._dataframe.median().round(2)
        std = self._dataframe.std().round(2)

        for language in self._dataframe.index:
            language_data = self._dataframe.loc[language]
            self._table += f"\t<tr>\n\t\t<td>{language}</td>\n"

            for column in self._columns:
                accuracy_value = language_data.loc[[column]][0]
                if not math.isnan(accuracy_value):
                    accuracy_value = int(round(accuracy_value))
                    accuracy_str = str(accuracy_value)
                else:
                    accuracy_str = "-"

                color = self._get_square_color(accuracy_value)
                self._table += (
                    f'\t\t<td><img src="images/{color}.png"> {accuracy_str}</td>\n'
                )

            self._table += "\t</tr>\n"

        self._table += '\t<tr>\n\t\t<td colspan="16"></td>\n\t</tr>\n'
        self._table += "\t<tr>\n\t\t<td><strong>Mean</strong></td>\n"

        for column in self._columns:
            accuracy_value = mean.loc[[column]][0]
            color = self._get_square_color(accuracy_value)
            self._table += f'\t\t<td><img src="images/{color}.png"> <strong>{accuracy_value}</strong></td>\n'

        self._table += "\t</tr>\n"
        self._table += '\t<tr>\n\t\t<td colspan="16"></td>\n\t</tr>\n'
        self._table += "\t<tr>\n\t\t<td>Median</td>\n"

        for column in self._columns:
            accuracy_value = median.loc[[column]][0]
            self._table += f"\t\t<td>{accuracy_value}</td>\n"

        self._table += "\t</tr>\n"
        self._table += "\t<tr>\n\t\t<td>Standard Deviation</td>\n"

        for column in self._columns:
            accuracy_value = std.loc[[column]][0]
            self._table += f"\t\t<td>{accuracy_value}</td>\n"

        self._table += "\t</tr>\n"
        self._table += "</table>"

        with open(
            Path(__file__).parent / f"../{file_name}", mode="w"
        ) as accuracy_table_file:
            accuracy_table_file.write(self._table)

    def _read_into_dataframe(self, file_path) -> pd.DataFrame:
        frame = pd.read_csv(filepath_or_buffer=file_path).set_index("language")
        return frame.reindex(sorted(frame.columns), axis=1)

    def _get_square_color(self, accuracy_value: float):
        if math.isnan(accuracy_value):
            return "grey"
        elif 0 <= accuracy_value <= 20:
            return "red"
        elif 21 <= accuracy_value <= 40:
            return "orange"
        elif 41 <= accuracy_value <= 60:
            return "yellow"
        elif 61 <= accuracy_value <= 80:
            return "lightgreen"
        elif 81 <= accuracy_value <= 100:
            return "green"
        else:
            raise ValueError("invalid accuracy value:", accuracy_value)


if __name__ == "__main__":
    file_path = (
        Path(__file__).parent / "../accuracy-reports/aggregated-accuracy-values.csv"
    )
    writer = AccuracyTableWriter(file_path)
    writer.write_accuracy_table(file_name="ACCURACY_TABLE.md")
    print("Accuracy table written successfully")
