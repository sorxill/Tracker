import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TaskCollaborators(Base):
    __tablename__ = "tasks_collaborators"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
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
