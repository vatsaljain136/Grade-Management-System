from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentUpdate,
)
from app.services.assessment_service import (
    create_assessment,
    get_assessment,
    list_assessments,
    update_assessment,
)


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post("", response_model=AssessmentResponse)
def create_assessment_route(
    assessment_data: AssessmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_assessment(
            db=db,
            assessment_data=assessment_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("", response_model=list[AssessmentResponse])
def list_assessments_route(
    course_id: int | None = Query(default=None),
    semester_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_assessments(
        db=db,
        course_id=course_id,
        semester_id=semester_id,
    )


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment_route(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    assessment = get_assessment(
        db=db,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found.",
        )

    return assessment


@router.put("/{assessment_id}", response_model=AssessmentResponse)
def update_assessment_route(
    assessment_id: int,
    assessment_data: AssessmentUpdate,
    db: Session = Depends(get_db),
):
    try:
        assessment = update_assessment(
            db=db,
            assessment_id=assessment_id,
            assessment_data=assessment_data,
        )

        if assessment is None:
            raise HTTPException(
                status_code=404,
                detail="Assessment not found.",
            )

        return assessment

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )