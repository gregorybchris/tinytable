import os
import tempfile
import time

import pandas as pd

from tinytable.serialization.experiment_constants import *


class Serializer:
    def __init__(self, loaders=dict()):
        self._loaders = loaders

    def register_loader(self, name, loader_class):
        self._loaders[name] = loader_class

    def serialize(self, dataset_path, n_trials=1, sample_fraction=None):
        # TODO: Load many types of input files
        df = pd.read_csv(dataset_path)
        return self._run_serializations(df, n_trials, sample_fraction)

    def _run_serializations(self, df, n_trials, sample_fraction, show_result=False):
        if sample_fraction is not None:
            df = df.sample(frac=sample_fraction)

        results = []
        for trial in range(n_trials):
            for loader_name, loader_class in self._loaders.items():
                print(f"Benchmarking {loader_name}...")
                size, write, load = self._serialize_dataset(df, loader_class)
                metric_map = {
                    METRIC_FILE_SIZE: size,
                    METRIC_WRITE_TIME: write,
                    METRIC_LOAD_TIME: load
                }
                for metric, score in metric_map.items():
                    result = {COL_TRIAL: trial, COL_FILE_FORMAT: loader_name,
                              COL_METRIC: metric, COL_SCORE: score}
                    if show_result:
                        print(f"\tResult: {result}")
                    results.append(result)
        return pd.DataFrame(results)

    def _serialize_dataset(self, df, loader_class):
        with tempfile.TemporaryDirectory() as data_dir:
            filepath = os.path.join(data_dir, 'df_file')

            write_start_time = time.time()
            loader_class.dump(df, filepath)
            write_time = time.time() - write_start_time

            load_start_time = time.time()
            loader_class.load(filepath)
            load_time = time.time() - load_start_time

            file_size = os.path.getsize(filepath)

        return file_size, write_time, load_time
