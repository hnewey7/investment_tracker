'''
Module for utils functions for testing.

Created on 22-06-2025
@author: Harry New

'''
import random
import string

# - - - - - - - - - - - - - - - - - - -

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"