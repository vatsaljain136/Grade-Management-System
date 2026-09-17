from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate
from app.validation.grade_validation import validate_grade


def create_grade(
    db: Session,
    grade_data: GradeCreate,
) -> Grade:
    assessment = validate_grade(            #checking wether the grades are valid or not(like grade is +ve and less than max marks)
        db=db,
        student_id=grade_data.student_id,
        assessment_id=grade_data.assessment_id,
        marks=grade_data.marks,
    )

    existing_grade = db.scalar(
        select(Grade).where(
            Grade.student_id == grade_data.student_id,
            Grade.assessment_id == grade_data.assessment_id,
        )
    )

    if existing_grade is not None:
        raise ValueError(
            "Grade already exists. Use update instead."
        )

    grade = Grade(
        student_id=grade_data.student_id,
        assessment_id=grade_data.assessment_id,
        marks=grade_data.marks,
    )

    db.add(grade)
    db.commit()
    db.refresh(grade)

    return grade


def get_grade(
    db: Session,
    grade_id: int,
) -> Grade | None:
    statement = select(Grade).where(
        Grade.id == grade_id
    )

    return db.scalar(statement)


def get_student_assessment_grade(
    db: Session,
    student_id: int,
    assessment_id: int,
) -> Grade | None:
    statement = select(Grade).where(
        Grade.student_id == student_id,
        Grade.assessment_id == assessment_id,
    )

    return db.scalar(statement)


def update_grade(
    db: Session,
    student_id: int,
    assessment_id: int,
    grade_data: GradeUpdate,
) -> Grade | None:
    grade = get_student_assessment_grade(
        db=db,
        student_id=student_id,
        assessment_id=assessment_id,
    )

    if grade is None:
        return None

    if grade_data.marks is not None:
        validate_grade(
            db=db,
            student_id=student_id,
            assessment_id=assessment_id,
            marks=grade_data.marks,
        )

    grade.marks = grade_data.marks

    db.commit()
    db.refresh(grade)

    return grade