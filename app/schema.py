from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    Fullname:str
    Phone_number:str
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

class BorrowBook(BaseModel):
    Google_id:str
    Title:str
    Author:str
    Category:str
    

