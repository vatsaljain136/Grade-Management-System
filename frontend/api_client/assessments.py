from frontend.api_client.client import (
    get_request,
    post_request,
    put_request,
)


def get_assessments(
    course_id: int | None = None,
    semester_id: int | None = None,
):
    params = {}

    if course_id is not None:
        params["course_id"] = course_id

    if semester_id is not None:
        params["semester_id"] = semester_id

    return get_request(
        "/assessments",
        params=params,
    )


def get_assessment(assessment_id: int):
    return get_request(
        f"/assessments/{assessment_id}"
    )


def create_assessment(assessment_data: dict):
    return post_request(
        "/assessments",
        data=assessment_data,
    )


def update_assessment(
    assessment_id: int,
    assessment_data: dict,
):
    return put_request(
        f"/assessments/{assessment_id}",
        data=assessment_data,
    )