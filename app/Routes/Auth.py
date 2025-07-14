from fastapi import APIRouter,Depends,status
from ..databases import get_db,Session
from ..schema import User,Login
from ..Services import auth


Auth=APIRouter(prefix="/auth")
@Auth.post("/signup",status_code=status.HTTP_201_CREATED)
async def Signup(request:User):
    print("SIGNUP ROUTE HIT")
    return auth.signup(request)

@Auth.post("/login",status_code=status.HTTP_200_OK)
async def Login(request:Login,db:Session=Depends(get_db)):
    return auth.login(request,db)