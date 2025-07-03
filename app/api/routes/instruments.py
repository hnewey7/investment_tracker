'''
Module for handling instrument endpoints.

Created on 02-07-2025
@author: Harry New

'''
from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.models import InstrumentBase, Instrument, InstrumentsPublic
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter(prefix="/instruments",tags=["instruments"])

# - - - - - - - - - - - - - - - - - - -
# GET /INSTRUMENT

@router.get(
    "/",
    response_model=InstrumentsPublic
)
def get_instruments(*, session: SessionDep, name: str=None, exchange: str=None, symbol: str=None, currency: str=None) -> InstrumentsPublic:
    """
    Get all instruments.

    Args:
        session (SessionDep): SQL session.
        name (str, optional): Name of instrument. Defaults to None.
        exchange (str, optional): Exchange. Defaults to None.
        symbol (str, optional): Symbol. Defaults to None.
        currency (str, optional): Currency. Defaults to None.

    Returns:
        InstrumentsPublic: List of instruments.
    """
    # Counts all instruments, independent of what instruments returned.
    count_statement = select(func.count()).select_from(Instrument)
    count = session.exec(count_statement).one()

    # Filtering instruments.
    statement = select(Instrument)
    if name: 
        statement = statement.where(Instrument.name == name)
    elif exchange:
        statement = statement.where(Instrument.exchange == exchange)
    elif symbol:
        statement = statement.where(Instrument.symbol == symbol)
    elif currency:
        statement = statement.where(Instrument.currency == currency)
    instruments = session.exec(statement).all()

    return InstrumentsPublic(data=instruments, count=count)

# - - - - - - - - - - - - - - - - - - -
# POST /INSTRUMENT

@router.post(
    "/",
    response_model=Instrument
)
def create_instrument(*, session: SessionDep, instrument_in: InstrumentBase):
    """
    Create an instrument.

    Args:
        session (SessionDep): SQL session.
        instrument_in (InstrumentBase): Instrument to create.
    """
    instrument = crud.get_instrument_by_symbol(session=session, symbol=instrument_in.symbol)
    if instrument:
        raise HTTPException(
            status_code=400,
            detail="Instrument with symbol already exists."
        )

    instrument = crud.create_instrument(
        session=session,
        name=instrument_in.name,
        exchange=instrument_in.exchange,
        symbol=instrument_in.symbol,
        currency=instrument_in.currency
    )
    return instrument

# - - - - - - - - - - - - - - - - - - -
# GET /INSTRUMENTS/{INSTRUMENT_ID}

@router.get(
    "/{instrument_id}",
    response_model=Instrument
)
def get_instrument(*, session: SessionDep, instrument_id: int):
    """
    Get instrument.

    Args:
        session (SessionDep): SQL session.
        instrument_id (int): Instrument ID.
    """
    # Get instrument.
    instrument = crud.get_instrument_by_id(session=session, id=instrument_id)
    if not instrument:
        raise HTTPException(
            status_code=400,
            detail="No instrument exists with instrument id."
        )
    return instrument