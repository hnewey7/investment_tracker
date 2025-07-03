'''
Module for handling CRUD operations on database.

Created on 22-06-2025
@author: Harry New

'''
from datetime import datetime

from sqlmodel import Session, select

from app.models import User, UserCreate, Portfolio, Instrument, Asset, PreviousTrade
from app.core.security import get_password_hash, verify_password

# - - - - - - - - - - - - - - - - - - -
# USER OPERATIONS

def create_user(*, session: Session, user_create: UserCreate) -> User:
    """
    Create user.

    Args:
        session (Session): SQL session.
        user_create (UserCreate): UserCreate model.

    Returns:
        User: User model.
    """
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """
    Get user by email.

    Args:
        session (Session): SQL session.
        email (str): Email address to search for.

    Returns:
        User | None: User model or none.
    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_username(*, session: Session, username: str) -> User | None:
    """
    Get user by username.

    Args:
        session (Session): SQL session.
        username (str): Username to search for.

    Returns:
        User | None: User model or none.
    """
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_id(*, session: Session, id: int) -> User | None:
    """
    Get user by id.

    Args:
        session (Session): SQL session.
        id (int): User id.

    Returns:
        User | None: User model.
    """
    statement = select(User).where(User.id == id)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str = None, username: str = None , password: str) -> User | None:
    """
    Authenticate user.

    Args:
        session (Session): SQL session.
        email (str | None): Email address, optional.
        username (str | None): Username, optional.
        password (str): Password.

    Returns:
        User | None: User model or none.
    """
    # Getting user by email or username.
    if email:
        db_user = get_user_by_email(session=session, email=email)
    else:
        db_user = get_user_by_username(session=session, username=username)

    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def change_username(*, session: Session, email: str, new_username: str) -> User:
    """
    Change username.

    Args:
        session (Session): SQL session.
        email (str): Email address.
        new_username (str): New username.

    Returns:
        User: Updated user model.
    """
    # Get user.
    user = get_user_by_email(session=session, email=email)
    # Update username.
    user.username = new_username
    session.commit()
    session.refresh(user)
    return user


def change_password(*, session: Session, email: str, new_password: str) -> User:
    """
    Change password.

    Args:
        session (Session): SQL session.
        email (str): Email address.
        new_password (str): New password.

    Returns:
        User: Updated User model.
    """
    # Get user.
    user = get_user_by_email(session=session, email=email)
    # Update username.
    user.hashed_password = get_password_hash(new_password)
    session.commit()
    session.refresh(user)
    return user


def delete_user(*, session: Session, user: User):
    """
    Delete user.

    Args:
        session (Session): SQL session.
        user (User): User to delete.
    """
    # Delete user.
    session.delete(user)
    session.commit()

# - - - - - - - - - - - - - - - - - - -
# PORTFOLIO OPERATIONS

def create_portfolio(*, session: Session, user: User):
    """
    Creating portfolio for user.

    Args:
        session (Session): SQL session.
        user (User): User to assign portfolio.
    """
    db_obj = Portfolio(
        user=user
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def delete_portfolio(*, session: Session, portfolio: Portfolio):
    """
    Delete portfolio.

    Args:
        session (Session): SQL session.
        portfolio (Portfolio): Portfolio to delete.
    """
    # Delete portfolio.
    session.delete(portfolio)
    session.commit()

# - - - - - - - - - - - - - - - - - - -
# INSTRUMENT OPERATIONS

def create_instrument(*, session: Session, name:str, exchange: str, symbol: str, currency: str):
    """
    Creating instrument.

    Args:
        session (Session): 
        exchange (str): Exchange instrument is available on.
        symbol (str): Symbol.
    """
    db_obj = Instrument(
        name=name,
        exchange=exchange,
        symbol=symbol,
        currency=currency
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_instrument_by_symbol(*, session: Session, symbol:str) -> Instrument:
    """
    Get instrument by symbol.

    Args:
        session (Session): SQL session.
        symbol (str): Symbol.

    Returns:
        Instrument: Instrument in database.
    """
    statement = select(Instrument).where(Instrument.symbol == symbol)
    session_instrument = session.exec(statement).first()
    return session_instrument


def get_instrument_by_id(*, session: Session, id: int) -> Instrument:
    """
    Get instrument by id.

    Args:
        session (Session): SQL session.
        id (int): Instrument id.

    Returns:
        Instrument: Instrument
    """
    statement = select(Instrument).where(Instrument.id == id)
    session_instrument = session.exec(statement).first()
    return session_instrument


def update_instrument_prices(*, session: Session, instrument: Instrument, open: float, high: float, low: float, close: float) -> Instrument:
    """
    Update prices of an instrument.

    Args:
        session (Session): SQL session.
        instrument (Instrument): Instrument to update.
        open (float): Open price.
        high (float): High price.
        low (float): Low price.
        close (float): Close price.

    Returns:
        Instrument: Updated instrument.
    """
    # Update prices.
    instrument.open = open
    instrument.high = high
    instrument.low = low
    instrument.close = close
    # Commit to db.
    session.commit()
    session.refresh(instrument)
    return instrument


def update_instrument_currency(*, session: Session, instrument: Instrument, currency: str) -> Instrument:
    """
    Update currency of instrument.

    Args:
        session (Session): SQL session.
        instrument (Instrument): Instrument to update.
        currency (str): Currency.

    Returns:
        Instrument: Updated instrument.
    """
    instrument.currency = currency
    session.commit()
    session.refresh(instrument)
    return instrument


def delete_instrument(*, session: Session, instrument: Instrument):
    """
    Delete instrument.

    Args:
        session (Session): SQL session.
        instrument (Instrument): Instrument to delete.
    """
    # Delete instrument.
    session.delete(instrument)
    session.commit()

# - - - - - - - - - - - - - - - - - - -
# ASSET OPERATIONS

def create_asset(*, session: Session, portfolio: Portfolio, instrument: Instrument ,buy_date: datetime, buy_price: float, volume: float) -> Asset:
    """
    Create asset.

    Args:
        session (Session): SQL session.
        portfolio (Portfolio): Portfolio.
        instrument (Instrument): Instrument.
        buy_date (datetime): Buy date.
        buy_price (float): Buy price.
        volume (float): Volume

    Returns:
        Asset: Asset.
    """
    db_obj = Asset(
        portfolio=portfolio,
        instrument=instrument,
        buy_date=buy_date,
        buy_price=buy_price,
        volume=volume,
        currency=instrument.currency
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_assets_by_instrument(*, session: Session, portfolio: Portfolio, instrument: Instrument):
    """
    Get assets from instrument within a given portfolio.

    Args:
        session (Session): _description_
        portfolio (Portfolio): _description_
        instrument (Instrument): _description_
    """
    statement = select(Asset).where(Asset.portfolio_id == portfolio.id).where(Asset.instrument_id == instrument.id)
    results = session.exec(statement).all()
    return results


def update_asset_buy_price(*, session: Session, asset: Asset, buy_price: float) -> Asset:
    """
    Update buy price of an asset.

    Args:
        session (Session): SQL session.
        asset (Asset): Asset to update.
        buy_price (float): New buy price.

    Returns:
        Asset: Updated asset.
    """
    asset.buy_price = buy_price
    session.commit()
    session.refresh(asset)
    return asset


def update_asset_volume(*, session: Session, asset: Asset, volume: float) -> Asset:
    """
    Update volume of an asset.

    Args:
        session (Session): SQL session.
        asset (Asset): Asset to update.
        volume (float): New volume.

    Returns:
        Asset: Updated asset.
    """
    asset.volume = volume
    session.commit()
    session.refresh(asset)
    return asset


def delete_asset(*, session: Session, asset: Asset):
    """
    Deleting asset.

    Args:
        session (Session): SQL session.
        asset (Asset): Asset to delete.
    """
    session.delete(asset)
    session.commit()

# - - - - - - - - - - - - - - - - - - -
# PREVIOUS TRADE OPERATIONS

def create_previous_trade(*, session:Session, asset:Asset, sell_date:datetime, sell_price: float) -> PreviousTrade:
    """
    Create previous trade from asset.

    Args:
        session (Session): SQL session
        asset (Asset): Asset to create previous trade from.
        sell_date (datetime): Sell datetime.
        sell_price (float): Sell price.
    
    Returns:
        PreviousTrade: New previous trade.
    """
    db_obj = PreviousTrade.model_validate(asset,
        update={
            "sell_date":sell_date,
            "sell_price":sell_price
        }
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_previous_trade_by_instrument(*, session:Session, portfolio:Portfolio, instrument:Instrument) -> PreviousTrade:
    """
    Get previous trade by instrument for a given portfolio.

    Args:
        session (Session): SQL session.
        portfolio (Portfolio): Portfolio.
        instrumnet (Instrument): Instrument.

    Returns:
        PreviousTrade: Previous trade.
    """
    statement = select(PreviousTrade).where(PreviousTrade.portfolio_id == portfolio.id).where(PreviousTrade.instrument_id == instrument.id)
    results = session.exec(statement).all()
    return results


def update_previous_trade_sell_price(*, session:Session, previous_trade:PreviousTrade, sell_price:float) -> PreviousTrade:
    """
    Update previous trade's sell price.

    Args:
        session (Session): SQL session.
        previous_trade (PreviousTrade): Previous trade.
        sell_price (float): Sell price.

    Returns:
        PreviousTrade: Previous trade.
    """
    previous_trade.sell_price = sell_price
    session.commit()
    session.refresh(previous_trade)
    return previous_trade


def delete_previous_trade(*, session:Session, previous_trade:PreviousTrade):
    """
    Delete previous trade.

    Args:
        session (Session): SQL session.
        previous_trade (PreviousTrade): Previous trade.
    """
    session.delete(previous_trade)
    session.commit()