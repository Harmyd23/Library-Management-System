from fastapi import APIRouter,status,Depends,File,UploadFile,Form
from ..databases import get_db,Session
from ..Services.Users import upload_profile_image,get_user_detail,edit_user
from ..Util.oauth import decode_token
from ..schema import UserOut,Edit_user

user=APIRouter(prefix="/user")
@user.post("/upload_profile",status_code=status.HTTP_200_OK)
def upload_image(
    Picture:UploadFile=File(default=None),
    db:Session=Depends(get_db),
    user=Depends(decode_token)
):
    return upload_profile_image.upload_profile_image(Picture,db,user)

@user.get("/get_user_detail",status_code=status.HTTP_200_OK,response_model=UserOut)
async def user_info(db:Session=Depends(get_db),user=Depends(decode_token)):
    return get_user_detail.get_user_detail(db,user)

@user.post("/edit_user_detail",status_code=status.HTTP_200_OK)
async def edit_user_detail(
    request:Edit_user,
    db:Session=Depends(get_db),
    user=Depends(decode_token)
):
    return await edit_user.edit_user(request,db,user)