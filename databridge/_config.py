from pathlib import Path


class Directory:
    BASE = Path(__file__).resolve().parent
    DATA = BASE / "data"
    TEST_ASSETS = DATA / "test_assets"
    TEST_GALLERY = DATA / "test_gallery"
