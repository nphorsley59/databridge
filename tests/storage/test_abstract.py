import os
import pytest
from typing import Callable

import pandas as pd

from databridge.storage._abstract import Storage


class ConcreteStorage(Storage):

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


@pytest.fixture
def concrete_storage_instance():
    return ConcreteStorage()


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


@pytest.fixture
def temp_json_fpath(tmp_path):
    return tmp_path / "test.json"


@pytest.fixture
def temp_txt_fpath(tmp_path):
    return tmp_path / "test.txt"


@pytest.fixture
def temp_xml_fpath(tmp_path):
    return tmp_path / "test.xml"


@pytest.fixture
def temp_xlsx_fpath(tmp_path):
    return tmp_path / "test.xlsx"


@pytest.fixture
def temp_parquet_fpath(tmp_path):
    return tmp_path / "test.parquet"


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


def test_write_csv(concrete_storage_instance, sample_df, temp_csv_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    assert concrete_storage_instance.exists(fpath=temp_csv_fpath)


def test_read_csv(concrete_storage_instance, sample_df, temp_csv_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    df = concrete_storage_instance.read(fpath=temp_csv_fpath)
    pd.testing.assert_frame_equal(sample_df, df)


def test_write_json(concrete_storage_instance, sample_dict, temp_json_fpath):
    concrete_storage_instance.write(obj=sample_dict, fpath=temp_json_fpath)
    assert concrete_storage_instance.exists(fpath=temp_json_fpath)


def test_read_json(concrete_storage_instance, sample_dict, temp_json_fpath):
    concrete_storage_instance.write(obj=sample_dict, fpath=temp_json_fpath)
    output_dict = concrete_storage_instance.read(fpath=temp_json_fpath)
    assert sample_dict == output_dict


def test_write_txt(concrete_storage_instance, sample_str, temp_txt_fpath):
    concrete_storage_instance.write(obj=sample_str, fpath=temp_txt_fpath)
    assert concrete_storage_instance.exists(fpath=temp_txt_fpath)


def test_read_txt(concrete_storage_instance, sample_str, temp_txt_fpath):
    concrete_storage_instance.write(obj=sample_str, fpath=temp_txt_fpath)
    output_str = concrete_storage_instance.read(fpath=temp_txt_fpath)
    assert sample_str == output_str


def test_write_xml(concrete_storage_instance, sample_df, temp_xml_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xml_fpath)
    assert concrete_storage_instance.exists(fpath=temp_xml_fpath)


def test_read_xml(concrete_storage_instance, sample_df, temp_xml_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xml_fpath)
    output_dataframe = concrete_storage_instance.read(fpath=temp_xml_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


def test_write_xlsx(concrete_storage_instance, sample_df, temp_xlsx_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xlsx_fpath)
    assert concrete_storage_instance.exists(fpath=temp_xlsx_fpath)


def test_read_xlsx(concrete_storage_instance, sample_df, temp_xlsx_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_xlsx_fpath)
    output_dataframe = concrete_storage_instance.read(fpath=temp_xlsx_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


def test_write_parquet(concrete_storage_instance, sample_df, temp_parquet_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_parquet_fpath)
    assert concrete_storage_instance.exists(fpath=temp_parquet_fpath)


def test_read_parquet(concrete_storage_instance, sample_df, temp_parquet_fpath):
    concrete_storage_instance.write(obj=sample_df, fpath=temp_parquet_fpath)
    output_dataframe = concrete_storage_instance.read(fpath=temp_parquet_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


class DummyStorage(Storage):
    def _read(self, fpath, reader=None):
        super()._read(fpath, reader)

    def _write(self, obj, fpath, writer=None):
        super()._write(obj, fpath, writer)

    def exists(self, fpath):
        super().exists(fpath)
    
    def delete(self, fpath):
        super().delete(fpath)


@pytest.fixture
def dummy_storage_instance():
    return DummyStorage()


def test_dummy_storage_init(dummy_storage_instance):
    assert isinstance(dummy_storage_instance, DummyStorage)


def test_format_fpath_with_path(temp_csv_fpath, dummy_storage_instance):
    fpath = dummy_storage_instance._format_fpath(fpath=temp_csv_fpath)
    assert isinstance(fpath, str)


def test_format_fpath_with_str(temp_csv_fpath, dummy_storage_instance):
    fpath = dummy_storage_instance._format_fpath(fpath=str(temp_csv_fpath))
    assert isinstance(fpath, str)
    with pytest.raises(TypeError):
        not_str_fpath = {"test": "csv"}
        dummy_storage_instance._format_fpath(fpath=not_str_fpath)


def test_format_fpath_with_invalid(dummy_storage_instance):
    with pytest.raises(TypeError):
        not_str_fpath = {"test": "csv"}
        dummy_storage_instance._format_fpath(fpath=not_str_fpath)


def test_storage_read_not_implemented(dummy_storage_instance, temp_csv_fpath):
    with pytest.raises(NotImplementedError):
        dummy_storage_instance._read(fpath=temp_csv_fpath)


def test_storage_write_not_implemented(dummy_storage_instance, temp_csv_fpath, mocker):
    mock_obj = mocker.Mock()
    with pytest.raises(NotImplementedError):
        dummy_storage_instance._write(obj=mock_obj, fpath=temp_csv_fpath)


def test_storage_exists_not_implemented(dummy_storage_instance, temp_csv_fpath):
    with pytest.raises(NotImplementedError):
        dummy_storage_instance.exists(fpath=temp_csv_fpath)


def test_storage_delete_not_implemented(dummy_storage_instance, temp_csv_fpath):
    with pytest.raises(NotImplementedError):
        dummy_storage_instance.delete(fpath=temp_csv_fpath)
