from fastapi import APIRouter,status,Depends
from ..databases import get_db,Session
from ..schema import send_reset,VerifyCodeRequest,ResetPassword
from ..Services import Reset_code,Reset_password

forgot_password=APIRouter(prefix="/password_reset")
@forgot_password.post("/send_reset_code",status_code=status.HTTP_200_OK)
def reset_code(request:send_reset,db:Session=Depends(get_db)):
    return Reset_code.send_reset_code(request,db)

@forgot_password.post("/verify_code",status_code=status.HTTP_200_OK)
def verify_code(request:VerifyCodeRequest,db:Session=Depends(get_db)):
    return Reset_code.verify_reset_code(request,db)

@forgot_password.post("/change_password",status_code=status.HTTP_200_OK)
def change_password(request:ResetPassword,db:Session=Depends(get_db)):
    return Reset_password.reset_password(request,db)