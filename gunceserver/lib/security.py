import enum
from passlib.hash import argon2


class Roles(str, enum.Enum):
    admin: str = "admin"
    user: str = "user"


def verify_serverkey(plain_serverkey: str, hashed_serverkey: str) -> bool:
    """Return True if serverkey is true. False otherwise."""
    return argon2.verify(plain_serverkey, hashed_serverkey)


def get_serverkey_hash(serverkey: str) -> str:
    """Get argon2id password hash from password."""
    return argon2.hash(serverkey)
