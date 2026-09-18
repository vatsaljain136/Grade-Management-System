from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.semester import (
    SemesterCreate,
    SemesterResponse,
    SemesterUpdate,
)
from app.services.semester_service import (
    create_semester,
    get_semester,
    list_semesters,
    update_semester,
)


router = APIRouter(
    prefix="/semesters",
    tags=["Semesters"],
)


@router.post(
    "",
    response_model=SemesterResponse,
)
def create_semester_route(
    semester_data: SemesterCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_semester(
            db=db,
            semester_data=semester_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[SemesterResponse],
)
def list_semesters_route(
    db: Session = Depends(get_db),
):
    return list_semesters(db=db)


@router.get(
    "/{semester_id}",
    response_model=SemesterResponse,
)
def get_semester_route(
    semester_id: int,
    db: Session = Depends(get_db),
):
    semester = get_semester(
        db=db,
        semester_id=semester_id,
    )

    if semester is None:
        raise HTTPException(
            status_code=404,
            detail="Semester not found.",
        )

    return semester


@router.put(
    "/{semester_id}",
    response_model=SemesterResponse,
)
def update_semester_route(
    semester_id: int,
    semester_data: SemesterUpdate,
    db: Session = Depends(get_db),
):
    try:
        semester = update_semester(
            db=db,
            semester_id=semester_id,
            semester_data=semester_data,
        )

        if semester is None:
            raise HTTPException(
                status_code=404,
                detail="Semester not found.",
            )

        return semester

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )