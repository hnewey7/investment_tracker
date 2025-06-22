'''
Module for creating pytest fixtures.

Created on 22-06-2025
@author: Harry New

'''
import pytest
from typing import Generator

from sqlmodel import Session, create_engine

from app.core.db import engine, create_db_and_tables
from app.core.config import test_settings

# - - - - - - - - - - - - - - - - - - -

@pytest.fixture(scope="session",autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        create_db_and_tables()
        yield session