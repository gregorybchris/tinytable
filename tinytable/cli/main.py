import argparse
import os
import shutil

import pandas as pd

from tinytable.loaders.csv_loader import CsvLoader
from tinytable.loaders.hdf_loader import HdfLoader
from tinytable.loaders.pandas_pickle_loader import PandasPickleLoader
from tinytable.loaders.parquet_loader import ParquetLoader
from tinytable.loaders.pickle_loader import PickleLoader
from tinytable.serialization.serializer import Serializer
from tinytable.visualization.visualizer import Visualizer


COMMAND_RUN = 'run'
COMMAND_CLEAN = 'clean'
COMMAND_PLOT = 'plot'
CLI_COMMANDS = {COMMAND_RUN, COMMAND_CLEAN, COMMAND_PLOT}

RESULTS_FILENAME = 'results.csv'

DEFAULT_LOADER_MAP = {
    'pkl': PickleLoader,
    'pd_pkl': PandasPickleLoader,
    'hdf': HdfLoader,
    'parquet': ParquetLoader,
    'csv': CsvLoader,
}


def main():
    args = parse_args()

    if args.subcommand == COMMAND_RUN:
        run(args.dataset_path, args.experiments_dir, args.experiment_name,
            args.write, args.sample, args.trials)
    elif args.subcommand == COMMAND_CLEAN:
        clean(args.experiments_dir, args.experiment_name)
    elif args.subcommand == COMMAND_PLOT:
        plot(args.experiments_dir, args.experiment_name)


def run(dataset_path, experiments_dir, experiment_name,
        write, sample_fraction, trials):
    experiment_name = create_experiment_name(experiment_name, dataset_path)
    experiment_dir = os.path.join(experiments_dir, experiment_name)

    if os.path.exists(experiment_dir):
        raise ValueError(f"Experiment name must be unique: {experiment_name}")

    print(f"Running experiment: {experiment_name}")
    serializer = Serializer(DEFAULT_LOADER_MAP)

    results_df = serializer.serialize(dataset_path, n_trials=trials,
                                      sample_fraction=sample_fraction)

    print(results_df)

    if write:
        os.makedirs(experiment_dir)
        results_filepath = os.path.join(experiment_dir, RESULTS_FILENAME)
        results_df.to_csv(results_filepath)


def create_experiment_name(experiment_name, dataset_filepath):
    if experiment_name is not None:
        return experiment_name

    _, dataset_filename = os.path.split(dataset_filepath)
    dataset_name, _ = os.path.splitext(dataset_filename)
    return dataset_name


def clean(experiments_dir, experiment_name):
    experiment_dir = os.path.join(experiments_dir, experiment_name)
    if not os.path.exists(experiment_dir):
        raise ValueError(f"Couldn't find experiment {experiment_name} directory")

    # TODO: Add verification step to avoid accidental deletion
    shutil.rmtree(experiment_dir)
    print(f"Cleaned up experiment {experiment_name}")


def plot(experiments_dir, experiment_name):
    experiment_dir = os.path.join(experiments_dir, experiment_name)
    results_filepath = os.path.join(experiment_dir, RESULTS_FILENAME)

    if not os.path.exists(results_filepath):
        raise ValueError("Can't plot, couldn't find cached results")
    results_df = pd.read_csv(results_filepath)

    Visualizer.create_plots(experiment_dir, results_df)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiments_dir', default="experiments",
                        help="Path to directory to store experiments.")
    parser.add_argument('--experiment_name', '-e',
                        help="Experiment name (defaults to dataset name).")

    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    subparser_run = subparsers.add_parser(COMMAND_RUN)
    subparser_run.add_argument('--dataset_path', '-d', required=True,
                               help="Path to dataset.")
    subparser_run.add_argument('--no_write', dest='write',
                               default=True, action='store_false',
                               help="Don't write results to a file, only print.")
    subparser_run.add_argument('--sample', '-s', type=float,
                               help="Fraction of dataset to sample.")
    subparser_run.add_argument('--trials', '-t', default=1, type=int,
                               help="Number of trials to run.")

    subparser_clean = subparsers.add_parser(COMMAND_CLEAN)

    subparser_plot = subparsers.add_parser(COMMAND_PLOT)

    return parser.parse_args()
