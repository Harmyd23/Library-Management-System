from ...databases import Session
from ...models import Borrowed_books
from datetime import datetime,timedelta
from fastapi import status
from fastapi.responses import JSONResponse

def borrowBook(request,db:Session,user):
    userId=user["user_id"]
    if not userId:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Not authorized"}
        )
    #check if this book has been borrowed
    existing = db.query(Borrowed_books).filter(Borrowed_books.user_id==userId,Borrowed_books.google_book_id==request.Google_id).first()
    if existing:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"Book already borrowed"}
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
                 "due_date":recent_borrow.due_date.isoformat()
                 }
    )



