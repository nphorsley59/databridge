
from adapters.storage import enum


def test_storagetype_properties():
    assert enum.StorageType.LOCAL.name == "LOCAL"
    assert enum.StorageType.LOCAL.value == "local"
    assert isinstance(enum.StorageType.LOCAL, enum.StorageType)


def test_storagetype_members():
    assert enum.StorageType.LOCAL == "local"


def test_storagetype_retrieval():
    assert enum.StorageType("local") == enum.StorageType.LOCAL


def test_storagetype_member_uniqueness():
    values = set(item.value for item in enum.StorageType)
    assert len(values) == len(enum.StorageType)


def test_filetype_properties():
    assert enum.FileType.CSV.name == "CSV"
    assert enum.FileType.CSV.value == ".csv"
    assert isinstance(enum.FileType.CSV, enum.FileType)


def test_filetype_members():
    assert enum.FileType.CSV == ".csv"


def test_filetype_retrieval():
    assert enum.FileType(".csv") == enum.FileType.CSV


def test_filetype_member_uniqueness():
    values = set(item.value for item in enum.FileType)
    assert len(values) == len(enum.FileType)
