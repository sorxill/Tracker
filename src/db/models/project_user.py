import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base


class ProjectUser(Base):
    __tablename__ = "projects_users"
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.project_id"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.user_id"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"ProjectUser(project_id={self.project_id!r}, user_id={self.user_id!r})"
