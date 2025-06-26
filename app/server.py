from fastapi import FastAPI, HTTPException, status
from models import User
from auth.register import register_user
from errors import DatabaseError, UserRegistrationError
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