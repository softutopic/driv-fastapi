from fastapi import FastAPI, Depends
from database import Database

app = FastAPI()

@app.get("/")
def read_root(db: Database = Depends()):
    connection = db.get_connection()
    print(connection)
    connection.close()
    return {"Hello": "World"}

