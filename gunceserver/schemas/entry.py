import datetime
from pydantic import BaseModel, UUID4


class EntryBase(BaseModel):
    date: datetime.date

    title: str
    title_key_tag: str
    title_key_nonce: str

    content: str
    content_key_tag: str
    content_key_nonce: str


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
