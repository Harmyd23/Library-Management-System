from ...databases import Session
from fastapi import status,HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ...models import User
from ...schema import UserOut

async def get_user_detail(db:Session,user):
    userId=user["user_id"]
    if not userId:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"messsage":"Not authorised"}
        )
    try:
        USER= db.query(User).filter(User.id==userId).first()
        if not USER:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"User does not exist"}
            )
        user_data=UserOut.from_orm(USER)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                    "message":"Successfull",
                    "User":jsonable_encoder(user_data)
                     }
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    

    