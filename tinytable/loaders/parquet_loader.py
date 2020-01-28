import pandas as pd

from tinytable.loaders.loader import Loader


class ParquetLoader(Loader):
    @staticmethod
    def dump(df, filepath):
        df.to_parquet(filepath)

    @staticmethod
    def load(filepath):
        return pd.read_parquet(filepath)
