"""Crypt4GH middleware."""
import uuid
from copy import deepcopy
from pathlib import Path

import flask
from pro_tes.middleware.abstract_middleware import AbstractMiddleware

# Decrypted files must be written to a writable path inside the container.
# e.g. Funnel runs containers with `--read-only` and mounts only specific dirs as RW
VOLUME_PATH = f"/vol/{str(uuid.uuid4().hex)}"
# mypy: disable-error-code="index"

class PathNotAllowedException(ValueError):
    """Raised when a path is not allowed."""

class EmptyPayloadException(ValueError):
    """Raised when request has no JSON payload."""

class CryptMiddleware(AbstractMiddleware):
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
                VOLUME_PATH
            ]
        }
        request.json["executors"].insert(0, executor)
        return request

    def _add_volume(self, request: flask.Request) -> flask.Request:
        """Check volumes to ensure none start with VOLUME_PATH and add VOLUME_PATH.

        Raises:
            PathNotAllowedError if volumes start with VOLUME_PATH.
        """
        for volume in request.json["volumes"]:
            if volume.startswith(VOLUME_PATH):
                raise PathNotAllowedException(f"{VOLUME_PATH} is not allowed in volumes.")
        request.json["volumes"].append(VOLUME_PATH)
        return request

    def _change_executor_paths(self, request: flask.Request) -> flask.Request:
        """Change original input file paths in executors to the output directory."""
        for executor_body in request.json["executors"]:
            for i, path in enumerate(executor_body["command"]):
                if path in self.original_input_paths:
                    executor_body["command"][i] = str(Path(VOLUME_PATH)/Path(path).name)
        return request

    def _check_output_paths(self, request: flask.Request) -> None:
        """Check if an input path is present in the output paths. Inplace
        modifications are not allowed.

        Raises:
            PathNotAllowedError if input path is present in output paths.
        """
        for output_body in request.json["outputs"]:
            path = output_body["path"]
            if path in self.original_input_paths:
                raise PathNotAllowedException(f"{path} is being modified inplace.")

    def _set_original_input_paths(self, request: flask.Request) -> None:
        """Retrieve and store the original input file paths.
        
        Raises:
            PathNotAllowedError if any path starts with VOLUME_PATH.
        """
        for input_body in request.json["inputs"]:
            path = input_body.get("path")
            if path.startswith(VOLUME_PATH):
                raise PathNotAllowedException(f"{VOLUME_PATH} is not allowed in input path.")
            if str(path).lower().endswith(".c4gh"):
                self.original_input_paths.append(path)

    def apply_middleware(self, request: flask.Request) -> flask.Request:
        """Apply middleware to request."""
        if not request.json:
            raise EmptyPayloadException("Request JSON has no payload.")
        self._set_original_input_paths(request)
        self._check_output_paths(request)
        request = self._change_executor_paths(request)
        request = self._add_volume(request)
        request = self._add_decryption_executor(request)
        tes_urls=deepcopy(
                flask.current_app.config.foca.custom.tes.service_list  # type: ignore
        )
        self.tes_urls = list(set(tes_urls))
        request.json["tes_urls"] = self.tes_urls
        return request
