from ...databases import Session
from fastapi.responses import JSONResponse
from fastapi import status,UploadFile
from ...models  import User
import cloudinary

async def edit_user(request,db,user):
    userId=user["user_id"]
    if not userId:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Not authorised"}
        )
    #created a dictionary in so i can easily use setattr func to update the present attr of the object
    try:
        data=request.dict(exclude_unset=True)
        #fetching the students result from the database 
        user_record= db.query(User).filter(User.id==userId).first()
        if not user_record:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"User not found"}
            )
        for field,value in data.items():    
            setattr(user_record,field,value)
        db.commit()
        db.refresh(user_record)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                    "message":"Updated",
                    "Updated_data":data
                    }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"msg":"An error occured internally"}
        )


    




    

    