'''
Module for testing assets endpoint.

Created on 04-07-2025
@author: Harry New

'''
from datetime import datetime

from fastapi.testclient import TestClient

from app.models import Portfolio, Instrument

# - - - - - - - - - - - - - - - - - - -
# CREATE /USERS/{USER_ID}/PORTFOLIO/ASSETS TESTS

def test_create_asset(client: TestClient, portfolio: Portfolio, instrument: Instrument):
    """
    Test creating asset endpoint.

    Args:
        client (TestClient): Test client.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument.
    """
    # Send request to create asset.
    response = client.post(f"/users/{portfolio.user_id}/portfolio/assets", json={
        "buy_date":datetime.now().strftime("%d/%m/%Y"),
        "buy_price":1,
        "volume":1,
        "instrument_id":instrument.id
    })
    asset_json = response.json()
    assert response.status_code == 200
    assert asset_json["instrument_id"] == instrument.id
    assert asset_json["portfolio_id"] == portfolio.id
    assert asset_json["buy_price"] == 1
    assert asset_json["volume"] == 1