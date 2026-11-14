import pytest

from tests.conftest import login, register


def test_health_check(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "CampusFlow API is running"}


def test_register_and_login(client):
    assert register(client).status_code == 200

    res = login(client)
    assert res.status_code == 200
    assert res.json()["token_type"] == "bearer"
    assert res.json()["access_token"]


def test_password_is_hashed_not_stored_in_plain_text(client):
    from app.database.config import SessionLocal
    from app.models.user import User

    register(client, password="password123")
    with SessionLocal() as db:
        stored = db.query(User).one().password
    assert stored != "password123"
    assert stored.startswith("$2")  # bcrypt hash


def test_email_is_case_insensitive_and_trimmed(client):
    register(client, email="  Zaheeb@Example.COM ")
    assert login(client, email="zaheeb@example.com").status_code == 200
    assert login(client, email="ZAHEEB@example.com").status_code == 200


def test_duplicate_email_is_rejected(client):
    register(client, email="test@example.com")
    res = register(client, email="TEST@example.com")
    assert res.status_code == 400
    assert res.json()["detail"] == "Email already registered"


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "", "email": "", "password": ""},  # the original empty-account bug
        {"name": "A", "email": "not-an-email", "password": "password123"},
        {"name": "A", "email": "a@example.com", "password": "short"},
        {"name": "   ", "email": "a@example.com", "password": "password123"},
        {"name": "A", "email": "a@example.com", "password": "x" * 73},
    ],
    ids=["all-empty", "bad-email", "short-password", "blank-name", "password-too-long"],
)
def test_register_rejects_invalid_input(client, payload):
    assert client.post("/register", json=payload).status_code == 422


def test_empty_credentials_cannot_log_in(client):
    res = client.post("/login", json={"email": "", "password": ""})
    assert res.status_code == 422


def test_wrong_password_and_unknown_email_give_the_same_error(client):
    register(client)
    wrong_password = login(client, password="wrong-password")
    unknown_email = login(client, email="nobody@example.com")

    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json() == unknown_email.json() == {"detail": "Invalid email or password"}


def test_me_returns_the_logged_in_user(client, auth):
    res = client.get("/me", headers=auth)
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"
    assert res.json()["name"] == "Test User"
    assert "password" not in res.json()


def test_me_requires_a_token(client):
    assert client.get("/me").status_code in (401, 403)


def test_invalid_token_is_rejected(client):
    res = client.get("/me", headers={"Authorization": "Bearer not.a.real.token"})
    assert res.status_code == 401
