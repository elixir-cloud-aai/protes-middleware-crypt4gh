"""Crypt4GH middleware."""

from pathlib import Path

import flask

class PathNotAllowedError(ValueError):
    """Error raised when a path is not allowed."""

class CryptMiddleware:
    """Middleware class to handle Crypt4GH file inputs."""

    def __init__(self):
        self.original_input_paths = []

    def _add_decryption_executor(self, request: flask.Request) -> flask.Request:
        """Add the decryption executor to the executor list."""
        executor = {
            "image": "athitheyag/crypt4gh:1.0",
            "command": [
                "python3",
                "decrypt.py"
            ] + self.original_input_paths + [
                "--output-dir",
                "/vol/crypt/"
            ]
        }
        request.json["executors"].insert(0, executor)
        return request

    def _change_executor_paths(self, request: flask.Request) -> flask.Request:
        """Change original input file paths in executors to the output directory."""
        for executor_body in request.json["executors"]:
            for i, path in enumerate(executor_body["command"]):
                if path in self.original_input_paths:
                    executor_body["command"][i] = str(Path("/vol/crypt")/Path(path).name)
        return request

    def _change_output_paths(self, request: flask.Request) -> flask.Request:
        """Change original output file paths to the output directory if the output path is
        the same as an input path.

        Accounts for case where input file is modified in place in a TES request.
        """
        for output_body in request.json["outputs"]:
            path = output_body["path"]
            if path in self.original_input_paths:
                output_body["path"] = str(Path("/vol/crypt")/Path(path).name)
        return request

    def _check_volumes(self, request: flask.Request) -> None:
        """Check volumes to ensure none start with /vol/crypt.
        
        Raises:
            ValueError if volumes start with /vol/crypt.
        """
        for volume in request.json["volumes"]:
            if volume.startswith("/vol/crypt"):
                raise PathNotAllowedError("/vol/crypt is not allowed in volumes.")

    def _set_original_input_paths(self, request: flask.Request) -> None:
        """Retrieve and store the original input file paths.
        
        Raises:
            ValueError if any path starts with /vol/crypt.
        """
        for input_body in request.json["inputs"]:
            if input_body["path"].startswith("/vol/crypt"):
                raise PathNotAllowedError("/vol/crypt/ is not allowed in input path.")
            self.original_input_paths.append(input_body["path"])

    def apply_middleware(self, request: flask.Request) -> flask.Request:
        """Apply middleware to request."""
        self._set_original_input_paths(request)
        self._check_volumes(request)
        request = self._change_executor_paths(request)
        request = self._change_output_paths(request)
        request = self._add_decryption_executor(request)
        return request
