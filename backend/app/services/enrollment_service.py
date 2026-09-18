from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment


def create_enrollment(
    db: Session,
    student_id: int,
    course_id: int,
    semester_id: int,
) -> Enrollment:

    existing_enrollment = db.scalar(
        select(Enrollment).where(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id,
            Enrollment.semester_id == semester_id,
        )
    )

    if existing_enrollment is not None:
        raise ValueError(
            "Student is already enrolled in this course for this semester."
        )

    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
        semester_id=semester_id,
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


def list_enrollments(
    db: Session,
    student_id: int | None = None,
    course_id: int | None = None,
    semester_id: int | None = None,
) -> list[Enrollment]:

    statement = select(Enrollment)

    if student_id is not None:
        statement = statement.where(
            Enrollment.student_id == student_id
        )

    if course_id is not None:
        statement = statement.where(
            Enrollment.course_id == course_id
        )

    if semester_id is not None:
        statement = statement.where(
            Enrollment.semester_id == semester_id
        )

    statement = statement.order_by(Enrollment.id)

    return list(db.scalars(statement).all())