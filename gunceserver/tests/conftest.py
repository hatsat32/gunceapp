import pytest
from starlette.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from main import app
from core.deps import get_db
from core.db import Base

SQLALCHEMY_DATABASE_URL = "postgresql://gunce:gunce@localhost/guncetest"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def test_app(db_session) -> TestClient:
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)  # testing happens here
