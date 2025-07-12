from password_validator import PasswordValidator
from email_validator import EmailNotValidError,validate_email 
from fastapi.responses import JSONResponse
from fastapi import status
from hash import Hash

check_valid=PasswordValidator()
check_valid \
    .min(6)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().symbols()\
    .has().no().spaces()

def valid_password(password):
    if not check_valid.validate(password):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Min 8 chars, A-Z, a-z, 0-9, no spaces."}
        )
    password_hash=Hash()
    return password_hash.Hash_pas(password)

def valid_email(email):
    try:
        Email=validate_email(email)
        return Email.email
    except EmailNotValidError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":str(e)}
        )

        