from databridge.database._enum import DatabaseType


def test_databasetype_properties():
    assert DatabaseType.POSTGRES.name == "POSTGRES"
    assert DatabaseType.POSTGRES.value == "postgres"
    assert isinstance(DatabaseType.POSTGRES, DatabaseType)


def test_databasetype_members():
    assert DatabaseType.POSTGRES == "postgres"


def test_databasetype_retrieval():
    assert DatabaseType("postgres") == DatabaseType.POSTGRES


def test_databasetype_member_uniqueness():
    values = set(item.value for item in DatabaseType)
    assert len(values) == len(DatabaseType)
