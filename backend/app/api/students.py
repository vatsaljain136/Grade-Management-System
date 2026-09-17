from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session


# APIRouter → creates a group of related API endpoints.
# Depends → lets FastAPI provide dependencies automatically, such as a database session.
# HTTPException → sends HTTP errors like 404 or 400.
# Query → defines and validates query parameters such as ?page=1.


from app.database.session import get_db
from app.models.student import Student
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
)
from app.services.student_service import (
    create_student,
    get_student,
    update_student,
)

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "",
    response_model=StudentResponse,
)
def create_student_route(
    student_data: StudentCreate,
    db: Session = Depends(get_db),     #Before running this function, call get_db() and give me the result.
):
    try:
        return create_student(
            db=db,
            student_data=student_data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(                        # List students API
    "",
    response_model=list[StudentResponse],
)
def list_students(
    search: str | None = Query(      #This means search is optional.
        default=None,
    ),
    batch: str | None = Query(
        default=None,
    ),
    page: int = Query(                #page number for pagination, default is 1, must be >= 1
        default=1,
        ge=1,
    ),
    page_size: int = Query(            #page size for pagination, default is 10, must be between 1 and 100(how many students to return per page)
        default=10,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    statement = select(Student)

    # Search by student code OR name.
    if search:
        search_pattern = f"%{search}%"    #The % means "anything before or after."

        statement = statement.where(
            or_(
                Student.student_code.ilike(
                    search_pattern
                ),
                Student.name.ilike(
                    search_pattern
                ),
            )
        )

    # Filter by batch.
    if batch:
        statement = statement.where(
            Student.batch == batch
        )

    # Pagination.
    offset = (page - 1) * page_size

    statement = (
        statement
        .order_by(Student.id)
        .offset(offset)
        .limit(page_size)
    )

    return list(
        db.scalars(statement).all()
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student_route(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = get_student(
        db=db,
        student_id=student_id,
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found.",
        )

    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_student_route(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    try:
        student = update_student(
            db=db,
            student_id=student_id,
            student_data=student_data,
        )

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        return student

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )