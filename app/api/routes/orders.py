'''
Module for handling orders endpoint.

Created on 06-07-2025
@author: Harry New

'''
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models import Order, OrderCreate, OrdersPublic, OrderUpdate
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


@router.delete(
    "/",
    response_model=OrdersPublic
)
def delete_orders(*, session: SessionDep, user_id: int) -> OrdersPublic:
    """
    Delete orders.

    Args:
        session (SessionDep): SQL session.
        user_id (int): User id.

    Returns:
        OrdersPublic: Deleted orders.
    """
    # Check valid user.
    user = crud.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No valid user found with user id."
        )
    
    # Delete orders.
    orders = crud.get_orders(session=session, user_id=user_id)
    for order in orders.data:
        crud.delete_order(session=session, order=order)

    return orders


@router.get(
    "/{order_id}",
    response_model=Order
)
def get_order(*, session: SessionDep, order_id: int) -> Order:
    """
    Get order.

    Args:
        session (SessionDep): SQL session.
        order_id (int): Order id.

    Returns:
        Order: Returned order.
    """
    order = crud.get_order_by_id(session=session, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=400,
            detail="No order found with order id."
        )
    return order


@router.put(
    "/{order_id}",
    response_model=Order
)
def update_order(*, session: SessionDep, order_id: int, order_update: OrderUpdate) -> Order:
    """
    Update order.

    Args:
        session (SessionDep): SQL session.
        order_id (int): Order id.
        order_update (OrderUpdate): Order update.

    Returns:
        Order: Updated order.
    """
    order = crud.get_order_by_id(session=session, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=400,
            detail="No order found with order id."
        )
    order = crud.update_order(session=session, order=order, order_update=order_update)
    return order