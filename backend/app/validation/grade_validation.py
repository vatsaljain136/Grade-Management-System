from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.enrollment import Enrollment


def validate_grade(
    db: Session,
    student_id: int,
    assessment_id: int,
    marks: float,
) -> Assessment:
    # 1. Find the assessment
    assessment = db.scalar(
        select(Assessment).where(
            Assessment.id == assessment_id
        )
    )

    if assessment is None:
        raise ValueError("Assessment not found.")
    
    if marks is None:               #because marks is optional in the GradeUpdate schema, we need to handle the case where it is None. If marks is None, we can skip the validation checks and return the assessment.
         return assessment          #tldr test failed for more info read above comment

    # 2. Check that the student is enrolled
    enrollment = db.scalar(
        select(Enrollment).where(                         #This checks whether the student is actually enrolled in the same course and semester as the assessment.
            Enrollment.student_id == student_id,
            Enrollment.course_id == assessment.course_id,
            Enrollment.semester_id == assessment.semester_id,
        )
    )

    if enrollment is None:
        raise ValueError(
            "Student is not enrolled in this course "
            "for this semester."
        )

    # 3. Check marks are within the valid range
    if marks < 0:
        raise ValueError("Marks cannot be negative.")

    if marks > float(assessment.maximum_marks):
        raise ValueError(
            f"Marks cannot exceed maximum marks "
            f"({assessment.maximum_marks})."
        )

    return assessment