from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student


def validate_student_code(
    db: Session,
    student_code: str,
    student_id: int | None = None,
) -> None:
    statement = select(Student).where(
        Student.student_code == student_code
    )

    existing_student = db.scalar(statement)

    if existing_student and existing_student.id != student_id:    #see validation.md basically if the student code already exists in the database and if it does, we check if the existing student's id is different from the provided student_id (if any). If they are different, it means that the student code is already taken by another student, and we raise a ValueError to indicate that the student code already exists.
        raise ValueError("Student code already exists.")