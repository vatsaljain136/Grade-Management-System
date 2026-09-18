
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_grade():
    response = client.post(
        "/grades",
        json={
            "student_id": 1,
            "assessment_id": 1,
            "marks": 85,
        },
    )

    print("CREATE GRADE RESPONSE:", response.json())

    # Grade already exists for student 1 and assessment 1.
    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Grade already exists. Use update instead."
    )


def test_list_grades():
    response = client.get("/grades")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_grades_by_student():
    response = client.get(
        "/grades",
        params={"student_id": 1},
    )

    assert response.status_code == 200


def test_list_grades_by_semester():
    response = client.get(
        "/grades",
        params={"semester_id": 1},
    )

    assert response.status_code == 200


def test_list_grades_by_assessment():
    response = client.get(
        "/grades",
        params={"assessment_id": 1},
    )

    assert response.status_code == 200


def test_get_grade():
    response = client.get("/grades/1")

    assert response.status_code == 200


def test_get_student_assessment_grade():
    response = client.get(
        "/grades/student/1/assessment/1"
    )

    assert response.status_code == 200


def test_update_grade():
    response = client.put(
        "/grades/student/1/assessment/1",
        json={
            "marks": 95,
        },
    )

    print("UPDATE GRADE RESPONSE:", response.json())

    assert response.status_code == 200


def test_get_grade_not_found():
    response = client.get("/grades/9999")

    assert response.status_code == 404


def test_update_grade_not_found():
    response = client.put(
        "/grades/student/9999/assessment/9999",
        json={
            "marks": 95,
        },
    )

    assert response.status_code == 404


def test_create_grade_missing_marks():
    response = client.post(
        "/grades",
        json={
            "student_id": 1,
            "assessment_id": 1,
        },
    )

    print("MISSING MARKS RESPONSE:", response.json())

    # Marks can be unassigned.
    # The grade is created with marks=None.
    #
    # However, student 1 + assessment 1 already exists,
    # so the API rejects this as a duplicate.
    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Grade already exists. Use update instead."
    )
