
import os

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.models import Base, User
from app.schemas import UserCreate, UserRead
from app.security import verify_password
from app.user_service import create_user


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_test_db",
)

if "fastapi_test_db" not in TEST_DATABASE_URL:
    raise RuntimeError("Tests must use the dedicated test database")

engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        session.query(User).delete()
        session.commit()

        yield session

        session.rollback()

    with Session(engine) as session:
        session.query(User).delete()
        session.commit()


def test_create_user(db):
    data = UserCreate(
        username="newuser",
        email="newuser@example.com",
        password="SecurePassword123!",
    )

    user = create_user(db, data)

    assert user.id is not None
    assert user.username == "newuser"
    assert user.password_hash != data.password
    assert verify_password(data.password, user.password_hash)


def test_duplicate_username(db):
    create_user(
        db,
        UserCreate(
            username="duplicate",
            email="first@example.com",
            password="SecurePassword123!",
        ),
    )

    with pytest.raises(ValueError, match="already exists"):
        create_user(
            db,
            UserCreate(
                username="duplicate",
                email="second@example.com",
                password="SecurePassword123!",
            ),
        )


def test_duplicate_email(db):
    create_user(
        db,
        UserCreate(
            username="firstuser",
            email="duplicate@example.com",
            password="SecurePassword123!",
        ),
    )

    with pytest.raises(ValueError, match="already exists"):
        create_user(
            db,
            UserCreate(
                username="seconduser",
                email="duplicate@example.com",
                password="SecurePassword123!",
            ),
        )


def test_user_saved_in_database(db):
    data = UserCreate(
        username="saveduser",
        email="saved@example.com",
        password="SecurePassword123!",
    )

    create_user(db, data)

    saved_user = db.scalar(
        select(User).where(User.username == "saveduser")
    )

    assert saved_user is not None
    assert saved_user.email == "saved@example.com"


def test_user_read_excludes_password(db):
    data = UserCreate(
        username="publicuser",
        email="public@example.com",
        password="SecurePassword123!",
    )

    user = create_user(db, data)
    response = UserRead.model_validate(user)

    assert response.username == "publicuser"
    assert "password_hash" not in response.model_dump()
