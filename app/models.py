from .databases import Base
from sqlalchemy import String,Integer,ForeignKey,Column,DateTime
from sqlalchemy.orm import Relationship
from datetime import datetime

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(String)
    fullname=Column(String)
    phone_number=Column(String)
    email=Column(String)
    department=Column(String)
    password=Column(String)

class Password_reset(Base):
    __tablename__="reset_code"
    id=Column(Integer,primary_key=True,index=True)
    code=Column(Integer)
    email=Column(String,index=True)
    expiry_at=Column(DateTime)