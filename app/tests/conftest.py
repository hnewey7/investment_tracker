'''
Module for creating pytest fixtures.

Created on 22-06-2025
@author: Harry New

'''
import pytest
from typing import Generator
from datetime import datetime

from sqlmodel import Session, create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.core.db import engine, create_db_and_tables, clear_db
from app.core.config import test_settings
from app.models import User, UserCreate, Instrument, InstrumentBase
from app.tests.utils.utils import random_email, random_lower_string
from app import crud

# - - - - - - - - - - - - - - - - - - -

@pytest.fixture(scope="function",autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        # Clear previous tables.
        clear_db()
        # Create database with new tables.
        create_db_and_tables()
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def user() -> Generator[User, None, None]:
    with Session(engine) as session:
        # Create user.
        properties = {
            "username": random_lower_string(),
            "email": random_email(),
            "password": random_lower_string()
        }
        user_create = UserCreate(**properties)
        user = crud.create_user(session=session,user_create=user_create)
    yield user


@pytest.fixture
def multiple_users(request) -> Generator[list[User], None, None]:
    # User list.
    users = []
    with Session(engine) as session:
        for i in range(request.param):
            # Create users.
            properties = {
                "username": random_lower_string(),
                "email": random_email(),
                "password": random_lower_string()
            }
            user_create = UserCreate(**properties)
            user = crud.create_user(session=session,user_create=user_create)
            users.append(user)
    yield users


@pytest.fixture(scope="function")
def instrument() -> Generator[Instrument, None, None]:
    with Session(engine) as session:
        # Create instrument.
        properties = {
            "name":"C&C GROUP ORD EURO.01",
            "exchange":"LSE",
            "symbol":"CCR",
            "currency":"GBX"
        }
        instrument_create = InstrumentBase(**properties)
        instrument = crud.create_instrument(session=session,instrument_create=instrument_create)
    yield instrument


@pytest.fixture(scope="function")
def multiple_instruments(request) -> Generator[list[Instrument], None, None]:
    # Instrument list.
    instruments = []
    with Session(engine) as session:
        for i in range(request.param):
            # Create instruments.
            properties = {
                "name": random_lower_string(),
                "exchange": random_lower_string(),
                "symbol": random_lower_string(),
                "currency":"GBX"
            }
            instrument_create = InstrumentBase(**properties)
            instrument = crud.create_instrument(session=session,instrument_create=instrument_create)
            instruments.append(instrument)
    yield instruments