"""Integration tests for decrypt.py."""

import logging
import os
from pathlib import Path
import shutil
from unittest import mock

import pytest

from crypt4gh_middleware.decrypt import main
from tests.utils import INPUT_DIR, INPUT_TEXT, patch_cli


@pytest.fixture(name="secret_keys")
def fixture_secret_keys(tmp_path):
    """Returns temporary copies of secret keys."""
    encrypted_files = [INPUT_DIR/"alice.sec", INPUT_DIR/"bob.sec"]
    temp_files = [tmp_path/"alice.sec", tmp_path/"bob.sec"]
    for src, dest in zip(encrypted_files, temp_files):
        shutil.copy(src, dest)
    return temp_files


@pytest.fixture(name="string_paths")
def fixture_string_paths(encrypted_files, secret_keys):
    """Returns string version of file paths for use in patch_cli."""
    return [str(f) for f in (encrypted_files + secret_keys)]


def files_decrypted_successfully(encrypted_files, tmp_path):
    """Check if encrypted files have been decrypted."""
    for filename in encrypted_files:
        with open(tmp_path/filename, encoding="utf-8") as f:
            if f.read() != INPUT_TEXT:
                return False
    return True


def test_decryption(encrypted_files, string_paths, tmp_path):
    """Test that files are decrypted successfully."""
    with patch_cli(["decrypt.py", "--output-dir", str(tmp_path)] + string_paths):
        main()
        assert files_decrypted_successfully(encrypted_files=encrypted_files, tmp_path=tmp_path)


def test_default_dir(encrypted_files, string_paths, tmp_path):
    """Test that $TMPDIR is used when no output dir is provided."""
    with (patch_cli(["decrypt.py"] + string_paths),
            mock.patch.dict(os.environ, {"TMPDIR": str(tmp_path)})):
        main()
        assert files_decrypted_successfully(encrypted_files=encrypted_files, tmp_path=tmp_path)


def test_missing_tmpdir(encrypted_files, string_paths, monkeypatch):
    """Test that ./tmpdir is used when no output dir is specified and $TMPDIR is not set."""
    monkeypatch.delenv("TMPDIR", raising=False)
    with patch_cli(["decrypt.py"] + string_paths):
        main()
        assert files_decrypted_successfully(encrypted_files=encrypted_files,
                                            tmp_path=Path("tmpdir"))


def test_no_args():
    """Test that an exception is thrown when no arguments are provided."""
    with patch_cli(["decrypt.py"]) as patched_cli, pytest.raises(SystemExit) as exc_info:
        main()
        assert "usage:" in str(exc_info.value)
        assert patched_cli.stderr.getvalue().startswith("usage:")


@pytest.mark.parametrize("keys", [[], "secret_keys"])
def test_no_valid_sk_provided(encrypted_files, caplog, keys, request):
    """Test that error messages are printed when no keys or invalid secret keys are provided."""
    # Fixture names passed to pytest.mark.parametrize are strings, so get value
    if isinstance(keys, str):
        # bob.pk was not used to encrypt hello.c4gh and hello2.c4gh
        keys = [request.getfixturevalue(keys)[1]]

    with (patch_cli(["decrypt.py"] + [str(f) for f in (encrypted_files[:2] + keys)]),
          caplog.at_level(logging.CRITICAL)):
        main()
        assert f"Private key for {encrypted_files[0].name} not provided" in caplog.text
        assert f"Private key for {encrypted_files[1].name} not provided" in caplog.text


def test_one_sk_provided(encrypted_files, caplog, secret_keys):
    """Test that appropriate error message is printed when only one valid secret key is provided."""
    with (patch_cli(["decrypt.py"] + [str(f) for f in (encrypted_files + [secret_keys[0]])]),
          caplog.at_level(logging.CRITICAL)):
        main()
        assert f"Private key for {encrypted_files[2].name} not provided" in caplog.text


def test_invalid_output_dir(string_paths):
    """Test that an exception occurs when an invalid output directory is provided."""
    with (patch_cli(["decrypt.py", "--output-dir", "bad_dir"] + string_paths),
            pytest.raises(FileNotFoundError)):
        main()


def test_output_dir_no_write_permission(string_paths, tmp_path):
    """Test handling of output directory without write permissions."""
    no_write_dir = tmp_path/"no_write"
    no_write_dir.mkdir()
    no_write_dir.chmod(0o555)
    with (patch_cli(["decrypt.py", "--output-dir", str(no_write_dir)] + string_paths),
            pytest.raises(PermissionError)):
        main()


def test_no_files_in_output_dir_on_exception(string_paths, tmp_path):
    """Test that no files are in the output directory when an exception occurs."""
    with (patch_cli(["decrypt.py", "--output-dir", str(tmp_path)] + string_paths + ["bad_file"]),
            pytest.raises(FileNotFoundError)):
        main()
        assert not any(file.exists() for file in tmp_path.iterdir())
