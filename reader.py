"""
Classes to read file to data.
Supported funcationalities:
    .csv -> dataframe
"""

from abc import ABC, abstractmethod
import os

import pandas as pd


class Reader(ABC):
    """Representation of a basic reader object."""

    def __init__(self, fpath: str):
        """
        Initialize Reader instance.
        Args:
            fpath (str): Absolute path to read from.
        """
        self.fpath = fpath
        self.extension = self._get_extension()

    @abstractmethod
    def read_to_df(self):
        """Read file at fpath to dataframe."""
        raise NotImplementedError

    @abstractmethod
    def read_to_text(self):
        """Read file at fpath to text."""
        raise NotImplementedError

    def _get_extension(self) -> str:
        """Get extension from fpath."""
        return os.path.splitext(self.fpath)


class CsvReader(Reader):
    """Representation of a CSV reader object."""

    def read_to_df(self) -> pd.DataFrame:
        """Read CSV file at fpath to dataframe."""
        return pd.read_csv(self.fpath)

    def read_to_text(self):
        """Read CSV file at fpath to text; not supported."""
        raise AttributeError("Method not supported.")
