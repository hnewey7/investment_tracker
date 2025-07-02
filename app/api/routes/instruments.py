'''
Module for handling instrument endpoints.

Created on 02-07-2025
@author: Harry New

'''
from fastapi import APIRouter, HTTPException

from app.models import InstrumentBase, Instrument
from app.api.deps import SessionDep
from app import crud

# - - - - - - - - - - - - - - - - - - -

router = APIRouter(prefix="/instruments",tags=["instruments"])

# - - - - - - - - - - - - - - - - - - -

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