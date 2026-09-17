from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.upload import UploadResponse
from app.services.upload_service import process_grade_upload

#File → Tells FastAPI that the parameter is coming from a file upload.
#upload_file → Represents the uploaded file, which FastAPI will handle automatically.

router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)


@router.post("/grades", response_model=UploadResponse)
def upload_grades(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".xlsx"):
        return UploadResponse(
            success=False,
            created_count=0,
            updated_count=0,
            errors=[
                {
                    "row": 1,
                    "reason": "Only .xlsx files are supported.",
                }
            ],
        )

    temporary_file = f"temp_{file.filename}"

    try:
        with open(temporary_file, "wb") as output_file:
            output_file.write(file.file.read())

        return process_grade_upload(
            db=db,
            file_path=temporary_file,
        )

    finally:
        import os

        if os.path.exists(temporary_file):
            os.remove(temporary_file)