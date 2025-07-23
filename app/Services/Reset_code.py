from ..databases import Session
from ..Util.validator import valid_email
from fastapi.responses import JSONResponse
from ..models import User,Password_reset
from datetime import timedelta,datetime
from ..Util import OTP,Email,Token
from fastapi import status

def send_reset_code(request,db:Session):
    #check if the email actually exists & is a valid email addr
    email_check=valid_email(request.Email.strip().lower())
    if isinstance(email_check,JSONResponse):
        return email_check
    EMAIL=email_check
    user=db.query(User).filter(User.email==EMAIL).first()
    if not user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message":"Email not found"}
        )
    
    expiry=datetime.utcnow()+timedelta(minutes=1)
    now = datetime.utcnow()
    Otp_code=OTP.generate_OTP(4)        
    existing=db.query(Password_reset).filter(Password_reset.email==EMAIL).first()
    if existing:
        if existing.expiry_at > now:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                        "message":"A code had already been sent,Check email",
                        "expiry_at":existing.expiry_at.isoformat()
                        }
            )
        existing.code=Otp_code
        existing.expiry_at=expiry
        
    else:
        reset_code=Password_reset(email=EMAIL,code=Otp_code,expiry_at=expiry)
        db.add(reset_code)

    db.commit()
    try:
        subject="Password_reset"
        message=f"Here is your reset code {Otp_code},This code will expire in 1 minute"
        Send_email=Email.send_email(EMAIL,subject,message)
        print(f"sending email to {Email} with code {Otp_code}...")
    except Exception as e:
        if reset_code:
            db.delete(reset_code)
            db.commit()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":f"Failed to send email:{str(e)}"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"Reset code is sent successfully",
                 "expiry":expiry.isoformat()}
    )


def verify_reset_code(request,db):
    email_check=valid_email(request.Email.strip().lower())
    if isinstance(email_check,JSONResponse):
        return email_check
    Email=email_check
    now=datetime.utcnow()
    otp=db.query(Password_reset).filter(Password_reset.email==Email).first()

    if  otp.code!=request.Code:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message":"Code not match"}
        )
    elif otp.expiry_at < now:
        return JSONResponse(
            status_code=status.HTTP_410_GONE,
            content={"message":"Code Expired"}
        )
    else:
        USER=db.query(User).filter(User.email==Email).first()
        if not USER:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"User does not exist"}
            )
        token=Token.create_access_token(data={"user_id":USER.id,"user_name":USER.fullname,"email":USER.email})
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                     "message":"Code Verified",
                     "Token":token,
                     "Token_type":"Bearer"
                     }
        )
    


    

    
        
        
    
    
   