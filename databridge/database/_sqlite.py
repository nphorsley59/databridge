from sqlalchemy import create_engine

from databridge.database._abstract import Database
from databridge.database._session import Session


class SqliteDatabase(Database):
    def __init__(self):
        self.engine = create_engine("sqlite://")

    @property
    def session(self):
        Session.configure(bin=self.engine)
        return Session
