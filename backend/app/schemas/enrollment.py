from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    semester_id: int


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    semester_id: int

    model_config = {"from_attributes": True}