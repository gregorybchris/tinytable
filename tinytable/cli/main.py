import argparse

from tinytable.loaders.csv_loader import CsvLoader
from tinytable.loaders.hdf_loader import HdfLoader
from tinytable.loaders.pandas_pickle_loader import PandasPickleLoader
from tinytable.loaders.parquet_loader import ParquetLoader
from tinytable.loaders.pickle_loader import PickleLoader
from tinytable.serialization.serializer import Serializer


COMMAND_RUN = 'run'
COMMAND_PLOT = 'plot'
COMMAND_GEN = 'gen'
CLI_COMMANDS = {COMMAND_RUN, COMMAND_PLOT, COMMAND_GEN}


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
        run(args.dataset, args.experiment_name,
            args.experiments_dir, args.write, args.sample, args.trials)
    elif args.subcommand == COMMAND_PLOT:
        plot()
    elif args.subcommand == COMMAND_GEN:
        gen()


def run(dataset_path, experiments_dir, experiment_name, write, sample_fraction, trials):
    serializer = Serializer(experiments_dir)
    serializer.register_loaders(DEFAULT_LOADER_MAP)

    results_df = serializer.serialize(dataset_path, experiment_name,
                                      n_trials=trials, sample_fraction=sample_fraction)
    print(results_df)


def plot():
    raise NotImplementedError


def gen():
    raise NotImplementedError


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--experiments_dir', default="experiments",
                        help="Path to directory to store experiments.")
    parser.add_argument('--experiment_name', '--exp',
                        help="Experiment name (defaults to dataset name).")

    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    subparser_run = subparsers.add_parser(COMMAND_RUN)
    subparser_run.add_argument('--dataset', required=True,
                               help="Path to dataset.")
    subparser_run.add_argument('--no_write', dest='write',
                               default=True, action='store_false',
                               help="Don't write results to a file, only print.")
    subparser_run.add_argument('--sample', type=float,
                               help="Fraction of dataset to sample.")
    subparser_run.add_argument('--trials', default=1,
                               help="Number of trials to run.")

    subparser_plot = subparsers.add_parser(COMMAND_PLOT)

    subparser_gen = subparsers.add_parser(COMMAND_GEN)

    args = parser.parse_args()

    return args


# def setup_experiment(experiment_dir, experiment_name):
#     if os.path.exists(experiment_dir):
#         raise ValueError(f"Experiment name must be unique: {experiment_name}")
#     os.makedirs(experiment_dir)

# if __name__ == '__main__':
#     task = PLOT
#     experiment_name = 'full-with-csv'

#     experiment_dir = os.path.join(EXPERIMENTS_DIR, experiment_name)
#     results_filepath = os.path.join(experiment_dir, RESULTS_FILENAME)

#     if task == RUN:
#         sample_fraction = None
#         n_trials = 1

#         setup_experiment(experiment_dir, experiment_name)
#         benchmarks_df = run_format_benchmarks(n_trials=n_trials, sample_fraction=sample_fraction)
#         benchmarks_df.to_csv(results_filepath)
#     elif task == PLOT:
#         show_plots = False

#         if not os.path.exists(results_filepath):
#             raise ValueError("Can't plot, couldn't find cached results")
#         benchmarks_df = pd.read_csv(results_filepath)
#         plot_benchmarks(experiment_dir, benchmarks_df, show=show_plots)
#     else:
#         raise ValueError(f"Not a valid task: {task}")
