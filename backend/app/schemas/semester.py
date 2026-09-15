from pydantic import BaseModel, Field


class SemesterBase(BaseModel):
    name: str
    sequence: int = Field(gt=0)


class SemesterCreate(SemesterBase):
    pass


class SemesterUpdate(BaseModel):
    name: str | None = None
    sequence: int | None = Field(default=None, gt=0)


class SemesterResponse(SemesterBase):
    id: int

    model_config = {
        "from_attributes": True
    }