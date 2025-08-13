from pydantic import BaseModel
from datetime import datetime
from typing import List,Optional


class User(BaseModel):
    Fullname:str
    Phone_number:str
    Email:str
    Password:str
    Department:str

class UserOut(BaseModel):
    Full_name:str
    Phone_number:str
    Department:str
    Email:str
    profile_image:Optional[str]=None

    class Config:
        from_attributes=True

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
    Author:List[str]
    Category:str

class ReturnBook(BaseModel):
    Google_id:str

class UserOut(BaseModel):
    Full_name:str
    Matric_No:str
    Department:str
    Level:str
    Email:str
    profile_image:Optional[str]=None

    class Config:
        from_attributes=True
     
class Edit_user(BaseModel):
    Full_name:Optional[str]=None
    Matric_No:Optional[str]=None
    Department:Optional[str]=None
    Level:Optional[str]=None
    Email:Optional[str]=None


class Admin(BaseModel):
    Admin_name:str
    Email:str
    Phone_number:str
    Password:str

class AdminLogin(Login):
    pass


#09169081780