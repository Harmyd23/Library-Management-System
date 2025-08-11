from fastapi import status
from ...databases import Session
from fastapi.responses import JSONResponse
from datetime import timedelta
from ...models import Borrowed_books,Reservations
from ...Util.Email import send_email


def reservations(request,db:Session,user):
    try:
        userId=user["user_id"]
        Email=user["email"]

        if not userId:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message":"Not Authorized"}
            )
        
        #check the book in the borrowed_book table for the expected return date
        borrowed_book=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==request.Google_book_id).order_by(Borrowed_books.due_date.asc()).all()
        if not borrowed_book:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"This book is available, not borrowed"}
            )
        
        earliest_copy=borrowed_book[0]
        #incase the book was not returned,the current holder has a grace of 3 days
        predicted_availability=earliest_copy.due_date + timedelta(days=3)
        Reservation_expiry=predicted_availability+timedelta(days=2)
        user_name=earliest_copy.user.fullname
        reserve_book=Reservations(user_id=userId,
                                borrowed_book_id=borrowed_book[0].id,
                                email=Email,
                                reservation_expiry=Reservation_expiry,
                                status="Pending")
        db.add(reserve_book)
        db.commit()
        db.refresh(reserve_book)
      
        subject="Book Reservations"
        message=f"Dear {user_name},The book will likely be available on {predicted_availability.strftime('%Y-%m-%d')} We will notify you if it becomes available earlier."
        send_email(subject=subject,message=message,receiver_email=Email)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message":"Book Reserved",
                     "Expected_availability":predicted_availability.isoformat()}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )

    




    



    


