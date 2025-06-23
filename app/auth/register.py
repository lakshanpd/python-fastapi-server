import bcrypt
from app.database.db import add_user_to_db, check_email_exist
from app.models.index import User
from datetime import date, datetime

def register_user(user: User):
    try:
        if check_email_exist(user.email):
            raise Exception("user has already registered")
        password = user.password
        bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes, salt)
        # hashing password
        user.password = hashed_password
        add_user_to_db(user)
    except Exception as error:
        raise Exception("Error while registering the user")
    
        