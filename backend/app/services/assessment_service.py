from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate,
)
from app.validation.assessment_validation import (
    validate_assessment_weights,
    validate_maximum_marks,
)


def create_assessment(
    db: Session,
    assessment_data: AssessmentCreate,
) -> Assessment:
    validate_assessment_weights(
        db=db,
        course_id=assessment_data.course_id,
        semester_id=assessment_data.semester_id,
        new_weight=assessment_data.weight,
    )

    assessment = Assessment(
        course_id=assessment_data.course_id,
        semester_id=assessment_data.semester_id,
        title=assessment_data.title,
        type=assessment_data.type,
        maximum_marks=assessment_data.maximum_marks,
        weight=assessment_data.weight,
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


def get_assessment(
    db: Session,
    assessment_id: int,
) -> Assessment | None:
    statement = select(Assessment).where(
        Assessment.id == assessment_id
    )

    return db.scalar(statement)


def list_assessments(
    db: Session,
    course_id: int | None = None,
    semester_id: int | None = None,
) -> list[Assessment]:
    statement = select(Assessment)

    if course_id is not None:
        statement = statement.where(
            Assessment.course_id == course_id
        )

    if semester_id is not None:
        statement = statement.where(
            Assessment.semester_id == semester_id
        )

    statement = statement.order_by(Assessment.id)

    return list(db.scalars(statement).all())


def update_assessment(
    db: Session,
    assessment_id: int,
    assessment_data: AssessmentUpdate,
) -> Assessment | None:
    assessment = get_assessment(db, assessment_id)

    if assessment is None:
        return None

    update_data = assessment_data.model_dump(
        exclude_unset=True
    )

    new_course_id = update_data.get(
        "course_id",
        assessment.course_id,
    )

    new_semester_id = update_data.get(
        "semester_id",
        assessment.semester_id,
    )

    new_weight = update_data.get(
        "weight",
        assessment.weight,
    )

    validate_assessment_weights(
        db=db,
        course_id=new_course_id,
        semester_id=new_semester_id,
        new_weight=float(new_weight),
        assessment_id=assessment_id,
    )

    if "maximum_marks" in update_data:
        validate_maximum_marks(
            db=db,
            assessment_id=assessment_id,
            new_maximum_marks=update_data["maximum_marks"],
        )

    for field, value in update_data.items():
        setattr(assessment, field, value)

    db.commit()
    db.refresh(assessment)

    return assessment