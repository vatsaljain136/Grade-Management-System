import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.grade import Grade
from app.models.student import Student
from app.models.assessment import Assessment
from app.schemas.upload import UploadError, UploadResponse
from app.validation.upload_validation import (
    REQUIRED_COLUMNS,
    validate_upload_row,
)


def process_grade_upload(
    db: Session,
    file_path: str,
) -> UploadResponse:
    # Read the Excel file.
    try:
        dataframe = pd.read_excel(file_path)
    except Exception as exc:
        return UploadResponse(
            success=False,
            created_count=0,
            updated_count=0,
            errors=[
                UploadError(
                    row=1,
                    reason=f"Unable to read Excel file: {exc}",
                )
            ],
        )

    # Check that all required columns exist.
    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing_columns:
        return UploadResponse(
            success=False,
            created_count=0,
            updated_count=0,
            errors=[
                UploadError(
                    row=1,
                    reason=(
                        "Missing required columns: "
                        + ", ".join(sorted(missing_columns))
                    ),
                )
            ],
        )

    errors: list[UploadError] = []
    seen_pairs: set[tuple[str, int]] = set()    #used to detect duplicate student/assessment combinations within the uploaded Excel file.

    # Store valid rows so we can process them only after
    # the complete file has been validated.
    valid_rows: list[dict] = []

    for index, row in dataframe.iterrows():
        row_number = index + 2

        row_data = row.to_dict()

        try:
            assessment_id = int(row_data["assessment_id"])
        except (TypeError, ValueError):
            errors.append(
                UploadError(
                    row=row_number,
                    reason="assessment_id must be an integer.",
                )
            )
            continue

        student_code = str(
            row_data["student_code"]
        ).strip()

        if not student_code:
            errors.append(
                UploadError(
                    row=row_number,
                    reason="student_code cannot be empty.",
                )
            )
            continue

        row_data["student_code"] = student_code
        row_data["assessment_id"] = assessment_id

        # Validate this row.
        error = validate_upload_row(
            db=db,
            row=row_data,
            row_number=row_number,
            seen_pairs=seen_pairs,
        )

        if error:
            errors.append(
                UploadError(
                    row=row_number,
                    reason=error,
                )
            )
            continue

        valid_rows.append(row_data)

    # IMPORTANT:
    # Do not modify the database if even one row is invalid.
    if errors:
        return UploadResponse(
            success=False,
            created_count=0,
            updated_count=0,
            errors=errors,
        )

    created_count = 0
    updated_count = 0

    try:
        for row in valid_rows:
            student = db.scalar(
                select(Student).where(
                    Student.student_code
                    == row["student_code"]
                )
            )

            assessment = db.scalar(
                select(Assessment).where(
                    Assessment.id
                    == row["assessment_id"]
                )
            )

            marks = float(row["marks"])

            existing_grade = db.scalar(
                select(Grade).where(
                    Grade.student_id == student.id,
                    Grade.assessment_id == assessment.id,
                )
            )

            if existing_grade:
                existing_grade.marks = marks
                updated_count += 1
            else:
                grade = Grade(
                    student_id=student.id,
                    assessment_id=assessment.id,
                    marks=marks,
                )

                db.add(grade)
                created_count += 1

        db.commit()

    except Exception:
        db.rollback()

        return UploadResponse(
            success=False,
            created_count=0,
            updated_count=0,
            errors=[
                UploadError(
                    row=1,
                    reason="Upload failed. No changes were saved.",
                )
            ],
        )

    return UploadResponse(
        success=True,
        created_count=created_count,
        updated_count=updated_count,
        errors=[],
    )