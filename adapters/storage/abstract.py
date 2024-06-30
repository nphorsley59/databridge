
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Union

import pandas as pd

from adapters.storage.enum import FileType


class Storage(ABC):
    def __init__(self):
        pass

    def _get_csv_reader(self):
        def read_csv_file(fpath: Path, data_structure, **kwargs):
            if data_structure is pd.DataFrame:
                return pd.read_csv(fpath, **kwargs)
        return read_csv_file
    
    @staticmethod
    def _get_csv_writer():
        def write_csv_file(obj, fpath: Path, **kwargs):
            if isinstance(obj, pd.DataFrame):
                return obj.to_csv(fpath, index=False, **kwargs)
        return write_csv_file
    
    def _get_reader_callable(self, fpath: Path) -> Callable:
        filetype = FileType(fpath.suffix)
        if filetype == FileType.CSV:
            return self._get_csv_reader()

    def _get_writer_callable(self, fpath: Path) -> Callable:
        filetype = FileType(fpath.suffix)
        if filetype == FileType.CSV:
            return self._get_csv_writer()
    
    @abstractmethod
    def file_exists(self, fpath: Union[Path, str]):
        raise NotImplementedError("Subclasses must implement file_exists().")

    @abstractmethod
    def read_file(self, fpath: Union[Path, str], data_structure = pd.DataFrame, reader: Callable = None, **kwargs):
        raise NotImplementedError("Subclasses must implement read_file().")

    @abstractmethod
    def write_file(self, obj, fpath: Union[Path, str], writer: Callable = None, **kwargs):
        raise NotImplementedError("Subclasses must implement write_file().")
