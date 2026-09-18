from frontend.api_client.client import (
    get_request,
    post_request,
    put_request,
)


def get_grades(
    student_id: int | None = None,
    semester_id: int | None = None,
    assessment_id: int | None = None,
):
    params = {}

    if student_id is not None:
        params["student_id"] = student_id

    if semester_id is not None:
        params["semester_id"] = semester_id

    if assessment_id is not None:
        params["assessment_id"] = assessment_id

    return get_request(
        "/grades",
        params=params,
    )


def get_grade(grade_id: int):
    return get_request(
        f"/grades/{grade_id}"
    )


def get_student_assessment_grade(
    student_id: int,
    assessment_id: int,
):
    return get_request(
        f"/grades/student/{student_id}/assessment/{assessment_id}"
    )


def create_grade(grade_data: dict):
    return post_request(
        "/grades",
        data=grade_data,
    )


def update_grade(
    student_id: int,
    assessment_id: int,
    grade_data: dict,
):
    return put_request(
        f"/grades/student/{student_id}/assessment/{assessment_id}",
        data=grade_data,
    )