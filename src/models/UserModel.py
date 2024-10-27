
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import String

class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=50, )
    password: str = Field(min_length=8, max_length=200)
    name: str = Field(min_length=5, max_length=200)
    email: EmailStr
    
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "username": "johndoe",
    #             "email": "johndoe@example.com",
    #             "password": "secretpassword",
    #             "full_name": "John Doe",
    #             "age": 30
    #         }
    #     }