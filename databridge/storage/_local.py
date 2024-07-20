import os
from pathlib import Path
from typing import Callable, Union

from databridge.storage._abstract import Storage


class LocalStorage(Storage):
    def _format_fpath(self, fpath: Union[Path, str]):
        if isinstance(fpath, Path):
            fpath = str(fpath)
        if not isinstance(fpath, str):
            raise TypeError("File path must be Path or str.")
        return fpath

    def _read(
        self,
        fpath: str,
        reader: Callable,
        **kwargs,
    ):
        reader = reader or self._get_reader_callable(fpath=fpath)
        return reader(fpath=fpath, **kwargs)

    def _write(
        self,
        obj,
        fpath: str,
        writer: Callable,
        **kwargs,
    ):
        writer = writer or self._get_writer_callable(fpath=fpath)
        return writer(obj=obj, fpath=fpath, **kwargs)

    def exists(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        return os.path.exists(fpath)
