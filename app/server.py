from fastapi import FastAPI
from routes import auth, ai

app = FastAPI()

app.include_router(auth.router)
app.include_router(ai.router)
    