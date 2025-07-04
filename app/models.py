'''
Module for defining models to store in database.

Created on 21-06-2025
@author: Harry New

'''
from datetime import datetime
from typing import Optional, List

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


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class UserUpdate(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None

# - - - - - - - - - - - - - - - - - - -

class PortfolioBase(SQLModel):
    type: str = Field(default="Overview",max_length=255)


class Portfolio(PortfolioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="portfolio")

    assets: list["Asset"] = Relationship(back_populates="portfolio")
    previous_trades: list["PreviousTrade"] = Relationship(back_populates="portfolio")

# - - - - - - - - - - - - - - - - - - -

class InstrumentBase(SQLModel):
    name: str = Field(max_length=255)
    exchange: str = Field(max_length=255)
    symbol: str = Field(index=True,max_length=255)
    currency: str = Field(max_length=5)


class Instrument(InstrumentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    open: float | None
    high: float | None
    low: float | None
    close: float | None


class InstrumentsPublic(SQLModel):
    data: list[Instrument]
    count: int


class InstrumentUpdate(SQLModel):
    currency: Optional[str] = None
    prices: Optional[List[float]] = None

# - - - - - - - - - - - - - - - - - - -

class AssetBase(SQLModel):
    buy_date: str
    buy_price: float
    volume: float


class Asset(AssetBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    currency: str = Field(max_length=5)

    instrument_id: int = Field(index=True,foreign_key="instrument.id")
    instrument: Instrument = Relationship()

    portfolio_id: int = Field(index=True,foreign_key="portfolio.id")
    portfolio: Portfolio = Relationship(back_populates="assets")


class AssetsPublic(SQLModel):
    data: list[Asset]
    count: int


class AssetCreate(AssetBase):
    instrument_id: int


class AssetUpdate(SQLModel):
    buy_price: Optional[float] = None
    volume: Optional[float] = None

# - - - - - - - - - - - - - - - - - - -

class PreviousTradeBase(AssetBase):
    sell_date: datetime
    sell_price: float


class PreviousTrade(PreviousTradeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    instrument_id: int = Field(foreign_key="instrument.id")
    instrument: Instrument = Relationship()

    portfolio_id: int = Field(foreign_key="portfolio.id")
    portfolio: Portfolio = Relationship(back_populates="previous_trades")

# - - - - - - - - - - - - - - - - - - -