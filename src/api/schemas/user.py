"""
User Schemas for handlers and responses
"""

import re
from typing import Optional

from fastapi import HTTPException
from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserShow(BaseModel):
    """
    Show all user information
    """

    user_id: UUID4
    name: str
    surname: str
    hashed_password: bytes
    email: EmailStr
    is_active: bool


class UserCreate(BaseModel):
    """
    Schema to create a new user
    Has a special validator for name and surname
    """

    name: str
    surname: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_name(cls, value):
        """
        Validate name by contains only letters
        """

        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        """
        Validate surname by contains only letters
        """

        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserDelete(BaseModel):
    """
    Schema to delete user answer deleted user id
    """

    deleted_user_id: UUID4


class UserUpdateRequest(BaseModel):
    """
    Schema to update user params
    May not contain no one param
    """

    name: Optional[str] = Field(min_length=1, default=None)
    surname: Optional[str] = Field(min_length=1, default=None)
    email: Optional[EmailStr] = None

    @field_validator("name")
    def validate_name(cls, value):
        """
        Validate name by contains only letters
        """

        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        """
        Validate surname by contains only letters
        """

        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserForToken(BaseModel):
    """
    Schema unique info about user for jwt token
    """

    email: EmailStr
    user_id: UUID4
