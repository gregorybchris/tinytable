import pandas as pd

from tinytable.loaders.loader import Loader


class PandasPickleLoader(Loader):
    @staticmethod
    def dump(df, filepath):
        df.to_pickle(filepath)

    @staticmethod
    def load(filepath):
        return pd.read_pickle(filepath)
