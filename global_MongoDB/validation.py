from typing import Optional,Annotated
from pydantic import BaseModel,Field,field_validator

import motor 
from bson import ObjectId

PyobjectId=Annotated[str,Field()]

class StudentBase(BaseModel):
    """Shared fields + validation rules."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Student's full name"
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Course the student is enrolled in"
    )

    age: int = Field(
        ...,
        ge=5,
        le=100,
        description="Student's age"
    )

    email: Optional[str] = Field(
        None,
        description="Student's email address"
    )

    @field_validator("name", "course")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank or whitespace")
        return v.strip().title()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v

        v = v.strip().lower()

        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("must be a valid email address")

        return v