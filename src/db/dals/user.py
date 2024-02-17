"""
User queries to database
"""

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import User


class UserDAL:
    """
    Data Access Layer for operating user info
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def dal_create_user(
        self,
        name: str,
        surname: str,
        email: str,
        password: bytes,
    ) -> User:
        """
        Create a new user
        """

        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=password,
        )
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user

    async def dal_get_user_by_email(self, email: str) -> User | None:
        """
        Get user by email
        Email is unique for user
        """

        query = select(User).where(User.email == email, User.is_active)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def dal_get_user_by_id(self, user_id: UUID) -> User | None:
        """
        Get user bu uuid
        """

        query = select(User).where(User.user_id == user_id, User.is_active)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def dal_update_user(self, user_id: UUID, **kwargs) -> User | None:
        """
        Update user with not necessary params
        """

        query = (
            update(User)
            .where(User.user_id == user_id, User.is_active)
            .values(kwargs)
            .returning(User)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def dal_delete_user(self, user_id: UUID) -> UUID | None:
        """
        Delete user by id
        """

        query = (
            update(User)
            .where(User.user_id == user_id, User.is_active)
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]
