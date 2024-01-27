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
    collaborators: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    timestamp: Mapped[TIMESTAMP] = mapped_column(
        type_=TIMESTAMP(timezone=True), nullable=True
    )

    project_relationship = relationship(
        "Project",
        back_populates="project_task_relationship",
    )
    author_relationship = relationship(
        "User",
        back_populates="author_task_relationship",
    )

    def __repr__(self) -> str:
        return (
            f"Task(task_id={self.task_id!r}, project_id={self.project_id!r})"
            # f"author_id={self.author_id!r}, name={self.name!r}, "
            # f"description={self.description!r}, task_status={self.task_status!r}, "
            # f"task_type={self.task_type!r}, collaborators={self.collaborators!r}, "
            # f"timestamp={self.timestamp!r})"
        )
