
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# ---------------------------------------------------------
# Student Validation
# ---------------------------------------------------------

def test_student_invalid_email():
    response = client.post(
        "/students/",
        json={
            "name": "Test Student",
            "email": "invalid-email",
            "roll_number": "VAL001",
        },
    )

    assert response.status_code == 422


def test_student_empty_name():
    response = client.post(
        "/students/",
        json={
            "name": "",
            "email": "test@example.com",
            "roll_number": "VAL002",
        },
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Assessment Validation
# ---------------------------------------------------------

def test_assessment_missing_required_fields():
    response = client.post(
        "/assessments/",
        json={},
    )

    assert response.status_code == 422


def test_assessment_invalid_marks():
    response = client.post(
        "/assessments/",
        json={
            "course_id": 1,
            "semester_id": 1,
            "title": "Test Exam",
            "type": "exam",
            "maximum_marks": -100,
            "weight": 20,
        },
    )

    assert response.status_code == 422


def test_assessment_invalid_weight():
    response = client.post(
        "/assessments/",
        json={
            "course_id": 1,
            "semester_id": 1,
            "title": "Test Exam",
            "type": "exam",
            "maximum_marks": 100,
            "weight": -10,
        },
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Grade Validation
# ---------------------------------------------------------

def test_grade_missing_required_fields():
    response = client.post(
        "/grades/",
        json={},
    )

    assert response.status_code == 422


def test_grade_negative_marks():
    response = client.post(
        "/grades/",
        json={
            "student_id": 1,
            "assessment_id": 1,
            "marks": -10,
        },
    )

    assert response.status_code == 422


# ---------------------------------------------------------
# Invalid IDs
# ---------------------------------------------------------

def test_invalid_student_id():
    response = client.get("/students/abc")

    assert response.status_code == 422


def test_invalid_assessment_id():
    response = client.get("/assessments/abc")

    assert response.status_code == 422


def test_invalid_grade_id():
    response = client.get("/grades/abc")

    assert response.status_code == 422
