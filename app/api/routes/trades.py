'''
Module for defining trades endpoints.

Created on 05-07-2025
@author: Harry New

'''
from fastapi import APIRouter, HTTPException

from app.models import Trade, TradeCreate
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter()

# - - - - - - - - - - - - - - - - - - -
# CREATE /USERS/{USER_ID}/PORTFOLIO/TRADES

@router.post(
    "/",
    response_model=Trade
)
def create_trade(*, session: SessionDep, trade_in: TradeCreate) -> Trade:
    """
    Creating trade.

    Args:
        session (SessionDep): SQL session.
        trade_in (TradeCreate): Trade details.

    Returns:
        Trade: New trade.
    """
    # Get asset.
    asset = crud.get_asset_by_id(session=session, asset_id=trade_in.asset_id)
    if not asset:
        raise HTTPException(
            status_code=400,
            detail="No asset with asset id."
        )
    
    # Create trade.
    trade = crud.create_trade(session=session, asset=asset, sell_date=trade_in.sell_date, sell_price=trade_in.sell_price)
    return trade