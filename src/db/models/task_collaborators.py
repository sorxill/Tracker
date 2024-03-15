"""
Database model for relationship Task with Project
"""


import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TaskCollaborators(Base):
    __tablename__ = "tasks_collaborators"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.task_id"),
        nullable=False,
    )
    collaborators_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"{__class__.__name__}(id = {self.id!r}, task_id = {self.task_id!r}, "
            f"collaborators_id = {self.collaborators_id!r})"
        )
