'''
Module for handling orders endpoint.

Created on 06-07-2025
@author: Harry New

'''
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models import Order, OrderCreate, OrdersPublic
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter()

# - - - - - - - - - - - - - - - - - - -

@router.get(
    "/",
    response_model=OrdersPublic
)
def get_orders(*, session: SessionDep, user_id: int, instrument_id: int=None, start_date: str=None, end_date: str=None, type: str=None) -> OrdersPublic:
    """
    Get orders endpoint.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.
        instrument_id (int, optional): Instrument id. Defaults to None.
        start_date (str, optional): Start date. Defaults to None.
        end_date (str, optional): End date. Defaults to None.
        type (str, optional): Order type. Defaults to None.

    Returns:
        OrdersPublic: Order list.
    """
    # Check valid user.
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code = 400,
            detail="No user found with user id."
        )
    
    # Convert dates.
    if start_date:
        start_date = datetime.strptime(start_date,"%d/%m/%Y")
    if end_date:
        end_date = datetime.strptime(end_date,"%d/%m/%Y")
    
    # Get orders.
    orders = crud.get_orders(session=session, user_id=user_id, instrument_id=instrument_id, start_date=start_date, end_date=end_date, type=type)
    return orders


@router.post(
    "/",
    response_model=Order
)
def create_order(*, session: SessionDep, user_id: int, order_in: OrderCreate) -> Order:
    """
    Create order.

    Args:
        session (SessionDep): SQL sesssion.
        user_id (int): User id.
        order_in (OrderCreate): Order details.

    Returns:
        Order: New order.
    """
    # Check valid user.
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No valid user found with user id."
        )

    # Check valid instrument.
    instrument = crud.get_instrument_by_id(session=session, id=order_in.instrument_id)
    if not instrument:
        raise HTTPException(
            status_code=400,
            detail="No valid instrument found with instrument id."
        )

    order = crud.create_order(session=session, user_id=user_id, order_create=order_in)
    return order