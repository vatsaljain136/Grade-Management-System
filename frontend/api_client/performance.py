from frontend.api_client.client import get_request


def get_student_performance(student_id: int):
    return get_request(f"/performance/students/{student_id}")