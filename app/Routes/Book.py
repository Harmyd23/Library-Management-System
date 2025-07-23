from fastapi import APIRouter,status,Depends,Query
from ..databases import Session,get_db
from ..Util.oauth import decode_token
from ..schema import BorrowBook
from ..Services.Books import get_books,borrow_book,Get_borrowed_books
from typing import Optional

Book=APIRouter(prefix="/books")

@Book.get("/get_book",status_code=status.HTTP_200_OK)
def get_book(db:Session=Depends(get_db),user=Depends(decode_token)):
    return get_books.get_all(db,user)

@Book.post("/borrow_book",status_code=status.HTTP_201_CREATED)
def borrowBOOK(request:BorrowBook,db:Session=Depends(get_db),user=Depends(decode_token)):
    return borrow_book.borrowBook(request,db,user)

@Book.get("/search_book",status_code=status.HTTP_200_OK)
def search_book(title:Optional[str]=Query(None),
                author:Optional[str]=Query(None),
                genre:Optional[str]=Query(None),
                user=Depends(decode_token),
                db:Session=Depends(get_db)):
    return get_books.get_by_filter(title,author,genre,user,db)

@Book.get("/get_borrowed_books",status_code=status.HTTP_200_OK)
def get_borrowed_Books(db:Session=Depends(get_db),user=Depends(decode_token)):
    return Get_borrowed_books.get_borrowed_books(db,user)