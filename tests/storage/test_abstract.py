import os
from pathlib import Path
from typing import Callable, Union

import pandas as pd
import pytest

from databridge.storage._abstract import Storage


class ConcreteStorage(Storage):
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


@pytest.fixture
def concrete_storage_instance():
    return ConcreteStorage()


def test_storage_init(concrete_storage_instance):
    assert isinstance(concrete_storage_instance, Storage)


def test_storage_get_csv_reader_callable(
    concrete_storage_instance,
    temp_csv_fpath,
):
    func = concrete_storage_instance._get_reader_callable(
        fpath=str(temp_csv_fpath),
    )
    assert isinstance(func, Callable)


def test_storage_get_csv_writer_callable(
    concrete_storage_instance,
    temp_csv_fpath,
):
    func = concrete_storage_instance._get_writer_callable(
        fpath=str(temp_csv_fpath),
    )
    assert isinstance(func, Callable)


@pytest.fixture
def sample_df():
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40],
        "Occupation": ["Engineer", "Doctor", "Artist", "Data Scientist"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_dict():
    return {
        "name": "John",
        "age": 30,
        "city": "New York",
        "children": ["Anna", "Ella"],
    }


@pytest.fixture
def sample_str():
    return """
        Name, Age, Occupation
        Alice, 25, Engineer
        Bob, 30, Doctor
        Charlie, 35, Artist
        David, 40, Data Scientist
        """


@pytest.fixture
def temp_csv_fpath(tmp_path):
    return tmp_path / "test.csv"


def test_write_csv(concrete_storage_instance, sample_df, temp_csv_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    assert concrete_storage_instance.exists(fpath=temp_csv_fpath)


def test_read_csv(concrete_storage_instance, sample_df, temp_csv_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    df = concrete_storage_instance.read(fpath=temp_csv_fpath)
    pd.testing.assert_frame_equal(sample_df, df)


@pytest.fixture
def temp_json_fpath(tmp_path):
    return tmp_path / "test.json"


def test_write_json(concrete_storage_instance, sample_dict, temp_json_fpath):
    concrete_storage_instance.write(obj=sample_dict, fpath=temp_json_fpath)
    assert concrete_storage_instance.exists(fpath=temp_json_fpath)


def test_read_json(concrete_storage_instance, sample_dict, temp_json_fpath):
    concrete_storage_instance.write(obj=sample_dict, fpath=temp_json_fpath)
    output_dict = concrete_storage_instance.read(fpath=temp_json_fpath)
    assert sample_dict == output_dict


@pytest.fixture
def temp_txt_fpath(tmp_path):
    return tmp_path / "test.txt"


def test_write_txt(concrete_storage_instance, sample_str, temp_txt_fpath):
    concrete_storage_instance.write(obj=sample_str, fpath=temp_txt_fpath)
    assert concrete_storage_instance.exists(fpath=temp_txt_fpath)


def test_read_txt(concrete_storage_instance, sample_str, temp_txt_fpath):
    concrete_storage_instance.write(obj=sample_str, fpath=temp_txt_fpath)
    output_str = concrete_storage_instance.read(fpath=temp_txt_fpath)
    assert sample_str == output_str


@pytest.fixture
def temp_xml_fpath(tmp_path):
    return tmp_path / "test.xml"


def test_write_xml(concrete_storage_instance, sample_df, temp_xml_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xml_fpath)
    assert concrete_storage_instance.exists(fpath=temp_xml_fpath)


def test_read_xml(concrete_storage_instance, sample_df, temp_xml_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xml_fpath)
    output_dataframe = concrete_storage_instance.read(fpath=temp_xml_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


@pytest.fixture
def temp_xlsx_fpath(tmp_path):
    return tmp_path / "test.xlsx"


def test_write_xlsx(concrete_storage_instance, sample_df, temp_xlsx_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xlsx_fpath)
    assert concrete_storage_instance.exists(fpath=temp_xlsx_fpath)


def test_read_xlsx(concrete_storage_instance, sample_df, temp_xlsx_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xlsx_fpath)
    output_dataframe = concrete_storage_instance.read(fpath=temp_xlsx_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


@pytest.fixture
def temp_parquet_fpath(tmp_path):
    return tmp_path / "test.parquet"


def test_write_parquet(concrete_storage_instance, sample_df, temp_parquet_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_parquet_fpath)
    assert concrete_storage_instance.exists(fpath=temp_parquet_fpath)


def test_read_parquet(concrete_storage_instance, sample_df, temp_parquet_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_parquet_fpath)
    output_dataframe = concrete_storage_instance.read(fpath=temp_parquet_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


class DummyStorage(Storage):
    def _format_fpath(self, fpath):
        super()._format_fpath(fpath)

    def _read(self, fpath, reader):
        super()._read(fpath, reader)

    def _write(self, obj, fpath, writer):
        super()._write(obj, fpath, writer)

    def exists(self, fpath):
        super().exists(fpath)


def test_storage_format_fpath_not_implemented(temp_csv_fpath):
    storage = DummyStorage()
    with pytest.raises(NotImplementedError):
        storage._format_fpath(fpath=temp_csv_fpath)


def test_storage_read_not_implemented(temp_csv_fpath, mocker):
    storage = DummyStorage()
    mock_reader = mocker.Mock()
    with pytest.raises(NotImplementedError):
        storage._read(fpath=temp_csv_fpath, reader=mock_reader)


def test_storage_write_not_implemented(temp_csv_fpath, mocker):
    mock_obj = mocker.Mock()
    storage = DummyStorage()
    mock_writer = mocker.Mock()
    with pytest.raises(NotImplementedError):
        storage._write(obj=mock_obj, fpath=temp_csv_fpath, writer=mock_writer)


def test_storage_exists_not_implemented(temp_csv_fpath):
    storage = DummyStorage()
    with pytest.raises(NotImplementedError):
        storage.exists(fpath=temp_csv_fpath)
