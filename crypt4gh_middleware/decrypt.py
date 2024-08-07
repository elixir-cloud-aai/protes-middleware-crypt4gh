"""Identify and decrypt Crypt4GH keys and files.

Moves all files in a given list and places the output in a specified directory. Any encrypted files
are subsequently decrypted in place. If a Crypt4GH file is included, the private key associated with
that file must be provided.

Example:
    python3 decrypt.py --output-dir /outputs/ file.txt file.c4gh sk.sec pk.pub
"""
from argparse import ArgumentParser
import logging
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import NamedTemporaryFile

from crypt4gh.lib import decrypt  # type: ignore
from crypt4gh.keys import get_private_key  # type: ignore

logger = logging.getLogger(__name__)


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
            key = get_private_key(filepath=file_path, callback=lambda x: '')
            private_keys.append(key)
            logger.debug(f"{file_path} identified as a private key", )
        except ValueError:
            logger.debug(f"{file_path} not identified as a private key")
            continue
    return private_keys


def decrypt_files(file_paths: list[Path], private_keys: list[bytes]):
    """Decrypt files in place.

    Args:
        file_paths: A list of file paths.
        private_keys: A list of private keys as byte objects.
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
                decrypt(keys=key_tuples, infile=f_in, outfile=f_out)  # Checks for magic
                shutil.move(f_out.name, file_path)
                logger.info(f"Decrypted {file_path} successfully")
            except ValueError as e:
                if str(e) != "Not a CRYPT4GH formatted file":
                    logger.error(f"Private key for {file_path.name} not provided")
                continue


def move_files(file_paths: list[Path], output_dir: Path) -> list[Path]:
    """Move files to a specified output directory.

    Args:
        file_paths: A list of file paths with unique file names.
        output_dir: Directory to move files to.

    Returns:
        A list containing the new file paths.
    """
    output_paths = []
    existing_names = set()
    for file_path in file_paths:
        if file_path.name in existing_names:
            raise ValueError(f"Duplicate file name found: {file_path.name}")
        output_paths = [output_dir/file_path.name for file_path in file_paths]
        existing_names.add(file_path.name)
    for src, dest in zip(file_paths, output_paths):
        shutil.move(src, dest)
        logger.debug(f"Moved {src} to {dest}")
    return output_paths


def remove_files(directory: Path):
    """Rewrites and removes all files in a directory using rm -P.

    Args:
        directory: Directory that holds the files to be deleted.

    Raises:
        ValueError if specified directory does not exist.
    """
    if not directory.is_dir():
        raise ValueError(f"Could not remove files: {directory} is not a directory.")
    for file in directory.iterdir():
        subprocess.run(["rm", "-P", str(file)], check=True)
        logger.debug(f"Removed {file.name}")


def get_args():
    """Parse command-line arguments.

    Returns:
        argparse.ArgumentParser object containing the file_paths and output_dir arguments
    """
    parser = ArgumentParser()
    parser.add_argument(
        "file_paths",
        nargs='+',
        type=Path,
        help="Paths to the input files. File names must be unique.")
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("TMPDIR", "./tmpdir"),
        help="Directory to upload files to. Defaults to $TMPDIR if set, otherwise './tmpdir'.",
        type=Path)

    return parser.parse_args()


def main():
    """Coordinate execution of script."""
    args = get_args()
    logger.debug(f"File paths: {", ".join([f.name for f in args.file_paths])}")
    logger.debug(f"Output directory: {args.output_dir}")
    new_paths = move_files(file_paths=args.file_paths, output_dir=args.output_dir)
    keys = get_private_keys(file_paths=new_paths)
    try:
        decrypt_files(file_paths=new_paths, private_keys=keys)
    except Exception as e:
        remove_files(directory=args.output_dir)
        raise e


if __name__ == "__main__":
    main()
