import uuid
from sqlalchemy import Enum, Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from core.db import Base
from lib import security


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    serverkey = Column(String(255))
    masterkey = Column(String(64))
    nonce = Column(String(24))
    tag = Column(String(32))
    role = Column(Enum(security.Roles), default=security.Roles.user)
    is_active = Column(Boolean, default=True)

    def set_serverkey(self, plaintext: str):
        self.serverkey = security.get_serverkey_hash(plaintext)

    def verify_serverkey(self, serverkey: str):
        return True if security.verify_serverkey(serverkey, self.serverkey) else False
