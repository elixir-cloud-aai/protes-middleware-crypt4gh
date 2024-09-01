"""Tests for I/O and decryption tasks"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep

import pytest
import requests

from task_bodies import (
    get_decryption_task_body,
    get_uppercase_task_body,
    get_uppercase_task_with_decryption_body,
)
from tests.utils import INPUT_TEXT, timeout

TES_URL = "http://localhost:8090/ga4gh/tes/v1"
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
WAIT_STATUSES = ("UNKNOWN", "INITIALIZING", "RUNNING", "QUEUED")


def wait_for_file_download(filename, output_path):
    """Waits for file with given filename to download."""
    while not (output_path/filename).exists():
        sleep(1)


@pytest.fixture(name="output_dir")
def fixture_output_dir():
    """Returns temporary directory to store task outputs."""
    return Path(TemporaryDirectory().name)


@pytest.fixture(name="task")
def fixture_task(request, output_dir):
    """Returns response received after creating task."""
    return requests.post(
        url=f"{TES_URL}/tasks", headers=HEADERS, json=request.param(output_dir)
    )


@pytest.fixture(name="final_task_info")
@timeout(time_limit=60)
def fixture_final_task_info(task):
    """Returns task information after completion."""
    assert task.status_code == 200
    task_id = json.loads(task.text)["id"]
    task_info = None
    for _ in range(30):
        task_info = requests.get(
            url=f"{TES_URL}/tasks/{task_id}", headers=HEADERS
        )
        task_state = json.loads(task_info.text)["state"]
        if task_state not in WAIT_STATUSES:
            break
        sleep(1)

    return json.loads(task_info.text)


@pytest.mark.parametrize("task,filename,expected_output", [
    (get_uppercase_task_body, "hello-upper.txt", INPUT_TEXT.upper()),
    (get_decryption_task_body, "hello-decrypted.txt", INPUT_TEXT),
    (get_uppercase_task_with_decryption_body, "hello-upper-decrypt.txt", INPUT_TEXT.upper())
], indirect=["task"])
@timeout(time_limit=10)
def test_task(task, final_task_info, filename, expected_output, output_dir):  # pylint: disable=unused-argument
    """Test tasks for successful completion and intended behavior."""
    assert final_task_info["state"] == "COMPLETE"

    wait_for_file_download(filename=filename, output_path=output_dir)
    with open(output_dir/filename, encoding="utf-8") as f:
        output = f.read()
        assert output == expected_output
        true_result = output.isupper() if "upper" in filename else not output.isupper()
        assert true_result
