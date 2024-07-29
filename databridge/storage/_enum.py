from enum import Enum


class StorageType(str, Enum):
    LOCAL = "local"
    S3 = "s3"


class FileType(str, Enum):
    CSV = "csv"
    JSON = "json"
    TXT = "txt"
    XLSX = "xlsx"
    PARQUET = "parquet"
    XML = "xml"
