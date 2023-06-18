from pydantic import BaseModel, UUID4
from typing import Optional

from lib.security import Roles


class UserBase(BaseModel):
    username: str
    serverkey: str
    masterkey: str
    nonce: str
    tag: str


class UserCreate(UserBase):
    pass


class UserCangePassword(BaseModel):
    serverkey: str
    masterkey: str
    nonce: str
    tag: str


class UserOut(UserBase):
    id: UUID4

    class Config:
        orm_mode = True


class UserInDB(UserOut):
    id: UUID4
    role: Optional[Roles]
    is_active: Optional[bool] = True
