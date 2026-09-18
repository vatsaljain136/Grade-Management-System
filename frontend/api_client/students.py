from frontend.api_client.client import (
    get_request,
    post_request,
    put_request,
)


def get_students(
    search: str | None = None,
    batch: str | None = None,
    page: int = 1,
    page_size: int = 10,
):
    params = {
        "search": search,
        "batch": batch,
        "page": page,
        "page_size": page_size,
    }

    return get_request(
        "/students",
        params=params,
    )


def get_student(student_id: int):
    return get_request(
        f"/students/{student_id}"
    )


def create_student(student_data: dict):
    return post_request(
        "/students",
        data=student_data,
    )


def update_student(
    student_id: int,
    student_data: dict,
):
    return put_request(
        f"/students/{student_id}",
        data=student_data,
    )