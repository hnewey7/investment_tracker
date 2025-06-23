'''
Module for defining config.

Created on 21-06-2025
@author: Harry New

'''
from dotenv import load_dotenv
import os

from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings

# - - - - - - - - - - - - - - - - - - -
# Load secret values.

load_dotenv()
SECRET_POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
SECRET_POSTGRES_USER = os.getenv("POSTGRES_USER")
SECRET_POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# - - - - - - - - - - - - - - - - - - -

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

# - - - - - - - - - - - - - - - - - - -

settings = Settings(
    POSTGRES_SERVER=SECRET_POSTGRES_SERVER,
    POSTGRES_USER=SECRET_POSTGRES_USER,
    POSTGRES_PASSWORD=SECRET_POSTGRES_PASSWORD,
    POSTGRES_DB="investment_tracker"
)

# Settings configured for test setup.
test_settings = Settings(
    POSTGRES_SERVER=SECRET_POSTGRES_SERVER,
    POSTGRES_USER=SECRET_POSTGRES_USER,
    POSTGRES_PASSWORD=SECRET_POSTGRES_PASSWORD,
    POSTGRES_DB="investment_tracker_test"
)