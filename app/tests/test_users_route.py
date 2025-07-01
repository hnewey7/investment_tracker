'''
Module for testing the users route.

Created on 29-06-2025
@author: Harry New

'''
import pytest

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import User
from app.tests.utils.utils import random_email, random_lower_string
from app import crud

# - - - - - - - - - - - - - - - - - - -
# GET /USERS TESTS

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


    # Repeat for email query.
    # Send request to get users with email query.
    response = client.get("/users",params={
        "email":user.email
    })
    user_list = response.json()

    # Check length of response.
    assert len(user_list["data"]) == 1
    assert user_list["count"] == 1

    # Check user provided.
    assert user_list["data"][0]["username"] == user.username
    assert user_list["data"][0]["email"] == user.email
    assert user_list["data"][0]["id"] == user.id

    
    # Repeat for username query.
    # Send request to get users with username query.
    response = client.get("/users",params={
        "username":user.username
    })
    user_list = response.json()

    # Check length of response.
    assert len(user_list["data"]) == 1
    assert user_list["count"] == 1

    # Check user provided.
    assert user_list["data"][0]["username"] == user.username
    assert user_list["data"][0]["email"] == user.email
    assert user_list["data"][0]["id"] == user.id


@pytest.mark.parametrize("multiple_users", [10], indirect=True)
def test_get_multiple_users(client: TestClient, multiple_users: list[User]):
    """
    Test getting multiple users.

    Args:
        client (TestClient): Test client.
        multiple_users (list[User]): Test users.
    """
    # Send standard get request.
    response = client.get("/users")
    users_list = response.json()
    assert users_list["count"] == 10
    assert len(users_list["data"]) == 10

    # Send limited request.
    response = client.get("/users",params={
        "limit":5
    })
    users_list = response.json()
    assert users_list["count"] == 10
    assert len(users_list["data"]) == 5

    # Send skipped request.
    response = client.get("/users",params={
        "skip":1
    })
    skipped_users_list = response.json()
    assert skipped_users_list["count"] == 10
    assert len(skipped_users_list["data"]) == 9

# - - - - - - - - - - - - - - - - - - -
# CREATE /USERS TESTS

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

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID} TESTS

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

# - - - - - - - - - - - - - - - - - - -
# UPDATE /USERS/{USER_ID} TESTS

def test_update_username(client: TestClient, user: User):
    """
    Test updating a user's username.

    Args:
        client (TestClient): Test client.
        user (User): Test user.
    """
    # New username
    new_username = random_lower_string()

    # Send put request.
    response = client.put(f"/users/{user.id}",params={
        "username":new_username
    })
    user_response = response.json()
    assert response.status_code == 200
    assert user_response["username"] == new_username
    assert user_response["email"] == user.email
    assert user_response["id"] == user.id


def test_update_password(client: TestClient, db: Session, user: User):
    """
    Test updating a user's password.

    Args:
        client (TestClient): Test client.
        db (Session): SQL session.
        user (User): Test user.
    """
    # New password
    new_password = random_lower_string()

    # Send put request.
    response = client.put(f"/users/{user.id}",params={
        "password":new_password
    })
    assert response.status_code == 200
    assert crud.authenticate(session=db,email=user.email,password=new_password)


def test_update_username_and_password(client: TestClient, db: Session, user: User):
    """
    Test updating user's username and password.

    Args:
        client (TestClient): Test client.
        db (Session): SQL session.
        user (User): Test user.
    """
    # New username and password.
    new_username = random_lower_string()
    new_password = random_lower_string()

    # Send put request.
    response = client.put(f"/users/{user.id}",params={
        "username": new_username,
        "password": new_password
    })
    user_response = response.json()
    assert response.status_code == 200
    assert user_response["username"] == new_username
    assert user_response["email"] == user.email
    assert user_response["id"] == user.id
    assert crud.authenticate(session=db,email=user.email,password=new_password)
    assert crud.authenticate(session=db,username=new_username,password=new_password)

# - - - - - - - - - - - - - - - - - - -
# DELETE /USERS/{USER_ID} TESTS 

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