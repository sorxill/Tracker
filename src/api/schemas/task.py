"""
Task schemas for handlers and responses
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from pydantic import UUID4, BaseModel, Field, model_validator


class TaskTypeEnum(str, Enum):
    """
    Enum class for validate type for task
    """

    A = "a"
    B = "b"
    C = "c"
    MILESTONE = "milestone"


class TaskStatusEnum(str, Enum):
    """
    Enum class for validate status for task
    """

    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    ON_REVIEW = "on_review"
    DONE = "done"


class TaskShow(BaseModel):
    """
    Schema for show all task information
    """

    task_id: UUID4
    project_id: UUID4
    author_id: UUID4
    name: str = Field(min_length=3, max_length=35)
    task_type: TaskTypeEnum
    task_status: TaskStatusEnum
    description: Optional[str] = Field(max_length=250, default=None)
    timestamp: Optional[datetime] = None


class TaskCreate(BaseModel):
    """
    Schema for task create
    Has a validation for task_type milestone
    Only milestone has a timestamp
    """

    project: UUID4
    author: UUID4
    name: str = Field(min_length=3, max_length=35)
    task_type: TaskTypeEnum
    task_status: TaskStatusEnum
    description: Optional[str] = Field(max_length=250, default=None)
    timestamp: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_timestamp(self):
        """
        Validate timestamp
        If timestamp is getting but type is not milestone
        """

        if self.timestamp:
            if self.task_type != TaskTypeEnum.MILESTONE:
                raise HTTPException(
                    status_code=422,
                    detail="Timestamp is only available for type 'milestone'",
                )
        return self

    @model_validator(mode="after")
    def validate_milestone(self):
        """
        Validate milestone
        If milestone is getting but timestamp is not exist
        """

        if self.task_type == TaskTypeEnum.MILESTONE:
            if self.timestamp:
                return self
        raise HTTPException(status_code=422, detail="Type milestone needs timestamp.")


class TaskUpdate(BaseModel):
    """
    Schema for task update
    """

    name: Optional[str] = Field(min_length=3, max_length=35, default=None)
    task_type: Optional[TaskTypeEnum] = None
    description: Optional[str] = Field(max_length=250, default=None)
    timestamp: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_timestamp(self):
        """
        Validate timestamp
        If timestamp is getting but type is not milestone
        """

        if self.task_type != TaskTypeEnum.MILESTONE:
            if self.timestamp:
                raise HTTPException(
                    status_code=422,
                    detail="Timestamp is only available for type 'milestone'",
                )
        return self

    @model_validator(mode="after")
    def validate_milestone(self):
        """
        Validate milestone
        If milestone is getting but timestamp is not exist
        """

        if self.task_type == TaskTypeEnum.MILESTONE:
            if not self.timestamp:
                raise HTTPException(
                    status_code=422,
                    detail="Type milestone needs timestamp.",
                )
        return self


class TaskUpdateStatus(BaseModel):
    """
    Schema for status task update
    """
    task_status: TaskStatusEnum


class TaskDelete(BaseModel):
    """
    Schema for delete task
    Return deleted task id
    """
    task_id: UUID4
