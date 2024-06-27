"""Tests for decrypt.py"""
from pathlib import Path
import pytest

from crypt4gh.keys import get_private_key as get_pk_bytes
from decrypt import get_private_keys

INPUT_DIR = Path(__file__).parents[2]/"inputs"


class TestGetPrivateKeys:
    """Test get_private_keys."""

    def test_empty_list(self):
        """Test empty input."""
        assert not get_private_keys([])

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
            return [get_pk_bytes(INPUT_DIR/filename, callback=lambda x: '')
                    for filename in expected_keys_retrieved]

        assert get_private_keys([INPUT_DIR/file for file in files]) == get_expected_bytes()
