from datetime import datetime, timezone
import uuid
import bcrypt
from dotenv import load_dotenv
import os
import jwt
from database.sql_handler import sql_handler
from errors import UserLoginError, UserRegistrationError
from models import LoginDetails, RefreshTokenRequest, User
from fastapi import Request, HTTPException, status

load_dotenv()
secret_key = os.getenv("secret_key")

# save user in the database
def register_user(user: User):
    if sql_handler.check_email_exist(user.email):
        raise UserRegistrationError("user has already registered")
    id = uuid.uuid4()
    user.id = id
    password = user.password
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes, salt)
    # hashing password
    user.password = hashed_password
    sql_handler.add_user_to_db(user)
    
# check user credentials and issue tokens. (access and refresh)
def login_user(loginDetails: LoginDetails):
    hashed_password = sql_handler.get_hashed_password(loginDetails.email)
    if bcrypt.checkpw(loginDetails.password.encode('utf-8'), hashed_password.encode('utf-8')):
        user_claims = sql_handler.get_user_claims(loginDetails.email)
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
        user_claims = sql_handler.get_user_claims(decoded_jwt["email"])
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

# middleware for protected routes
def validate_token(request: Request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header is missing or invalid.")
        
    try:
        access_token = auth_header.split(" ")[1]
        decoded_jwt = jwt.decode(access_token, secret_key, algorithms=["HS256"], audience="python-fastapi-server", issuer="python-fastapi-server")
    
    except jwt.exceptions.ExpiredSignatureError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been expired.")
    
    if "type" not in decoded_jwt or decoded_jwt["type"] != "access_token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token type is invalid.")
    
    return {
        "user": sql_handler.get_user_claims(decoded_jwt["email"])[0],
        "request": request
    }
    
