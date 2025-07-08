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
    orders: list["Order"] = Relationship(back_populates="user")
    summary: "Summary" = Relationship(back_populates="user")
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

class InstrumentBase(SQLModel):
    name: str = Field(max_length=255)
    exchange: str = Field(max_length=255)
    symbol: str = Field(unique=True, index=True,max_length=255)
    currency: str = Field(max_length=5)


class Instrument(InstrumentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    open: float | None = Field(default=None)
    high: float | None = Field(default=None)
    low: float | None = Field(default=None)
    close: float | None = Field(default=None)


class InstrumentsPublic(SQLModel):
    data: list[Instrument]
    count: int


class InstrumentUpdate(SQLModel):
    currency: Optional[str] = None
    prices: Optional[List[float]] = None

# - - - - - - - - - - - - - - - - - - -

class OrderBase(SQLModel):
    date: datetime
    volume: float
    price: float
    type: str
    

class Order(OrderBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    instrument_id: int = Field(index=True,foreign_key="instrument.id")
    instrument: Instrument = Relationship()

    user_id: int = Field(index=True,foreign_key="user.id")
    user: User = Relationship(back_populates="orders")


class OrderCreate(OrderBase):
    instrument_id: int


class OrderUpdate(SQLModel):
    date: Optional[datetime] = None
    volume: Optional[float] = None
    price: Optional[float] = None
    type: Optional[str] = None
    user_id: Optional[int] = None
    instrument_id: Optional[int] = None


class OrdersPublic(SQLModel):
    data: list[Order]
    count: int


# - - - - - - - - - - - - - - - - - - -

class SummaryBase(SQLModel):
    ending_market_value: Optional[float] = None
    beginning_market_value: Optional[float] = None
    profit_loss: Optional[float] = None


class Summary(SummaryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(index=True,foreign_key="user.id")
    user: User = Relationship(back_populates="summary")


class SummaryUpdate(SummaryBase):
    user_id: Optional[int] = None
