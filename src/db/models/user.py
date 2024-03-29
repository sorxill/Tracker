import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.dialects.postgresql import BYTEA, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[BYTEA] = mapped_column(BYTEA, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    author_task = relationship("Task", back_populates="author")

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, name={self.name!r}, \
        surname={self.surname!r}, email={self.email!r}, hashed_password={self.hashed_password!r}, \
        is_active={self.is_active!r})"
