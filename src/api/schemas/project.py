from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ProjectShow(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    description: Optional[str] = Field(max_length=120)
    author: UUID4
    project_id: UUID4
    is_active: bool


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    description: Optional[str] = Field(max_length=120)
    author: UUID4


class ProjectDelete(BaseModel):
    project_id: UUID4


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=25)
    description: Optional[str] = Field(max_length=120)
