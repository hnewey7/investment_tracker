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