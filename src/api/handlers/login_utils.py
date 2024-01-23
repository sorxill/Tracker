from fastapi import Depends, Form, HTTPException
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from src.api.actions.user.crud import read_user_by_email
from src.api.schemas.user import UserForToken
from src.auth.hasher import Hasher
from src.db.session import get_db

from src.auth.jwt import JWT


http_bearer = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login/auth",
)


async def validate_auth_user(
    username: str = Form(
        description="This form for your Email",
    ),
    password: str = Form(),
    db: AsyncSession = Depends(get_db),
):
    unauthorized_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    user = await read_user_by_email(
        email=username,
        session=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {username} not found",
        )
    if not Hasher.validate_password(
        password,
        hashed_password=user.hashed_password,
    ):
        raise unauthorized_exc
    return user


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = JWT.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db),
) -> UserForToken:
    email = payload.get("email")
    user_db = await read_user_by_email(email, db)
    if user_db:
        return UserForToken(email=user_db.email, user_id=user_db.user_id)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
