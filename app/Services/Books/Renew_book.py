from fastapi import status
from .borrow_book import borrowBook
from ...databases import Session
from fastapi.responses import JSONResponse
from ...models import Reservations,Borrowed_books,Book
from datetime import timedelta,datetime

def renew_book(request,db:Session,user):
    try:
        userId=user["user_id"]
        if not userId:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message":"Not Unauthorised"}
            )
        #check if the book has been reserved already
        reserve_check=db.query(Reservations).filter(Reservations.borrowed_book_id==request.borrowed_book_id).first() 
        count_reserve=db.query(Reservations).filter(Reservations.borrowed_book_id==request.borrowed_book_id).count()
        #get the google book id 
        if reserve_check:
            google_id=reserve_check.borrowed_books.google_book_id
            #using the google_id to check for the borrowed book
            borrowedbook_count=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==google_id,Borrowed_books.status=="Returned").count()
            if count_reserve>borrowedbook_count:
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"message":"This book has been reserved"}
                )
            else:
                #extend the due date in borrowed_book table
                borrowed_book=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==google_id,Borrowed_books.user_id==userId).first()
                due_date=datetime.utcnow()+timedelta(days=14)
                borrowed_book.due_date=due_date
                db.commit()

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                             "message":"This book has Renewed",
                             "due_date":due_date.isoformat()
                             }
                )
        #count the total no of the reserved book and compare with the            
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )