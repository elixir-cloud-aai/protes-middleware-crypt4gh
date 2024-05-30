from pathlib import Path

DIR = Path(__file__).parents[2]
input_dir = DIR / "inputs"
output_dir = DIR / "outputs"

uppercase_task_body = {
        "name": "Hello world",
        "inputs": [
            {
                "url": f"file://{input_dir}/hello.txt",
                "path": "/inputs/hello.txt",
                "type": "FILE"
            },
            {
                "url": f"file://{input_dir}/make_uppercase.py",
                "path": "/inputs/make_uppercase.py",
                "type": "FILE"
            }
        ],
        "outputs": [
            {
                "url": f"file://{output_dir}/hello-upper.txt",
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

decryption_task_body = {
        "name": "Decrypt with secret key as environment variable",
        "inputs": [
            {
                "url": f"file://{input_dir}/hello.c4gh",
                "path": "/inputs/hello.c4gh",
                "type": "FILE"
            },
            {
                "url": f"file://{input_dir}/alice.sec",
                "path": "/inputs/alice.sec",
                "type": "FILE"
            },
            {
                "url": f"file://{input_dir}/decrypt.sh",
                "path": "/inputs/decrypt.sh",
                "type": "FILE"
            }
        ],
        "outputs": [
            {
                "url": f"file://{output_dir}/hello-decrypted.txt",
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

uppercase_task_with_decryption_body = {
    "name": "Decrypt with secret key as environment variable",
    "inputs": [
        {
            "url": f"file://{input_dir}/hello.c4gh",
            "path": "/inputs/hello.c4gh",
            "type": "FILE"
        },
        {
            "url": f"file://{input_dir}/alice.sec",
            "path": "/inputs/alice.sec",
            "type": "FILE"
        },
        {
            "url": f"file://{input_dir}/decrypt.sh",
            "path": "/inputs/decrypt.sh",
            "type": "FILE"
        },
        {
            "url": f"file://{input_dir}/make_uppercase.py",
            "path": "/inputs/make_uppercase.py",
            "type": "FILE"
        }
    ],
    "outputs": [
        {
            "url": f"file://{output_dir}/hello-upper-decrypt.txt",
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
