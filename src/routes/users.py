from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordBearer
from src.models.UserModel import UserLogin, User, UserBaseResponse, UserLoginResponse
import src.functions.password_crypt as password_crypt
import src.functions.create_access_token as at
from sqlalchemy.orm import Session
from dbCon import get_db

user = APIRouter()

@user.post("/api/auth/", status_code= status.HTTP_200_OK)
def auth_user(user: UserLogin, db: Session = Depends(get_db)):
    user_indb = db.query(User).filter(User.email == user.email).first()
    if user_indb is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="User not found")
    
    passbites = str(user_indb.password).encode('utf-8')
    if not password_crypt.verify_password(user.password, passbites):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid credentials")
    
    user_response = UserLoginResponse(access_token=at.create_access_token({"sub": str(user_indb.id)}), token_type="bearer", user=UserBaseResponse( id=user_indb.id, username=user_indb.username, name=user_indb.name, email=user_indb.email, phone=user_indb.phone, age=user_indb.age, business_id=user_indb.business_id))

    return user_response

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@user.get("/api/users/me", status_code= status.HTTP_200_OK, response_model=UserBaseResponse)
def user_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id : str|None = at.decrypt_token(token)
    if not user_id:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid credentials")
    user_indb = db.query(User).filter(User.id == user_id).first()
    if user_indb is None:
        return Response(status_code=404, content="User not found")
    
    return user_indb