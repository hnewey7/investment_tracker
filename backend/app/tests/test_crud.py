'''
Module for testing CRUD operations.

Created on 22-06-2025
@author: Harry New

'''
from sqlmodel import Session

from app.crud import create_user
from app.models import UserCreate

# - - - - - - - - - - - - - - - - - - -

def test_create_user(db: Session):
    """
    Test for creating new user.

    Args:
        db (Session): Fixture for getting Session for database.
    """
    email = "random_email@gmail.com"
    password = "testtest"
    user_in = UserCreate(email=email, password=password)
    user = create_user(session=db, user_create=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")