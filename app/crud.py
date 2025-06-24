'''
Module for handling CRUD operations on database.

Created on 22-06-2025
@author: Harry New

'''
from sqlmodel import Session, select

from app.models import User, UserCreate, Portfolio
from app.core.security import get_password_hash, verify_password

# - - - - - - - - - - - - - - - - - - -

def create_user(*, session: Session, user_create: UserCreate) -> User:
    """
    Create user.

    Args:
        session (Session): SQL session.
        user_create (UserCreate): UserCreate model.

    Returns:
        User: User model.
    """
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    Get user by email.

    Args:
        session (Session): SQL session.
        email (str): Email address to search for.

    Returns:
        User | None: User model or none.
    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """
    Authenticate user.

    Args:
        session (Session): SQL session.
        email (str): Email address.
        password (str): Password.

    Returns:
        User | None: User model or none.
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

# - - - - - - - - - - - - - - - - - - -

def create_portfolio(*, session: Session, user: User):
    """
    Creating portfolio for user.

    Args:
        session (Session): SQL session.
        user (User): User to assign portfolio.
    """
    db_obj = Portfolio(
        type="Overview",
        user=user
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj