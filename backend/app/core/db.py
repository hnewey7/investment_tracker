'''
Module for functions dealing with database.

Created on 21-06-2025
@author: Harry New

'''
import sys

from sqlmodel import create_engine,SQLModel

from app.core.config import settings, test_settings

# - - - - - - - - - - - - - - - - - - -

if "pytest" in sys.modules:
    engine = create_engine(str(test_settings.SQLALCHEMY_DATABASE_URI))
else:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# - - - - - - - - - - - - - - - - - - -

def create_db_and_tables():
    """
    Create tables in db.
    """
    SQLModel.metadata.create_all(engine)

