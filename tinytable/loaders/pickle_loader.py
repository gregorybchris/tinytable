import pickle

from tinytable.loaders.loader import Loader


class PickleLoader:
    @staticmethod
    def dump(df, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(df, f)

    @staticmethod
    def load(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
