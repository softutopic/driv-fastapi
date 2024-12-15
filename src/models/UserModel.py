
import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError
from typing import Optional

class UserModel(BaseModel):
    # username: str = Field(min_length=3, max_length=50, )
    # password: str = Field(min_length=8, max_length=200)
    # name: str = Field(min_length=5, max_length=200)
    # email: EmailStr
    # phone: Optional[str] = Field(min_length=10, max_length=12) 
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None 
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[str] = None
    business: Optional[str] = None
    
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
    