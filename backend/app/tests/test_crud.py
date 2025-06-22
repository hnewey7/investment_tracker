'''
Module for testing CRUD operations.

Created on 22-06-2025
@author: Harry New

'''
from sqlmodel import Session

from app.crud import create_user, authenticate
from app.models import UserCreate
from app.tests.utils.utils import random_email, random_lower_string

# - - - - - - - - - - - - - - - - - - -

def test_create_user(db: Session):
    """
    Test for creating new user.

    Args:
        db (Session): Database fixture.
    """
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    """
    Test user authentication.

    Args:
        db (Session): Database fixture.
    """
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = create_user(session=db, user_create=user_in)
    authenticated_user = authenticate(session=db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    """
    Test authentication failure.

    Args:
        db (Session): Database fixture.
    """
    email = random_email()
    password = random_lower_string()
    user = authenticate(session=db, email=email, password=password)
    assert user is None