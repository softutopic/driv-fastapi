from fastapi import Depends
from sqlalchemy import Connection
from database import database as db

def validate_if_user_exist(email: str) -> bool:
    
    connection: Connection = db.get_connection()
    cursor = connection.connection.cursor()
    sql = f"""SELECT 1 FROM users WHERE email = %s"""
    cursor.execute(sql, [email])
    
    result = cursor.fetchmany()
    cursor.close()
    return True if len(result) > 0 else False