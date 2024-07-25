from abc import ABC, abstractmethod
from pathlib import Path


class Storage(ABC):
    def __init__(self):
        pass

    def _format_fpath(self, fpath):
        if isinstance(fpath, Path):
            fpath = str(fpath)
        if not isinstance(fpath, str):
            raise TypeError("File path must be Path or str.")
        return fpath

    @abstractmethod
    def _read(
        self,
        fpath,
        **kwargs,
    ):
        raise NotImplementedError("Subclasses must implement _read_file().")

    @abstractmethod
    def _write(
        self,
        obj,
        fpath,
        **kwargs,
    ):
        raise NotImplementedError("Subclasses must implement _write_file().")

    def read(
        self,
        fpath,
        **kwargs,
    ):
        fpath = self._format_fpath(fpath=fpath)
        return self._read(fpath=fpath, **kwargs)

    def write(
        self,
        obj,
        fpath,
        **kwargs,
    ):
        fpath = self._format_fpath(fpath=fpath)
        self._write(obj=obj, fpath=fpath, **kwargs)

    @abstractmethod
    def exists(self, fpath):
        raise NotImplementedError("Subclasses must implement exists().")

    @abstractmethod
    def delete(self,fpath):
        raise NotImplementedError("Subclasses must implement delete().")
