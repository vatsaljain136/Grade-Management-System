from pydantic import BaseModel, Field


class GradeBase(BaseModel):
    student_id: int
    assessment_id: int
    marks: float | None = Field(default=None, ge=0)


class GradeCreate(GradeBase):
    pass


class GradeUpdate(BaseModel):
    marks: float | None = Field(default=None, ge=0)


class GradeResponse(GradeBase):
    id: int

    model_config = {
        "from_attributes": True
    }