from passlib.context import CryptContext
from jose import jwt
pwd_context = CryptContext(schemes=["bcrypt"])
from datetime import datetime, timedelta, timezone
from decouple import config

SECRET_KEY = config("JWT_SECRET_KEY")
ALGORITHM = config("JWT_ALGORITHM")
def hashPassword(password: str):
    return pwd_context.hash(password)

def verifyPassword(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta=timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token