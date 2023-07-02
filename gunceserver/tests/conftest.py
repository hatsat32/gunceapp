import pytest
from starlette.testclient import TestClient

from main import app
from core.db import Base, engine


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def test_app(db_session) -> TestClient:
    yield TestClient(app)  # testing happens here
