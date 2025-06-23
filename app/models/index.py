from pydantic import BaseModel
from datetime import datetime, date

class User(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    birthday: date
    email: str
    phone_number: str | None = None
    updated_at: datetime
    created_at: datetime
    password: str
    