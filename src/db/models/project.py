import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Project(Base):
    __tablename__ = "projects"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"), nullable=False
    )
    description: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tasks = relationship(
        "Task",
        back_populates="project",
        lazy="selectin",
    )

    author = relationship(
        "User",
        back_populates="projects",
    )

    collaborators = relationship(
        "User",
        secondary="project_collaborators",
    )

    def __repr__(self) -> str:
        return (
            f"Project(project_id={self.project_id!r}, name={self.name!r}, "
            f"author={self.author_id!r}, description={self.description!r}, "
            f"is_active={self.is_active!r})"
        )
