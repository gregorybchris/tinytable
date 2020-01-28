import pandas as pd

from tinytable.loaders.loader import Loader


class CsvLoader(Loader):
    @staticmethod
    def dump(df, filepath):
        df.to_csv(filepath)

    @staticmethod
    def load(filepath):
        return pd.read_csv(filepath)
