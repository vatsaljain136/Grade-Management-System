from pydantic import BaseModel


class UploadError(BaseModel):
    row: int
    reason: str


class UploadResponse(BaseModel):
    success: bool
    created_count: int
    updated_count: int                                      #standard pydantic practice to use default_factory for mutable types like list, dict, set, etc. This ensures that each instance of the model gets its own separate copy of the mutable type, rather than sharing a single instance across all instances of the model.
    errors: list[UploadError] = Field(default_factory=list) #basically default is empty list created at model instace