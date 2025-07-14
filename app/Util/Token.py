from jose import jwt
from datetime import timedelta,datetime
from typing import Optional
from .config import Secret_key,Algorithm

def create_access_token(data:dict,expiry:Optional[timedelta] = None):
    to_encode=data.copy()

    if(expiry):
        expiry_date=datetime.utcnow()+expiry
    else:
        expiry_date=datetime.utcnow()+ timedelta(hours=1)

    to_encode.update({"exp":expiry_date})
    encoded_jwt=jwt.encode(to_encode,Secret_key,algorithm=Algorithm)
    return encoded_jwt

