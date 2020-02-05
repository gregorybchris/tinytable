import matplotlib.pyplot as plt

import seaborn as sns

from tinytable.serialization.experiment_constants import *


class Visualizer:
    def __init__(self):
        sns.set()

    def plot_benchmarks(self, experiment_dir, benchmarks_df, show=False):
        metrics = [METRIC_FILE_SIZE, METRIC_WRITE_TIME, METRIC_LOAD_TIME]
        titles = [metric.replace('_', ' ').title() for metric in metrics]
        filenames = [f'chart_{metric}.png' for metric in metrics]

        for metric, title, filename in zip(metrics, titles, filenames):
            metric_df = benchmarks_df[benchmarks_df[COL_METRIC] == metric]
            plot = sns.barplot(x=COL_FILE_FORMAT, y=COL_SCORE, data=metric_df)
            plot.set_title(title)
            plot.set(xlabel='File Format', ylabel=title)
            if show:
                plt.show()
            filepath = os.path.join(experiment_dir, filename)
            plot.get_figure().savefig(filepath)
            plt.clf()  # Need to clear screen when plt.show() is not called
