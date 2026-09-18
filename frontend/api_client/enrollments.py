from frontend.api_client.client import (
    get_request,
    post_request,
)


def get_enrollments(
    student_id: int | None = None,
    course_id: int | None = None,
    semester_id: int | None = None,
):
    params = {}

    if student_id is not None:
        params["student_id"] = student_id

    if course_id is not None:
        params["course_id"] = course_id

    if semester_id is not None:
        params["semester_id"] = semester_id

    return get_request(
        "/enrollments",
        params=params,
    )


def create_enrollment(
    student_id: int,
    course_id: int,
    semester_id: int,
):
    return post_request(
        "/enrollments",
        data={
            "student_id": student_id,
            "course_id": course_id,
            "semester_id": semester_id,
        },
    )