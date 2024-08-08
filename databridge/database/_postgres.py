from sqlalchemy import create_engine

from databridge.database._abstract import Database
from databridge.database._session import Session


class PostgresDatabase(Database):
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: str,
        database: str,
    ):
        self.url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.url, pool_size=20)

    @property
    def _session(self):
        Session.configure(bind=self.engine)
        return Session
