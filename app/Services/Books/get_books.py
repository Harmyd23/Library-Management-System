import requests
from fastapi import status
from ...databases import Session
from ...models import User,Book,Borrowed_books
from fastapi.responses import JSONResponse
from ...Services.Books import get_user_fav_cat
from ...Util.config import Api_key


def get_all(db:Session,user):
    user_id=user["user_id"]
    current_user=db.query(User).filter(User.id==user_id).first()
    if not current_user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message":"User not authorized"}
        )
    try:
        user_cat=get_user_fav_cat.get_user_fav_category(user_id,db)
        books={}
        # for each category in the user's favourite category
        for category in user_cat:
            req=requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                timeout=5,
                params={
                "q":f"subject:{category}",
                "maxResults": 5,
                "printType":"Books",
                "key":Api_key
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
                #checking if the user has borrowed any of the book in loop
                borrowed=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==goog_book_id,Borrowed_books.user_id==user_id).first() 
                needed_attr.append({
                    "Google_book_id":goog_book_id,
                    "Category":category,
                    "Title":volume_info.get("title"),
                    "Authors":volume_info.get("authors",[]),
                    "Publisher":volume_info.get("publisher"),
                    "Published_date":volume_info.get("publishedDate"),
                    "Description":volume_info.get("description"),
                    "Availability":"Available" if availability > 0 else "Unavailable",
                    "Borrowed":True if borrowed else False
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


                        #GETTING THE BOOK BY FILTERS


def get_by_filter(title,author,genre,user,db:Session):
    user_id=user["user_id"]
    current_user=db.query(User).filter(User.id==user_id).first()
    if not current_user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content ={"message":"not authorised"}
        )
    books={}
    query=None
    if title:
        query=f"intitle:{title}"
        search=title
    elif author:
        query=f"inauthor:{author}"
        search=author
    elif genre:
        query=f"subject:{genre}"
        search=genre
    try:
        req=requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            timeout=5,
            params={
                "q":query,
                "maxResults":20,
                "printType":"Books",
                "key":Api_key
            }
        )
        #getting the detail of the book
        needed_attr=[]
        filtered=req.json().get("items",[])
        for info in filtered:
            google_id=info.get("id")
            volume_info=info.get("volumeInfo",{})
            #checking if the book exist in my db using the google book id
            existing = db.query(Book).filter(Book.google_book_id==google_id).first()
            if existing:
                book_count= existing.copies
                borrowed_book_count=db.query(Borrowed_books).filter(Borrowed_books.google_book_id==google_id).count()
                availability = book_count-borrowed_book_count 
            needed_attr.append({
                "google_id":google_id,
                "title":volume_info.get("title"),
                "authors":volume_info.get("authors",[]),
                "category":volume_info.get("categories",[]),
                "availability":"Available" if not existing or availability>0 else "Unavailable"
                })

        books[search]=needed_attr
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message":str(e)}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message":"Successfull",
                 "book":books}

    )

    pass