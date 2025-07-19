from fastapi import APIRouter,status,Depends
from ..databases import Session,get_db
from ..Util.oauth import decode_token
from ..schema import BorrowBook
from ..Services.Books import get_books,borrow_book

Book=APIRouter(prefix="/books")

@Book.get("/get_book",status_code=status.HTTP_200_OK)
def get_book(db:Session=Depends(get_db),user=Depends(decode_token)):
    return get_books.get_all(db,user)

@Book.post("/borrow_book",status_code=status.HTTP_201_CREATED)
def borrowBOOK(request:BorrowBook,db:Session=Depends(get_db),user=Depends(decode_token)):
    return borrow_book.borrowBook(request,db.user)
