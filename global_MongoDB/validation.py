from typing import Optional,Annotated
from pydantic import BaseModel,Field,field_validator,ConfigDict

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

class Student_create(StudentBase):
    pass

class Student_update(BaseModel):
    name:Optional[str]=Field(None, min_length=2, max_length=50)
    course:Optional[str]=Field(None, min_length=2, max_length=50)
    age:Optional[int]=Field(None, ge=5,le=100)
    email:Optional[str]=None

    @field_validator("name","course")
    @classmethod
    def not_blanck(cls,v:Optional[str])->Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Please Enter a valid value")
        return v.strip().title() if v else v

class Student_out(StudentBase):
    id:str=Field(...,alias="_id")

    model_config=ConfigDict(populate_by_name=True,arbitrary_types_allowed=True)
