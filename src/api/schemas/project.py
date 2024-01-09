from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(min_length=3, max_length=25)
    description: Optional[str] = Field(None, max_length=120)
    author: UUID4


class ProjectShow(ProjectBase):
    project_id: UUID4
    is_active: bool


class ProjectCreate(ProjectBase):
    pass
