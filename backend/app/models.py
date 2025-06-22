'''
Module for defining models to store in database.

Created on 21-06-2025
@author: Harry New

'''
import uuid

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

# - - - - - - - - - - - - - - - - - - -

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
