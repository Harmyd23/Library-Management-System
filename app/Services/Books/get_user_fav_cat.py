from collections import Counter
from ...models import Borrowed_books
from ...databases import Session
import random
from ...Util.config import Departments

def get_user_fav_category(user_id,db:Session):
    borrowed_history=db.query(Borrowed_books).filter(Borrowed_books.user_id==user_id).all()
    if not borrowed_history:
        return random.sample(Departments,4)
    category=[book.category for book in borrowed_history]
    #count the categories for the no of times there appear
    category_count=Counter(category)
    #pick the 3 highest count of category
    most_common=category_count.most_common(3)
    category_names=[cat[0] for cat in most_common]
    
    if len(category_names)<3:
        needed_len=3-len(category_names)
        category_names.extend(random.sample(Departments,needed_len))
    return category_names
    
        

