'''
Module for functions dealing with database.

Created on 21-06-2025
@author: Harry New

'''
import sys
import os

from sqlmodel import create_engine,SQLModel

if __name__ == "core.db":
    from core.config import settings, test_settings
else:
    from app.core.config import settings, test_settings, docker_settings

# - - - - - - - - - - - - - - - - - - -
# Selecting configuration settings.

if "pytest" in sys.modules:
    engine = create_engine(str(test_settings.SQLALCHEMY_DATABASE_URI))
elif os.path.exists('/.dockerenv'):
    engine = create_engine(str(docker_settings.SQLALCHEMY_DATABASE_URI))
else:
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# - - - - - - - - - - - - - - - - - - -

def create_db_and_tables():
    """
    Create tables in db.
    """
    SQLModel.metadata.create_all(engine)


def clear_db():
    """
    Clear all previous tables in database.
    """
    SQLModel.metadata.drop_all(engine)