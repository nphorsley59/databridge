import pytest

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from databridge.database._sqlite import SqliteDatabase


@pytest.fixture
def sqlite_database_instance():
    return SqliteDatabase()


def test_init(sqlite_database_instance):
    assert isinstance(sqlite_database_instance, SqliteDatabase)
    assert isinstance(sqlite_database_instance.engine, Engine)


def test_session_property(sqlite_database_instance):
    assert isinstance(sqlite_database_instance.session, sessionmaker)
    with sqlite_database_instance.session() as active_session, active_session.begin():
        assert active_session.bind == sqlite_database_instance.engine
        assert active_session.bind.connect()


def test_can_connect(sqlite_database_instance):
    assert sqlite_database_instance.can_connect
