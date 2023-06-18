from functools import lru_cache
import sqlalchemy.orm.session

import core.config
import core.db


@lru_cache()
def get_settings() -> core.config.Settings:
    return core.config.Settings()


async def get_db() -> sqlalchemy.orm.session.Session:
    db = core.db.SessionLocal()
    try:
        yield db
    finally:
        db.close()
