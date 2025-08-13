from .databases import Base
from sqlalchemy import String,Integer,ForeignKey,Column,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(String,nullable=True)
    fullname=Column(String)
    phone_number=Column(String)
    email=Column(String)
    department=Column(String,nullable=True)
    password=Column(String)
    role=Column(String,default="Student")
    created_at=Column(DateTime,default=datetime.utcnow)

    borrowed_books=relationship("Borrowed_books",back_populates="user")
    reservations=relationship("Reservations",back_populates="user")


class Password_reset(Base):
    __tablename__="reset_code"
    id=Column(Integer,primary_key=True,index=True)
    code=Column(String)
    email=Column(String,index=True)
    expiry_at=Column(DateTime)

class Book(Base):
    __tablename__ ="books"
    id = Column(Integer,primary_key=True,index=True)
    google_book_id = Column(String, unique=True)
    title = Column(String)
    authors = Column(ARRAY(String))
    description = Column(String)
    category=Column(String)
    copies = Column(Integer, default=10)


class Borrowed_books(Base):
    __tablename__="Borrowed_books"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(ForeignKey("users.id"))
    google_book_id=Column(String,index=True)
    title=Column(String,index=True)
    author= Column(ARRAY(String))
    category=Column(String,index=True)
    borrow_date=Column(DateTime,default=datetime.utcnow)
    due_date=Column(DateTime)
    status=Column(String,default="Borrowed")
    return_initiated_at=Column(DateTime)

    user=relationship("User",back_populates="borrowed_books")
    reservations=relationship("Reservations",back_populates="borrowed_books")

class Reservations(Base):
    __tablename__="Reservations"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    borrowed_book_id=Column(Integer,ForeignKey("Borrowed_books.id"))
    email=Column(String,index=True)
    reserved_at=Column(DateTime,default=datetime.utcnow())
    reservation_expiry=Column(DateTime)
    status=Column(String,default="Active")

    user=relationship("User",back_populates="reservations")
    borrowed_books=relationship("Borrowed_books",back_populates="reservations")
    
    