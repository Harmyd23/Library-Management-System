import requests
from fastapi import status
from ...databases import Session
from ...models import User,Book,Borrowed_books
from fastapi.responses import JSONResponse
from ...Services.Books import get_user_fav_cat


def get_all(db:Session,user):
    user_id=user["user_id"]
    current_user=db.query(User).filter(User.id==user_id).first()
    if not current_user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"User not authorized"}
        )
    try:
        user_cat=get_user_fav_cat(user_id,db)
        books={}
        # for each category in the user's favourite category
        for category in user_cat:
            req=requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                timeout=5,
                params={
                "q":f"subject:{category}",
                "maxResults": 5,
                "printType":"Books"
                }
            )
            req.raise_for_status()
            items=req.json().get("items",[])
            needed_attr=[]
            #looping through each item each books related to the category
            for item in items: 
                goog_book_id=item.get("id")
                volume_info=item.get("volumeInfo",{})
                #check if this book existed already in my db
                existing=db.query(Book).filter(Book.google_book_id==goog_book_id).first()
                if not existing:
                    book_in_db=Book(
                                    google_book_id=goog_book_id,
                                    title=volume_info.get("title"),
                                    authors=volume_info.get("authors",[]),
                                    description=volume_info.get("description"),
                                    category=category
                                    )
                    db.add(book_in_db)
                    db.commit()
                    db.refresh(book_in_db)
                    existing=book_in_db
                #check for availability
                borrowed_count=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==goog_book_id).count()
                book_total_count=existing.copies
                availability=book_total_count-borrowed_count
                needed_attr.append({
                    "Google_book_id":goog_book_id,
                    "Category":category,
                    "Title":volume_info.get("title"),
                    "Authors":volume_info.get("authors",[]),
                    "Publisher":volume_info.get("publisher"),
                    "Published_date":volume_info.get("publishedDate"),
                    "Description":volume_info.get("description"),
                    "Availability":"Available" if availability > 0 else "Unavailable"
                })
            #store in the book dictionary, each with a key of its own category
            books[category]=needed_attr            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                    "message":"Successfull",
                    "Books":books
                    }
        )
    except requests.exceptions.RequestException as err:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":str(err)
            }
        )
