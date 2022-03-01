from app import app
import json
import pytest
import requests

# You are welcome to use a Flask client fixture or test the running instance, as below
BASE_URL = 'http://127.0.0.1:5000/'


def test_startup():
    """Asserts that your service starts and responds"""
    r = requests.get(BASE_URL)
    assert r.status_code == 200 and r.text == "OK"


@pytest.mark.parametrize("train", [
    {'id': 'TOMO', 'schedule': [180, 640, 1440]},
    {'id': 'FOMO', 'schedule': [440, 640]},
    {'id': '1', 'schedule': [100, 220, 300]}
])
@pytest.mark.parametrize("error", [
    {'id': 'TOMO', 'schedule': [180, 640, 1440]},
    {'id': 'TOOLONG', 'schedule': [440, 640]},
    {'id': 'BAD-', 'schedule': [440, 640]},
    {'id': 1234, 'schedule': [440, 640]},
    {'id': 'INT', 'schedule': 100},
    {'id': 'BAD', 'schedule': ["-1o", 100]},
    {'id': 'BIG', 'schedule': [440, 50000]},
    {'id': 'SMOL', 'schedule': [-1, 640]},
])
def test_add(train, error):
    """Asserts that schedules are added and returned as expected"""

    requests.post(f"{BASE_URL}/trains", json=train)
    r = requests.get(f"{BASE_URL}/trains/{train['id']}")

    assert r.json() == train['schedule']

    r = requests.post(f"{BASE_URL}/trains", json=error)
    assert r.status_code == 400


def test_next():

    time_header = {"time": "500"} # case where next time is before next day
    r = requests.get(f"{BASE_URL}/trains/next", headers = time_header)
    assert r.json() == 640

    time_header["time"] = "700" # case where next time isn't until next day and must "wrap around"
    r = requests.get(f"{BASE_URL}/trains/next", headers = time_header)
    assert r.json() == 640

    time_header["time"] = "4000" # time out of bounds
    r = requests.get(f"{BASE_URL}/trains/next", headers = time_header)
    assert r.status_code == 400

    time_header["time"] = "-1" # time out of bounds
    r = requests.get(f"{BASE_URL}/trains/next", headers = time_header)
    assert r.status_code == 400

    time_header["time"] = "abc" # invalid time
    r = requests.get(f"{BASE_URL}/trains/next", headers = time_header)
    assert r.status_code == 400

    time_header["time"] = "" # invalid header
    r = requests.get(f"{BASE_URL}/trains/next", headers = time_header)
    assert r.status_code == 400

