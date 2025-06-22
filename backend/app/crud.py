'''
Module for handling CRUD operations on database.

Created on 22-06-2025
@author: Harry New

'''
from sqlmodel import Session

from app.models import User, UserCreate
from app.core.security import get_password_hash

# - - - - - - - - - - - - - - - - - - -

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj