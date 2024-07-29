from sqlalchemy import create_engine

from databridge.database._abstract import Database
from databridge.database._session import Session


class PostgresDatabase(Database):
        def __init__(
            self,
            username: str,
            password: str,
            host: str,
            port: str,
            name: str,
        ):
            url = f"postgresql://{username}:{password}@{host}:{port}/{name}"
            self.engine = create_engine(url, pool_size=20)

        @property
        def session(self):
            Session.configure(bind=self.engine)
            return Session
              