'''
Module for functions dealing with database.

Created on 21-06-2025
@author: Harry New

'''
from sqlmodel import create_engine,SQLModel

from core.config import settings

# - - - - - - - - - - - - - - - - - - -

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI),echo=True)

# - - - - - - - - - - - - - - - - - - -

def create_db_and_tables():
    """
    Create tables in db.
    """
    SQLModel.metadata.create_all(engine)

