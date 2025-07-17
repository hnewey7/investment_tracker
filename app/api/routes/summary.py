'''
Module for handling summary endpoints.

Created on 16-07-2025
@author: Harry New

'''
from fastapi import APIRouter, HTTPException

from app.models import Summary, SummaryUpdate
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter()

# - - - - - - - - - - - - - - - - - - -
# /USERS/{USER_ID}/SUMMARY

@router.get(
    "/",
    response_model=Summary
)
def get_summary(*, session: SessionDep, user_id: int) -> Summary:
    """
    Get summary for a given user.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.

    Returns:
        SummaryBase: Summary.
    """
    # Check valid user.
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code = 400,
            detail="No user found with user id."
        )
    
    # Get summary.
    summary = user.summary
    if not summary:
        raise HTTPException(
            status_code=400,
            detail="No summary found with user."
        )
    return summary


@router.put(
    "/",
    response_model=Summary
)
def update_summary(*, session: SessionDep, user_id: int, summary_update: SummaryUpdate) -> Summary:
    """Update summary for a given user.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
        summary_update (SummaryUpdate): Summary update details.

    Returns:
        SummaryBase: Updated summary.
    """
    # Check valid user.
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code = 400,
            detail="No user found with user id."
        )
    
    # Check valid summary.
    summary = user.summary
    if not summary:
        raise HTTPException(
            status_code=400,
            detail="No summary found with user."
        )
    
    # Update summary.
    summary = crud.update_summary(session=session, summary=summary, summary_update=summary_update)
    return summary