import pytest

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from databridge._config import Config
from databridge.database._postgres import PostgresDatabase


@pytest.fixture
def postgres_database_instance():
    return PostgresDatabase(
        user=Config.PG_USER,
        password=Config.PG_PASSWORD,
        host=Config.PG_HOST,
        port=Config.PG_PORT,
        database=Config.PG_DATABASE,
    )


def test_init(postgres_database_instance):
    assert isinstance(postgres_database_instance, PostgresDatabase)
    assert isinstance(postgres_database_instance.engine, Engine)


def test_session_property(postgres_database_instance):
    assert isinstance(postgres_database_instance.session, sessionmaker)
    with postgres_database_instance.session() as active_session, active_session.begin():
        assert active_session.bind == postgres_database_instance.engine
        assert active_session.bind.connect()


def test_can_connect(postgres_database_instance):
    assert postgres_database_instance.can_connect
