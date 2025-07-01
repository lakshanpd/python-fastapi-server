from fastapi import APIRouter, HTTPException, status
from utils.models import User, LoginDetails, RefreshTokenRequest
from utils.auth import register_user, login_user, token_refresh
from utils.errors import DatabaseError, UserRegistrationError, UserLoginError
import jwt
import traceback
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.post("/register")
async def register(user: User):
    try:
        register_user(user=user)
        logging.info("user registered successfully")
        return {"message": "user registered successfully", "status": status.HTTP_201_CREATED}
    
    except (DatabaseError, UserRegistrationError) as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/login")
async def login(loginDetails: LoginDetails):
    try:
        return login_user(loginDetails)
    
    except UserLoginError as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except (DatabaseError, UserRegistrationError) as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.post("/refresh-token")
async def refresh_token(request: RefreshTokenRequest):
    try:
        return token_refresh(request)
        
    except (jwt.exceptions.InvalidIssuerError) as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except (jwt.exceptions.InvalidAudienceError) as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except UserLoginError as e:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    except (DatabaseError, UserRegistrationError) as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))  