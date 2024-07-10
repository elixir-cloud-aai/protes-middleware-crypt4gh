"""Tests for decrypt.py"""
from pathlib import Path
import shutil

from crypt4gh.keys import get_private_key as get_sk_bytes, get_public_key as get_pk_bytes
import pytest

from crypt4gh_middleware.decrypt import get_private_keys, decrypt_files

INPUT_DIR = Path(__file__).parents[2]/"inputs"
INPUT_TEXT = "hello world from the input!"


class TestGetPrivateKeys:
    """Test get_private_keys."""

    def test_empty_list(self):
        """Test empty input."""
        assert not get_private_keys([])

    def test_invalid_path(self):
        """Test input with an invalid filename."""
        with pytest.raises(FileNotFoundError):
            get_private_keys([INPUT_DIR/'bad_file_path'])

    @pytest.mark.parametrize("files,expected_keys_retrieved", [
        (["alice.pub", "bob.pub", "hello.c4gh"], []),
        (["alice.sec", "alice.pub", "bob.pub"], ["alice.sec"]),
        (["alice.sec", "bob.sec", "alice.pub", "bob.pub"], ["alice.sec", "bob.sec"])
    ])
    def test_get_keys(self, files, expected_keys_retrieved):
        """Test ability to retrieve keys from a list of files.

        Ensure that `get_private_keys` gets only private keys from a list of files.
        """
        def get_expected_bytes():
            return [get_sk_bytes(INPUT_DIR/filename, callback=lambda x: '')
                    for filename in expected_keys_retrieved]

        assert get_private_keys([INPUT_DIR/file for file in files]) == get_expected_bytes()


class TestDecryptFiles:
    """Test decrypt_files."""

    @pytest.fixture()
    def key_pair(self):
        """Returns the key pair used to encrypt the input files."""
        return INPUT_DIR/"alice.sec", INPUT_DIR/"alice.pub"

    @pytest.fixture()
    def key_pair_bytes(self, key_pair):
        """Returns the bytes of the key pair."""
        sk, pk = key_pair
        sk_bytes = get_sk_bytes(filepath=sk, callback=lambda x: '')
        pk_bytes = get_pk_bytes(filepath=pk)
        return sk_bytes, pk_bytes

    @pytest.fixture()
    def encrypted_files(self, tmp_path):
        """Returns the encrypted file paths and re-encrypts files after use."""
        encrypted_files = [INPUT_DIR/"hello.c4gh", INPUT_DIR/"hello2.c4gh"]
        temp_files = [tmp_path/"hello.c4gh", tmp_path/"hello2.c4gh"]
        for src, dest in zip(encrypted_files, temp_files):
            shutil.copy(src, dest)
        return temp_files

    @pytest.fixture()
    def unencrypted_files(self):
        """Returns the unencrypted file paths"""
        return [INPUT_DIR/"hello.txt"]

    @pytest.mark.parametrize("files", ["encrypted_files", "unencrypted_files", []])
    def test_handles_encrypted_and_unencrypted_files(self, files, key_pair_bytes, request):
        """Test that decrypt_files decrypts only encrypted files in-place.

        Ensure no exception is thrown when attempting to decrypt unencrypted files.
        """
        def files_exist():
            return all(file_path.exists() for file_path in files)

        def file_contents_are_valid():
            for file_path in files:
                with open(file_path, encoding="utf-8") as f:
                    output = f.read()
                    if output != INPUT_TEXT:
                        return False
            return True

        # Fixture names passed to pytest.mark.parametrize are strings, so get value
        if isinstance(files, str):
            files = request.getfixturevalue(files)

        assert files_exist()
        decrypt_files(file_paths=files,
                      private_keys=[key_pair_bytes[0]])
        assert files_exist()

        assert file_contents_are_valid()
