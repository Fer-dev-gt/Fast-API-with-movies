
from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse


user_router = APIRouter()



class User(BaseModel):
    username: str
    email: str
    password: str


@user_router.post('/login', tags=["auth"])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        try:
            token: str = create_token(user.dict())
            return JSONResponse(content={"token": token}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)
    else:
        return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)