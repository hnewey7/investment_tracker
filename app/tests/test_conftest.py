'''
Module for testing conftest.py.

Created on 24-06-2025
@author: Harry New

'''
from sqlmodel import Session, SQLModel

from app.core.db import engine

# - - - - - - - - - - - - - - - - - - -

def test_db(db: Session):
    """
    Testing connection to correctly defined database.

    Args:
        db (Session): Database fixture.
    """
    # Correct table names.
    table_names = ["user","instrument","order"]

    # Available tables.
    available_tables = SQLModel.metadata.tables.keys()

    # Check each table name.
    for table_name in table_names:
        assert table_name in available_tables