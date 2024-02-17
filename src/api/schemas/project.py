"""
Project schemas for handlers and responses
"""

from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ProjectShow(BaseModel):
    """
    Schema for show all project information
    """

    name: str = Field(min_length=3, max_length=25)
    description: Optional[str] = Field(max_length=120, default=None)
    author_id: UUID4
    project_id: UUID4
    is_active: bool


class ProjectCreate(BaseModel):
    """
    Schema for Project create
    """

    name: str = Field(min_length=3, max_length=25)
    description: Optional[str] = Field(max_length=120, default=None)
    author_id: UUID4


class ProjectDelete(BaseModel):
    """
    Schema for delete project
    Return deleted project id
    """

    project_id: UUID4


class ProjectUpdate(BaseModel):
    """
    Schema for project update
    """

    name: Optional[str] = Field(min_length=3, max_length=25, default=None)
    description: Optional[str] = Field(max_length=120, default=None)


class ProjectAddContributor(BaseModel):
    """
    Schema for add a new collaborator
    """
    project_id: UUID4
    collaborators_id: UUID4
