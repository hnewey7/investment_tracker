'''
Module for testing instrument endpoint.

Created on 02-07-2025
@author: Harry New

'''
from fastapi.testclient import TestClient

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