from ...databases import Session
from ...Util.validator import valid_email,valid_password
from fastapi.responses import JSONResponse
from ...models import User
from fastapi import status
from ...Util.Token import create_access_token
from ...Util.hash import Hash

def transfer_admin_account(request,db:Session):
    #checking if there is an existing admin already,if there is delete
    existing_admin=db.query(User).filter(User.role=="Admin").first()
    if existing_admin:
        db.delete(existing_admin)
        db.commit()
    #checking if email is a valid email
    emailcheck=valid_email(request.Email.strip().lower())
    if isinstance(emailcheck,JSONResponse):
        return emailcheck
    Email=emailcheck
    #checking if password meets all the requirement of a strong password
    passwordcheck=valid_password(request.Password)
    if isinstance(passwordcheck,JSONResponse):
        return passwordcheck
    hashed_password=passwordcheck
    #checking if the email is not in use already
    Email_dup_check=db.query(User).filter(User.email==Email).first()
    if Email_dup_check:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Email already exists"}
        )
    #making sure the phone number is unique
    phoneNumberCheck=db.query(User).filter(User.phone_number==request.Phone_number).first()
    if phoneNumberCheck:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Phone number exists"}
        )
    try:
        new_admin=User(fullname=request.Admin_name,phone_number=request.Phone_number,email=Email,password=hashed_password,role="Admin")
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message":"Admin Signed up Successfull",
                     "Token":create_access_token(data=
                                                {
                                                    "user_id":new_admin.id,
                                                    "email":new_admin.email,
                                                    "user_name":new_admin.fullname
                                                    }),
                     "Token_type":"Bearer",                           
                }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )

def login(request,db:Session):
     #checking if email is a valid email
    emailcheck=valid_email(request.Email.strip().lower())
    if isinstance(emailcheck,JSONResponse):
        return emailcheck
    Email=emailcheck
    #check if the email belongs to the user
    user=db.query(User).filter(User.email==Email).first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message":"Email does not exist"}
        )
    Hasher=Hash()
    password_validity=Hasher.verify_pas(request.Email,user.password)
    if password_validity==False:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Wrong Password"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"LoggedIn Successfully",
                 "Token":create_access_token(data={"user_id":user.id,"user_name":user.fullname,"email":user.email}),
                 "Token_type":"Bearer"
                 }
    )

    
