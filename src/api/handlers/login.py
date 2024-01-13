from logging import getLogger

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.actions.user.crud import read_user_by_email
from src.api.schemas.token import TokenInfo
from src.api.schemas.user import UserForToken
from src.auth.hasher import Hasher
from src.auth.jwt import JWT
from src.db.session import get_db

logger = getLogger(__name__)

login_router = APIRouter(prefix="/login", tags=["login"])


async def validate_auth_user(
    email: str = Form(),
    password: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    user = await read_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {email} not found",
        )
    if not Hasher.validate_password(password, hashed_password=user.hashed_password):
        raise unauthorized_exc
    return user


@login_router.post("/", response_model=TokenInfo)
async def auth_user_jwt(user: UserForToken = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.email,
        "name": user.name,
    }
    token = JWT.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        type_token="Bearer",
    )
