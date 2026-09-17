from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.grade import Grade


def validate_assessment_weights(
    db: Session,
    course_id: int,
    semester_id: int,
    new_weight: float,
    assessment_id: int | None = None,
) -> None:
    statement = select(
        func.coalesce(func.sum(Assessment.weight), 0)   #coalesce is basically (if value use this, else use this as default)
    ).where(
        Assessment.course_id == course_id,
        Assessment.semester_id == semester_id,
    )

    if assessment_id is not None:                       #incase of updating existing assessment, we need to exclude the current assessment from the total weight calculation. 
        statement = statement.where(
            Assessment.id != assessment_id
        )

    existing_weight = db.scalar(statement) or 0         #safety fallback to 0 incase of null value return from db

    total_weight = float(existing_weight) + new_weight

    if total_weight > 100:
        raise ValueError(
            "Total assessment weight cannot exceed 100%."
        )


def validate_maximum_marks(                             #incase someone tries to update maximum marks for an assessment to a value lower than the highest existing student score for that assessment, we raise a ValueError.
    db: Session,                                        
    assessment_id: int,
    new_maximum_marks: float,
) -> None:
    statement = select(func.max(Grade.marks)).where(
        Grade.assessment_id == assessment_id
    )

    highest_existing_mark = db.scalar(statement)

    if (
        highest_existing_mark is not None
        and new_maximum_marks < float(highest_existing_mark)
    ):
        raise ValueError(
            "Maximum marks cannot be lower than an "
            "existing student score."
        )