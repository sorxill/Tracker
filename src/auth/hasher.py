import bcrypt


class Hasher:
    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode(encoding="utf-8")
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
