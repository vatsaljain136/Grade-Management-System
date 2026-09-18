
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.models.student import Student
from app.models.assessment import Assessment
from app.models.enrollment import Enrollment
from app.schemas.grade import GradeCreate, GradeUpdate
from app.services.grade_service import (
    create_grade,
    get_grade,
    get_student_assessment_grade,
    update_grade,
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

    # ---------------------------------------------------------
    # Create student
    # ---------------------------------------------------------

    student = Student(
        student_code="STU001",
        name="Asha Sharma",
        email="asha@example.com",
        batch="2026",
    )

    session.add(student)
    session.commit()
    session.refresh(student)

    # ---------------------------------------------------------
    # Create assessment
    # ---------------------------------------------------------

    assessment = Assessment(
        course_id=1,
        semester_id=1,
        title="Midterm Exam",
        type="EXAM",
        maximum_marks=100,
        weight=30,
    )

    session.add(assessment)
    session.commit()
    session.refresh(assessment)

    # ---------------------------------------------------------
    # Enroll student in the same course and semester
    # ---------------------------------------------------------

    enrollment = Enrollment(
        student_id=student.id,
        course_id=assessment.course_id,
        semester_id=assessment.semester_id,
    )

    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)

    yield session

    session.close()


# ---------------------------------------------------------
# Create Grade
# ---------------------------------------------------------

def test_create_grade(db):
    grade_data = GradeCreate(
        student_id=1,
        assessment_id=1,
        marks=85,
    )

    grade = create_grade(db, grade_data)

    assert grade.id is not None
    assert grade.student_id == 1
    assert grade.assessment_id == 1
    assert grade.marks == 85


# ---------------------------------------------------------
# Duplicate Grade
# ---------------------------------------------------------

def test_duplicate_grade_is_rejected(db):
    grade_data = GradeCreate(
        student_id=1,
        assessment_id=1,
        marks=85,
    )

    create_grade(db, grade_data)

    with pytest.raises(
        ValueError,
        match="Grade already exists",
    ):
        create_grade(db, grade_data)


# ---------------------------------------------------------
# Get Grade
# ---------------------------------------------------------

def test_get_grade(db):
    grade_data = GradeCreate(
        student_id=1,
        assessment_id=1,
        marks=90,
    )

    created = create_grade(
        db,
        grade_data,
    )

    result = get_grade(
        db,
        created.id,
    )

    assert result is not None
    assert result.id == created.id
    assert result.marks == 90


# ---------------------------------------------------------
# Get Student Assessment Grade
# ---------------------------------------------------------

def test_get_student_assessment_grade(db):
    grade_data = GradeCreate(
        student_id=1,
        assessment_id=1,
        marks=75,
    )

    created = create_grade(
        db,
        grade_data,
    )

    result = get_student_assessment_grade(
        db,
        student_id=1,
        assessment_id=1,
    )

    assert result is not None
    assert result.id == created.id
    assert result.marks == 75


# ---------------------------------------------------------
# Update Grade
# ---------------------------------------------------------

def test_update_grade(db):
    grade_data = GradeCreate(
        student_id=1,
        assessment_id=1,
        marks=70,
    )

    created = create_grade(
        db,
        grade_data,
    )

    update_data = GradeUpdate(
        marks=95,
    )

    updated = update_grade(
        db,
        student_id=1,
        assessment_id=1,
        grade_data=update_data,
    )

    assert updated is not None
    assert updated.id == created.id
    assert updated.marks == 95


# ---------------------------------------------------------
# Update Grade Not Found
# ---------------------------------------------------------

def test_update_grade_not_found(db):
    update_data = GradeUpdate(
        marks=95,
    )

    result = update_grade(
        db,
        student_id=999,
        assessment_id=999,
        grade_data=update_data,
    )

    assert result is None
