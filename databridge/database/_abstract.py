from abc import ABC, abstractmethod

import pandas as pd

from sqlalchemy import text
from sqlalchemy.exc import OperationalError


class Database(ABC):
    def __init__(self):
        self.engine = None

    def __del__(self):
        if self.engine is not None:
            self.engine.dispose()

    @property
    @abstractmethod
    def session(self):
        raise NotImplementedError("Subclasses must implement session().")

    @property
    def can_connect(self) -> bool:
        try:
            with self.engine.connect() as connection:
                pass
            return True
        except OperationalError as e:
            return False
        except Exception as e:
            return False

    def execute(self, sql: str) -> None:
        if isinstance(sql, str):
            sql = text(sql)
        with self.session() as active_session, active_session.begin():
            active_session.execute(sql)

    def load(
        self,
        table,
        df: pd.DataFrame,
        if_exists: str = "replace",
        index: bool = False,
    ) -> None:
        with self.session() as active_session, active_session.begin():
            df.to_sql(
                name=table.__tablename__,
                con=active_session.bind,
                if_exists=if_exists,
                index=index,
            )

    def query(self, sql, params: dict = None) -> pd.DataFrame:
        if isinstance(sql, str):
            sql = text(sql)
        with self.session() as active_session, active_session.begin():
            df = pd.read_sql(
                sql=sql,
                con=active_session.bind.connect(),
                params=params,
            )
        df.columns = df.columns.str.upper()
        return df
