'''
Module for testing portfolio subrouter for user.

Created on 01-07-2025
@author: Harry New

'''
from fastapi.testclient import TestClient

from app.models import Portfolio, User

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID}/PORTFOLIO TESTS

def test_get_portfolio(client: TestClient, portfolio: Portfolio):
    """
    Test get user's portfolio.

    Args:
        client (TestClient): Test client.
        portfolio (Portfolio): Test portfolio.
    """
    # Send get request.
    response = client.get(f"/users/{portfolio.user_id}/portfolio")
    portfolio_json = response.json()
    assert response.status_code == 200
    assert portfolio_json["id"] == portfolio.id
    assert portfolio_json["user_id"] == portfolio.user_id
    assert portfolio_json["type"] == portfolio.type


def test_get_portfolio_invalid_user(client: TestClient):
    """
    Test get portfolio for an invalid user.

    Args:
        client (TestClient): Test client.
    """
    # Send get request.
    response = client.get(f"/users/1/portfolio")
    assert response.status_code == 400


def test_get_portfolio_invalid_portfolio(client: TestClient, user: User):
    """
    Test get user's portfolio for invalid portfolio.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Send get request.
    response = client.get(f"/users/{user.id}/portfolio")
    assert response.status_code == 400

# - - - - - - - - - - - - - - - - - - -
# CREATE /USERS/{USER_ID}/PORTFOLIO TESTS

def test_create_portfolio(client: TestClient, user: User):
    """
    Test creating a new portfolio for a user.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Send post request.
    response = client.post(f"/users/{user.id}/portfolio")
    portfolio_json = response.json()
    assert response.status_code == 200
    assert "id" in portfolio_json.keys()
    assert "type" in portfolio_json.keys()
    assert portfolio_json["user_id"] == user.id


def test_create_portfolio_invalid_user(client: TestClient):
    """
    Test creating portfolio for an invalid user.

    Args:
        client (TestClient): Test client.
    """
    # Send post request.
    response = client.post(f"/users/1/portfolio")
    assert response.status_code == 400