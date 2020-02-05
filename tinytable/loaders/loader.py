from abc import ABC, abstractmethod


class Loader(ABC):
    @staticmethod
    @abstractmethod
    def load(filepath):
        """
        Load a data object from a file.

        :param filepath: Input filepath.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def dump(o, filepath):
        """
        Dump a data object to a file.

        :param o: Data object.
        :param filepath: Output filepath.
        """
        raise NotImplementedError()
