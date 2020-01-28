import os
import tempfile
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns; sns.set()

import format_wrappers


RUN = 'run'
PLOT = 'plot'

EXPERIMENTS_DIR = 'experiments'
RESULTS_FILENAME = 'results.csv'


def benchmark_format(df, wrapper_class):
    with tempfile.TemporaryDirectory() as data_dir:
        filepath = os.path.join(data_dir, 'df_file')

        write_start_time = time.time()
        wrapper_class.write(filepath, df)
        write_time = time.time() - write_start_time

        load_start_time = time.time()
        wrapper_class.load(filepath)
        load_time = time.time() - load_start_time

        file_size = os.path.getsize(filepath)

    return file_size, write_time, load_time


def run_format_benchmarks(n_trials=1, sample_fraction=None):
    print("Benchmarking file formats...")
    wrapper_map = {
        'pkl': format_wrappers.PklWrapper,
        'pd_pkl': format_wrappers.PdPklWrapper,
        'hdf': format_wrappers.HdfWrapper,
        'parquet': format_wrappers.ParquetWrapper,
        'csv': format_wrappers.CsvWrapper,  # CSV is really slow
    }

    print("Pulling experiment data...")
    df = pd.read_parquet('data/experiments-classification-AUC_weighted.parquet')
    if sample_fraction is not None:
        df = df.sample(frac=sample_fraction)

    results = []
    for trial in range(n_trials):
        for file_format, format_wrapper in wrapper_map.items():
            print(f"Benchmarking {file_format}...")
            size, write, load = benchmark_format(df, format_wrapper)
            metric_map = {'file_size': size, 'write_time': write, 'load_time': load}
            for metric, score in metric_map.items():
                result = {'trial': trial, 'file_format': file_format,
                          'metric': metric, 'score': score}
                print(result)
                results.append(result)
    print("Done benchmarking.")
    return pd.DataFrame(results)


def plot_benchmarks(experiment_dir, benchmarks_df, show=False):
    metrics = ['file_size', 'write_time', 'load_time']
    titles = [column.replace('_', ' ').title() for column in metrics]
    filenames = [f'chart_{column}.png' for column in metrics]

    for metric, title, filename in zip(metrics, titles, filenames):
        metric_df = benchmarks_df[benchmarks_df['metric'] == metric]
        plot = sns.barplot(x='file_format', y='score', data=metric_df)
        plot.set_title(title)
        plot.set(xlabel='File Format', ylabel=title)
        if show:
            plt.show()
        filepath = os.path.join(experiment_dir, filename)
        plot.get_figure().savefig(filepath)
        plt.clf()  # Need to clear screen when plt.show() is not called


def setup_experiment(experiment_dir, experiment_name):
    if os.path.exists(experiment_dir):
        raise ValueError(f"Experiment name must be unique: {experiment_name}")
    os.makedirs(experiment_dir)


if __name__ == '__main__':
    task = PLOT
    experiment_name = 'full-with-csv'

    experiment_dir = os.path.join(EXPERIMENTS_DIR, experiment_name)
    results_filepath = os.path.join(experiment_dir, RESULTS_FILENAME)

    if task == RUN:
        sample_fraction = None
        n_trials = 1

        setup_experiment(experiment_dir, experiment_name)
        benchmarks_df = run_format_benchmarks(n_trials=n_trials, sample_fraction=sample_fraction)
        benchmarks_df.to_csv(results_filepath)
    elif task == PLOT:
        show_plots = False

        if not os.path.exists(results_filepath):
            raise ValueError("Can't plot, couldn't find cached results")
        benchmarks_df = pd.read_csv(results_filepath)
        plot_benchmarks(experiment_dir, benchmarks_df, show=show_plots)
    else:
        raise ValueError(f"Not a valid task: {task}")
