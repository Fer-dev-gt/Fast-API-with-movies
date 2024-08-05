from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import validate_token




class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
       auth = await super().__call__(request)
       data = validate_token(auth.credentials)
       if data['email'] != "admin@gmail.com":
           raise HTTPException(status_code=403, detail="Credentials not valid") 

    # def __init__(self, auto_error: bool = True):
    #     super(JWTBearer, self).__init__(auto_error=auto_error)

    # async def __call__(self, request: Request):
    #     credentials = await super(JWTBearer, self).__call__(request)
    #     if credentials:
    #         return credentials
    #     else:
    #         raise HTTPException(
    #             status_code=403, detail="Invalid authorization code"
    #         )