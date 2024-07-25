import pytest

from databridge.storage._abstract import Storage


class DummyStorage(Storage):
    def _read(self, fpath):
        super()._read(fpath)

    def _write(self, obj, fpath):
        super()._write(obj, fpath)

    def exists(self, fpath):
        super().exists(fpath)
    
    def delete(self, fpath):
        super().delete(fpath)


@pytest.fixture
def dummy_storage_instance():
    return DummyStorage()


@pytest.fixture
def temp_csv_fpath(tmp_path):
    return tmp_path / "test.csv"


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
