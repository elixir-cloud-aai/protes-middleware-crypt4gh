""" Utility functions for tests."""
from functools import wraps
import contextlib
from pathlib import Path
import signal
from unittest import mock

INPUT_DIR = Path(__file__).parents[1]/"inputs"
INPUT_TEXT = "hello world from the input!"
S3_BUCKET_ENDPOINT = "host.docker.internal:9000"


@contextlib.contextmanager
def patch_cli(args):
    """Context manager that patches sys.argv."""
    with mock.patch("sys.argv", args):
        yield


def timeout(time_limit):
    """Decorator that enforces a time limit on a function."""
    def handler(signum, frame):
        raise TimeoutError(f"Task did not complete within {time_limit} seconds.")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(time_limit)
            result = func(*args, **kwargs)
            signal.alarm(0)
            return result
        return wrapper
    return decorator
