
import pytest
from pydantic import ValidationError

from app.schemas import UserCreate
from app.security import hash_password, verify_password


def test_hash_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$argon2")


def test_verify_correct_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_wrong_password():
    hashed = hash_password("SecurePassword123!")

    assert verify_password("WrongPassword", hashed) is False


def test_hashes_are_unique():
    password = "SecurePassword123!"

    first_hash = hash_password(password)
    second_hash = hash_password(password)

    assert first_hash != second_hash


def test_valid_user_schema():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        password="SecurePassword123!",
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"


def test_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="invalid-email",
            password="SecurePassword123!",
        )


def test_short_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            password="short",
        )


def test_short_username():
    with pytest.raises(ValidationError):
        UserCreate(
            username="ab",
            email="test@example.com",
            password="SecurePassword123!",
        )
