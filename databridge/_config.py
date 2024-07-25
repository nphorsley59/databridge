from pathlib import Path


class Directory:
    BASE = Path(__file__).resolve().parent
    DATA = BASE / "_data"
    TEST_ASSETS = DATA / "_test_assets"
    TEST_GALLERY = DATA / "_test_gallery"
