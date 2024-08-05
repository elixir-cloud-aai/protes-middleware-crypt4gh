"""Integration tests for decrypt.py."""

import pytest

from crypt4gh_middleware.decrypt import main
from tests.utils import patch_cli, INPUT_TEXT, INPUT_DIR


@pytest.mark.parametrize("keys,files", [
    [["alice.sec"], ["hello.c4gh"]],
    [["alice.sec", "bob.sec"], ["hello.c4gh", "hello2.c4gh"]]
])
def test_decryption(keys, files, tmp_path):
    """Test that files can be decrypted successfully."""
    patch_cli(["--output-dir", tmp_path] + [INPUT_DIR/f for f in files] + keys)
    main()
    for filename in files:
        with open(tmp_path/filename, encoding="utf-8") as f:
            assert f.read() == INPUT_TEXT

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

