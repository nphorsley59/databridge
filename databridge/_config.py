import os
from pathlib import Path


class Config:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "test-bucket")
    S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localhost:4566")
    PG_USER = os.getenv("PG_USER", "myuser")
    PG_PASSWORD = os.getenv("PG_PASSWORD", "mypassword")
    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = os.getenv("PG_PORT", "5432")
    PG_DATABASE = os.getenv("PG_DATABASE", "mydatabase")


class Directory:
    BASE = Path(__file__).resolve().parent
    DATA = BASE / "_data"
    TEST_ASSETS = DATA / "_test_assets"
    TEST_GALLERY = DATA / "_test_gallery"
