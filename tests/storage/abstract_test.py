
from typing import Callable

import pytest

from adapters.storage import abstract


class ConcreteStorage(abstract.Storage):
    def _format_fpath(self):
        pass

    def _read(self):
        pass

    def _write(self):
        pass

    def exists(self):
        pass


@pytest.fixture
def storage_instance():
    return ConcreteStorage()


@pytest.fixture
def temp_csv_fpath(tmp_path):
    return tmp_path / "test.csv"


def test_storage_init(storage_instance):
    assert isinstance(storage_instance, abstract.Storage)


def test_storage_get_csv_reader_callable(
        storage_instance,
        temp_csv_fpath,
):
    func = storage_instance._get_reader_callable(
        fpath=str(temp_csv_fpath),
    )
    assert isinstance(func, Callable)


def test_storage_get_csv_writer_callable(
        storage_instance,
        temp_csv_fpath,
):
    func = storage_instance._get_writer_callable(
        fpath=str(temp_csv_fpath),
    )
    assert isinstance(func, Callable)


class DummyStorage(abstract.Storage):
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
