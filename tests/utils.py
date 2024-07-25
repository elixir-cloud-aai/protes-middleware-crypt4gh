""" Utility functions for tests."""
from functools import wraps
import signal


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
