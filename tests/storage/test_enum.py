
from databridge.storage._enum import FileType, StorageType


def test_storagetype_properties():
    assert StorageType.LOCAL.name == "LOCAL"
    assert StorageType.LOCAL.value == "local"
    assert isinstance(StorageType.LOCAL, StorageType)


def test_storagetype_members():
    assert StorageType.LOCAL == "local"


def test_storagetype_retrieval():
    assert StorageType("local") == StorageType.LOCAL


def test_storagetype_member_uniqueness():
    values = set(item.value for item in StorageType)
    assert len(values) == len(StorageType)


def test_filetype_properties():
    assert FileType.CSV.name == "CSV"
    assert FileType.CSV.value == "csv"
    assert isinstance(FileType.CSV, FileType)


def test_filetype_members():
    assert FileType.CSV == "csv"


def test_filetype_retrieval():
    assert FileType("csv") == FileType.CSV


def test_filetype_member_uniqueness():
    values = set(item.value for item in FileType)
    assert len(values) == len(FileType)
