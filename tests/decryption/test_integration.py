"""Integration tests for decrypt.py."""

import pytest
from tests.utils import patch_cli, INPUT_TEXT, INPUT_DIR

@pytest.mark.parametrize("files", [
    ["alice.sec", "hello.c4gh"],
    ["alice.sec", "bob.sec", "hello.c4gh", "hello2.c4gh"]
])
def test_decryption(files):
    """Test that files can be decrypted successfully."""


def test_default_dir():
    """Test that $TMPDIR is used when no output dir is provided."""


def test_no_args():
    """Test that an exception is thrown when no arguments are provided."""


def test_no_sk_provided_single():
    """Test that an exception is raised when no sk for a single file is provided."""


def test_no_sk_provided_multiple():
    """Test that an exception is raised when the sk is provided for one file but not another."""


def test_files_removed():
    """Test that files are deleted when an exception occurs."""


