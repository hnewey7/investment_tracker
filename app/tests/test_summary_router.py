'''
Module for handling testing of summary endpoints.

Created on 16-07-2025
@author: Harry New

'''
from fastapi.testclient import TestClient

from app.models import User, Summary, SummaryUpdate

# - - - - - - - - - - - - - - - - - - -

def test_get_summary(client: TestClient, user: User, summary: Summary):
    """
    Test get summary endpoint for given user.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
        summary (Summary): Test summary.
    """
    # Send get request to endpoint.
    response = client.get(f"/users/{user.id}/summary")
    summary_json = response.json()

    # Check summary.
    assert response.status_code == 200
    assert summary_json["user_id"] == user.id
    assert summary_json["ending_market_value"] == None
    assert summary_json["beginning_market_value"] == None
    assert summary_json["profit_loss"] == None


def test_put_summary(client: TestClient, user: User, summary: Summary):
    """
    Test updating summary.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
        summary (Summary): Test summary.
    """
    # Properties to update.
    properties = {
        "ending_market_value":1,
        "beginning_market_value":1,
        "profit_loss":1
    }
    
    # Send put request.
    response = client.put(f"/users/{user.id}/summary",json=properties)
    updated_summary = response.json()

    assert response.status_code == 200
    for key in properties:
        assert updated_summary[key] == properties[key]