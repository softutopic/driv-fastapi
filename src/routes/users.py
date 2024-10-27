from fastapi import APIRouter, Depends
from psycopg2 import DatabaseError
from sqlalchemy import Connection
from database import Database
from src.models.UserModel import UserModel
import src.functions.password_crypt as password_crypt
import src.middlewares.user_middleware as middleware

user = APIRouter()

@user.post("/api/user/")
def create_user(user: UserModel, db: Database = Depends()):
    
    user_exists = middleware.validate_if_user_exist(username=user.username)
    print(user.name)
    
    if user_exists:
        return {"error": True, "message": "User already exists"}
    
    crypt_password = password_crypt.hash_password(user.password)
    connection: Connection = db.get_connection()
    cursor = connection.connection.cursor()
    sql = f"""INSERT INTO users 
            (name, username, email, password) 
            values (%s, %s, %s, %s)"""
    
    try:
        cursor.execute(sql, (user.username, user.username, user.email, user.password))
        connection.commit()
        cursor.close()
        connection.close()
    except DatabaseError as e:
        return {"error": True, "message": e}

    return {"password": crypt_password}