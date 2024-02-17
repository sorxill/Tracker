"""
Hasher to hash and validate password
"""

import bcrypt


class Hasher:
    """
    Hasher class to hash and validate password
    With salt to crypt and check gor validate
    """

    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        """
        Return a hashed password by salt
        """

        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode(encoding="utf-8")
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        """
        Return validate password
        """

        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
