'''
Module for testing orders endpoint.

Created on 07-07-2025
@author: Harry New

'''
import pytest
from datetime import datetime

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import User, Instrument, OrderCreate
from app import crud

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID}/ORDERS TESTS

@pytest.mark.parametrize("multiple_users", [2], indirect=True)
def test_get_orders(client: TestClient, db: Session, multiple_users: list[User], instrument: Instrument):
    """
    Testing for get orders endpoint.

    Args:
        client (TestClient): Test client.
        multiple_users (list[User]): Test multiple users.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "date": datetime.now(),
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "instrument_id": instrument.id,
    }

    # Create orders.
    order_create_1 = OrderCreate(**properties)
    order_create_2 = OrderCreate(**properties)
    crud.create_order(session=db, user_id=1, order_create=order_create_1)
    crud.create_order(session=db, user_id=2, order_create=order_create_2)

    # Send get request.
    response = client.get("/users/1/orders")
    orders_json = response.json()
    assert response.status_code == 200
    assert len(orders_json["data"]) == 1
    assert orders_json["count"] == 1


@pytest.mark.parametrize("multiple_instruments", [2], indirect=True)
def test_get_orders_by_instrument(client: TestClient, db: Session, user: User, multiple_instruments: list[Instrument]):
    """
    Test get orders by instrument through endpoint.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
        multiple_instruments (list[Instrument]): Test multiple instruments.
    """
    # Properties.
    properties = {
        "date": datetime.now(),
        "volume": 1,
        "price": 1,
        "type": "BUY"
    }

    # Create orders.
    order_create_1 = OrderCreate(instrument_id=1,**properties)
    order_create_2 = OrderCreate(instrument_id=2,**properties)
    crud.create_order(session=db, user_id=user.id, order_create=order_create_1)
    crud.create_order(session=db, user_id=user.id, order_create=order_create_2)

    # Send get request.
    response = client.get("/users/1/orders",params={
        "instrument_id":1
    })
    orders_json = response.json()
    assert response.status_code == 200
    assert len(orders_json["data"]) == 1
    assert orders_json["count"] == 1


def test_get_orders_by_date(client: TestClient, db: Session, user: User, instrument: Instrument):
    """
    Test get orders by date through endpoint.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "volume": 1,
        "price": 1,
        "type": "BUY",
        "instrument_id": instrument.id
    }

    # Create orders.
    order_create_1 = OrderCreate(date=datetime.strptime("06/07/2025","%d/%m/%Y"),**properties)
    order_create_2 = OrderCreate(date=datetime.strptime("07/07/2025","%d/%m/%Y"),**properties)
    crud.create_order(session=db, user_id=user.id, order_create=order_create_1)
    crud.create_order(session=db, user_id=user.id, order_create=order_create_2)

    # Send get request.
    response = client.get("/users/1/orders",params={
        "start_date":"07/07/2025"
    })
    orders_json = response.json()
    assert response.status_code == 200
    assert len(orders_json["data"]) == 1
    assert orders_json["count"] == 1


def test_get_orders_by_type(client: TestClient, db: Session, user: User, instrument: Instrument):
    """
    Test get orders by type through endpoint.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    properties = {
        "volume": 1,
        "price": 1,
        "date": datetime.now(),
        "instrument_id": instrument.id
    }

    # Create orders.
    order_create_1 = OrderCreate(type="BUY",**properties)
    order_create_2 = OrderCreate(type="SELL",**properties)
    crud.create_order(session=db, user_id=user.id, order_create=order_create_1)
    crud.create_order(session=db, user_id=user.id, order_create=order_create_2)

    # Send get request.
    response = client.get("/users/1/orders",params={
        "type":"BUY"
    })
    orders_json = response.json()
    assert response.status_code == 200
    assert len(orders_json["data"]) == 1
    assert orders_json["count"] == 1

# - - - - - - - - - - - - - - - - - - -
# POST /USERS/{USER_ID}/ORDERS TESTS

def test_create_order(client: TestClient, db: Session, user: User, instrument: Instrument):
    """
    Test create order.

    Args:
        client (TestClient): Test client.
        db (Session): SQL session.
        user (User): Test user.
        instrument (Instrument): Test instrument.
    """
    # Properties.
    datetime_property = datetime.now()
    properties = {
        "volume": 1,
        "price": 1,
        "date": str(datetime_property),
        "type": "BUY",
        "instrument_id": instrument.id
    }

    # Send post request.
    response = client.post(f"/users/{user.id}/orders",json=properties)
    order_json = response.json()
    assert response.status_code == 200

    # Check database.
    order = crud.get_order_by_id(session=db, order_id=order_json["id"])
    assert order.volume == order_json["volume"]
    assert order.price == order_json["price"]
    assert order.date == datetime_property
    assert order.type == order_json["type"]
    assert order.instrument_id == order_json["instrument_id"]
    assert order.user_id == order_json["user_id"]

# - - - - - - - - - - - - - - - - - - -
# DELETE /USERS/{USER_ID}/ORDERS TESTS

def test_delete_orders(client: TestClient, db: Session, user: User, instrument: Instrument):
    """
    Test delete orders.

    Args:
        client (TestClient): Test client.
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
        "instrument_id": instrument.id,
    }

    # Create orders.
    order_create = OrderCreate(**properties)
    crud.create_order(session=db, user_id=1, order_create=order_create)
    crud.create_order(session=db, user_id=1, order_create=order_create)

    # Delete request.
    response = client.delete(f"/users/{user.id}/orders")
    orders_json = response.json()
    assert response.status_code == 200
    assert len(orders_json["data"]) == 2
    assert orders_json["count"] == 2
    
    # Check database.
    orders = crud.get_orders(session=db, user_id=user.id)
    assert len(orders.data) == 0
    assert orders.count == 0

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID}/ORDERS/{ORDER_ID} TESTS

def test_get_order(client: TestClient, db: Session, user: User, instrument: Instrument):
    """
    Test get order endpoint.

    Args:
        client (TestClient): Test client.
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
        "instrument_id": instrument.id,
    }

    # Create orders.
    order_create = OrderCreate(**properties)
    order = crud.create_order(session=db, user_id=user.id, order_create=order_create)

    # Send get request.
    response = client.get(f"/users/{user.id}/orders/{order.id}")
    order_json = response.json()
    assert response.status_code == 200
    assert order_json["id"] == order.id
    assert order_json["user_id"] == order.user_id
    assert order_json["instrument_id"] == order.instrument_id
    assert order_json["date"] == order.date.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert order_json["volume"] == order.volume
    assert order_json["price"] == order.price
    assert order_json["type"] == order.type