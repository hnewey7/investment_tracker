'''
Module for defining models to store in database.

Created on 21-06-2025
@author: Harry New

'''
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

# - - - - - - - - - - - - - - - - - - -

class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    portfolio: "Portfolio" = Relationship(back_populates="user")
    hashed_password: str

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserPublic(UserBase):
    id: int

# - - - - - - - - - - - - - - - - - - -

class PortfolioBase(SQLModel):
    type: str

class Portfolio(PortfolioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="portfolio")

    assets: list["Asset"] = Relationship(back_populates="portfolio")
    previous_trades: list["PreviousTrade"] = Relationship(back_populates="portfolio")

# - - - - - - - - - - - - - - - - - - -

class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    portfolio_id: int | None = Field(default=None, foreign_key="portfolio.id")
    portfolio: Portfolio = Relationship(back_populates="assets")

# - - - - - - - - - - - - - - - - - - -

class PreviousTrade(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    portfolio_id: int | None = Field(default=None, foreign_key="portfolio.id")
    portfolio: Portfolio = Relationship(back_populates="previous_trades")
