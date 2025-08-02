from fastapi import status
from fastapi.responses import JSONResponse
from ...models import Borrowed_books
from ...databases import Session
from datetime import datetime,timedelta
from ...Util import Email

def initiate_return(request,db:Session,user):
    userId=user["user_id"]
    if not userId:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Not authorised"}
        )
    try:
        email=user["email"]
        user_name=user["user_name"]
        book=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==request.Google_id,Borrowed_books.user_id==userId).first()
        if book.status=="Borrowed" or book.status=="Overdue":
            now=datetime.utcnow()
            db_due_date=book.due_date
            Time_remaining:timedelta=db_due_date-now
            if Time_remaining < timedelta(0):
                book.status="Return_initiated"
                db.commit()
                Subject="Return Initiated"
                MEssage=f"Dear {user_name},Go to the Library for Visual confirmation of the book"
                Email.send_email(receiver_email=email,subject=Subject,message=MEssage)
            else:
                days_left=Time_remaining.days
                Message=f"You still have {days_left} left, are you sure u want to return"
                Email.send_email(receiver_email=email,subject="Did You Mean to Return This Book before Time?",message=Message)
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
                "message":"Return initiated. Check your email",
                 }
    )