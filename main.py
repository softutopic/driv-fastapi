import re
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
        r"^/?$",
        r"^/api/auth/?$",
        r"^/docs/?$",
        r"^/openapi.json/?$",
    ]

    # Check if the current path matches any of the exempt patterns
    if any(re.match(pattern, request.url.path) for pattern in exempt_paths):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse({"error": True, "message": "Authorization header missing or invalid"}, 401)

    token = auth_header[len("Bearer "):]
    try:
        if decrypt_token(token):
            return await call_next(request)
        return JSONResponse({"error": True, "message": "Token has expired"}, 401)
    except Exception as e:
        return JSONResponse({"error": True, "message": f"Token validation failed: {e}"}, 401)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(user)
app.include_router(category)
app.include_router(subcategoryRoute)
app.include_router(vehicleRoute)