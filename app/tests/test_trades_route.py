'''
Module for testing trades endpoint.

Created on 05-07-2025
@author: Harry New

'''
from datetime import datetime

from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models import Asset, Portfolio, Instrument
from app import crud

# - - - - - - - - - - - - - - - - - - -
# CREATE /USERS/{USER_ID}/PORTFOLIO/TRADES TESTS

def test_create_trade(client: TestClient, db: Session, portfolio: Portfolio, instrument: Instrument):
    """
    Test creating trade.

    Args:
        client (TestClient): Test client.
        db (Session): SQL session.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument.
    """
    # Create asset.
    asset = crud.create_asset(session=db, portfolio=portfolio, instrument=instrument, buy_date=datetime.now().strftime("%d/%m/%Y"), buy_price=1, volume=1)
    # Send post request.
    response = client.post(f"/users/{portfolio.user_id}/portfolio/trades", json={
        "asset_id": asset.id,
        "sell_date": datetime.now().strftime("%d/%m/%Y"),
        "sell_price": 1
    })
    trade_json = response.json()
    assert response.status_code == 200
    assert trade_json["instrument_id"] == instrument.id
    assert trade_json["portfolio_id"] == portfolio.id
