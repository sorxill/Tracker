from datetime import datetime, timedelta

import jwt

from configs.app_config import (
    PRIVATE_KEY_JWT,
    PUBLIC_KEY_JWT,
    EXPIRE_MINUTES_JWT,
    ALGORITHM_JWT,
)

EXPIRE_M = EXPIRE_MINUTES_JWT
ALG = ALGORITHM_JWT
PRIVATE = PRIVATE_KEY_JWT
PUBLIC = PUBLIC_KEY_JWT


class JWT:
    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = PRIVATE,
        algorithm: str = ALG,
        expire_minutes: int = EXPIRE_M,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = PUBLIC,
        algorithm: str = ALG,
    ) -> dict:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
