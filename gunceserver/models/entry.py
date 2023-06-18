import uuid
import datetime

from sqlalchemy import Date, Column, String, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    date = Column(Date, default=datetime.date.today)

    title = Column(String(256))
    title_key_tag = Column(String(24))
    title_key_nonce = Column(String(32))

    content = Column(Text, nullable=True)
    content_key_tag = Column(String(24))
    content_key_nonce = Column(String(32))

    __table_args__ = (UniqueConstraint("user_id", "date"),)
