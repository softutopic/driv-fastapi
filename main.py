import re
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Connection
# from database import Database
from src.routes.users import user
from src.routes.categories import category
from src.routes.subcategories import subcategoryRoute
from src.routes.vehicles import vehicleRoute
from fastapi.security import OAuth2PasswordBearer
from src.functions.create_access_token import decrypt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    exempt_paths = [
        r"^/api/auth/?$",
        # r"^/api/categories/?$",
        # r"^/api/categories/[^/]+/?$",
        r"^/docs/?$",
        r"^/openapi.json/?$",
    ]

    # Comprueba si la ruta actual coincide con alguno de los patrones exentos
    if any(re.match(pattern, request.url.path) for pattern in exempt_paths):
        return await call_next(request)
    if not request.headers.get("Authorization"):
        return JSONResponse(None, 401)
    else:
        # try:
            
        if decrypt_token(request.headers.get("Authorization")):
            return await call_next(request)
        return JSONResponse({"error": True, "message": "Token has expired"}, 401)
        # except Exception as e:
        #     return JSONResponse({"error": True, "message": f"Token has expired {e}"}, 401)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user)
app.include_router(category)
app.include_router(subcategoryRoute)
app.include_router(vehicleRoute)