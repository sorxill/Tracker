from logging import getLogger

from fastapi import APIRouter, Depends

from src.api.handlers.login_utils import validate_auth_user, get_current_auth_user
from src.api.schemas.token import TokenInfo
from src.api.schemas.user import UserForToken
from src.auth.jwt import JWT

logger = getLogger(__name__)

login_router = APIRouter(prefix="/login", tags=["login"])


@login_router.post("/auth", response_model=TokenInfo)
async def auth_user_jwt(user: UserForToken = Depends(validate_auth_user)):
    jwt_payload = {
        "email": user.email,
        "user_id": str(user.user_id),
    }
    token = JWT.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        type_token="Bearer",
    )


@login_router.get("/check_user")
async def auth_check_user_info(
    user: UserForToken = Depends(get_current_auth_user),
):
    return {
        "email": user.email,
        "user_id": user.user_id,
    }
