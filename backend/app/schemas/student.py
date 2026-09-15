from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    student_code: str
    name: str
    email: EmailStr
    batch: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    student_code: str | None = None
    name: str | None = None
    email: EmailStr | None = None
    batch: str | None = None


class StudentResponse(StudentBase):
    id: int

    model_config = {                    #because we are using SQLAlchemy ORM, we need to set orm_mode to True in the model_config of the Pydantic model. This allows Pydantic to work with SQLAlchemy models and convert them to Pydantic models.
        "from_attributes": True         #TLDR this basically means object as a dict so pydantic understands.
    }