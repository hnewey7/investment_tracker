'''
Module for testing instrument endpoint.

Created on 02-07-2025
@author: Harry New

'''
from fastapi.testclient import TestClient

from app.models import Instrument

# - - - - - - - - - - - - - - - - - - -
# GET /INSTRUMENTS

def test_get_instruments(client: TestClient, instrument: Instrument):
    """
    Test get all instruments.

    Args:
        client (TestClient): _description_
    """
    # Send get request.
    response = client.get("/instruments")
    instrument_list_json = response.json()
    assert response.status_code == 200
    assert instrument_list_json["count"] == 1
    assert instrument_list_json["data"][0]["name"] == instrument.name
    assert instrument_list_json["data"][0]["exchange"] == instrument.exchange
    assert instrument_list_json["data"][0]["symbol"] == instrument.symbol
    assert instrument_list_json["data"][0]["currency"] == instrument.currency

    # Test for different params.
    response = client.get("/instruments",params={
        "name":"test"
    })
    instrument_list_json = response.json()
    assert response.status_code == 200
    assert len(instrument_list_json["data"]) == 0

    response = client.get("/instruments",params={
        "exchange":"test"
    })
    instrument_list_json = response.json()
    assert response.status_code == 200
    assert len(instrument_list_json["data"]) == 0

    response = client.get("/instruments",params={
        "symbol":"test"
    })
    instrument_list_json = response.json()
    assert response.status_code == 200
    assert len(instrument_list_json["data"]) == 0

    response = client.get("/instruments",params={
        "currency":"test"
    })
    instrument_list_json = response.json()
    assert response.status_code == 200
    assert len(instrument_list_json["data"]) == 0

# - - - - - - - - - - - - - - - - - - -
# POST /INSTRUMENTS

def test_create_instrument(client: TestClient):
    """
    Test create instrument.

    Args:
        client (TestClient): Test client.
    """
    # Instrument properties.
    properties = {
        "name":"C&C GROUP ORD EURO.01",
        "exchange":"LSE",
        "symbol":"CCR",
        "currency":"GBX"
    }
    # Send post request.
    response = client.post("/instruments",json=properties)
    instrument_json = response.json()
    assert response.status_code == 200
    assert instrument_json["name"] == properties["name"]
    assert instrument_json["exchange"] == properties["exchange"]
    assert instrument_json["symbol"] == properties["symbol"]
    assert instrument_json["currency"] == properties["currency"]

# - - - - - - - - - - - - - - - - - - -
# GET /INSTRUMENTS/{INSTRUMENT_ID}

def test_get_instrument(client: TestClient, instrument: Instrument):
    """
    Test get instrument.

    Args:
        client (TestClient): Test client.
        instrument (Instrument): Test instrument.
    """
    # Send get request.
    response = client.get(f"/instruments/{instrument.id}")
    instrument_json = response.json()
    assert response.status_code == 200
    assert instrument_json["id"] == instrument.id
    assert instrument_json["name"] == instrument.name
    assert instrument_json["exchange"] == instrument.exchange
    assert instrument_json["symbol"] == instrument.symbol
    assert instrument_json["currency"] == instrument.currency


def test_get_instrument_invalid(client: TestClient):
    """
    Test get instrument for invalid instrument.

    Args:
        client (TestClient): Test client.
    """
    # Send get request.
    response = client.get("/instruments/1")
    assert response.status_code == 400

# - - - - - - - - - - - - - - - - - - -
# UPDATE /INSTRUMENTS/{INSTRUMENT_ID}

def test_update_instrument_currency(client: TestClient, instrument: Instrument):
    """
    Test update instrument currency.

    Args:
        client (TestClient): Test client.
        instrument (Instrument): Test instrument.
    """
    # New currency.
    new_currency = "GBP"
    # Send update request.
    response = client.put(f"/instruments/{instrument.id}/",json={
        "currency":new_currency
    })
    instrument_json = response.json()
    assert response.status_code == 200
    assert instrument_json["currency"] == new_currency


def test_update_instrument_prices(client: TestClient, instrument: Instrument):
    """
    Test update instrument prices.

    Args:
        client (TestClient): Test client.
        instrument (Instrument): Test instrument.
    """
    # New prices.
    new_prices = [1,1,1,1]
    # Send update request.
    response = client.put(f"/instruments/{instrument.id}/",json={
        "prices":new_prices
    })
    instrument_json = response.json()
    assert response.status_code == 200
    assert instrument_json["open"] == new_prices[0]
    assert instrument_json["high"] == new_prices[1]
    assert instrument_json["low"] == new_prices[2]
    assert instrument_json["close"] == new_prices[3]


def test_update_instrument_currency_and_prices(client: TestClient, instrument: Instrument):
    """
    Test updating instrument currency and prices.

    Args:
        client (TestClient): Test client.
        instrument (Instrument): Test instrument.
    """
    # New currency and prices.
    new_currency = "GBP"
    new_prices = [1,1,1,1]
    # Send update request.
    response = client.put(f"/instruments/{instrument.id}/",json={
        "currency":new_currency,
        "prices":new_prices
    })
    instrument_json = response.json()
    assert response.status_code == 200
    assert instrument_json["currency"] == new_currency
    assert instrument_json["open"] == new_prices[0]
    assert instrument_json["high"] == new_prices[1]
    assert instrument_json["low"] == new_prices[2]
    assert instrument_json["close"] == new_prices[3]


def test_update_instrument_invalid_instrument(client: TestClient):
    """
    Test updating instrument with invalid instrument.

    Args:
        client (TestClient): Test client.
    """
    # New currency.
    new_currency = "GBP"
    # Send update request.
    response = client.put("/instruments/1/",json={
        "currency":new_currency
    })
    assert response.status_code == 400


def test_update_instrument_invalid_input(client: TestClient, instrument: Instrument):
    """
    Test update instrument with invalid input.

    Args:
        client (TestClient): Test client.
        instrument (Instrument): Test instrument.
    """
    # Send update request.
    response = client.put("/instruments/1/",json={})
    assert response.status_code == 400