'''
Module for testing CRUD operations to db.

Created on 24-06-2025
@author: Harry New

'''
from sqlmodel import Session, select

from app.models import UserCreate, User
from app import crud
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password

# - - - - - - - - - - - - - - - - - - -

def test_create_user(db: Session):
    """
    Test user creation.

    Args:
        db (Session): SQL session.
    """
    # Properties.
    properties = {
        "username": random_lower_string(),
        "email": random_email(),
        "password": random_lower_string()
    }

    # Create user.
    user_create = UserCreate(**properties)

    # Add to database.
    db_obj = crud.create_user(session=db,user_create=user_create)

    # Check provided properties returned by db obj.
    for key in properties.keys():
        if key != "password":
            assert key in db_obj.__dict__
            assert db_obj.__dict__[key] == properties[key]
        else:
            assert verify_password(properties[key],db_obj.__dict__["hashed_password"])
    
    # Check db generated properties.
    assert db_obj.id == 1
    assert db_obj.portfolio is None

    # Check object in database.
    statement = select(User).where(User.username == properties["username"])
    result = db.exec(statement).one()
    assert result.id == 1