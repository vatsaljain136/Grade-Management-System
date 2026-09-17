from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.performance import PerformanceResponse
from app.services.performance_service import get_student_performance

router = APIRouter(
    prefix="/performance",
    tags=["Performance"],
)


@router.get(
    "/students/{student_id}",
    response_model=PerformanceResponse,
)
def get_student_performance_route(
    student_id: int,
    db: Session = Depends(get_db),
):
    try:
        performance = get_student_performance(
            db=db,
            student_id=student_id,
        )

        if performance is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found.",
            )

        return performance

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )