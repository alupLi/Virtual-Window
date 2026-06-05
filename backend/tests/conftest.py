import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import Base, get_db
from main import app

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DB_URL, 
    connect_args={"check_same_thread": False},
    poolclass=NullPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield

    engine.dispose()
    Base.metadata.drop_all(bind=engine)
    
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except PermissionError:
            pass


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_client(client):
    """Client with registered and logged-in user."""
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123",
    })
    client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123",
    })
    return client