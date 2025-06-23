'''
Module for handling user endpoints.

Created on 22-06-2025
@author: Harry New

'''
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.models import UserCreate, UserPublic
from app.api.deps import SessionDep

# - - - - - - - - - - - - - - - - - - -

router = APIRouter(tags=["users"])

# - - - - - - - - - - - - - - - - - - -

@router.post(
    "/users",
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