import os
from botocore.exceptions import ClientError

import pandas as pd
import pytest

from databridge._config import Config, Directory
from databridge.storage._s3 import S3Storage


@pytest.fixture
def s3_storage_instance():
    return S3Storage(
        bucket_name=Config.S3_BUCKET_NAME,
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        region_name=Config.AWS_REGION,
        endpoint_url=Config.S3_ENDPOINT_URL,
    )


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
def nonexistent_fpath(tmp_path):
    return tmp_path / "nonexistent_file.txt"


@pytest.fixture
def sample_df():
    data = {
        "Name": ["Alice", "Bob", "Charlie", "David"],
        "Age": [25, 30, 35, 40],
        "Occupation": ["Engineer", "Doctor", "Artist", "Data Scientist"],
    }
    return pd.DataFrame(data)


def test_write_exists(s3_storage_instance, sample_df, temp_csv_fpath):
    assert not s3_storage_instance.exists(temp_csv_fpath)
    s3_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    assert s3_storage_instance.exists(fpath=temp_csv_fpath)
    s3_storage_instance.delete(fpath=temp_csv_fpath)
    assert not s3_storage_instance.exists(temp_csv_fpath)


def test_read(s3_storage_instance, sample_df, temp_csv_fpath):
    s3_storage_instance.write(obj=sample_df, fpath=temp_csv_fpath)
    df = s3_storage_instance.read(fpath=temp_csv_fpath)
    pd.testing.assert_frame_equal(sample_df, df)
    s3_storage_instance.delete(fpath=temp_csv_fpath)
    assert not s3_storage_instance.exists(temp_csv_fpath)


def test_exists_file_not_found(s3_storage_instance, nonexistent_fpath):
    s3_storage_instance.exists(fpath=nonexistent_fpath)


def test_exists_with_non_404_error(s3_storage_instance, mocker, nonexistent_fpath):
    error_response = {"Error": {"Code": "500", "Message": "Internal Server Error"}}
    mock_s3_client = mocker.Mock()
    mock_s3_client.head_object.side_effect = ClientError(error_response, "head_object")
    s3_storage_instance.s3_client = mock_s3_client
    with pytest.raises(ClientError) as exc_info:
        s3_storage_instance.exists(fpath=nonexistent_fpath)
    assert exc_info.value.response["Error"]["Code"] == "500"
    assert exc_info.value.response["Error"]["Message"] == "Internal Server Error"


def test_delete(s3_storage_instance, sample_df, gallery_csv_fpath):
    s3_storage_instance.write(obj=sample_df, fpath=gallery_csv_fpath)
    assert s3_storage_instance.exists(fpath=gallery_csv_fpath)
    s3_storage_instance.delete(fpath=gallery_csv_fpath)
    assert not s3_storage_instance.exists(fpath=gallery_csv_fpath)


def test_delete_file_not_found(s3_storage_instance, nonexistent_fpath):
    with pytest.raises(FileNotFoundError):
        s3_storage_instance.delete(fpath=nonexistent_fpath)
