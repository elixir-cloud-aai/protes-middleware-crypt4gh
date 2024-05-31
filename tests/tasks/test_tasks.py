"""Tests for I/O and decryption tasks"""

from time import sleep
import json
import requests
import pytest

from task_bodies import (
    output_dir,
    uppercase_task_body,
    decryption_task_body,
    uppercase_task_with_decryption_body
)

TES_URL = "http://localhost:8090/ga4gh/tes/v1"
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
WAIT_STATUSES = ("UNKNOWN", "INITIALIZING", "RUNNING")
INPUT_TEXT = "hello world from the input!"
TIME_LIMIT = 10


def create_task(tasks_body):
    """Creates task with the given task body."""
    return requests.post(
        url=f"{TES_URL}/tasks", headers=HEADERS, json=tasks_body, timeout=TIME_LIMIT
    )


def get_task(task_id):
    """Retrieves list of tasks."""
    return requests.get(
        url=f"{TES_URL}/tasks/{task_id}", headers=HEADERS, timeout=TIME_LIMIT
    )


def get_task_state(task_id):
    """Retrieves state of task until completion."""
    def wait_for_task_completion():
        nonlocal task_state
        elapsed_seconds = 0
        get_response = get_task(task_id)
        task_state = json.loads(get_response.text)["state"]
        while task_state in WAIT_STATUSES:
            if elapsed_seconds == TIME_LIMIT:
                raise requests.Timeout
            sleep(0.5)
            elapsed_seconds += 0.5
            get_response = get_task(task_id)
            task_state = json.loads(get_response.text)["state"]

    task_state = ""
    wait_for_task_completion()
    return task_state


@pytest.fixture(name="post_response", params=[
    uppercase_task_body,
    decryption_task_body,
    uppercase_task_with_decryption_body
])
def fixture_post_response(request):
    """Returns response received after creating task."""
    return create_task(request.param)


@pytest.fixture(name="task_state")
def fixture_task_state(post_response):
    """Returns state of task after completion."""
    task_id = json.loads(post_response.text)["id"]
    return get_task_state(task_id)


@pytest.mark.parametrize("filename,expected_output", [
    ("hello-upper.txt", INPUT_TEXT.upper()),
    ("hello-decrypted.txt", INPUT_TEXT),
    ("hello-upper-decrypt.txt", INPUT_TEXT.upper())
])
def test_task(post_response, task_state, filename, expected_output):
    """Test tasks for successful completion and intended behavior."""
    assert post_response.status_code == 200
    assert task_state == "COMPLETE"

    with open(output_dir/filename) as f:
        output = f.read()
        assert output == expected_output
        assert len(output) == len(expected_output)
        if "upper" in filename:
            assert output.isupper()
