import os
import tempfile

# Point the app at a throwaway SQLite database BEFORE it is imported,
# so tests never touch the real PostgreSQL database.
_db_file = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_db_file}"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["ALGORITHM"] = "HS256"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.database.config import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_database():
    """Every test starts with empty tables."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


def register(client, name="Test User", email="test@example.com", password="password123"):
    return client.post("/register", json={"name": name, "email": email, "password": password})


def login(client, email="test@example.com", password="password123"):
    return client.post("/login", json={"email": email, "password": password})


@pytest.fixture
def make_user(client):
    """Create a user and return auth headers for them."""

    def _make(email="test@example.com", password="password123", name="Test User"):
        assert register(client, name=name, email=email, password=password).status_code == 200
        token = login(client, email=email, password=password).json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _make


@pytest.fixture
def auth(make_user):
    return make_user()
