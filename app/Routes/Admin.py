from fastapi import APIRouter ,status,Depends
from ..databases import Session,get_db
from ..Services.Admin import auth
from ..schema import AdminLogin,Admin

admin=APIRouter(prefix="/admin")
@admin.post("/signup",status_code=status.HTTP_200_OK)
def admin_handover(request:Admin,db:Session=Depends(get_db)):
    return auth.transfer_admin_account(request,db)

@admin.post("/login",status_code=status.HTTP_200_OK)
def login(request:AdminLogin,db:Session=Depends(get_db)):
    return auth.login(request,db)
