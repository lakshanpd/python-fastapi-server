from fastapi import FastAPI, HTTPException, status
from models import User, LoginDetails
from auth.register import register_user
from auth.login   import login_user
from errors import DatabaseError, UserRegistrationError, UserLoginError
import logging
import traceback

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

@app.post("/register/")
async def register(user: User):
    try:
        register_user(user=user)
        logging.info("user registered successfully")
        return {"message": "user registered successfully", "status": status.HTTP_201_CREATED}
    
    except (DatabaseError, UserRegistrationError) as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.post("/login")
async def login(loginDetails: LoginDetails):
    try:
        return login_user(loginDetails)
    
    except UserLoginError as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except (DatabaseError, UserRegistrationError) as e:
        logging.error("handled error: \n%s", traceback.format_exc())
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))