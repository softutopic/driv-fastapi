from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta
from config import settings

def create(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SALT, algorithm="HS256")
    return encoded_jwt

def decrypt_token(token: str) -> dict:
    user : dict = jwt.decode(token, settings.JWT_SALT, algorithms=["HS256"])
    return user 