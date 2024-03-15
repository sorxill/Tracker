"""
JWT
Encode and Decode a jwt tokens
"""

from datetime import datetime, timedelta

import jwt

from configs.app_config import (
    ALGORITHM_JWT,
    EXPIRE_MINUTES_JWT,
    PRIVATE_KEY_JWT,
    PUBLIC_KEY_JWT,
)

EXPIRE_M = int(EXPIRE_MINUTES_JWT)
ALG = ALGORITHM_JWT
PRIVATE = PRIVATE_KEY_JWT
PUBLIC = PUBLIC_KEY_JWT


class JWT:
    """
    JWT class uses jwt authentication
    """

    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = PRIVATE,
        algorithm: str = ALG,
        expire_minutes: int = EXPIRE_M,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        """
        Method to encode payload info
        """

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
        """
        Method to decode payload info from jwt
        """

        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return decoded
