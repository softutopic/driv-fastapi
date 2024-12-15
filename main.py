from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Connection
from database import Database
from src.routes.users import user
from fastapi.security import OAuth2PasswordBearer
from src.functions.create_access_token import decrypt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(request.url.path)
    if request.url.path in ["/api/auth/", "/api/auth"]:
        
        # No verificamos el header de autorización para estas rutas
        return await call_next(request)
    if not request.headers.get("Authorization"):
        return JSONResponse(None, 401)
    else:
        try:
            decrypt = decrypt_token(request.headers.get("Authorization"))
            return JSONResponse(decrypt, 200)
        except:
            return JSONResponse({"error": True, "message": "Token has expired"}, 401)

@app.get("/")
def read_root(db: Database = Depends()):
    connection : Connection = db.get_connection()
    connection.close()
    return {"Hello": "World"}

app.include_router(user)