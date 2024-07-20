
from pathlib import Path

import pytest

from databridge._config import Directory


@pytest.fixture
def directory_instance():
    return Directory()


def test_directory_init(directory_instance):
    assert isinstance(directory_instance, Directory)


def test_directory_folders_exist():
    for attribute in Directory.__dict__.items():
        if isinstance(attribute, Path):
            assert attribute.is_dir()
