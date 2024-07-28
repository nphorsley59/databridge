import os
from typing import Callable

from databridge.storage._abstract import Storage


class LocalStorage(Storage):

    def _read(
        self,
        fpath: str,
        reader: Callable = None,
        **kwargs,
    ):
        reader = reader or self._get_reader_callable(fpath=fpath)
        return reader(fpath=fpath, **kwargs)

    def _write(
        self,
        obj,
        fpath: str,
        writer: Callable = None,
        **kwargs,
    ):
        writer = writer or self._get_writer_callable(fpath=fpath)
        return writer(obj=obj, fpath=fpath, **kwargs)

    def exists(self, fpath):
        fpath = self._format_fpath(fpath=fpath)
        return os.path.exists(fpath)

    def delete(self, fpath):
        if not os.path.isfile(fpath):
            raise FileNotFoundError(f"No such file: '{fpath}'")
        os.remove(fpath)
