'''
Module for handling CRUD operations on database.

Created on 22-06-2025
@author: Harry New

'''
from sqlmodel import Session, select

from app.models import User, UserCreate, Portfolio, Instrument
from app.core.security import get_password_hash, verify_password

# - - - - - - - - - - - - - - - - - - -

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

def create_instrument(*, session: Session, name:str, exchange: str, symbol: str):
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
        symbol=symbol
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


def update_price(*, session: Session, instrument: Instrument, open: float, high: float, low: float, close: float) -> Instrument:
    """
    Update price of an instrument.

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
