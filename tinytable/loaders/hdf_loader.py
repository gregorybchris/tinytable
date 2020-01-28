import pandas as pd

from tinytable.loaders.loader import Loader


class HdfLoader(Loader):
    @staticmethod
    def dump(df, filepath):
        df.to_hdf(filepath, key='df')

    @staticmethod
    def load(filepath):
        return pd.read_hdf(filepath)
