from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.enrollment import Enrollment
from app.models.student import Student


REQUIRED_COLUMNS = {
    "student_code",
    "assessment_id",
    "marks",
}


def validate_upload_row(
    db: Session,
    row: dict,
    row_number: int,
    seen_pairs: set[tuple[str, int]],   #to detetect duplicate student-assessment rows in the uploaded data,(student_code, assessment_id) pairs are stored in a set called seen_pairs. If a pair is already in the set.
) -> str | None:
    # 1. Check required columns
    missing_columns = REQUIRED_COLUMNS - row.keys()

    if missing_columns:
        return (
            f"Missing required columns: "
            f"{', '.join(sorted(missing_columns))}"
        )

    student_code = row["student_code"]
    assessment_id = row["assessment_id"]
    marks = row["marks"]

    # 2. Check for duplicate student-assessment rows
    pair = (str(student_code), int(assessment_id))

    if pair in seen_pairs:
        return "Duplicate student-assessment row."

    seen_pairs.add(pair)

    # 3. Find student
    student = db.scalar(
        select(Student).where(
            Student.student_code == str(student_code)
        )
    )

    if student is None:
        return f"Unknown student_code: {student_code}"

    # 4. Find assessment
    assessment = db.scalar(
        select(Assessment).where(
            Assessment.id == int(assessment_id)
        )
    )

    if assessment is None:
        return f"Unknown assessment_id: {assessment_id}"

    # 5. Check marks
    try:
        marks = float(marks)
    except (TypeError, ValueError):
        return "Marks must be a number."

    if marks < 0:
        return "Marks cannot be negative."

    if marks > float(assessment.maximum_marks):
        return (
            f"Marks cannot exceed maximum marks "
            f"({assessment.maximum_marks})."
        )

    # 6. Check enrollment
    enrollment = db.scalar(
        select(Enrollment).where(
            Enrollment.student_id == student.id,
            Enrollment.course_id == assessment.course_id,
            Enrollment.semester_id == assessment.semester_id,
        )
    )

    if enrollment is None:
        return (
            "Student is not enrolled in the assessment's "
            "course for this semester."
        )

    return None