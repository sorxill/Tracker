from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from pydantic import UUID4, BaseModel, Field, model_validator


class TaskTypeEnum(str, Enum):
    A = "a"
    B = "b"
    C = "c"
    MILESTONE = "milestone"


class TaskStatusEnum(str, Enum):
    BACKLOG = "backlog"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    ON_REVIEW = "on_review"
    DONE = "done"


class TaskShow(BaseModel):
    task_id: UUID4
    project_id: UUID4
    author_id: UUID4
    name: str = Field(min_length=3, max_length=35)
    task_type: TaskTypeEnum
    task_status: TaskStatusEnum
    # collaborators: type[set[UUID4]] = conset(UUID4, min_length=1)
    collaborators: UUID4
    description: Optional[str] = Field(max_length=250, default=None)
    timestamp: Optional[datetime] = None


class TaskCreate(BaseModel):
    project: UUID4
    author: UUID4
    name: str = Field(min_length=3, max_length=35)
    task_type: TaskTypeEnum
    task_status: TaskStatusEnum
    # collaborators: type[set[UUID4]] = conset(UUID4, min_length=1)
    collaborators: UUID4
    description: Optional[str] = Field(max_length=250, default=None)
    timestamp: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_timestamp(self):
        if self.timestamp:
            if self.task_type != TaskTypeEnum.MILESTONE:
                raise HTTPException(
                    status_code=422,
                    detail="Timestamp is only available for type 'milestone'",
                )
        return self

    @model_validator(mode="after")
    def validate_milestone(self):
        if self.task_type == TaskTypeEnum.MILESTONE:
            if self.timestamp:
                return self
        raise HTTPException(
            status_code=422, detail="Type milestone needs timestamp."
        )


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=35, default=None)
    task_type: Optional[TaskTypeEnum] = None
    collaborators: Optional[UUID4] = None
    description: Optional[str] = Field(max_length=250, default=None)
    timestamp: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_timestamp(self):
        if self.timestamp:
            if self.task_type != TaskTypeEnum.MILESTONE:
                raise HTTPException(
                    status_code=422,
                    detail="Timestamp is only available for type 'milestone'",
                )
        return self

    @model_validator(mode="after")
    def validate_milestone(self):
        if self.task_type == TaskTypeEnum.MILESTONE:
            if self.timestamp:
                return self
        raise HTTPException(
            status_code=422, detail="Type milestone needs timestamp."
        )


class TaskUpdateStatus(BaseModel):
    task_status: TaskStatusEnum


class TaskDelete(BaseModel):
    task_id: UUID4
