
from typing import Callable

import pytest

from adapters.storage import abstract


class ConcreteStorage(abstract.Storage):
    def file_exists(self):
        pass

    def read_file(self):
        pass

    def write_file(self):
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
        fpath=temp_csv_fpath,
    )
    assert isinstance(func, Callable)


def test_storage_get_csv_writer_callable(
        storage_instance,
        temp_csv_fpath,
):
    func = storage_instance._get_reader_callable(
        fpath=temp_csv_fpath,
    )
    assert isinstance(func, Callable)