'''
Module for testing CRUD operations to db.

Created on 24-06-2025
@author: Harry New

'''
from datetime import datetime

from sqlmodel import Session, select

from app.models import UserCreate, User, Portfolio, Instrument, Asset
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


def test_get_user_by_email(db:Session,user:User):
    """
    Test get user by email.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
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


def test_get_user_by_username(db:Session,user:User):
    """
    Test get user by username.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
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


def test_change_username(db:Session,user:User):
    """
    Test change username.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
    # Properties.
    properties = {
        "new_username": random_lower_string()
    }

    # Update username.
    db_obj = crud.change_username(session=db,email=user.email,new_username=properties["new_username"])
    assert db_obj.username == properties["new_username"]

    # Check database for new user.
    db_obj = crud.get_user_by_username(session=db, username=properties["new_username"])
    assert db_obj.username == properties["new_username"]


def test_change_password(db:Session,user:User):
    """
    Test change password.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
    # Properties.
    properties = {
        "new_password": random_lower_string()
    }

    # Update password.
    db_obj = crud.change_password(session=db,email=user.email,new_password=properties["new_password"])
    assert verify_password(properties["new_password"],db_obj.hashed_password)

    # Verify authentication.
    user = crud.get_user_by_email(session=db,email=user.email)
    db_obj = crud.authenticate(session=db,email=user.email,password=properties["new_password"])
    assert db_obj == user


def test_delete_user(db:Session, user:User):
    """
    Test delete user.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
    # Reference email.
    email = user.email

    # Delete user.
    crud.delete_user(session=db,user=user)
    
    # Verify delete.
    db_obj = crud.get_user_by_email(session=db,email=email)
    assert db_obj == None

# - - - - - - - - - - - - - - - - - - -
# PORTFOLIO TESTS.

def test_create_portfolio(db: Session,user:User):
    """
    Test creating portfolio.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
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


def test_delete_portfolio(db: Session, user:User):
    """
    Test deleting portfolio.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
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
        "symbol":"CCR",
        "currency":"GBX"
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


def test_get_instrument_by_symbol(db: Session, instrument:Instrument):
    """
    Test get instrument by symbol.

    Args:
        db (Session): SQL session.
        instrument (Instrument): Test instrument.
    """
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
        "symbol":"CCR",
        "currency":"GBX"
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


def test_update_instrument_currency(db: Session):
    """
    Test update currency of instrument.

    Args:
        db (Session): SQL session.
    """
    # Properties.
    properties = {
        "name":"C&C GROUP ORD EURO.01",
        "exchange":"LSE",
        "symbol":"CCR",
        "currency":"GBX"
    }

    # Create instrument.
    instrument = crud.create_instrument(session=db,**properties)

    # Update currency.
    db_obj = crud.update_currency(session=db,instrument=instrument,currency="GBP")
    assert db_obj.currency == "GBP"
    assert db_obj == instrument


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
        "symbol":"CCR",
        "currency":"GBX"
    }

    # Create instrument.
    instrument = crud.create_instrument(session=db,**properties)
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=instrument.symbol)
    assert db_obj == instrument

    # Delete instrument and check.
    crud.delete_instrument(session=db,instrument=instrument)
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=instrument.symbol)
    assert db_obj == None

# - - - - - - - - - - - - - - - - - - -
# ASSET TESTS

def test_create_asset(db:Session,portfolio:Portfolio,instrument:Instrument):
    """
    Test creating asset.

    Args:
        db (Session): SQL session.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    asset_properties = {
        "buy_date":datetime.now(),
        "buy_price":1,
        "volume":1
    }

    # Create asset.
    db_obj = crud.create_asset(session=db,portfolio=portfolio,instrument=instrument,**asset_properties)
    
    # Check given properties.
    assert db_obj.buy_date == asset_properties["buy_date"]
    assert db_obj.buy_price == asset_properties["buy_price"]
    assert db_obj.volume == asset_properties["volume"]
    assert db_obj.instrument == instrument
    assert db_obj.instrument_id == instrument.id
    assert db_obj.portfolio == portfolio
    assert db_obj.portfolio_id == portfolio.id


def test_get_assets_by_instrument(db:Session,portfolio:Portfolio,instrument:Instrument):
    """
    Test get assets by instrument within a given portfolio.

    Args:
        db (Session): SQL session.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    asset_properties = {
        "buy_date":datetime.now(),
        "buy_price":1,
        "volume":1
    }

    # Create asset.
    asset = crud.create_asset(session=db,portfolio=portfolio,instrument=instrument,**asset_properties)

    # Get asset by instrument.
    db_obj = crud.get_assets_by_instrument(session=db,portfolio=portfolio,instrument=instrument)
    assert db_obj[0] == asset


def test_update_asset_buy_price(db:Session,portfolio:Portfolio,instrument:Instrument):
    """
    Test update asset buy price.

    Args:
        db (Session): SQL session.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    asset_properties = {
        "buy_date":datetime.now(),
        "buy_price":1,
        "volume":1
    }
    
    # Create asset.
    asset = crud.create_asset(session=db,portfolio=portfolio,instrument=instrument,**asset_properties)

    # Update volume
    db_obj = crud.update_asset_buy_price(session=db,asset=asset,buy_price=2)
    assert asset.buy_price == 2
    assert db_obj.buy_price == 2


def test_update_asset_volume(db:Session,portfolio:Portfolio,instrument:Instrument):
    """
    Test update asset volume.

    Args:
        db (Session): SQL session.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    asset_properties = {
        "buy_date":datetime.now(),
        "buy_price":1,
        "volume":1
    }
    
    # Create asset.
    asset = crud.create_asset(session=db,portfolio=portfolio,instrument=instrument,**asset_properties)

    # Update volume
    db_obj = crud.update_asset_volume(session=db,asset=asset,volume=2)
    assert asset.volume == 2
    assert db_obj.volume == 2


def test_delete_asset(db:Session,portfolio:Portfolio,instrument:Instrument):
    """
    Test delete asset.

    Args:
        db (Session): SQL session.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrumnet.
    """
    # Properties.
    asset_properties = {
        "buy_date":datetime.now(),
        "buy_price":1,
        "volume":1
    }
    
    # Create asset.
    asset = crud.create_asset(session=db,portfolio=portfolio,instrument=instrument,**asset_properties)
    db_obj = crud.get_assets_by_instrument(session=db,portfolio=portfolio,instrument=instrument)
    assert db_obj[0] == asset

    # Delete asset.
    crud.delete_asset(session=db,asset=asset)
    db_obj = crud.get_assets_by_instrument(session=db,portfolio=portfolio,instrument=instrument)
    assert len(db_obj) == 0