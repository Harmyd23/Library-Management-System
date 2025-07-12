from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from .config import Secret_key,Algorithm
from fastapi.responses import JSONResponse

Oauth2scheme=OAuth2PasswordBearer("/login")

def decode_token(token:str=Depends(Oauth2scheme)):
    try:
        decoded_token=jwt.decode(token,Secret_key,algorithms=Algorithm)
        user_id = decoded_token.get("user_id")
        user_name=decoded_token.get("user_name")
        email=decoded_token.get("email")
        if not user_id or not email:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"Invalid token payload"}
            )
        return {"user_id":user_id,"user_name":user_name,"email":email}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired or invalid"
        )

