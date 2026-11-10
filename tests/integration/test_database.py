from unittest.mock import MagicMock, patch

from sqlalchemy import text

from app import database


def test_database_engine_configured():
    assert database.engine is not None
    assert database.engine.pool is not None
    assert database.engine.pool._pre_ping is True


def test_session_factory_configured():
    assert database.SessionLocal.kw["autoflush"] is False
    assert database.SessionLocal.kw["autocommit"] is False
    assert database.SessionLocal.kw["bind"] is database.engine


def test_database_connection():
    with database.engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar_one() == 1


def test_get_db_yields_and_closes_session():
    mock_session = MagicMock()

    with patch.object(database, "SessionLocal", return_value=mock_session):
        generator = database.get_db()

        assert next(generator) is mock_session

        try:
            next(generator)
        except StopIteration:
            pass
        else:
            raise AssertionError("get_db should yield only once")

        mock_session.close.assert_called_once()
