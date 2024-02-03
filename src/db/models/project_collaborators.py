import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class ProjectCollaborators(Base):
    __tablename__ = "project_collaborators"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
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
