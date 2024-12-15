from fastapi import APIRouter, Depends, status, Response, Request
from psycopg2 import DatabaseError
from psycopg2.extras import RealDictCursor
from sqlalchemy import Connection
from database import Database, database
from src.models.UserModel import UserModel
import src.functions.password_crypt as password_crypt
import src.middlewares.user_middleware as middleware
import src.functions.create_access_token as at

user = APIRouter()


@user.post("/api/auth/", status_code= status.HTTP_200_OK)
def create_user(user: UserModel, response: Response, db: Database = Depends()):
    
    user_exists = middleware.validate_if_user_exist(email=user.email)
    
    if user_exists:
        result = login(user)
        if result:
            return result
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"error": True, "message": "Credentials are not valid"}
    
    crypt_password = password_crypt.hash_password(user.password)
    connection: Connection = db.get_connection()
    cursor = connection.connection.cursor(cursor_factory=RealDictCursor)
    sql = """INSERT INTO users 
            (name, username, email, password, phone) 
            values (%s, %s, %s, %s, %s)"""
    
    try:
        cursor.execute(sql, [user.name, user.username, user.email, str(crypt_password).replace("b'", "").replace("'",""), user.phone])
        connection.connection.commit()
        cursor.close()
        connection.close()
    except DatabaseError as e:
        return {"error": True, "message": e.pgerror}

    result = login(user)
    if result:
            return result
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": True, "message": "Credentials are not valid"}

@user.get("/api/users/me", status_code= status.HTTP_200_OK)
def user_me(response: Response, request: Request):
    token = request.headers.get("Authorization")
    return {
        "token": token,
    }

""" Other functions
"""
def login(user: UserModel) -> bool:
    db = database
    connection: Connection = db.get_connection()
    with connection.connection.cursor() as cursor :
        sql = """SELECT name, username, password, email, phone from users where email = %s"""
        cursor.execute(sql, [user.email])
        data = cursor.fetchone()
        cursor.close()
        connection.connection.close()
        if password_crypt.verify_password(user.password, str(data[2]).encode('utf8')):
            result = {
                "username": data[1],
                "name" : data[0],
                "email" : data[3],
                "phone": data[4]
            }
            token = at.create(result)
            result["token"] = token
            return result
        else:
            return False