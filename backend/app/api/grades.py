from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.grade import Grade
from app.models.assessment import Assessment
from app.schemas.grade import (
    GradeCreate,
    GradeResponse,
    GradeUpdate,
)
from app.services.grade_service import (
    create_grade,
    get_grade,
    get_student_assessment_grade,
    update_grade,
)

router = APIRouter(
    prefix="/grades",
    tags=["Grades"],
)


@router.post("", response_model=GradeResponse)
def create_grade_route(
    grade_data: GradeCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_grade(
            db=db,
            grade_data=grade_data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("", response_model=list[GradeResponse])
def list_grades(
    student_id: int | None = Query(default=None),
    semester_id: int | None = Query(default=None),
    assessment_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    statement = (                                      #Select grades and join them with assessments where the grade's assessment_id matches the assessment's id.
        select(Grade)                                      #semester_id belongs to Assessment, not directly to Grade.
        .join(Assessment, Grade.assessment_id == Assessment.id)
    )

    if student_id is not None:
        statement = statement.where(
            Grade.student_id == student_id
        )

    if semester_id is not None:
        statement = statement.where(
            Assessment.semester_id == semester_id
        )

    if assessment_id is not None:
        statement = statement.where(
            Grade.assessment_id == assessment_id
        )

    statement = statement.order_by(Grade.id)

    return list(db.scalars(statement).all())


@router.get("/{grade_id}", response_model=GradeResponse)
def get_grade_route(
    grade_id: int,
    db: Session = Depends(get_db),
):
    grade = get_grade(
        db=db,
        grade_id=grade_id,
    )

    if grade is None:
        raise HTTPException(
            status_code=404,
            detail="Grade not found.",
        )

    return grade


@router.get(
    "/student/{student_id}/assessment/{assessment_id}",       # Get student's grade for a specific assessment
    response_model=GradeResponse,
)
def get_student_assessment_grade_route(
    student_id: int,
    assessment_id: int,
    db: Session = Depends(get_db),
):
    grade = get_student_assessment_grade(
        db=db,
        student_id=student_id,
        assessment_id=assessment_id,
    )

    if grade is None:
        raise HTTPException(
            status_code=404,
            detail="Grade not found.",
        )

    return grade


@router.put(
    "/student/{student_id}/assessment/{assessment_id}",       #Update a student's assessment grade
    response_model=GradeResponse,
)
def update_grade_route(
    student_id: int,
    assessment_id: int,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
):
    try:
        grade = update_grade(
            db=db,
            student_id=student_id,
            assessment_id=assessment_id,
            grade_data=grade_data,
        )

        if grade is None:
            raise HTTPException(
                status_code=404,
                detail="Grade not found.",
            )

        return grade

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )