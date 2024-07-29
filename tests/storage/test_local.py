import os

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
def sample_df():
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40],
        "Occupation": ["Engineer", "Doctor", "Artist", "Data Scientist"],
    }
    return pd.DataFrame(data)


def test_write_exists(local_storage_instance, sample_df, temp_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    assert local_storage_instance.exists(fpath=temp_csv_fpath)


def test_read(local_storage_instance, sample_df, temp_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    df = local_storage_instance.read(fpath=temp_csv_fpath)
    pd.testing.assert_frame_equal(sample_df, df)


def test_delete(local_storage_instance, sample_df, gallery_csv_fpath):
    local_storage_instance.write(obj=sample_df, fpath=gallery_csv_fpath)
    assert local_storage_instance.exists(fpath=gallery_csv_fpath)
    local_storage_instance.delete(fpath=gallery_csv_fpath)
    assert not local_storage_instance.exists(fpath=gallery_csv_fpath)


def test_delete_file_not_found(local_storage_instance):
    with pytest.raises(FileNotFoundError):
        local_storage_instance.delete(fpath="nonexistent_file")
