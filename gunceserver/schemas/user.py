from typing import Optional

from pydantic import BaseModel, UUID4, Field

from lib.security import Roles


class UserBase(BaseModel):
    username: str = Field(min_length=6)
    masterkey: str = Field(min_length=64, max_length=64)
    nonce: str = Field(min_length=24, max_length=24)
    tag: str = Field(min_length=32, max_length=32)


class UserCreate(UserBase):
    serverkey: str = Field(min_length=64, max_length=64)


class UserCangePassword(BaseModel):
    serverkey: str = Field(min_length=64, max_length=64)
    masterkey: str = Field(min_length=64, max_length=64)
    nonce: str = Field(min_length=24, max_length=24)
    tag: str = Field(min_length=32, max_length=32)


class UserOut(UserBase):
    id: UUID4

    class Config:
        orm_mode = True


class UserInDB(UserOut):
    id: UUID4
    role: Optional[Roles]
    is_active: Optional[bool] = True
