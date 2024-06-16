"""Identify and decrypt Crypt4GH keys and files.

Decrypts crypt4GH files given a list of files and places the output in a specified
directory. If a file is not Crypt4GH-encrypted, it moves the file to the output directory
without alteration. If a Crypt4GH file is included, the private key associated with that
file must be provided.

Example:
    python3 decrypt.py --output-dir /outputs/ file.txt file.c4gh sk.sec pk.pub
"""
import os
from argparse import ArgumentParser
from pathlib import Path
from crypt4gh.lib import decrypt  # type: ignore
from crypt4gh.keys import get_private_key  # type: ignore


def get_private_keys(file_paths: list[Path]) -> list[bytes]:
    """Retrieve private keys from a list of files.

    Args:
        file_paths (list[Path]): A list of file paths.

    Returns:
        list[bytes]: A list of retrieved private keys as byte objects.
    """
    private_keys = []
    for file_path in file_paths:
        try:
            key = get_private_key(Path(file_path), lambda x: '')
            private_keys.append(key)
        except ValueError:
            continue
    return private_keys


def decrypt_files(
        file_paths: list[Path],
        private_keys: list[bytes],
        output_path: Path) -> None:
    """Decrypt files and save to specified output directory.

    Args:
        file_paths (list[Path]): A list of file paths.
        private_keys (list[bytes]): A list of private keys as byte objects.
        output_path: (Path): Directory to place decrypted files in.

    Raises:
        ValueError: If no private key for a Crypt4GH file is provided.
    """
    for file_path in file_paths:
        with open(file_path, "rb") as f_in:
            filename = file_path.name
            try:
                with open(output_path/filename, "wb") as f_out:
                    decrypt([(0, pk, "") for pk in private_keys], f_in, f_out)
            except ValueError as e:
                if str(e) == "Not a CRYPT4GH formatted file":
                    continue
                raise ValueError(f"Private key for {file_path} not provided") from e


def move_files(file_paths: list[Path], output_path: Path) -> None:
    """Move files that are not in the specified output directory to the directory.

    Args:
        file_paths (list[Path]): A list of file paths.
        output_path: (Path): Directory to place decrypted files in.
    """
    for file_path in file_paths:
        filename = file_path.name
        if not (output_path/filename).exists():
            os.replace(file_path, output_path/filename)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file_paths", nargs='+')
    parser.add_argument(
        "--output-dir",
        required=True,
        dest="output_dir",
        help="Directory to upload files to.")

    output_dir = Path(parser.parse_args().output_dir)
    paths = [Path(path) for path in parser.parse_args().file_paths]
    keys = get_private_keys(paths)
    decrypt_files(paths, keys, output_dir)
    move_files(paths, output_dir)
