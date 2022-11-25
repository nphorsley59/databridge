"""
Classes to write data to file.
Supported functionalities:
    dataframe -> .csv
"""

from abc import ABC, abstractmethod
from datetime import datetime
import os


class Writer(ABC):
    """Representation of basic writer object."""

    def __init__(self, data: object, fpath: str):
        """
        Initialize Writer instance.
        Args:
            data (object): Data to write to file.
            fpath (str): Absolute path to write to.
        """
        self.data = data
        self.fpath = fpath

    @abstractmethod
    def write_from_df(self):
        """Write dataframe to file at fpath."""
        raise NotImplementedError

    @abstractmethod
    def write_from_dict(self):
        """Write dictionary to file at fpath."""
        raise NotImplementedError

    def _get_versioned_fpath(self):
        """Get fpath with timestamp-versioned fname."""
        timestamp = str(datetime.now().strftime('%Y%m%d_%H%M%S'))
        return f'{os.path.splitext(self.fpath)[0]}' \
               f'--{timestamp}{os.path.splitext(self.fpath)[-1]}'


class CsvWriter(Writer):
    """Representation of CSV writer object."""

    def write_from_df(self, versioned: bool = False):
        """Write dataframe to CSV file at fpath.
        Args:
            versioned (bool): Write timestamp-versioned copy.
        """
        self.data.to_csv(self.fpath)
        if versioned:
            self.data.to_csv(self._get_versioned_fpath())

    def write_from_dict(self):
        """Write dictionary to CSV file at fpath."""
        raise AttributeError("Method not supported.")
