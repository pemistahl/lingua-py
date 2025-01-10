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

import math
import pandas as pd

from lingua import Language
from pathlib import Path


class AccuracyTableWriter:
    _column_labels = {
        "cld2": "&nbsp;&nbsp;CLD2&nbsp;&nbsp;",
        "cld3": "&nbsp;&nbsp;CLD3&nbsp;&nbsp;",
        "langdetect": "Langdetect",
        "langid": "Langid",
        "lingua-low-accuracy": "Lingua<br>(low accuracy mode)",
        "lingua-high-accuracy": "Lingua<br>(high accuracy mode)",
        "lingua-single-language-detector": "Lingua<br>(single language mode)",
        "simplemma": "Simplemma",
    }

    def __init__(self, table_title: str, report_file_path: Path):
        self._table_title = table_title
        self._dataframe = self._read_into_dataframe(report_file_path)

    def write_accuracy_table(self, file_path: Path):
        mean = self._dataframe.mean().round()
        median = self._dataframe.median().round(2)
        std = self._dataframe.std().round(2)

        colspan = len(self._column_labels)
        table = f"""<table>
    <tr>
        <th>Language</th>
        <th colspan="{colspan}">{self._table_title}</th>
    </tr>
    <tr>
        <th></th>
    """

        for column_label in self._column_labels.values():
            table += f"    <th>{column_label}</th>\n    "

        table += "</tr>\n    <tr>\n"

        for language in self._dataframe.index:
            language_data = self._dataframe.loc[language]
            table += f"        <td>{language}</td>\n"

            for column in self._column_labels.keys():
                accuracy_value = language_data.loc[[column]].iloc[0]
                if not math.isnan(accuracy_value):
                    accuracy_value = int(round(accuracy_value))
                    accuracy_str = str(accuracy_value)
                else:
                    accuracy_str = "-"

                color = self._get_square_color(accuracy_value)
                table += f'        <td><img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/{color}.png"> {accuracy_str}</td>\n'

            table += "    </tr>\n"

        table += f'    <tr>\n        <td colspan="{colspan}"></td>\n    </tr>\n'
        table += "    <tr>\n        <td><strong>Mean</strong></td>\n"

        for column in self._column_labels.keys():
            accuracy_value = mean.loc[[column]].iloc[0]
            color = self._get_square_color(accuracy_value)
            table += f'        <td><img src="https://raw.githubusercontent.com/pemistahl/lingua-py/pure-python-impl/images/{color}.png"> <strong>{accuracy_value}</strong></td>\n'

        table += "    </tr>\n"
        table += f'    <tr>\n        <td colspan="{colspan}"></td>\n    </tr>\n'
        table += "    <tr>\n        <td>Median</td>\n"

        for column in self._column_labels.keys():
            accuracy_value = median.loc[[column]].iloc[0]
            table += f"        <td>{accuracy_value}</td>\n"

        table += "    </tr>\n"
        table += "    <tr>\n        <td>Standard Deviation</td>\n"

        for column in self._column_labels.keys():
            accuracy_value = std.loc[[column]].iloc[0]
            table += f"        <td>{accuracy_value}</td>\n"

        table += "    </tr>\n"
        table += "</table>"

        with open(file_path, mode="w") as accuracy_table_file:
            accuracy_table_file.write(table)

    def _read_into_dataframe(self, report_file_path: Path) -> pd.DataFrame:
        df = pd.read_csv(report_file_path, index_col="language")

        single_language_mode_columns = [
            f"lingua-{language.name.lower()}-detector" for language in Language
        ]
        merged_single_language_mode_column = {
            "lingua-single-language-detector": df[single_language_mode_columns].mean(
                axis="columns"
            )
        }
        df = df.assign(**merged_single_language_mode_column).drop(
            single_language_mode_columns, axis="columns"
        )

        return df

    def _get_square_color(self, accuracy_value: float) -> str:
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
    report_directory_path = Path(__file__).parent / "../accuracy-reports"
    table_directory_path = Path(__file__).parent / "../tables"
    prefixes = ("average", "single-words", "word-pairs", "sentences")

    for prefix in prefixes:
        table_title = prefix.title().replace("-", " ")
        table_file_name = prefix.upper().replace("-", "_")
        writer = AccuracyTableWriter(
            table_title=f"{table_title} Detection Performance",
            report_file_path=report_directory_path / f"{prefix}-accuracy-values.csv",
        )
        writer.write_accuracy_table(
            file_path=table_directory_path / f"{table_file_name}_ACCURACY_TABLE.md"
        )

    print("All accuracy tables created successfully")
