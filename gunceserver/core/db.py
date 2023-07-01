from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

import core.deps

SQLALCHEMY_DATABASE_URL = core.deps.get_settings().DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
