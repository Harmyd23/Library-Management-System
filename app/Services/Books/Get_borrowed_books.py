from ...models import Borrowed_books
from ...databases import Session
from fastapi.responses import JSONResponse
from fastapi import status

def get_borrowed_books(db:Session,user):
    user_id=user["user_id"]
    if not user_id:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"Not authorised"}
        )
    try:
        borrowed_book=db.query(Borrowed_books).filter(Borrowed_books.user_id==user_id).all()
        if not borrowed_book:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message":"No book borrowed yet"}
            )
        books=[]
        for book in borrowed_book:
            books.append({
            "Google_book_id":book.google_book_id,
            "Title":book.title,
            "Author":book.author,
            "Category":book.category,
            "due_date":book.due_date
            })
    
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                    "message":"Successfull",
                    "Books":books
                    }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )

    
        