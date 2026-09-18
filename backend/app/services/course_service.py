from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(
    db: Session,
    course_data: CourseCreate,
) -> Course:
    existing_course = db.scalar(
        select(Course).where(
            Course.code == course_data.code
        )
    )

    if existing_course is not None:
        raise ValueError("Course code already exists.")

    course = Course(
        code=course_data.code,
        name=course_data.name,
        credits=course_data.credits,
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


def get_course(
    db: Session,
    course_id: int,
) -> Course | None:
    statement = select(Course).where(
        Course.id == course_id
    )

    return db.scalar(statement)


def list_courses(
    db: Session,
) -> list[Course]:
    statement = (
        select(Course)
        .order_by(Course.id)
    )

    return list(
        db.scalars(statement).all()
    )


def update_course(
    db: Session,
    course_id: int,
    course_data: CourseUpdate,
) -> Course | None:
    course = get_course(
        db=db,
        course_id=course_id,
    )

    if course is None:
        return None

    update_data = course_data.model_dump(
        exclude_unset=True
    )

    if "code" in update_data:
        existing_course = db.scalar(
            select(Course).where(
                Course.code == update_data["code"],
                Course.id != course_id,
            )
        )

        if existing_course is not None:
            raise ValueError(
                "Course code already exists."
            )

    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course