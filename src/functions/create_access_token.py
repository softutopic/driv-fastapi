import os
from dotenv import load_dotenv
from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta

load_dotenv()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SALT"), algorithm="HS256")
    return encoded_jwt

def decrypt_token(token: str) -> str:
    user : dict = jwt.decode(token, os.getenv("JWT_SALT"), algorithms=["HS256"])
    exp = user.get('exp')
    if datetime.fromtimestamp(exp) < datetime.utcnow():
        return None
    return user.get('sub')