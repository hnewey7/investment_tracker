'''
Module for testing CRUD operations to db.

Created on 24-06-2025
@author: Harry New

'''
from sqlmodel import Session, select

from app.models import UserCreate, User, Portfolio, Instrument
from app import crud
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password

# - - - - - - - - - - - - - - - - - - -
# USER TESTS.

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
    assert db_obj.portfolio is None

    # Check object in database.
    statement = select(User).where(User.username == properties["username"])
    result = db.exec(statement).one()
    assert result.id == db_obj.id

# - - - - - - - - - - - - - - - - - - -
# PORTFOLIO TESTS.

def test_create_portfolio(db: Session):
    """
    Test creating portfolio.

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
    user = crud.create_user(session=db,user_create=user_create)

    # Create portfolio.
    db_obj = crud.create_portfolio(session=db,user=user)

    # Check properties.
    assert db_obj.user_id == user.id
    assert db_obj.user == user

    # TODO: Check properties for assets and previous trades.

    # Check object in database.
    statement = select(Portfolio).where(Portfolio.user == user)
    result = db.exec(statement).one()
    assert result.id == db_obj.id

# - - - - - - - - - - - - - - - - - - -
# INSTRUMENT TESTS

def test_create_instrument(db: Session):
    """
    Test create instrument.

    Args:
        db (Session): SQL session.
    """
    # Properties.
    properties = {
        "name":"C&C GROUP ORD EURO.01",
        "exchange":"LSE",
        "symbol":"CCR"
    }

    # Create instrument.
    db_obj = crud.create_instrument(session=db,**properties)
    print(db_obj.__dict__)

    # Check properties.
    assert db_obj.name == properties["name"]
    assert db_obj.exchange == properties["exchange"]
    assert db_obj.symbol == properties["symbol"]

    # Check object in database.
    statement = select(Instrument).where(Instrument.name == properties["name"])
    result = db.exec(statement).one()
    assert result.id == db_obj.id