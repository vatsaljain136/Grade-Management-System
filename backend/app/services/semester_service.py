from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.semester import Semester
from app.schemas.semester import SemesterCreate, SemesterUpdate


def create_semester(
    db: Session,
    semester_data: SemesterCreate,
) -> Semester:
    existing_semester = db.scalar(
        select(Semester).where(
            Semester.sequence == semester_data.sequence
        )
    )

    if existing_semester is not None:
        raise ValueError(
            "Semester sequence already exists."
        )

    semester = Semester(
        name=semester_data.name,
        sequence=semester_data.sequence,
    )

    db.add(semester)
    db.commit()
    db.refresh(semester)

    return semester


def get_semester(
    db: Session,
    semester_id: int,
) -> Semester | None:
    statement = select(Semester).where(
        Semester.id == semester_id
    )

    return db.scalar(statement)


def list_semesters(
    db: Session,
) -> list[Semester]:
    statement = (
        select(Semester)
        .order_by(Semester.sequence)
    )

    return list(
        db.scalars(statement).all()
    )


def update_semester(
    db: Session,
    semester_id: int,
    semester_data: SemesterUpdate,
) -> Semester | None:
    semester = get_semester(
        db=db,
        semester_id=semester_id,
    )

    if semester is None:
        return None

    update_data = semester_data.model_dump(
        exclude_unset=True
    )

    if "sequence" in update_data:
        existing_semester = db.scalar(
            select(Semester).where(
                Semester.sequence == update_data["sequence"],
                Semester.id != semester_id,
            )
        )

        if existing_semester is not None:
            raise ValueError(
                "Semester sequence already exists."
            )

    for field, value in update_data.items():
        setattr(semester, field, value)

    db.commit()
    db.refresh(semester)

    return semester