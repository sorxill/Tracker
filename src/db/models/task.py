"""
Database model for Task
Relationships with: Project, User
"""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    task_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.project_id"), nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    task_status: Mapped[str] = mapped_column(String, nullable=False, default="backlog")
    task_type: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[TIMESTAMP] = mapped_column(
        type_=TIMESTAMP(timezone=True), nullable=True
    )

    project = relationship(
        "Project",
        back_populates="tasks",
    )

    author = relationship(
        "User",
        back_populates="tasks",
    )

    collaborators = relationship(
        "User",
        secondary="tasks_collaborators",
    )

    def __repr__(self) -> str:
        return (
            f"Task(task_id={self.task_id!r}, project_id={self.project_id!r})"
            f"author_id={self.author_id!r}, name={self.name!r}, "
            f"description={self.description!r}, task_status={self.task_status!r}, "
            f"task_type={self.task_type!r}, timestamp={self.timestamp!r})"
        )
