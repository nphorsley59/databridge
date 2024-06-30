
from pathlib import Path

import pytest

from adapters import config


@pytest.fixture
def directory_instance():
    return config.Directory()


def test_directory_init(directory_instance):
    assert isinstance(directory_instance, config.Directory)


def test_directory_folders_exist():
    for attribute in config.Directory.__dict__.items():
        if isinstance(attribute, Path):
            assert attribute.is_dir()
