import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ProjectCollaborators(Base):
    __tablename__ = "project_collaborators"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.project_id"),
        nullable=False,
    )
    collaborators_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"{__class__.__name__}(id = {self.id!r}, project_id = {self.project_id!r}, "
            f"collaborators_id = {self.collaborators_id!r})"
        )
