import bcrypt
from database.db import add_user_to_db, check_email_exist
from models.index import User
from errors import UserRegistrationError

def register_user(user: User):
    if check_email_exist(user.email):
        raise UserRegistrationError("user has already registered")
    password = user.password
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    # hashing password
    user.password = hashed_password
    add_user_to_db(user)
    
        