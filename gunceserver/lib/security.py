import enum
from passlib.hash import argon2


class Roles(str, enum.Enum):
    admin: str = "admin"
    user: str = "user"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if password is true. False otherwise."""
    # return argon2.verify(plain_password, hashed_password)
    return plain_password == hashed_password


def get_password_hash(password: str) -> str:
    """Get argon2id password hash from password."""
    return argon2.hash(password)
