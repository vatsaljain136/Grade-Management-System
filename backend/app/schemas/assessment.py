from typing import Literal

from pydantic import BaseModel, Field


AssessmentType = Literal[
    "assignment",
    "project",
    "quiz",
    "exam",       #ask sandeep sir/puru sir if more types are needed
]


class AssessmentBase(BaseModel):
    course_id: int
    semester_id: int
    title: str
    type: AssessmentType
    maximum_marks: float = Field(gt=0)
    weight: float = Field(ge=0, le=100) #also confirm constraints for the wieght field


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    course_id: int | None = None
    semester_id: int | None = None
    title: str | None = None
    type: AssessmentType | None = None
    maximum_marks: float | None = Field(default=None, gt=0)
    weight: float | None = Field(default=None, ge=0, le=100)


class AssessmentResponse(AssessmentBase):
    id: int

    model_config = {
        "from_attributes": True
    }