from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime,timedelta
from fastapi import Depends
from ...databases import Session,get_db
from ...Util.config import Database_url
from ...Util.Email import send_email
from ...models import Borrowed_books,User
from sqlalchemy import func

def send_due_date_reminder(): 
    db_gen=get_db()
    db:Session=next(db_gen)
    closer_due=(datetime.utcnow()+ timedelta(days=3)).date()
    borrowed_books=db.query(Borrowed_books).filter(func.date(Borrowed_books.due_date)==closer_due).all()
    subject="Libraconnect Book Due Reminder"
    for books in borrowed_books:
        userId=books.user_id
        #get user email
        user=db.query(User).filter(User.id==userId).first()
        email=user.email
        message=f"Dear {user.fullname},the book{books.title} will be due in 3 days. Kindly return it to avoid fines"
        send_email(email,subject,message)
    db.close()
#save in db to persist job scheduling to avoid lost of jobs when the app restart
jobstores={"default":SQLAlchemyJobStore(url=Database_url)}

scheduler=BackgroundScheduler(jobstores=jobstores)
scheduler.add_job(send_due_date_reminder,"cron",hour=8,minute=0)
scheduler.start()

        