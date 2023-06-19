import datetime
from pydantic import BaseModel, UUID4, Field


class EntryBase(BaseModel):
    date: datetime.date

    title: str = Field(max_length=256)
    title_key_tag: str = Field(min_length=24, max_length=24)
    title_key_nonce: str = Field(min_length=32, max_length=32)

    content: str
    content_key_tag: str = Field(min_length=24, max_length=24)
    content_key_nonce: str = Field(min_length=32, max_length=32)


class EntryCreate(EntryBase):
    pass


class EntryUpdate(EntryBase):
    pass


class EntryOut(EntryBase):
    id: UUID4

    class Config:
        orm_mode = True


class EntryInDB(EntryOut):
    pass
