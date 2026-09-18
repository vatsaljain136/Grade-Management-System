from frontend.api_client.client import (
    get_request,
    post_request,
    put_request,
)


def get_semesters():
    return get_request("/semesters")


def get_semester(semester_id: int):
    return get_request(f"/semesters/{semester_id}")


def create_semester(semester_data: dict):
    return post_request(
        "/semesters",
        data=semester_data,
    )


def update_semester(semester_id: int, semester_data: dict):
    return put_request(
        f"/semesters/{semester_id}",
        data=semester_data,
    )