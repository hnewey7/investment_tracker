'''
Module for handling user endpoints.

Created on 22-06-2025
@author: Harry New

'''
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app import crud
from app.models import UserCreate, UserPublic, User, UsersPublic
from app.api.deps import SessionDep

# - - - - - - - - - - - - - - - - - - -

router = APIRouter(prefix="/users",tags=["users"])

# - - - - - - - - - - - - - - - - - - -

@router.get(
    "/",
    response_model=UsersPublic
)
def get_users(*, session: SessionDep, skip: int=0, limit: int=100, email: str=None, username: str=None):
    """
    Get users.

    Args:
        session (SessionDep): SQL session.
        skip (int, optional): Skip results. Defaults to 0.
        limit (int, optional): Limit results. Defaults to 100.
        email (str, optional): Email address. Defaults to None.
        username (str, optional): Username. Defaults to None.
    """
    # Counts all users, independent of what users returned.
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    # Statement for returning users.
    statement = select(User).offset(skip).limit(limit)
    if email:
        statement = statement.where(User.email == email)
    elif username:
        statement = statement.where(User.username == username)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.post(
    "/",
    response_model=UserPublic
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.

    Args:
        session (SessionDep): Database session.
        user_in (UserCreate): UserCreate model.

    Returns:
        UserPublic: UserPublic model after creation.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.get(
    "/{user_id}",
    response_model=UserPublic
)
def get_user_by_id(*, session: SessionDep, user_id: int):
    """
    Get user by id.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User ID.
    """
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user exists with this id."
        )
    return user


@router.delete(
    "/{user_id}",
    response_model=UserPublic
)
def delete_user(*, session: SessionDep, user_id: int):
    """
    Delete user by id.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
    """
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Unable to find user with id."
        )
    
    crud.delete_user(session=session,user=user)
    return user