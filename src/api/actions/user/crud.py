from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.user import UserCreate, UserShow
from src.db.dals.user import UserDAL
from src.db.models.user import User


async def create_new_user(body: UserCreate, session: AsyncSession) -> UserShow:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.dal_create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
        )
        return UserShow(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def read_user_by_email(email: str, session: AsyncSession) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.dal_get_user_by_email(email)
        if user is not None:
            return user


async def read_user_by_id(user_id, session) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.dal_get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return user


async def delete_user(user_id, session) -> UUID | None:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.dal_delete_user(
            user_id=user_id,
        )
        return deleted_user_id


async def update_user(updated_user_params: dict, user_id: UUID, session) -> User | None:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.dal_update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id
