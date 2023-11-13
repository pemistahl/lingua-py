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
    _plot_filepath = Path(__file__).parent / "../images/plots/"
    _plot_titles = ("Single Word", "Word Pair", "Sentence", "Average")
    _plot_title_suffix = "Detection Performance"
    _column_prefixes = ("single-words", "word-pairs", "sentences", "average")
    _column_suffixes = (
        "simplemma",
        "cld2",
        "cld3",
        "langid",
        "fasttext",
        "langdetect",
        "lingua-low",
        "lingua-high",
    )
    _legend_labels = (
        "Simplemma 0.9.1",
        "CLD 2",
        "CLD 3",
        "langid 1.1.6",
        "fastText 0.9.2",
        "langdetect 1.0.9",
        "Lingua 1.3.3\nlow accuracy mode",
        "Lingua 1.3.3\nhigh accuracy mode",
    )
    _hatches = ("|", "-", "/", "x", "+", ".", "*", "O")
    _palette = (
        "#39d7e6",
        "#6bbcff",
        "#347deb",
        "#b259ff",
        "#ff6347",
        "#ff8800",
        "#ffc400",
        "#41c46b",
    )
    _ticks = np.arange(0, 101, 10)
    _legend_handles = [
        Patch(facecolor=color, edgecolor="black", label=label, hatch=hatch)
        for color, label, hatch in zip(_palette, _legend_labels, _hatches)
    ]

    def __init__(self, file_path):
        self._dataframe = self._read_into_dataframe(file_path)

    def draw_all_barplots(self):
        for title, prefix in zip(self._plot_titles, self._column_prefixes):
            suffixed_title = f"{title} {self._plot_title_suffix}"
            columns = [f"{prefix}-{suffix}" for suffix in self._column_suffixes]
            self._draw_barplot(
                columns,
                suffixed_title,
                xlim=(0, 100),
                filename=f"barplot-{prefix}.png",
            )

    def draw_all_boxplots(self):
        for title, prefix in zip(self._plot_titles, self._column_prefixes):
            suffixed_title = f"{title} {self._plot_title_suffix}"
            columns = [f"{prefix}-{suffix}" for suffix in self._column_suffixes]
            self._draw_boxplot(
                columns,
                suffixed_title,
                ylim=(0, 100),
                filename=f"boxplot-{prefix}.png",
            )

    def _read_into_dataframe(self, file_path):
        frame = pd.read_csv(filepath_or_buffer=file_path)
        return pd.melt(
            frame=frame, id_vars="language", value_name="accuracy", var_name=self._hue
        )

    def _draw_barplot(self, columns, title, xlim, filename):
        row_filter = self._dataframe[self._hue].isin(columns)
        data = self._dataframe[row_filter]

        plt.figure(figsize=(16, 180))
        plt.title(
            title + "\n", fontsize=self._title_fontsize, fontweight=self._fontweight
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
        axes.set_xlim(xlim)
        axes.xaxis.tick_top()
        axes.xaxis.set_label_position("top")
        axes.tick_params(axis="both", which="major", labelsize=self._label_fontsize)
        axes.tick_params(axis="both", which="minor", labelsize=self._label_fontsize)
        axes.legend(handles=self._legend_handles, fontsize=28, loc="upper left")

        language_count = len(axes.patches) / len(self._legend_labels)
        for i, current_bar in enumerate(axes.patches):
            current_bar.set_edgecolor(self._grid_color)
            current_bar.set_hatch(self._hatches[floor(i / language_count)])

        plt.tight_layout()
        plt.savefig(self._plot_filepath / filename, dpi=self._dpi)

    def _draw_boxplot(self, columns, title, ylim, filename):
        row_filter = self._dataframe[self._hue].isin(columns)
        data = self._dataframe[row_filter]

        plt.figure(figsize=(40, 12))
        plt.title(title, fontsize=self._title_fontsize, fontweight=self._fontweight)
        plt.xticks(fontsize=self._ticks_fontsize)
        plt.yticks(fontsize=self._ticks_fontsize, ticks=self._ticks)
        plt.grid(self._grid_color)

        axes = sns.boxplot(
            data=data,
            x="classifier",
            hue="classifier",
            y="accuracy",
            linewidth=5,
            palette=self._palette,
            legend=False,
        )

        axes.set_ylim(ylim)
        axes.set_xlabel(
            "Classifier", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        axes.set_ylabel(
            "Accuracy (%)", fontsize=self._label_fontsize, fontweight=self._fontweight
        )
        # set_xticklabels should only be called after set_xticks
        axes.set_xticks(axes.get_xticks())
        axes.set_xticklabels(self._legend_labels)

        plt.tight_layout()
        plt.savefig(self._plot_filepath / filename, dpi=self._dpi)


if __name__ == "__main__":
    file_path = (
        Path(__file__).parent / "../accuracy-reports/aggregated-accuracy-values.csv"
    )
    drawer = AccuracyPlotDrawer(file_path)
    drawer.draw_all_barplots()
    drawer.draw_all_boxplots()
    print("All plots created successfully")
