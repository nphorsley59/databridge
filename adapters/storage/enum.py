
from enum import Enum


class StorageType(str, Enum):
    LOCAL = "local"


class FileType(str, Enum):
    CSV = ".csv"
