from pydantic import BaseModel

class User(BaseModel):
    Fullname:str
    Phone_number:int
    Email:str
    Password:str
    Department:str

class Login(BaseModel):
    Email:str
    Password:str

class send_reset(BaseModel):
    Email:str

class VerifyCodeRequest(BaseModel):
    Email:str
    Code:str

class ResetPassword(Login):
    pass