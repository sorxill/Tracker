from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.actions.user import create_new_user
from src.api.schemas import ShowUser, UserCreate
from src.db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter(prefix="/user")


@user_router.post("/create", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}") from err
