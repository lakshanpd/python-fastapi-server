from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

class User(BaseModel):
    id: UUID | None = None
    first_name: str
    last_name: str | None = None
    birthday: date
    email: str
    phone_number: str | None = None
    updated_at: datetime
    created_at: datetime
    password: str

class LoginDetails(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
    
class TranslatorParams(BaseModel):
    language: str
    text: str
    
class ChatModelParams(BaseModel):
    user_id: str
    user_input: str