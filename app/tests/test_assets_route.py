'''
Module for testing assets endpoint.

Created on 04-07-2025
@author: Harry New

'''
from datetime import datetime

from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models import Portfolio, Instrument, User, Asset
from app import crud

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID}/PORTFOLIO/ASSETS TESTS

def test_get_assets(client: TestClient, db: Session, portfolio: Portfolio, instrument: Instrument):
    """
    Test get assets in user's portfolio.

    Args:
        client (TestClient): Test client.
        portfolio (Portfolio): Test portfolio.
        instrument (Instrument): Test instrument
    """
    # Create asset.
    asset_properties = {
        "buy_date":datetime.now().strftime("%d/%m/%Y"),
        "buy_price":1,
        "volume":1
    }
    asset = crud.create_asset(session=db, portfolio=portfolio, instrument=instrument, **asset_properties)
    
    # Send get request.
    response = client.get(f"/users/{portfolio.user_id}/portfolio/assets")
    assets_json = response.json()
    assert response.status_code == 200
    assert len(assets_json["data"]) == 1
    assert assets_json["count"] == 1
    assert assets_json["data"][0]["id"] == asset.id


def test_get_assets_invalid_user(client: TestClient):
    """
    Test get assets for invalid user.

    Args:
        client (TestClient): Test client.
    """
    # Send get request.
    response = client.get("/users/1/portfolio/assets")
    assert response.status_code == 400


def test_get_assets_invalid_portfolio(client: TestClient, user: User):
    """
    Test get assets with invalid portfolio.

    Args:
        client (TestClient): Test client.
    """
    # Send get request.
    response = client.get(f"/users/{user.id}/portfolio/assets")
    assert response.status_code == 400

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


def test_create_asset_invalid_user(client: TestClient):
    """
    Test create asset for an invalid user.

    Args:
        client (TestClient): SQL session.
    """
    # Send post request.
    response = client.post(f"/users/1/portfolio/assets/", json={
        "buy_date":datetime.now().strftime("%d/%m/%Y"),
        "buy_price":1,
        "volume":1,
        "instrument_id":1
    })
    assert response.status_code == 400


def test_create_asset_invalid_portfolio(client: TestClient, user: User):
    """
    Test create asset for invalid portfolio.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Send post request.
    response = client.post(f"/users/{user.id}/portfolio/assets/",json={
        "buy_date":datetime.now().strftime("%d/%m/%Y"),
        "buy_price":1,
        "volume":1,
        "instrument_id":1
    })
    assert response.status_code == 400


def test_create_asset_invalid_instrument(client: TestClient, portfolio: Portfolio):
    """
    Test create asset for invalid instrument.

    Args:
        client (TestClient): Test client.
        portfolio (Portfolio): Test portfolio.
    """
    # Send post request.
    response = client.post(f"/users/{portfolio.user_id}/portfolio/assets/",json={
        "buy_date":datetime.now().strftime("%d/%m/%Y"),
        "buy_price":1,
        "volume":1,
        "instrument_id":1
    })
    assert response.status_code == 400