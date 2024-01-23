import re
from typing import Optional

from fastapi import HTTPException
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserShow(BaseModel):
    user_id: UUID4
    name: str
    surname: str
    hashed_password: bytes
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserDelete(BaseModel):
    deleted_user_id: UUID4


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(min_length=1, default=None)
    surname: Optional[str] = Field(min_length=1, default=None)
    email: Optional[EmailStr] = None

    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserForToken(BaseModel):
    email: EmailStr
    user_id: UUID4
