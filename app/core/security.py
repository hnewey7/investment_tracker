'''
Module for handling security.

Created on 22-06-2025
@author: Harry New

'''
from passlib.context import CryptContext

# - - - - - - - - - - - - - - - - - - -

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

# - - - - - - - - - - - - - - - - - - -

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)