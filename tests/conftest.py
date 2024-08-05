"""Shared fixtures for tests."""

import pytest
import shutil

from tests.utils import INPUT_DIR


@pytest.fixture(name="encrypted_files")
def fixture_encrypted_files(tmp_path):
    """Returns temporary copies of encrypted files."""
    encrypted_files = [INPUT_DIR/"hello.c4gh", INPUT_DIR/"hello2.c4gh"]
    temp_files = [tmp_path/"hello.c4gh", tmp_path/"hello2.c4gh"]
    for src, dest in zip(encrypted_files, temp_files):
        shutil.copy(src, dest)
    return temp_files
