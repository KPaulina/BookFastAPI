from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(passowrd: str) -> CryptContext:
    return pwd_context.hash(passowrd)


def verify(plain_password, hashed_passowrd):
    return pwd_context.verify(plain_password, hashed_passowrd)
