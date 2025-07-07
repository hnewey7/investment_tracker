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
    order_create_1 = OrderCreate(user_id=1,**properties)
    order_create_2 = OrderCreate(user_id=2,**properties)
    crud.create_order(session=db, order_create=order_create_1)
    crud.create_order(session=db, order_create=order_create_2)

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
        "type": "BUY",
        "user_id": user.id,
    }

    # Create orders.
    order_create_1 = OrderCreate(instrument_id=1,**properties)
    order_create_2 = OrderCreate(instrument_id=2,**properties)
    crud.create_order(session=db, order_create=order_create_1)
    crud.create_order(session=db, order_create=order_create_2)

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
        "user_id": user.id,
        "instrument_id": instrument.id
    }

    # Create orders.
    order_create_1 = OrderCreate(date=datetime.strptime("06/07/2025","%d/%m/%Y"),**properties)
    order_create_2 = OrderCreate(date=datetime.strptime("07/07/2025","%d/%m/%Y"),**properties)
    crud.create_order(session=db, order_create=order_create_1)
    crud.create_order(session=db, order_create=order_create_2)

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
        "user_id": user.id,
        "instrument_id": instrument.id
    }

    # Create orders.
    order_create_1 = OrderCreate(type="BUY",**properties)
    order_create_2 = OrderCreate(type="SELL",**properties)
    crud.create_order(session=db, order_create=order_create_1)
    crud.create_order(session=db, order_create=order_create_2)

    # Send get request.
    response = client.get("/users/1/orders",params={
        "type":"BUY"
    })
    orders_json = response.json()
    assert response.status_code == 200
    assert len(orders_json["data"]) == 1
    assert orders_json["count"] == 1
