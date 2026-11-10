"""Shared PostgreSQL test fixtures for Module 10.

Requires a dedicated TEST_DATABASE_URL containing fastapi_test_db.
Never points tests at the application database.
"""
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base


@pytest.fixture(scope="session")
def test_engine():
    url = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_test_db",
    )
    if "fastapi_test_db" not in url:
        raise RuntimeError("Refusing to run tests outside fastapi_test_db")
    engine = create_engine(url, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    """Isolated transaction: even committed changes roll back after the test."""
    with test_engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
            yield session
        transaction.rollback()
