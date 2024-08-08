import pandas as pd
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import DeclarativeBase

from databridge.database._abstract import Database
from databridge.database._session import Session


class ConcreteDatabase(Database):
    def __init__(self):
        self.engine = create_engine("sqlite://")

    @property
    def _session(self):
        Session.configure(bind=self.engine)
        return Session


class ConcreteBase(DeclarativeBase):
    pass


class SampleTable(ConcreteBase):
    __tablename__ = "sample_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)
    occupation = Column(String(255))


@pytest.fixture
def concrete_database_instance():
    concrete = ConcreteDatabase()
    ConcreteBase.metadata.create_all(concrete.engine)
    return concrete


@pytest.fixture
def sample_df():
    data = {
        "NAME": ["Alice", "Bob", "Charlie", "David"],
        "AGE": [25, 30, 35, 40],
        "OCCUPATION": ["Engineer", "Doctor", "Artist", "Data Scientist"],
    }
    return pd.DataFrame(data)


def test_init(concrete_database_instance):
    assert isinstance(concrete_database_instance, Database)


def test_can_connect(concrete_database_instance):
    assert concrete_database_instance.can_connect


def test_execute(concrete_database_instance):
    concrete_database_instance.execute(sql="""DELETE FROM sample_table""")
    count = concrete_database_instance.query(
        sql="""SELECT COUNT(*) FROM sample_table"""
    )
    assert count.iloc[0, 0] == 0


def test_load(concrete_database_instance, sample_df):
    concrete_database_instance.load(
        table=SampleTable,
        df=sample_df,
    )
    count = concrete_database_instance.query(
        sql="""SELECT COUNT(*) FROM sample_table"""
    )
    assert count.iloc[0, 0] == 4


def test_query(concrete_database_instance, sample_df):
    concrete_database_instance.load(
        table=SampleTable,
        df=sample_df,
    )
    df = concrete_database_instance.query(sql="""SELECT * FROM sample_table""")
    pd.testing.assert_frame_equal(df, sample_df)


class DummyDatabase(Database):
    def __init__(self):
        super().__init__()

    def _session(self):
        super()._session()


@pytest.fixture
def dummy_database_instance():
    return DummyDatabase()


def test_init_no_engine(dummy_database_instance):
    assert dummy_database_instance.engine is None


def test_session_not_implemented(dummy_database_instance):
    with pytest.raises(NotImplementedError):
        dummy_database_instance._session()


def test_can_connect_operational_error(dummy_database_instance, mocker):
    mock_engine = mocker.Mock()
    mock_engine.connect.side_effect = OperationalError(
        statement="SAMPLE_STATEMENT",
        params=None,
        orig=ValueError(),
    )
    dummy_database_instance.engine = mock_engine
    assert dummy_database_instance.can_connect is False


def test_can_connect_exception(dummy_database_instance, mocker):
    mock_engine = mocker.Mock()
    mock_engine.connect.side_effect = Exception()
    dummy_database_instance.engine = mock_engine
    assert dummy_database_instance.can_connect is False
