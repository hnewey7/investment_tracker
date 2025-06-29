'''
Module for creating initial database.

Created on  21-06-2025
@author: Harry New

'''
import logging

from sqlmodel import SQLModel

# - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    from core.db import engine, create_db_and_tables
else:
    from app.core.db import engine, create_db_and_tables

import models

# - - - - - - - - - - - - - - - - - - -

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# - - - - - - - - - - - - - - - - - - -

def init() -> None:
    """
    Initialising database.
    """
    # Create database.
    create_db_and_tables()

def clear_db_and_tables():
    """
    Clearing database.
    """
    # Clear database.
    SQLModel.metadata.drop_all(bind=engine)

# - - - - - - - - - - - - - - - - - - -

def main():
    logger.info("Clear database.")
    clear_db_and_tables()
    logger.info("Creating initial database.")
    create_db_and_tables()
    logger.info("Initial database created successfully.")

# - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    main()