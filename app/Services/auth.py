from ..databases import Session
from fastapi import status,HTTPException
from fastapi.responses import JSONResponse
from ..Util.validator import valid_email,valid_password
from ..models import User
from ..Util.hash import Hash
from ..Util.Token import create_access_token
from ..Util import Generate_user_id

def signup(request,db:Session):

    fullname= request.Fullname.strip().lower()
    Email_validation=valid_email(request.Email.strip().lower())
    #check if email is valid and return the err if not valid
    if isinstance(Email_validation,JSONResponse):
        return Email_validation
    email=Email_validation
    #check if password is valid and return err if not valid 
    password_validation=valid_password(request.Password)
    if isinstance (password_validation,JSONResponse):
        return password_validation
    hashed_password=password_validation

    #check if email exists
    email_Check=db.query(User).filter(User.email==email).first()
    if email_Check:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"email exists"}
        )
    user_Id=Generate_user_id.generate_unique_id(db)
    try:
        user=User(fullname=request.Fullname,user_id=user_Id,phone_number=request.Phone_number,email=email,department=request.Department,password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                     "messsage":"signup sucussful",
                     "Token":create_access_token(data={"user_id":user.id,"user_name":user.fullname,"email":user.email}),
                     "Token_type":"Bearer"
                    }
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=str(e))


def login(request,db:Session):

    email_check=valid_email(request.Email.strip().lower())
    if isinstance(email_check,JSONResponse):
        return email_check
    email=email_check
    #check if email exists
    user=db.query(User).filter(User.email==email).first()
    if not User:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message":"Email does not exist"}
        )
    Hasher=Hash()
    password_match=Hasher.verify_pas(request.password,user.password)
    if not password_match:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Wrong Password"}
        )
    else:
        Token=create_access_token(data={"user_id":user.id,"user_name":user.fullname,"email":user.email})
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                    "message":"logged in successful",
                    "Token":Token,
                    "Token_type":"Bearer"
                     }
        )


    
    

