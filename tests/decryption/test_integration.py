"""Integration tests for decrypt.py."""

import os
import pytest
import shutil
from unittest import mock

from crypt4gh_middleware.decrypt import main
from tests.utils import patch_cli, INPUT_TEXT, INPUT_DIR


@pytest.fixture(name="secret_keys")
def fixture_secret_keys(tmp_path):
    """Returns temporary copies of secret keys."""
    encrypted_files = [INPUT_DIR/"alice.sec", INPUT_DIR/"bob.sec"]
    temp_files = [tmp_path/"alice.sec", tmp_path/"bob.sec"]
    for src, dest in zip(encrypted_files, temp_files):
        shutil.copy(src, dest)
    return temp_files


def test_decryption(encrypted_files, secret_keys, tmp_path):
    """Test that files can be decrypted successfully."""
    with patch_cli(["decrypt.py", "--output-dir", str(tmp_path)]
                   + [str(f) for f in (encrypted_files + secret_keys)]):
        main()
        for filename in encrypted_files:
            with open(tmp_path/filename, encoding="utf-8") as f:
                assert f.read() == INPUT_TEXT


def test_default_dir(encrypted_files, secret_keys, tmp_path):
    """Test that $TMPDIR is used when no output dir is provided."""
    with (patch_cli(["decrypt.py"] + [str(f) for f in (encrypted_files + secret_keys)]),
            mock.patch.dict(os.environ, {"TMPDIR": str(tmp_path)})):
        main()
        for filename in encrypted_files:
            with open(tmp_path/filename, encoding="utf-8") as f:
                assert f.read() == INPUT_TEXT


def test_no_args():
    """Test that an exception is thrown when no arguments are provided."""
    with patch_cli(["decrypt.py"]), pytest.raises(SystemExit):
        main()


def test_no_sk_provided_single(encrypted_files, capsys):
    """Test that messages are error messages are printed when no secret keys are provided."""
    with patch_cli(["decrypt.py"] + [str(f) for f in encrypted_files]):
        main()
        captured = capsys.readouterr()
        assert captured.out == (f"Private key for {encrypted_files[0].name} not provided\n"
                                f"Private key for {encrypted_files[1].name} not provided\n")


def test_no_sk_provided_multiple():
    """Test that an exception is raised when the sk is provided for one file but not another."""


def test_files_removed():
    """Test that files are deleted when an exception occurs."""


