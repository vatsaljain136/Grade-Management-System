from frontend.api_client.client import (
    get_request,
    post_request,
    put_request,
)


def get_courses():
    return get_request("/courses")


def get_course(course_id: int):
    return get_request(f"/courses/{course_id}")


def create_course(course_data: dict):
    return post_request(
        "/courses",
        data=course_data,
    )


def update_course(course_id: int, course_data: dict):
    return put_request(
        f"/courses/{course_id}",
        data=course_data,
    )