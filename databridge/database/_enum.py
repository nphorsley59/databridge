from enum import Enum


class DatabaseType(str, Enum):
    POSTGRES = "postgres"
    SQLITE = "sqlite"
