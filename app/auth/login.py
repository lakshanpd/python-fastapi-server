from models import LoginDetails, RefreshTokenRequest
from database.db import get_hashed_password, get_user_claims
import bcrypt
import jwt
import os
from dotenv import load_dotenv
from errors import UserLoginError
from datetime import datetime, timezone

load_dotenv()
secret_key = os.getenv("secret_key")

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


