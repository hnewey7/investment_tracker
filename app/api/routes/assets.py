'''
Module for defining endpoint for assets subresource.

Created on 04-07-2025
@author: Harry New

'''
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.models import AssetCreate, Asset, AssetsPublic
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter()

# - - - - - - - - - - - - - - - - - - -
# GET /USERS/{USER_ID}/PORTFOLIO/ASSETs

@router.get(
    "/",
    response_model=AssetsPublic
)
def get_assets(*, session: SessionDep, user_id: int) -> AssetsPublic:
    """
    Get assets from user's portfolio.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.

    Returns:
        AssetsPublic: List of assets.
    """
    # Get user.
    user = crud.get_user_by_id(session=session,id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user available with user id."
        )
    if not user.portfolio:
        raise HTTPException(
            status_code=400,
            detail="User does not have a portfolio, please create a portfolio first."
        )
    portfolio = user.portfolio
    
    # Get assets and count.
    assets = crud.get_assets_by_portfolio(session=session,portfolio=user.portfolio)
    count_statement = select(func.count()).select_from(Asset).where(Asset.portfolio_id == portfolio.id)
    count = session.exec(count_statement).one()

    return AssetsPublic(data=assets,count=count)

# - - - - - - - - - - - - - - - - - - -
# CREATE /USERS/{USER_ID}/PORTFOLIO/ASSETS

@router.post(
    "/",
    response_model=Asset
)
def create_asset(*, session: SessionDep, user_id: int, asset_in: AssetCreate) -> Asset:
    """
    Create asset.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
        asset_in (AssetBase): Asset to create.

    Returns:
        Asset: New asset.
    """
    # Get user.
    user = crud.get_user_by_id(session=session,id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No user available with user id."
        )
    if not user.portfolio:
        raise HTTPException(
            status_code=400,
            detail="User does not have a portfolio, please create a portfolio first."
        )
    
    # Get instrument.
    instrument = crud.get_instrument_by_id(session=session,id=asset_in.instrument_id)
    if not instrument:
        raise HTTPException(
            status_code=400,
            detail="Invalid instrument id entered."
        )
    
    # Create asset.
    asset = crud.create_asset(session=session,portfolio=user.portfolio,instrument=instrument,buy_date=asset_in.buy_date,buy_price=asset_in.buy_price,volume=asset_in.volume)
    return asset