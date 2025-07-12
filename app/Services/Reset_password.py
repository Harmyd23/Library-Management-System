from ..databases import Session
from fastapi.responses import JSONResponse
from fastapi import Depends,status,HTTPException
from ..Util import validator
from ..models import User


def reset_password(request,db:Session):
    email_check=validator.valid_email(request.Email.strip().lower())
    if isinstance(email_check,JSONResponse):
        return email_check
    email=email_check
    try:
        user=db.query(User).filter(User.email==email).first()
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"User not found"}
            )

        user.password=validator.valid_password(request.Password)
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"message":"Password reset successfull"}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))
    




