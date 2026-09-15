from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    code: str
    name: str
    credits: float = Field(gt=0)  #bussiness cpnstraint: credits should be greater than 0


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    credits: float | None = Field(default=None, gt=0)


class CourseResponse(CourseBase):
    id: int

    model_config = {
        "from_attributes": True
    }