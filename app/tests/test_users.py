'''
Module for testing user endpoints.

Created on 22-06-2025
@author: Harry New

'''
from fastapi.testclient import TestClient

from app.tests.utils.utils import random_email, random_lower_string

# - - - - - - - - - - - - - - - - - - -

def test_create_user_by_normal_user(
    client: TestClient
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        "/users/",
        json=data,
    )
    assert r.status_code == 200