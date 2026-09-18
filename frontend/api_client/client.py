import requests

BASE_URL = "http://127.0.0.1:8000"


def get_request(endpoint: str, params: dict | None = None):    # for example ->params = {"page": 1,"page_size": 10}
    response = requests.get(
        f"{BASE_URL}{endpoint}",
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def post_request(endpoint: str, data=None, files=None):
    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=data,
        files=files,
        timeout=30,
    )

    response.raise_for_status()     #This checks whether the HTTP request was successful. for example 200 OK.

    return response.json()


def put_request(endpoint: str, data=None):
    response = requests.put(
        f"{BASE_URL}{endpoint}",
        json=data,
        timeout=10,
    )

    response.raise_for_status()  #raise_for_status() raises an exception.

    return response.json()