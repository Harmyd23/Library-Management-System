from fastapi import APIRouter,status,Depends
from ..databases import Session,get_db
from ..Util.oauth import decode_token
from ..Services.Books import get_books 

Book=APIRouter(prefix="/books")
@Book.get("/get_book",status_code=status.HTTP_200_OK)
def get_book(db:Session=Depends(get_db),user=Depends(decode_token)):
    return get_books.get_all(db,user)
