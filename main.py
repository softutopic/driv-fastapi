from fastapi import FastAPI, Depends
from sqlalchemy import Connection
from database import Database
from src.routes.users import user

app = FastAPI()

@app.get("/")
def read_root(db: Database = Depends()):
    connection : Connection = db.get_connection()
    connection.close()
    return {"Hello": "World"}

app.include_router(user)