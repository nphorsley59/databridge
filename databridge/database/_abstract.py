from abc import ABC, abstractmethod

import pandas as pd


class Database(ABC):
    def __init__(self):
        self.engine = None

    def __del__(self):
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
        except:
            return False
