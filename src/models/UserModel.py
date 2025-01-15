
import re
import uuid
from dbCon import Base
from typing import Optional
from datetime import datetime
from sqlalchemy import UUID, Column, Integer, String, DateTime, Boolean, ForeignKey
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError


class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    business_id = Column(Integer, ForeignKey('business.uuid', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # state = Column(Boolean, default=True)
    
class UserBase(BaseModel):
    username: str
    password: str
    name: str
    email: EmailStr
    phone: str
    age: Optional[int]
    business_id: int
    
class UserBaseResponse(BaseModel):
    username: Optional[str]
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    age: Optional[int]
    
class UserCreate(UserBase):
    @field_validator('username')
    def validate_username_length(cls, v):
        if len(v) < 4:
            raise ValueError("El nombre de usuario debe tener al menos 4 caracteres")
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("El password debe tener al menos 8 caracteres")
        return v
    
    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 8:
            raise ValueError("El nombre debe tener al menos 8 caracteres")
        return v
    
    @field_validator('phone')
    def validate_phone_number(cls, v):
        # Eliminamos espacios y guiones para facilitar la validación
        clean_number = v.replace(' ', '').replace('-', '')

        # Verificamos si comienza con el código de país +57
        if not clean_number.startswith('+57'):
            raise ValueError('Invalid country code. Must start with +57')

        # Verificamos la longitud total
        if len(clean_number) != 13:
            raise ValueError('Invalid phone number length')

        # Verificamos la longitud del código de área (puede variar)
        # Aquí asumimos que el código de área tiene 3 dígitos
        if not clean_number[3:].isdigit():
            raise ValueError('Invalid area code')

        return v
    
    @field_validator('email')
    def validate_email(cls, v):
        # Expresión regular básica para validar correos electrónicos
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, v):
            raise ValueError("Invalid email format")
        return v
    pass
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[str] = None
    business_id: Optional[str] = None
class UserInDB(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    # state: bool
    
    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserBaseResponse]