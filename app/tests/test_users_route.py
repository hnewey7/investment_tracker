'''
Module for testing the users route.

Created on 29-06-2025
@author: Harry New

'''

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import User
from app.tests.utils.utils import random_email, random_lower_string

# - - - - - - - - - - - - - - - - - - -

def test_get_users(client: TestClient, user: User):
    """
    Test get users endpoint.

    Args:
        client (TestClient): Test client.
        db (Session): SQL session.
    """
    # Send request to get users.
    response = client.get("/users")
    user_list = response.json()

    # Check length of response.
    assert len(user_list["data"]) == 1
    assert user_list["count"] == 1

    # Check user provided.
    assert user_list["data"][0]["username"] == user.username
    assert user_list["data"][0]["email"] == user.email
    assert user_list["data"][0]["id"] == user.id


def test_create_user(client: TestClient):
    """
    Test creating user endpoint.

    Args:
        client (TestClient): TestClient.
    """
    # User properties.
    user_properties = {
        "username": random_lower_string(),
        "email": random_email(),
        "password": random_lower_string()
    }

    # Send request to create user.
    response = client.post("/users",json=user_properties)
    user_response = response.json()
    
    # Check valid properties.
    valid_keys = ["username","email","id"]
    for key in valid_keys:
        assert key in user_response

    # Check properties.
    assert user_response["username"] == user_properties["username"]
    assert user_response["email"] == user_properties["email"]


def test_create_existing_user(client: TestClient, user: User):
    """
    Tets creating user with existing user details.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Get user properties from existing user.
    user_properties = {
        "username": user.username,
        "email": user.email,
        "password": random_lower_string()
    }

    # Send request to create user.
    response = client.post("/users",json=user_properties)
    assert response.status_code == 400


def test_get_user_by_id(client: TestClient, user:User):
    """
    Test get user by id endpoint.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Send get request for specific user id.
    response = client.get(f"/users/{user.id}")
    get_user_response = response.json()

    # Check two responses are equal.
    assert get_user_response["username"] == user.username
    assert get_user_response["email"] == user.email
    assert get_user_response["id"] == user.id


def test_get_user_by_id_invalid(client: TestClient):
    """
    Test get user by id with invalid id.

    Args:
        client (TestClient): Test client.
    """
    # Send get request for invalid id.
    response = client.get(f"/users/1")
    assert response.status_code == 400


def test_get_user(client: TestClient, user: User):
    """
    Test get user endpoint.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Get user by username.
    response = client.get("/users/user/",params={
        "username":user.username
    })
    username_response = response.json()
    assert response.status_code == 200
    assert username_response["username"] == user.username
    assert username_response["email"] == user.email
    assert username_response["id"] == user.id

    # Get user by email.
    response = client.get("/users/user/",params={
        "email":user.email
    })
    email_response = response.json()
    assert response.status_code == 200
    assert email_response["username"] == user.username
    assert email_response["email"] == user.email
    assert email_response["id"] == user.id

    # Get user with email and username
    response = client.get("/users/user/",params={
        "email":user.email,
        "username":user.username
    })
    email_username_response = response.json()
    assert response.status_code == 200
    assert email_username_response["username"] == user.username
    assert email_username_response["email"] == user.email
    assert email_username_response["id"] == user.id

    # Get user with valid email and invalid username.
    response = client.get("/users/user/",params={
        "email":user.email,
        "username":random_lower_string()
    })
    assert response.status_code == 400


def test_get_user_invalid(client: TestClient):
    """
    Test get individual user for invalid details.

    Args:
        client (TestClient): Test client.
    """
    # Get user by invalid username.
    response = client.get("/users/user/",params={
        "username":random_lower_string
    })
    assert response.status_code == 400

    # Get user by invalid email.
    response = client.get("/users/user/",params={
        "email":random_email
    })
    assert response.status_code == 400


def test_delete_user(client: TestClient, user: User):
    """
    Test deleting user.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # Delete user.
    response = client.delete(f"/users/{user.id}")
    delete_response = response.json()
    assert response.status_code == 200
    assert delete_response["username"] == user.username
    assert delete_response["email"] == user.email
    assert delete_response["id"] == user.id

    # Delete again for invalid.
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 400