from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services.enrollment_service import (
    create_enrollment,
    list_enrollments,
)


router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)


@router.post("", response_model=EnrollmentResponse)
def create_enrollment_route(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_enrollment(
            db=db,
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            semester_id=enrollment.semester_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("", response_model=list[EnrollmentResponse])
def list_enrollments_route(
    student_id: int | None = None,
    course_id: int | None = None,
    semester_id: int | None = None,
    db: Session = Depends(get_db),
):
    return list_enrollments(
        db=db,
        student_id=student_id,
        course_id=course_id,
        semester_id=semester_id,
    )