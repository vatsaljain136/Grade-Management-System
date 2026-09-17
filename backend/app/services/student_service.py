from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.validation.student_validation import validate_student_code


def create_student(
    db: Session,
    student_data: StudentCreate,  #pydantic model for student creation and data validation.
) -> Student:
    # Check whether the student code already exists.
    validate_student_code(
        db,
        student_data.student_code,
    )

    student = Student(
        student_code=student_data.student_code,
        name=student_data.name,
        email=student_data.email,
        batch=student_data.batch,
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student


def get_student(
    db: Session,
    student_id: int,
) -> Student | None:
    statement = select(Student).where(
        Student.id == student_id
    )

    return db.scalar(statement)


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate,
) -> Student | None:
    student = get_student(db, student_id)

    if student is None:
        return None

    # Only validate the code when it is actually being changed.
    if (
        student_data.student_code is not None
        and student_data.student_code != student.student_code
    ):
        validate_student_code(                           #basucally we are checking if the student code is being updated, and if it is, we validate the new student code to ensure it doesn't already exist in the database for another student. This prevents duplicate student codes.
            db,student_data.student_code,
            student_id=student_id,
        )

    update_data = student_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student(
    db: Session,
    student_id: int,
) -> bool:
    student = get_student(db, student_id)

    if student is None:
        return False

    db.delete(student)
    db.commit()

    return True