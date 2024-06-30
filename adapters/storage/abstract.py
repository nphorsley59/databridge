
from abc import ABC, abstractmethod
from typing import Callable

import pandas as pd

from adapters.storage.enum import FileType


class Storage(ABC):
    def __init__(self):
        pass

    def _get_csv_reader(self):
        def read_csv_file(fpath: str, **kwargs):
            return pd.read_csv(fpath, **kwargs)
        return read_csv_file
    
    @staticmethod
    def _get_csv_writer():
        def write_csv_file(obj, fpath: str, **kwargs):
            return obj.to_csv(fpath, index=False, **kwargs)
        return write_csv_file
    
    def _get_reader_callable(self, fpath: str) -> Callable:
        suffix = fpath.split('.')[-1]
        filetype = FileType(suffix)
        if filetype == FileType.CSV:
            return self._get_csv_reader()

    def _get_writer_callable(self, fpath: str) -> Callable:
        suffix = fpath.split('.')[-1]
        filetype = FileType(suffix)
        if filetype == FileType.CSV:
            return self._get_csv_writer()

    @abstractmethod
    def _format_fpath(self, fpath):
        raise NotImplementedError("Subclasses must implement _format_fpath().")

    @abstractmethod
    def _read(
            self, 
            fpath, 
            reader: Callable, 
            **kwargs,
    ):
        raise NotImplementedError("Subclasses must implement _read_file().")

    @abstractmethod
    def _write(
            self, 
            obj, 
            fpath,
            writer: Callable,
            **kwargs,
    ):
        raise NotImplementedError("Subclasses must implement _write_file().")

    def read(
            self, 
            fpath, 
            reader: Callable = None, 
            **kwargs,
    ):
        fpath = self._format_fpath(fpath=fpath)
        return self._read(fpath=fpath, reader=reader, **kwargs)

    def write(
            self, 
            obj, 
            fpath,
            writer: Callable = None,
            **kwargs,
    ):
        fpath = self._format_fpath(fpath=fpath)
        self._write(obj=obj, fpath=fpath, writer=writer, **kwargs)
    
    @abstractmethod
    def exists(self, fpath):
        raise NotImplementedError("Subclasses must implement exists().")
