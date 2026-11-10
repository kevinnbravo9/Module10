"""Real PostgreSQL integration tests for user creation and storage."""
import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.schemas import UserCreate, UserRead
from app.security import verify_password
from app.user_service import create_user


def user_data(username="alice", email="alice@example.com"):
    return UserCreate(username=username, email=email, password="StrongPassword123!")


def test_user_creation_and_password_hash(db_session):
    data = user_data()
    user = create_user(db_session, data)
    saved = db_session.scalar(select(User).where(User.id == user.id))
    assert saved is not None
    assert saved.created_at is not None
    assert saved.password_hash != data.password
    assert verify_password(data.password, saved.password_hash)
    assert not verify_password("wrong-password", saved.password_hash)


def test_user_read_does_not_expose_password(db_session):
    user = create_user(db_session, user_data())
    public = UserRead.model_validate(user).model_dump()
    assert public["username"] == "alice"
    assert "password" not in public
    assert "password_hash" not in public


@pytest.mark.parametrize("bad_email", ["not-an-email", "missing-at.example.com", "x@"])
def test_invalid_email_rejected(bad_email):
    with pytest.raises(ValidationError):
        user_data(email=bad_email)


@pytest.mark.parametrize("field", ["username", "email"])
def test_database_uniqueness_constraint(db_session, field):
    first = create_user(db_session, user_data())
    assert first.id is not None
    duplicate = User(
        username="alice" if field == "username" else "bob",
        email="alice@example.com" if field == "email" else "bob@example.com",
        password_hash="test-hash",
    )
    db_session.add(duplicate)
    with pytest.raises(IntegrityError):
        db_session.flush()
    db_session.rollback()


def test_user_service_rejects_duplicate_username(db_session):
    create_user(db_session, user_data())
    with pytest.raises(ValueError, match="already exists"):
        create_user(db_session, user_data(email="other@example.com"))


def test_user_service_rejects_duplicate_email(db_session):
    create_user(db_session, user_data())
    with pytest.raises(ValueError, match="already exists"):
        create_user(db_session, user_data(username="other"))
