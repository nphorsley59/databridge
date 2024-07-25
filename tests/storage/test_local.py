import os
from typing import Callable

import pandas as pd
import pytest

from databridge.storage._local import LocalStorage
from databridge._config import Directory


@pytest.fixture
def local_storage_instance():
    return LocalStorage()


@pytest.fixture
def asset_csv_fpath():
    return os.path.join(Directory.TEST_ASSETS, "test.csv")


@pytest.fixture
def gallery_csv_fpath():
    return os.path.join(Directory.TEST_GALLERY, "test.csv")


@pytest.fixture
def temp_csv_fpath(tmp_path):
    return tmp_path / "test.csv"


@pytest.fixture
def temp_xml_fpath(tmp_path):
    return tmp_path / "test.xml"


@pytest.fixture
def temp_xlsx_fpath(tmp_path):
    return tmp_path / "test.xlsx"


@pytest.fixture
def temp_txt_fpath(tmp_path):
    return tmp_path / "test.txt"


@pytest.fixture
def temp_parquet_fpath(tmp_path):
    return tmp_path / "test.parquet"


@pytest.fixture
def temp_json_fpath(tmp_path):
    return tmp_path / "test.json"


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


def test_storage_get_reader_callable(local_storage_instance, temp_csv_fpath):
    func = local_storage_instance._get_reader_callable(
        fpath=str(temp_csv_fpath),
    )
    assert isinstance(func, Callable)


def test_storage_get_writer_callable(local_storage_instance, temp_csv_fpath):
    func = local_storage_instance._get_writer_callable(
        fpath=str(temp_csv_fpath),
    )
    assert isinstance(func, Callable)


def test_storage_exists(local_storage_instance, asset_csv_fpath):
    assert local_storage_instance.exists(fpath=asset_csv_fpath)


def test_storage_delete(local_storage_instance, sample_df, gallery_csv_fpath): 
    local_storage_instance.write(obj=sample_df, fpath=gallery_csv_fpath)
    assert local_storage_instance.exists(fpath=gallery_csv_fpath)
    local_storage_instance.delete(fpath=gallery_csv_fpath)
    assert not local_storage_instance.exists(fpath=gallery_csv_fpath)


def test_storage_delete_file_not_found(local_storage_instance): 
    with pytest.raises(FileNotFoundError):
        local_storage_instance.delete(fpath="nonexistent_file")


def test_write_csv(local_storage_instance, sample_df, temp_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    assert local_storage_instance.exists(fpath=temp_csv_fpath)


def test_read_csv(local_storage_instance, sample_df, temp_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    df = local_storage_instance.read(fpath=temp_csv_fpath)
    pd.testing.assert_frame_equal(sample_df, df)


def test_write_json(local_storage_instance, sample_dict, temp_json_fpath):
    local_storage_instance.write(obj=sample_dict, fpath=temp_json_fpath)
    assert local_storage_instance.exists(fpath=temp_json_fpath)


def test_read_json(local_storage_instance, sample_dict, temp_json_fpath):
    local_storage_instance.write(obj=sample_dict, fpath=temp_json_fpath)
    output_dict = local_storage_instance.read(fpath=temp_json_fpath)
    assert sample_dict == output_dict


def test_write_txt(local_storage_instance, sample_str, temp_txt_fpath):
    local_storage_instance.write(obj=sample_str, fpath=temp_txt_fpath)
    assert local_storage_instance.exists(fpath=temp_txt_fpath)


def test_read_txt(local_storage_instance, sample_str, temp_txt_fpath):
    local_storage_instance.write(obj=sample_str, fpath=temp_txt_fpath)
    output_str = local_storage_instance.read(fpath=temp_txt_fpath)
    assert sample_str == output_str


def test_write_xml(local_storage_instance, sample_df, temp_xml_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_xml_fpath)
    assert local_storage_instance.exists(fpath=temp_xml_fpath)


def test_read_xml(local_storage_instance, sample_df, temp_xml_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_xml_fpath)
    output_dataframe = local_storage_instance.read(fpath=temp_xml_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


def test_write_xlsx(local_storage_instance, sample_df, temp_xlsx_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_xlsx_fpath)
    assert local_storage_instance.exists(fpath=temp_xlsx_fpath)


def test_read_xlsx(local_storage_instance, sample_df, temp_xlsx_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_xlsx_fpath)
    output_dataframe = local_storage_instance.read(fpath=temp_xlsx_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)


def test_write_parquet(local_storage_instance, sample_df, temp_parquet_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_parquet_fpath)
    assert local_storage_instance.exists(fpath=temp_parquet_fpath)


def test_read_parquet(local_storage_instance, sample_df, temp_parquet_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_parquet_fpath)
    output_dataframe = local_storage_instance.read(fpath=temp_parquet_fpath)
    pd.testing.assert_frame_equal(sample_df, output_dataframe)
