
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate
from app.security import hash_password


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user with a securely hashed password."""

    user = User(
        username=user_data.username,
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or email already exists")

    return user
