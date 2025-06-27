from datetime import datetime, timezone
import uuid
import bcrypt
from dotenv import load_dotenv
import os
import jwt
from database.db import add_user_to_db, check_email_exist, get_hashed_password, get_user_claims
from errors import UserLoginError, UserRegistrationError
from models import LoginDetails, RefreshTokenRequest, User

load_dotenv()
secret_key = os.getenv("secret_key")

# save user in the database
def register_user(user: User):
    if check_email_exist(user.email):
        raise UserRegistrationError("user has already registered")
    id = uuid.uuid4()
    user.id = id
    password = user.password
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    # hashing password
    user.password = hashed_password
    add_user_to_db(user)
    
# check user credentials and issue tokens. (access and refresh)
def login_user(loginDetails: LoginDetails):
    hashed_password = get_hashed_password(loginDetails.email)
    if bcrypt.checkpw(loginDetails.password.encode('utf-8'), hashed_password.encode('utf-8')):
        user_claims = get_user_claims(loginDetails.email)
        access_token = jwt.encode(
            payload=user_claims[0],
            key=secret_key,
            algorithm="HS256"
        )
        refresh_token = jwt.encode(
            payload=user_claims[1],
            key=secret_key,
            algorithm="HS256"
        )
        return {
            "access token": access_token,
            "refresh token": refresh_token
        }
    else:
        raise UserLoginError("user credentials are invalid.")
    
# check refresh token and issue new access token
def token_refresh(request: RefreshTokenRequest):
    decoded_jwt = jwt.decode(request.refresh_token, secret_key, algorithms=["HS256"], audience="python-fastapi-server", issuer="python-fastapi-server")
    if (decoded_jwt["exp"] > int(datetime.now(timezone.utc).timestamp())):
        user_claims = get_user_claims(decoded_jwt["email"])
        access_token = jwt.encode(
            payload=user_claims[0],
            key=secret_key,
            algorithm="HS256"
        )
        return {
            "access token": access_token
        }
    else:
        raise UserLoginError("refresh token has been expired.")
