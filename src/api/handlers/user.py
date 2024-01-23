from logging import getLogger
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.user.crud import (
    create_new_user,
    delete_user,
    read_user_by_email,
    read_user_by_id,
    update_user,
)
from src.api.handlers.login import auth_check_user_info
from src.api.schemas.user import (
    UserCreate,
    UserDelete,
    UserShow,
    UserUpdateRequest,
    UserForToken,
)
from src.db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/create", response_model=UserShow)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err


@user_router.get("/get_by_id", response_model=UserShow)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    user = await read_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    return user


@user_router.get("/get_by_email", response_model=UserShow)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    user = await read_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with email {email} not found."
        )
    return user


@user_router.patch("/update", response_model=UserShow)
async def update_user_by_id(
    user_id: UUID,
    body: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    user_params = body.model_dump(exclude_none=True)
    if user_params == {}:
        raise HTTPException(status_code=422, detail="No one parameters get")
    # this raise is don't work now.
    check_id = await read_user_by_id(user_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )

    try:
        updated_user = await update_user(user_params, user_id, db)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
    return updated_user


@user_router.delete("/delete", response_model=UserDelete)
async def delete_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserForToken = Depends(auth_check_user_info),
):
    check_id = await read_user_by_id(user_id, db)
    if check_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    deleted_user_id = await delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return UserDelete(deleted_user_id=deleted_user_id)
