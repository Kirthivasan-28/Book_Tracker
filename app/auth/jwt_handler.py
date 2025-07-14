from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def hashPassword(password: str):
    return pwd_context.hash(password)