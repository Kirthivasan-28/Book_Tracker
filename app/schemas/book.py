from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookCreate(BaseModel):
    title: str 
    description: str
    author : str 
    added_at : Optional[datetime] = None