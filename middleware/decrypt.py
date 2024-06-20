"""Identify and decrypt Crypt4GH keys and files.

Decrypts crypt4GH files given a list of files and places the output in a specified
directory. If a file is not Crypt4GH-encrypted, it moves the file to the output directory
without alteration. If a Crypt4GH file is included, the private key associated with that
file must be provided.

Example:
    python3 decrypt.py --output-dir /outputs/ file.txt file.c4gh sk.sec pk.pub
"""
from argparse import ArgumentParser
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile

from crypt4gh.lib import decrypt  # type: ignore
from crypt4gh.keys import get_private_key  # type: ignore


def get_private_keys(file_paths: list[Path]) -> list[bytes]:
    """Retrieve private keys from a list of files.

    Args:
        file_paths: A list of file paths.

    Returns:
        A list of retrieved private keys as byte objects.
    """
    private_keys = []
    for file_path in file_paths:
        try:
            # Callback returns password of sk
            key = get_private_key(file_path, callback=lambda x: '')
            private_keys.append(key)
        except ValueError:
            continue
    return private_keys


def decrypt_files(
        file_paths: list[Path],
        private_keys: list[bytes]):
    """Decrypt files in place.

    Args:
        file_paths: A list of file paths.
        private_keys: A list of private keys as byte objects.

    Raises:
        ValueError: If no private key for a Crypt4GH file is provided.
    """
    encryption_method_codes = {
        'ChaCha20': 0,
        'AES-GCM': 1  # Not currently supported by Crypt4GH standard
    }
    # Third element of tuple is the recipient pk, which isn't used in decryption
    key_tuples = [(encryption_method_codes['ChaCha20'], sk, None) for sk in private_keys]
    for file_path in file_paths:
        with open(file_path, "rb") as f_in, NamedTemporaryFile() as f_out:
            try:
                decrypt(keys=key_tuples, infile=f_in, outfile=f_out)
                shutil.move(f_out.name, file_path)
            except ValueError as e:
                if str(e) == "Not a CRYPT4GH formatted file":
                    continue
                raise ValueError(f"Private key for {file_path} not provided") from e


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file_paths", nargs='+', type=Path)
    parser.add_argument(
        "--output-dir",
        required=True,
        dest="output_dir",
        help="Directory to upload files to.",
        type=Path)

    args = parser.parse_args()
    paths = [args.output_dir/file_path.name for file_path in args.file_paths]
    for src, dest in zip(args.file_paths, paths):
        shutil.move(src, dest)
    keys = get_private_keys(paths)
    decrypt_files(paths, keys)
