import pandas as pd
import pytest

from databridge.storage._local import LocalStorage


@pytest.fixture
def local_storage_instance():
    return LocalStorage()


@pytest.fixture
def temp_csv_fpath(tmp_path):
    return tmp_path / "test.csv"


@pytest.fixture
def sample_df():
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40],
        "Occupation": ["Engineer", "Doctor", "Artist", "Data Scientist"],
    }
    return pd.DataFrame(data)


def test_format_fpath_with_path(temp_csv_fpath, local_storage_instance):
    fpath = local_storage_instance._format_fpath(fpath=temp_csv_fpath)
    assert isinstance(fpath, str)


def test_format_fpath_with_str(temp_csv_fpath, local_storage_instance):
    fpath = local_storage_instance._format_fpath(fpath=str(temp_csv_fpath))
    assert isinstance(fpath, str)
    with pytest.raises(TypeError):
        not_str_fpath = {"test": "csv"}
        local_storage_instance._format_fpath(fpath=not_str_fpath)


def test_format_fpath_with_invalid(local_storage_instance):
    with pytest.raises(TypeError):
        not_str_fpath = {"test": "csv"}
        local_storage_instance._format_fpath(fpath=not_str_fpath)


def test_write(local_storage_instance, sample_df, temp_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    assert local_storage_instance.exists(fpath=temp_csv_fpath)


def test_read(local_storage_instance, sample_df, temp_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    df = local_storage_instance.read(fpath=temp_csv_fpath)
    pd.testing.assert_frame_equal(sample_df, df)
