import os
from pathlib import Path


class Config:

    def __init__(self):
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
        self.AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
        self.S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "test-bucket")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "myuser")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mypassword")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "mydatabase")


class Directory:
    BASE = Path(__file__).resolve().parent
    DATA = BASE / "_data"
    TEST_ASSETS = DATA / "_test_assets"
    TEST_GALLERY = DATA / "_test_gallery"
