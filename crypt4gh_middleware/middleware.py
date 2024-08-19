"""Crypt4GH middleware."""

from pathlib import Path

import flask

class PathNotAllowedError(ValueError):
    """Error raised when a path is not allowed."""

class CryptMiddleware:
    """Middleware class to handle Crypt4GH file inputs."""

    def __init__(self):
        self.request = None
        self.original_input_paths = []
        self.output_dir = Path("/vol/crypt/")

    def _add_decryption_executor(self) -> None:
        """Add the decryption executor to the executor list."""
        executor = {
            "image": "athitheyag/crypt4gh:1.0",
            "command": [
                "python3",
                "decrypt.py"
            ] + self.original_input_paths + [
                "--output-dir",
                str(self.output_dir)
            ]
        }
        self.request.json["executors"].insert(0, executor)

    def _change_executor_paths(self) -> None:
        """Change original input file paths in executors to the output directory."""
        for executor_body in self.request.json["executors"]:
            for i, path in enumerate(executor_body["command"]):
                if path in self.original_input_paths:
                    executor_body["command"][i] = str(self.output_dir/Path(path).name)

    def _change_output_paths(self) -> None:
        """Change original output file paths to the output directory if the output path is
        the same as an input path.

        Accounts for case where input file is modified in place in a TES request.
        """
        for output_body in self.request.json["outputs"]:
            path = output_body["path"]
            if path in self.original_input_paths:
                output_body["path"] = str(self.output_dir/Path(path).name)

    def _check_volumes(self) -> None:
        """Check volumes to ensure none start with /vol/crypt.
        
        Raises:
            ValueError if volumes start with /vol/crypt.
        """
        for volume in self.request.json["volumes"]:
            if volume.startswith("/vol/crypt"):
                raise PathNotAllowedError("/vol/crypt/ is not allowed in volumes.")

    def _set_original_input_paths(self) -> None:
        """Retrieve and store the original input file paths.
        
        Raises:
            ValueError if any path starts with /vol/crypt.
        """
        for input_body in self.request.json["inputs"]:
            if input_body["path"].startswith("/vol/crypt"):
                raise PathNotAllowedError("/vol/crypt/ is not allowed in input path.")
            self.original_input_paths.append(input_body["path"])

    def apply_middleware(self, request: flask.Request) -> flask.Request:
        """Apply middleware to request."""
        self.request = request
        self._set_original_input_paths()
        self._check_volumes()
        self._change_executor_paths()
        self._change_output_paths()
        self._add_decryption_executor()

        return self.request
