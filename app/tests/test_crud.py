'''
Module for testing CRUD operations to db.

Created on 24-06-2025
@author: Harry New

'''
from datetime import datetime
import pytest

from sqlmodel import Session, select

from app.models import UserCreate, User, Instrument, OrderCreate, Order, InstrumentBase
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


def test_get_user_by_id(db:Session, user:User):
    """
    Testing get user by id.

    Args:
        db (Session): SQL session.
        user (User): Test user.
    """
    # Get user by id.
    db_obj = crud.get_user_by_id(session=db,id=user.id)

    # Check db obj.
    assert db_obj == user


def test_get_user_by_id_none(db:Session):
    """
    Testing get user by id when no user with id.

    Args:
        db (Session): SQL session.
    """
    # Get user by id.
    db_obj = crud.get_user_by_id(session=db,id=1)

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
    instrument_create = InstrumentBase(**properties)

    # Create instrument.
    db_obj = crud.create_instrument(session=db,instrument_create=instrument_create)

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


def test_get_instrument_by_id(db: Session, instrument:Instrument):
    """
    Test get instrument by id.

    Args:
        db (Session): SQL session.
        instrument (Instrument): Test instrument.
    """
    # Get instrument.
    db_obj = crud.get_instrument_by_id(session=db,id=instrument.id)
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
    instrument_create = InstrumentBase(**properties)

    # Create instrument.
    instrument = crud.create_instrument(session=db,instrument_create=instrument_create)

    # Update instrument prices.
    update_prices = {
        "open": 1,
        "high": 2,
        "low": 3,
        "close": 4
    }
    db_obj = crud.update_instrument_prices(session=db,instrument=instrument,**update_prices)

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
    instrument_create = InstrumentBase(**properties)

    # Create instrument.
    instrument = crud.create_instrument(session=db,instrument_create=instrument_create)

    # Update currency.
    db_obj = crud.update_instrument_currency(session=db,instrument=instrument,currency="GBP")
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
    instrument_create = InstrumentBase(**properties)

    # Create instrument.
    instrument = crud.create_instrument(session=db,instrument_create=instrument_create)
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=instrument.symbol)
    assert db_obj == instrument

    # Delete instrument and check.
    crud.delete_instrument(session=db,instrument=instrument)
    db_obj = crud.get_instrument_by_symbol(session=db,symbol=instrument.symbol)
    assert db_obj == None

# - - - - - - - - - - - - - - - - - - -
# ORDER TESTS

def test_create_order(db: Session, user: User, instrument: Instrument):
    """
    Test creating an order.

    Args:
        db (Session): SQL session.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "date": datetime.now(),
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "user_id": user.id,
        "instrument_id": instrument.id
    }

    # Create order.
    order_create = OrderCreate(**properties)
    db_obj = crud.create_order(session=db, order_create=order_create)

    # Check properties.
    assert db_obj.date == properties["date"]
    assert db_obj.volume == properties["volume"]
    assert db_obj.price == properties["price"]
    assert db_obj.type == properties["type"]
    assert db_obj.user_id == properties["user_id"]
    assert db_obj.instrument_id == properties["instrument_id"]

    # Check user and instrument.
    assert db_obj.user == user
    assert db_obj.instrument == instrument


@pytest.mark.parametrize("multiple_users", [2], indirect=True)
def test_get_orders_by_user(db: Session, multiple_users: list[User], instrument: Instrument):
    """
    Test getting orders for given user.

    Args:
        db (Session): SQL session.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "user_id": 1,
        "instrument_id": instrument.id
    }

    # Create order.
    order_create = OrderCreate(date=datetime.now(),**properties)
    test_order_1 = crud.create_order(session=db, order_create=order_create)

    # Get orders.
    db_obj = crud.get_orders_by_user(session=db, user_id=1)
    assert len(db_obj.data) == 1
    assert db_obj.count == 1
    assert db_obj.data[0] == test_order_1


@pytest.mark.parametrize("multiple_instruments", [2], indirect=True)
def test_get_orders_by_instrument(db: Session, user: User, multiple_instruments: list[Instrument]):
    """
    Test get order by instrument.

    Args:
        db (Session): SQL session.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "user_id": user.id,
        "instrument_id": 1
    }

    # Create order.
    order_create = OrderCreate(date=datetime.now(),**properties)
    test_order_1 = crud.create_order(session=db, order_create=order_create)

    # Get orders.
    db_obj = crud.get_orders_by_instrument(session=db, user_id=user.id, instrument_id=1)
    assert len(db_obj.data) == 1
    assert db_obj.count == 1
    assert db_obj.data[0] == test_order_1

    # Create another order.
    order_create = OrderCreate(date=datetime.now(),**properties)
    test_order_2 = crud.create_order(session=db, order_create=order_create)

    # Get orders.
    db_obj = crud.get_orders_by_instrument(session=db, user_id=user.id, instrument_id=1)
    assert len(db_obj.data) == 2
    assert db_obj.count == 2
    assert db_obj.data[0] == test_order_1
    assert db_obj.data[1] == test_order_2


def test_get_orders_by_date(db: Session, user: User, instrument: Instrument):
    """
    Test getting orders by date.

    Args:
        db (Session): SQL session.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "user_id": user.id,
        "instrument_id": instrument.id
    }

    # Create two orders.
    order_create_1 = OrderCreate(date=datetime.strptime("06/07/2025","%d/%m/%Y"),**properties)
    order_create_2 = OrderCreate(date=datetime.strptime("07/07/2025","%d/%m/%Y"),**properties)
    test_order_1 = crud.create_order(session=db, order_create=order_create_1)
    test_order_2 = crud.create_order(session=db, order_create=order_create_2)

    # Get orders by date.
    orders = crud.get_orders_by_date(session=db, user_id=user.id, start_date="07/07/2025")
    assert orders.count == 1
    assert orders.data[0] == test_order_2


def test_get_order_by_id(db: Session, user: User, instrument: Instrument):
    """
    Test get order by id.

    Args:
        db (Session): SQL session.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "user_id": user.id,
        "instrument_id": instrument.id
    }

    # Create two orders.
    order_create = OrderCreate(date=datetime.now(),**properties)
    test_order_1 = crud.create_order(session=db, order_create=order_create)
    test_order_2 = crud.create_order(session=db, order_create=order_create)

    # Get order by id.
    db_obj = crud.get_order_by_id(session=db, order_id=test_order_1.id)
    assert test_order_1 == db_obj