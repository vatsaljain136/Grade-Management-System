
from io import BytesIO

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


# ---------------------------------------------------------
# Grade Upload API Tests
# ---------------------------------------------------------

def test_upload_grades():
    csv_content = (
        "student_id,assessment_id,marks_obtained\n"
        "1,1,85\n"
        "2,1,90\n"
    )

    file = {
        "file": (
            "grades.csv",
            BytesIO(csv_content.encode("utf-8")),
            "text/csv",
        )
    }

    response = client.post(
        "/uploads/grades",
        files=file,
    )

    assert response.status_code in [200, 201]


def test_upload_grades_empty_file():
    file = {
        "file": (
            "grades.csv",
            BytesIO(b""),
            "text/csv",
        )
    }

    response = client.post(
        "/uploads/grades",
        files=file,
    )

    assert response.status_code == 200


def test_upload_grades_without_file():
    response = client.post(
        "/uploads/grades"
    )

    assert response.status_code == 422


def test_upload_invalid_file_type():
    file = {
        "file": (
            "grades.txt",
            BytesIO(b"this is not a csv file"),
            "text/plain",
        )
    }

    response = client.post(
        "/uploads/grades",
        files=file,
    )

    assert response.status_code == 200
