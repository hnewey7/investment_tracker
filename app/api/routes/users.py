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
def get_users(*, session: SessionDep, skip: int=0, limit: int=100):
    """
    Get users.

    Args:
        session (SessionDep): SQL session.
        skip (int, optional): Skip results. Defaults to 0.
        limit (int, optional): Limit results. Defaults to 100.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
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


@router.get(
    "/user/",
    response_model=UserPublic
)
def get_user(*, session: SessionDep, username: str = None, email: str = None):
    """
    Get individual user by username or email.

    Args:
        session (SessionDep): SQL session.
        username (str, optional): Username. Defaults to None.
        email (str, optional): Email. Defaults to None.
    """
    if not username and not email:
        raise HTTPException(
            status_code=400,
            detail="No username or email address provided to get user."
        )
    elif email:
        user = crud.get_user_by_email(session=session, email=email)
        
        # Check details match username if provided.
        if username and user.username != username:
            raise HTTPException(
                status_code=400,
                detail="Username provided doesn't match username for email provided."
            )
    else:
        user = crud.get_user_by_username(session=session, username=username)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user exists with these details."
        )
    return user