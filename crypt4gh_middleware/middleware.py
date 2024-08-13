"""Crypt4GH middleware."""

from pathlib import Path

import flask


class CryptMiddleware:

    def __init__(self):
        self.request = None
        self.original_input_paths = []
        self.output_dir = Path("/vol/crypt/")

    def _set_original_input_paths(self):
        """Retrieve the input file paths."""
        for input_body in self.request.json["inputs"]:
            self.original_input_paths.append(input_body["path"])

    def _change_executor_paths(self):
        """Change input file paths in provided executors."""
        for executor_body in self.request.json["executors"]:
            for i, path in enumerate(executor_body["command"]):
                if path in self.original_input_paths:
                    executor_body["command"][i] = self.output_dir / path.split("/")[-1]

    def _add_decryption_executor(self):
        """Add the decryption executor to the executor list."""
        executor = {
            "image": "athitheyag/crypt4gh:1.0",
            "command": [
                "python3",
                "decrypt.py"
            ] + self.original_input_paths + [
                "--output-dir",
                self.output_dir
            ]
        }
        self.request.json["executors"].insert(0, executor)

    def apply_middleware(self, request: flask.Request):
        self.request = request
        self._set_original_input_paths()
        self._change_executor_paths()
        self._add_decryption_executor()

        return self.request



