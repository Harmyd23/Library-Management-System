from email.message import EmailMessage
import smtplib
from email.utils import formataddr
from fastapi.responses import JSONResponse
from fastapi import status

def send_email(code,receiver_email):
    my_email="abdulharmyd3@gmail.com"
    my_app_password="ughtbouqgtkdhpzl"


    msg=EmailMessage()
    msg["From"]=formataddr(("Libraconnect",my_email))
    msg["To"]=receiver_email
    msg["subject"]="Password reset"
    msg.set_content(f"Here is your reset code {code},This code will expire in 1 minute")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        try:
            smtp.set_debuglevel(1)
            smtp.login(my_email,my_app_password)
            smtp.send_message(msg)
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message":str(e)}
            )
    



