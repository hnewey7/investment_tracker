'''
Module for handling portfolio endpoints.

Created on 01-07-2025
@author: Harry New

'''
from fastapi import APIRouter, HTTPException

from app.models import Portfolio
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter()

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID}/PORTFOLIO

@router.get(
    "/",
    response_model=Portfolio
)
def get_portfolio(*, session: SessionDep, user_id: int):
    """
    Get portfolio for user.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
    """
    # Get user.
    user = crud.get_user_by_id(session=session,id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user with this id."
        )

    # Get user's portfolio.
    portfolio = user.portfolio
    if not portfolio:
        raise HTTPException(
            status_code=400,
            detail="No portfolio associated with the user."
        )
    return user.portfolio

# - - - - - - - - - - - - - - - - - - -
# POST /USERS/{USER_ID}/PORTFOLIO

@router.post(
    "/",
    response_model=Portfolio
)
def create_portfolio(*, session: SessionDep, user_id: int):
    """
    Create portfolio for user.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
    """
    # Get user.
    user = crud.get_user_by_id(session=session,id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user with this id."
        )

    # Create portfolio.
    portfolio = crud.create_portfolio(session=session, user=user)
    return portfolio

# - - - - - - - - - - - - - - - - - - -
# DELETE /USERS/{USER_ID}/PORTFOLIO

@router.delete(
    "/",
    response_model=Portfolio
)
def delete_portfolio(*, session: SessionDep, user_id: int):
    """
    Delete a user's portfolio.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
    """
    # Get user.
    user = crud.get_user_by_id(session=session,id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user with this id."
        )
    portfolio = user.portfolio
    if not portfolio:
        raise HTTPException(
            status_code=400,
            detail="No portfolio associated with user."
        )

    # Delete portfolio.
    crud.delete_portfolio(session=session, portfolio=portfolio)
    return portfolio