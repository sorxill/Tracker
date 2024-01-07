from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.user.user_crud import (
    create_new_user,
    read_user_by_email,
    read_user_by_id,
)
from src.api.schemas import ShowUser, UserCreate
from src.db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter(prefix="/user")


@user_router.post("/create", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@user_router.get("/read_by_id", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    user = await read_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return user


@user_router.get("/get_by_email", response_model=ShowUser)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
):
    user = await read_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with email {email} not found."
        )
    return user
