"""Shared fixtures for tests."""

import shutil

import pytest

from tests.utils import INPUT_DIR


@pytest.fixture(name="encrypted_files")
def fixture_encrypted_files(tmp_path):
    """Returns temporary copies of encrypted files.
    First two files are encrypted with alice.sec. Third file is encrypted with bob.sec.
    """
    encrypted_files = [INPUT_DIR/"hello.c4gh", INPUT_DIR/"hello2.c4gh", INPUT_DIR/"hello3.c4gh"]
    temp_files = [tmp_path/f.name for f in encrypted_files]
    for src, dest in zip(encrypted_files, temp_files):
        shutil.copy(src, dest)
    return temp_files
