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


def test_get_user_by_email(db:Session):
    """
    Test get user by email.

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

    # Get user by email.
    db_obj = crud.get_user_by_email(session=db,email=user.email)

    # Check db obj.
    assert db_obj == user


def test_get_user_by_email_none(db:Session):
    """
    Test get user by email when no user created.

    Args:
        db (Session): SQL session.
    """
    # Get user by email.
    db_obj = crud.get_user_by_email(session=db,email=random_email())

    # Check db obj.
    assert db_obj == None


def test_get_user_by_username(db:Session):
    """
    Test get user by username.

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

    # Get user by username.
    db_obj = crud.get_user_by_username(session=db,username=user.username)

    # Check db obj.
    assert db_obj == user


def test_get_user_by_username_none(db:Session):
    """
    Test get user by username when no user created.

    Args:
        db (Session): SQL session.
    """
    # Get user by username.
    db_obj = crud.get_user_by_username(session=db,username=random_lower_string())

    # Check db obj.
    assert db_obj == None


def test_valid_authenticate(db:Session):
    """
    Test valid user authenication.

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

    # Authenticate user by email.
    db_obj = crud.authenticate(session=db,email=properties["email"],password=properties["password"])
    assert db_obj == user

    # Authenticate user by username.
    db_obj = crud.authenticate(session=db,username=properties["username"],password=properties["password"])
    assert db_obj == user


def test_invalid_authentication(db:Session):
    """
    Test invalid user authentication.

    Args:
        db (Session): SQL session.
    """
    # Properties.
    properties = {
        "email": random_email(),
        "password": random_lower_string(),
        "username":random_lower_string()
    }

    # Authenticate user by email.
    db_obj = crud.authenticate(session=db,email=properties["email"],password=properties["password"])
    assert db_obj == None

    # Authenticate user by username.
    db_obj = crud.authenticate(session=db,username=properties["username"],password=properties["password"])
    assert db_obj == None


def test_invalid_password_authentication(db:Session):
    """
    Test invalid password for user authentication.

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

    # Authenticate with invalid password.
    db_obj = crud.authenticate(session=db,email=properties["email"],password=random_lower_string())
    assert db_obj == None

    db_obj = crud.authenticate(session=db,username=properties["username"],password=random_lower_string())
    assert db_obj == None


def test_change_username(db:Session):
    """
    Test change username.

    Args:
        db (Session): SQL session.
    """
    # Properties.
    properties = {
        "username": random_lower_string(),
        "new_username": random_lower_string(),
        "email": random_email(),
        "password": random_lower_string()
    }

    # Create user.
    user_create = UserCreate(**properties)
    user = crud.create_user(session=db,user_create=user_create)

    # Update username.
    db_obj = crud.change_username(session=db,email=properties["email"],new_username=properties["new_username"])
    assert db_obj.username == properties["new_username"]

    # Check database for new user.
    db_obj = crud.get_user_by_username(session=db, username=properties["new_username"])
    assert db_obj.username == properties["new_username"]


def test_change_password(db:Session):
    """
    Test change password.

    Args:
        db (Session): SQL session.
    """
    # Properties.
    properties = {
        "username": random_lower_string(),
        "email": random_email(),
        "password": random_lower_string(),
        "new_password": random_lower_string()
    }

    # Create user.
    user_create = UserCreate(**properties)
    user = crud.create_user(session=db,user_create=user_create)

    # Update password.
    db_obj = crud.change_password(session=db,email=properties["email"],new_password=properties["new_password"])
    assert verify_password(properties["new_password"],db_obj.hashed_password)

    # Verify authentication.
    user = crud.get_user_by_email(session=db,email=properties["email"])
    db_obj = crud.authenticate(session=db,email=properties["email"],password=properties["new_password"])
    assert db_obj == user


def test_delete_user(db:Session):
    """
    Test delete user.

    Args:
        db (Session): _description_
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

    # Delete user.
    crud.delete_user(session=db,user=user)
    
    # Verify delete.
    db_obj = crud.get_user_by_email(session=db,email=properties["email"])
    assert db_obj == None

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


def test_delete_portfolio(db: Session):
    """
    Test deleting portfolio.

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
    portfolio = crud.create_portfolio(session=db,user=user)

    # Verify portfolio exists.
    assert user.portfolio == portfolio

    # Delete portfolio.
    crud.delete_portfolio(session=db,portfolio=portfolio)

    # Verify delete through user.
    assert user.portfolio == None

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

    # Check properties.
    assert db_obj.name == properties["name"]
    assert db_obj.exchange == properties["exchange"]
    assert db_obj.symbol == properties["symbol"]

    # Check object in database.
    statement = select(Instrument).where(Instrument.name == properties["name"])
    result = db.exec(statement).one()
    assert result.id == db_obj.id


def test_get_instrument_by_symbol(db: Session):
    """
    Test get instrument by symbol.

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
    instrument = crud.create_instrument(session=db,**properties)

    # Get instrument.
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=instrument.symbol)
    assert db_obj == instrument


def test_update_instrument_price(db: Session):
    """
    Test update instrument price.

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
    instrument = crud.create_instrument(session=db,**properties)

    # Update instrument prices.
    update_prices = {
        "open": 1,
        "high": 2,
        "low": 3,
        "close": 4
    }
    db_obj = crud.update_price(session=db,instrument=instrument,**update_prices)

    # Check prices.
    assert db_obj.open == update_prices["open"]
    assert db_obj.high == update_prices["high"]
    assert db_obj.low == update_prices["low"]
    assert db_obj.close == update_prices["close"]


def test_delete_instrument(db: Session):
    """
    Test deleting instrument.

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
    instrument = crud.create_instrument(session=db,**properties)
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=properties["symbol"])
    assert db_obj == instrument

    # Delete instrument and check.
    crud.delete_instrument(session=db,instrument=instrument)
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=properties["symbol"])
    assert db_obj == None