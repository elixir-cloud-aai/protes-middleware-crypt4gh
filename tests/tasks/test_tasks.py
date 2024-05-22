from time import sleep
import json
import requests

from task_bodies import (
    output_dir,
    uppercase_task_body,
    decryption_task_body,
    uppercase_task_with_decryption_body
)

tes_url = "http://localhost:8090/ga4gh/tes/v1"
headers = {"accept": "application/json", "Content-Type": "application/json"}
WAIT_STATUSES = ("UNKNOWN", "INITIALIZING", "RUNNING")


def create_task(tasks_body):
    post_response = requests.post(
            url=f"{tes_url}/tasks", headers=headers, json=tasks_body
        )

    return post_response


def get_task(task_id):
    get_response = requests.get(
        url=f"{tes_url}/tasks/{task_id}", headers=headers
        )

    return get_response


def get_task_state(task_id):

    def wait_for_task_completion():
        nonlocal task_state
        get_response = get_task(task_id)
        task_state = json.loads(get_response.text)["state"]
        while task_state in WAIT_STATUSES:
            sleep(0.5)
            get_response = get_task(task_id)
            task_state = json.loads(get_response.text)["state"]

    task_state = ""
    wait_for_task_completion()
    return task_state


def test_uppercase_task():
    """Test task that outputs uppercase version of input"""

    post_response = create_task(uppercase_task_body)
    assert post_response.status_code == 200

    task_id = json.loads(post_response.text)["id"]
    task_state = get_task_state(task_id)
    assert task_state == "COMPLETE"

    with open(output_dir/"hello-upper.txt") as f:
        output = f.readline()
        assert output == "HELLO WORLD FROM THE INPUT!"


def test_decryption_task():
    """Test task that takes outputs decrypted version of input"""

    post_response = create_task(decryption_task_body)
    assert post_response.status_code == 200

    task_id = json.loads(post_response.text)["id"]
    task_state = get_task_state(task_id)
    assert task_state == "COMPLETE"

    with open(output_dir / "hello-decrypted.txt") as f:
        output = f.readline()
        assert output == "hello world from the input!"


def test_uppercase_task_with_decryption():
    """Test task that decrypts input and outputs uppercase version of input"""

    post_response = create_task(uppercase_task_with_decryption_body)
    assert post_response.status_code == 200

    task_id = json.loads(post_response.text)["id"]
    task_state = get_task_state(task_id)
    assert task_state == "COMPLETE"

    with open(output_dir / "hello-upper-decrypt.txt") as f:
        output = f.readline()
        assert output == "HELLO WORLD FROM THE INPUT!"
