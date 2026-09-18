
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------
# Student API Tests
# ---------------------------------------------------------

def test_create_student():
    response = client.post(
        "/students/",
        json={
            "student_code": "TEST001",
            "name": "Test Student",
            "email": "teststudent@example.com",
            "batch": "2026",
        },
    )

    assert response.status_code in [200, 201]

    data = response.json()

    assert data["student_code"] == "TEST001"
    assert data["name"] == "Test Student"
    assert data["email"] == "teststudent@example.com"
    assert data["batch"] == "2026"


def test_get_student():
    response = client.get("/students/1")

    assert response.status_code in [200, 404]


def test_get_nonexistent_student():
    response = client.get("/students/999999")

    assert response.status_code == 404


def test_list_students():
    response = client.get("/students/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_update_student():
    response = client.put(
        "/students/1",
        json={
            "name": "Updated Student",
            "email": "updated@example.com",
        },
    )

    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()

        assert data["name"] == "Updated Student"
        assert data["email"] == "updated@example.com"


# ---------------------------------------------------------
# Validation Tests
# ---------------------------------------------------------

def test_create_student_missing_student_code():
    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "batch": "2026",
        },
    )

    assert response.status_code == 422


def test_create_student_missing_name():
    response = client.post(
        "/students/",
        json={
            "student_code": "TEST002",
            "email": "test@example.com",
            "batch": "2026",
        },
    )

    assert response.status_code == 422


def test_create_student_missing_email():
    response = client.post(
        "/students/",
        json={
            "student_code": "TEST003",
            "name": "Test Student",
            "batch": "2026",
        },
    )

    assert response.status_code == 422


def test_create_student_missing_batch():
    response = client.post(
        "/students/",
        json={
            "student_code": "TEST004",
            "name": "Test Student",
            "email": "test@example.com",
        },
    )

    assert response.status_code == 422
