import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate
from app.services.student_service import (
    create_student,
    get_student,
    update_student,
)


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def test_create_student(db):
    student_data = StudentCreate(
        student_code="STU001",
        name="Asha Sharma",
        email="asha@example.com",
        batch="2026",
    )

    student = create_student(
        db=db,
        student_data=student_data,
    )

    assert student.id is not None
    assert student.student_code == "STU001"
    assert student.name == "Asha Sharma"
    assert student.email == "asha@example.com"
    assert student.batch == "2026"


def test_duplicate_student_code_is_rejected(db):
    first_student = StudentCreate(
        student_code="STU001",
        name="Asha Sharma",
        email="asha@example.com",
        batch="2026",
    )

    second_student = StudentCreate(
        student_code="STU001",
        name="Rohan Verma",
        email="rohan@example.com",
        batch="2026",
    )

    create_student(
        db=db,
        student_data=first_student,
    )

    with pytest.raises(ValueError, match="Student code already exists"):
        create_student(
            db=db,
            student_data=second_student,
        )


def test_get_student(db):
    student_data = StudentCreate(
        student_code="STU001",
        name="Asha Sharma",
        email="asha@example.com",
        batch="2026",
    )

    created_student = create_student(
        db=db,
        student_data=student_data,
    )

    student = get_student(
        db=db,
        student_id=created_student.id,
    )

    assert student is not None
    assert student.student_code == "STU001"


def test_get_nonexistent_student(db):
    student = get_student(
        db=db,
        student_id=999,
    )

    assert student is None


def test_update_student(db):
    student_data = StudentCreate(
        student_code="STU001",
        name="Asha Sharma",
        email="asha@example.com",
        batch="2026",
    )

    student = create_student(
        db=db,
        student_data=student_data,
    )

    update_data = StudentUpdate(
        name="Asha Verma",
        batch="2027",
    )

    updated_student = update_student(
        db=db,
        student_id=student.id,
        student_data=update_data,
    )

    assert updated_student is not None
    assert updated_student.name == "Asha Verma"
    assert updated_student.batch == "2027"
    assert updated_student.student_code == "STU001"


def test_update_student_code_duplicate_is_rejected(db):
    first_student = StudentCreate(
        student_code="STU001",
        name="Asha Sharma",
        email="asha@example.com",
        batch="2026",
    )

    second_student = StudentCreate(
        student_code="STU002",
        name="Rohan Verma",
        email="rohan@example.com",
        batch="2026",
    )

    create_student(
        db=db,
        student_data=first_student,
    )

    second = create_student(
        db=db,
        student_data=second_student,
    )

    with pytest.raises(ValueError, match="Student code already exists"):
        update_student(
            db=db,
            student_id=second.id,
            student_data=StudentUpdate(
                student_code="STU001",
            ),
        )