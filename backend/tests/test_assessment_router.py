from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_assessment():
    response = client.post(
        "/assessments/",
        json={
            "course_id": 1,
            "semester_id": 1,
            "title": "Mid Term Exam",
            "type": "exam",
            "maximum_marks": 100,
            "weight": 2,
        },
    )

    print("CREATE RESPONSE:", response.json())

    assert response.status_code == 200


def test_get_assessment():
    response = client.get(
        "/assessments/1"
    )

    assert response.status_code == 200


def test_list_assessments():
    response = client.get(
        "/assessments/"
    )

    assert response.status_code == 200


def test_update_assessment():
    response = client.put(
        "/assessments/1",
        json={
            "title": "Updated Mid Term Exam",
        },
    )

    assert response.status_code == 200


def test_get_assessment_not_found():
    response = client.get(
        "/assessments/9999"
    )

    assert response.status_code == 404


def test_update_assessment_not_found():
    response = client.put(
        "/assessments/9999",
        json={
            "title": "Updated Assessment",
        },
    )

    assert response.status_code == 404


def test_list_assessments_with_pagination():
    response = client.get(
        "/assessments/?page=1&page_size=10"
    )

    assert response.status_code == 200