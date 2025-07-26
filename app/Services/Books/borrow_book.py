from ...databases import Session
from ...models import Borrowed_books,Book
from datetime import datetime,timedelta
from fastapi import status
import requests
from ...Util.config import Api_key
from fastapi.responses import JSONResponse

def borrowBook(request,db:Session,user):
    userId=user["user_id"]
    if not userId:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Not authorized"}
        )
    #save in my books table if it is not in it
    #first checking if the book is present
    book_check=db.query(Book).filter(Book.google_book_id==request.Google_id).first()
    if not book_check:
        req=requests.get(
            f"https://www.googleapis.com/books/v1/volumes/{request.Google_id}",
            timeout=5,
            params={
                "key":Api_key
            }
        )
        book_full_info=req.json()
        volume_info=book_full_info.get("volumeInfo",{})
        new_book=Book(google_book_id=request.Google_id,
                      title=volume_info.get("title"),
                      authors=volume_info.get("authors",[]),
                      description=volume_info.get("description"),
                      category=volume_info.get("categories")
                      )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    #check if this book has been borrowed
    existing = db.query(Borrowed_books).filter(Borrowed_books.user_id==userId,Borrowed_books.google_book_id==request.Google_id).first()
    if existing:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Book already borrowed"}
        )
    #checking if the borrow limit has been reached
    user_borrow_count=db.query(Borrowed_books).filter(Borrowed_books.user_id==userId,
                                                      Borrowed_books.status=="Borrowed").count()
    if user_borrow_count>10:
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"message":"Borrow limit reached,return a book to borrow"}
        )
    try:
        recent_borrow=Borrowed_books(
            user_id=userId,
            google_book_id=request.Google_id,
            title=request.Title,
            author=request.Author,
            category=request.Category,
            due_date=datetime.utcnow()+timedelta(days=14)
        )
        db.add(recent_borrow)
        db.commit()
        db.refresh(recent_borrow)
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
                 "message":"Book borrowed successfully",
                 "id":recent_borrow.id,
                 "title":recent_borrow.title,
                 "author":recent_borrow.author,
                 "due_date":recent_borrow.due_date.isoformat(),
                 "borrowed":True
                 }
    )







