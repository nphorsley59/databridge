from abc import ABC, abstractmethod

import pandas as pd


class Reader(ABC):
    """Representation of a basic reader object."""

    def __init__(self, fpath: str):
        """
        Initialize Reader instance.
        Args:
            fpath (str): Absolute path to file location.
        """
        self.fpath = fpath

    @abstractmethod
    def read_file(self):
        """Reader file at fpath."""
        raise NotImplementedException


class CsvReader(Reader):
    """Representation of a CSV reader object."""

    def read_file(self) -> pd.DataFrame:
        """Read CSV file at fpath."""
        return pd.read_csv(self.fpath)
