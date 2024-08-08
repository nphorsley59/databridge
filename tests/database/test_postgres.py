import pytest

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from databridge._config import Config
from databridge.database._postgres import PostgresDatabase


@pytest.fixture
def postgres_database_instance():
    return PostgresDatabase(
        user=Config().POSTGRES_USER,
        password=Config().POSTGRES_PASSWORD,
        host=Config().POSTGRES_HOST,
        port=Config().POSTGRES_PORT,
        database=Config().POSTGRES_DB,
    )


def test_init(postgres_database_instance):
    assert isinstance(postgres_database_instance, PostgresDatabase)
    assert isinstance(postgres_database_instance.engine, Engine)


def test_session_property(postgres_database_instance):
    assert isinstance(postgres_database_instance._session, sessionmaker)
    with postgres_database_instance._session() as active_session, active_session.begin():
        assert active_session.bind == postgres_database_instance.engine
        assert active_session.bind.connect()


def test_can_connect(postgres_database_instance):
    assert postgres_database_instance.can_connect
