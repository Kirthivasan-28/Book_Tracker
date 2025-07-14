from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class UserSignup(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length= 6, max_length = 15)
    created_at : Optional[datetime] = None