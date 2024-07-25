"""Tests for I/O and decryption tasks"""

import json
import signal
from time import sleep

import pytest
import requests

from task_bodies import (
    output_dir,
    uppercase_task_body,
    decryption_task_body,
    uppercase_task_with_decryption_body
)

TES_URL = "http://localhost:8090/ga4gh/tes/v1"
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
WAIT_STATUSES = ("UNKNOWN", "INITIALIZING", "RUNNING", "QUEUED")
INPUT_TEXT = "hello world from the input!"
TIME_LIMIT = 60


def timeout(func):
    """Decorator that enforces a time limit on a function."""
    def handler(signum, frame):
        raise TimeoutError(f"Task did not complete within {TIME_LIMIT} seconds")

    def wrapper(*args, **kwargs):
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(TIME_LIMIT)
        func(*args, **kwargs)
        signal.alarm(0)

    return wrapper


@timeout
def wait_for_file_to_download(filename):
    """Waits for file with given filename to download."""
    while not (output_dir/filename).exists():
        sleep(1)


@pytest.fixture(name="task")
def fixture_task(request):
    """Returns response received after creating task."""
    return requests.post(
        url=f"{TES_URL}/tasks", headers=HEADERS, json=request.param, timeout=TIME_LIMIT
    )


@pytest.fixture(name="final_task_state")
def fixture_final_task_state(task):
    """Returns state of task after completion."""
    def get_task():
        return requests.get(
            url=f"{TES_URL}/tasks/{task_id}", headers=HEADERS, timeout=TIME_LIMIT
        )

    @timeout
    def wait_for_task_completion():
        nonlocal final_task_state
        get_response = get_task()
        final_task_state = json.loads(get_response.text)["state"]
        while final_task_state in WAIT_STATUSES:
            sleep(1)
            get_response = get_task()
            final_task_state = json.loads(get_response.text)["state"]

    task_id = json.loads(task.text)["id"]
    final_task_state = ""
    wait_for_task_completion()
    return final_task_state


@pytest.mark.parametrize("task,filename,expected_output", [
    (uppercase_task_body, "hello-upper.txt", INPUT_TEXT.upper()),
    (decryption_task_body, "hello-decrypted.txt", INPUT_TEXT),
    (uppercase_task_with_decryption_body, "hello-upper-decrypt.txt", INPUT_TEXT.upper())
], indirect=['task'])
def test_task(task, final_task_state, filename, expected_output):
    """Test tasks for successful completion and intended behavior."""
    assert task.status_code == 200
    assert final_task_state == "COMPLETE"

    wait_for_file_to_download(filename)

    with open(output_dir/filename, encoding="utf-8") as f:
        output = f.read()
        assert output == expected_output
        assert len(output) == len(expected_output)
        if "upper" in filename:
            assert output.isupper()
