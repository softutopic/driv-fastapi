from fastapi import Depends
from sqlalchemy import Connection
from database import database as db

def validate_if_user_exist(username: str) -> bool:
    
    connection: Connection = db.get_connection()
    cursor = connection.connection.cursor()
    sql = f"""SELECT 1 FROM users WHERE username = %s"""
    cursor.execute(sql, [username])
    
    result = cursor.fetchmany()
    cursor.close()
    return True if len(result) > 0 else False