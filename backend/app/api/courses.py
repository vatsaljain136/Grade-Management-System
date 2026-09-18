from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate,
)
from app.services.course_service import (
    create_course,
    get_course,
    list_courses,
    update_course,
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)


@router.post(
    "",
    response_model=CourseResponse,
)
def create_course_route(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_course(
            db=db,
            course_data=course_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[CourseResponse],
)
def list_courses_route(
    db: Session = Depends(get_db),
):
    return list_courses(db=db)


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
)
def get_course_route(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = get_course(
        db=db,
        course_id=course_id,
    )

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found.",
        )

    return course


@router.put(
    "/{course_id}",
    response_model=CourseResponse,
)
def update_course_route(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
):
    try:
        course = update_course(
            db=db,
            course_id=course_id,
            course_data=course_data,
        )

        if course is None:
            raise HTTPException(
                status_code=404,
                detail="Course not found.",
            )

        return course

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )