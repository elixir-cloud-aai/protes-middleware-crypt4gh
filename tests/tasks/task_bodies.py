"""TES task request bodies used by tests"""

from tests.utils import INPUT_DIR

def get_uppercase_task_body(tmp_dir):
    """Returns TES task body that makes the contents of a file uppercase."""
    return {
        "name": "Hello world",
        "inputs": [
            {
                "url": f"file://{INPUT_DIR}/hello.txt",
                "path": "/inputs/hello.txt",
                "type": "FILE"
            },
            {
                "url": f"file://{INPUT_DIR}/make_uppercase.py",
                "path": "/inputs/make_uppercase.py",
                "type": "FILE"
            }
        ],
        "outputs": [
            {
                "url": f"file://{tmp_dir}/hello-upper.txt",
                "path": "/outputs/hello-upper.txt",
                "type": "FILE"
            }
        ],
        "executors": [
            {
                "image": "python:3",
                "command": [
                    "python3",
                    "/inputs/make_uppercase.py",
                    "/inputs/hello.txt"
                ],
                "stdout": "/outputs/hello-upper.txt"
            }
        ]
    }


def get_decryption_task_body(tmp_dir):
    """Returns TES task body that decrypts a crypt4GH file."""
    return {
        "name": "Decrypt with secret key as environment variable",
        "inputs": [
            {
                "url": f"file://{INPUT_DIR}/hello.c4gh",
                "path": "/inputs/hello.c4gh",
                "type": "FILE"
            },
            {
                "url": f"file://{INPUT_DIR}/alice.sec",
                "path": "/inputs/alice.sec",
                "type": "FILE"
            },
            {
                "url": f"file://{INPUT_DIR}/decrypt.sh",
                "path": "/inputs/decrypt.sh",
                "type": "FILE"
            }
        ],
        "outputs": [
            {
                "url": f"file://{tmp_dir}/hello-decrypted.txt",
                "path": "/outputs/hello-decrypted.txt",
                "type": "FILE"
            }
        ],
        "executors": [
            {
                "image": "athitheyag/c4gh:1.0",
                "command": ["bash", "/inputs/decrypt.sh"],
                "env": {
                    "INPUT_LOC": "/inputs/hello.c4gh",
                    "OUTPUT_LOC": "/outputs/hello-decrypted.txt",
                    "SECRET": "/inputs/alice.sec"
                }
            }
        ]
    }


def get_uppercase_task_with_decryption_body(tmp_dir):
    """Returns TES task body that makes the contents of a crypt4GH file uppercase."""
    return {
        "name": "Decrypt with secret key as environment variable",
        "inputs": [
            {
                "url": f"file://{INPUT_DIR}/hello.c4gh",
                "path": "/inputs/hello.c4gh",
                "type": "FILE"
            },
            {
                "url": f"file://{INPUT_DIR}/alice.sec",
                "path": "/inputs/alice.sec",
                "type": "FILE"
            },
            {
                "url": f"file://{INPUT_DIR}/decrypt.sh",
                "path": "/inputs/decrypt.sh",
                "type": "FILE"
            },
            {
                "url": f"file://{INPUT_DIR}/make_uppercase.py",
                "path": "/inputs/make_uppercase.py",
                "type": "FILE"
            }
        ],
        "outputs": [
            {
                "url": f"file://{tmp_dir}/hello-upper-decrypt.txt",
                "path": "/outputs/hello-upper-decrypt.txt",
                "type": "FILE"
            }
        ],
        "executors": [
            {
                "image": "athitheyag/c4gh:1.0",
                "command": ["bash", "/inputs/decrypt.sh"],
                "env": {
                    "INPUT_LOC": "/inputs/hello.c4gh",
                    "OUTPUT_LOC": "/vol/A/inputs/hello.txt",
                    "SECRET": "/inputs/alice.sec"
                }
            },
            {
                "image": "python:3",
                "command": [
                    "python3",
                    "/inputs/make_uppercase.py",
                    "/vol/A/inputs/hello.txt"
                ],
                "stdout": "/outputs/hello-upper-decrypt.txt"
            }
        ],
        "volumes": [
            "/vol/A/inputs"
        ]
}
