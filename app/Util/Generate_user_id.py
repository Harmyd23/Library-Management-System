import random
from ..databases import Session
from ..models import User
import logging

def generate_user_id(length=4,prefix="Stu"):
    return prefix + "".join(random.choices("0123456789",k=length))

def generate_unique_id(db:Session,prefix="Stu"):
    while True:
        try:
            user_Id=generate_user_id(4)
            #check if it exists in the db
            check_id=db.query(User).filter(User.user_id==user_Id).first()
            if not check_id:
                return user_Id
        except Exception as e:
            logging.error(f"Err while generating user_id")
            continue