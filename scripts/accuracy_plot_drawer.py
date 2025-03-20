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

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from lingua import Language
from math import floor
from matplotlib.patches import Patch
from pathlib import Path

matplotlib.use("TkAgg")
sns.set()
sns.set_style("whitegrid")


class AccuracyPlotDrawer:
    _dpi = 40
    _ticks_fontsize = 35
    _label_fontsize = 38
    _title_fontsize = 45
    _fontweight = "bold"
    _hue = "classifier"
    _grid_color = "#474747"
    _column_labels = {
        "cld2": "CLD 2",
        "cld3": "CLD 3",
        "langdetect": "Langdetect 1.0.9",
        "langid": "Langid 1.1.6",
        "lingua-low-accuracy": "Lingua 2.1.0\nlow accuracy mode",
        "lingua-high-accuracy": "Lingua 2.1.0\nhigh accuracy mode",
        "lingua-single-language-detector": "Lingua 2.1.0\nsingle language mode",
        "simplemma": "Simplemma 0.9.1",
    }
    _single_language_mode_columns = [
        f"lingua-{language.name.lower()}-detector" for language in Language
    ]
    _hatches = ("x", "+", "\\", "o", "oo", ".", "*", "O")
    _palette = (
        "#b259ff",
        "#ff6347",
        "#ff8800",
        "#ffb866",
        "#ffc400",
        "#fff480",
        "#8edca7",
        "#41c46b",
    )
    _ticks = np.arange(0, 101, 10)

    def __init__(self, plot_title: str, report_file_path: Path):
        self._plot_title = plot_title
        self._dataframe = self._read_into_dataframe(report_file_path)

    def _read_into_dataframe(self, report_file_path: Path) -> pd.DataFrame:
        df = pd.read_csv(report_file_path, index_col="language")

        merged_single_language_mode_column = {
            "lingua-single-language-detector": df[
                self._single_language_mode_columns
            ].mean(axis="columns")
        }

        df = df.assign(**merged_single_language_mode_column)

        # Sort classifier columns by their mean value
        df = df.reindex(df.mean().sort_values().index, axis="columns")

        return pd.melt(
            frame=df.reset_index(),
            id_vars="language",
            value_name="accuracy",
            var_name=self._hue,
        )

    def draw_barplot(self, file_path: Path):
        column_labels = self._column_labels.copy()
        del column_labels["lingua-single-language-detector"]
        row_filter = self._dataframe[self._hue].isin(column_labels.keys())
        data = self._dataframe[row_filter]
        classifiers = data[self._hue].unique()
        labels = [column_labels[classifier] for classifier in classifiers]
        handles = [
            Patch(facecolor=color, edgecolor="black", label=label, hatch=hatch)
            for color, label, hatch in zip(self._palette, labels, self._hatches)
        ]

        plt.figure(figsize=(16, 175))
        plt.title(
            self._plot_title + "\n",
            fontsize=self._title_fontsize,
            fontweight=self._fontweight,
        )
        plt.xticks(fontsize=self._ticks_fontsize, ticks=self._ticks)
        plt.yticks(fontsize=self._ticks_fontsize)
        plt.grid(color=self._grid_color)

        axes = sns.barplot(
            data=data, x="accuracy", y="language", hue=self._hue, palette=self._palette
        )

        axes.set_xlabel(
            "Accuracy (%)\n", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        axes.set_ylabel(
            "Language", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        axes.set_xlim((0, 100))
        axes.xaxis.tick_top()
        axes.xaxis.set_label_position("top")
        axes.tick_params(axis="both", which="major", labelsize=self._label_fontsize)
        axes.tick_params(axis="both", which="minor", labelsize=self._label_fontsize)
        axes.legend(handles=handles, fontsize=28, loc="upper left")

        language_count = len(axes.patches) / len(self._column_labels)
        for i, current_bar in enumerate(axes.patches):
            current_bar.set_edgecolor(self._grid_color)
            current_bar.set_hatch(self._hatches[floor(i / language_count)])

        plt.tight_layout()
        plt.savefig(file_path, dpi=self._dpi)

    def draw_boxplot(self, file_path: Path):
        row_filter = self._dataframe[self._hue].isin(self._column_labels.keys())
        data = self._dataframe[row_filter]
        classifiers = data[self._hue].unique()
        labels = [self._column_labels[classifier] for classifier in classifiers]

        plt.figure(figsize=(20, 20))
        plt.title(
            self._plot_title + "\n",
            fontsize=self._title_fontsize,
            fontweight=self._fontweight,
        )
        plt.xticks(fontsize=self._ticks_fontsize, ticks=self._ticks)
        plt.yticks(fontsize=self._ticks_fontsize)
        plt.grid(color=self._grid_color)

        axes = sns.boxplot(
            data=data,
            x="accuracy",
            hue="classifier",
            y="classifier",
            linewidth=5,
            palette=self._palette,
            legend=False,
        )

        axes.set_xlim((0, 100))
        axes.xaxis.tick_top()
        axes.xaxis.set_label_position("top")
        axes.tick_params(axis="both", which="major", labelsize=self._label_fontsize)
        axes.tick_params(axis="both", which="minor", labelsize=self._label_fontsize)
        axes.set_ylabel(
            "Classifier", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        axes.set_xlabel(
            "Accuracy (%)\n", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        # set_yticklabels should only be called after set_yticks
        axes.set_yticks(axes.get_yticks())
        axes.set_yticklabels(labels)

        plt.tight_layout()
        plt.savefig(file_path, dpi=self._dpi)

    def draw_single_language_mode_boxplot(self, file_path: Path):
        row_filter = self._dataframe[self._hue].isin(self._single_language_mode_columns)
        data = self._dataframe[row_filter].sort_values(by=self._hue)
        classifiers = data[self._hue].unique()
        labels = [classifier.split("-")[1].title() for classifier in classifiers]

        plt.figure(figsize=(20, 150))
        plt.title(
            self._plot_title + "\nSingle Language Mode\n",
            fontsize=self._title_fontsize,
            fontweight=self._fontweight,
        )
        plt.xticks(fontsize=self._ticks_fontsize, ticks=self._ticks)
        plt.yticks(fontsize=self._ticks_fontsize)
        plt.grid(color=self._grid_color)

        axes = sns.boxplot(
            data=data,
            x="accuracy",
            hue="classifier",
            y="classifier",
            linewidth=5,
            legend=False,
        )

        axes.set_xlim((0, 100))
        axes.xaxis.tick_top()
        axes.xaxis.set_label_position("top")
        axes.tick_params(axis="both", which="major", labelsize=self._label_fontsize)
        axes.tick_params(axis="both", which="minor", labelsize=self._label_fontsize)
        axes.set_ylabel(
            "Classifier", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        axes.set_xlabel(
            "Accuracy (%)\n", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        # set_yticklabels should only be called after set_yticks
        axes.set_yticks(axes.get_yticks())
        axes.set_yticklabels(labels)

        plt.tight_layout()
        plt.savefig(file_path, dpi=self._dpi)


if __name__ == "__main__":
    report_directory_path = Path(__file__).parent / "../accuracy-reports"
    plot_directory_path = Path(__file__).parent / "../images/plots"
    prefixes = ("average", "single-words", "word-pairs", "sentences")

    for prefix in prefixes:
        plot_title = prefix.title().replace("-", " ")
        drawer = AccuracyPlotDrawer(
            plot_title=f"{plot_title} Detection Performance",
            report_file_path=report_directory_path / f"{prefix}-accuracy-values.csv",
        )
        drawer.draw_barplot(file_path=plot_directory_path / f"barplot-{prefix}.png")
        drawer.draw_boxplot(file_path=plot_directory_path / f"boxplot-{prefix}.png")
        drawer.draw_single_language_mode_boxplot(
            file_path=plot_directory_path / f"boxplot-single-language-mode-{prefix}.png"
        )

    print("All plots created successfully")
