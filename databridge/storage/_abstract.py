from abc import ABC, abstractmethod
import json
from typing import Callable

import pandas as pd

from databridge.storage._enum import FileType


class Storage(ABC):
    def __init__(self):
        pass

    @staticmethod
    def _get_csv_reader() -> Callable:
        def read_csv_file(fpath: str, **kwargs):
            return pd.read_csv(fpath, **kwargs)

        return read_csv_file

    @staticmethod
    def _get_csv_writer() -> Callable:
        def write_csv_file(obj, fpath: str, **kwargs):
            return obj.to_csv(fpath, index=False, **kwargs)

        return write_csv_file

    @staticmethod
    def _get_parquet_reader() -> Callable:
        def read_parquet_file(fpath: str, **kwargs) -> pd.DataFrame:
            return pd.read_parquet(fpath, **kwargs)

        return read_parquet_file

    @staticmethod
    def _get_parquet_writer() -> Callable:
        def write_parquet_file(obj: pd.DataFrame, fpath: str, **kwargs) -> None:
            obj.to_parquet(fpath, index=False, **kwargs)

        return write_parquet_file

    @staticmethod
    def _get_excel_reader() -> Callable:
        def read_excel_file(fpath: str, **kwargs) -> pd.DataFrame:
            return pd.read_excel(fpath, **kwargs)

        return read_excel_file

    @staticmethod
    def _get_excel_writer() -> Callable:
        def write_excel_file(obj: pd.DataFrame, fpath: str, **kwargs) -> None:
            obj.to_excel(fpath, index=False, **kwargs)

        return write_excel_file

    @staticmethod
    def _get_json_reader() -> Callable:
        def read_json_file(fpath: str, **kwargs):
            with open(fpath, "r", **kwargs) as file:
                return json.load(file, **kwargs)

        return read_json_file

    @staticmethod
    def _get_json_writer() -> Callable:
        def write_json_file(obj, fpath: str, **kwargs):
            with open(fpath, "w", **kwargs) as file:
                json.dump(obj, file, indent=4, **kwargs)

        return write_json_file

    @staticmethod
    def _get_txt_reader() -> Callable:
        def read_txt_file(fpath: str, **kwargs):
            with open(fpath, "r", **kwargs) as file:
                return file.read()

        return read_txt_file

    @staticmethod
    def _get_txt_writer() -> Callable:
        def write_txt_file(obj: str, fpath: str, **kwargs):
            with open(fpath, "w", **kwargs) as file:
                file.write(obj)

        return write_txt_file

    @staticmethod
    def _get_xml_reader() -> Callable:
        def read_xml_file(fpath: str, **kwargs) -> pd.DataFrame:
            return pd.read_xml(fpath, **kwargs)

        return read_xml_file

    @staticmethod
    def _get_xml_writer() -> Callable:
        def write_xml_file(obj: pd.DataFrame, fpath: str, **kwargs) -> None:
            obj.to_xml(fpath, index=False, **kwargs)

        return write_xml_file

    def _get_reader_callable(self, fpath: str) -> Callable:
        suffix = fpath.split(".")[-1]
        filetype = FileType(suffix)
        if filetype == FileType.CSV:
            return self._get_csv_reader()
        if filetype == FileType.JSON:
            return self._get_json_reader()
        if filetype == FileType.TXT:
            return self._get_txt_reader()
        if filetype == FileType.XLSX:
            return self._get_excel_reader()
        if filetype == FileType.PARQUET:
            return self._get_parquet_reader()
        if filetype == FileType.XML:
            return self._get_xml_reader()

    def _get_writer_callable(self, fpath: str) -> Callable:
        suffix = fpath.split(".")[-1]
        filetype = FileType(suffix)
        if filetype == FileType.CSV:
            return self._get_csv_writer()
        if filetype == FileType.JSON:
            return self._get_json_writer()
        if filetype == FileType.TXT:
            return self._get_txt_writer()
        if filetype == FileType.XLSX:
            return self._get_excel_writer()
        if filetype == FileType.PARQUET:
            return self._get_parquet_writer()
        if filetype == FileType.XML:
            return self._get_xml_writer()

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
