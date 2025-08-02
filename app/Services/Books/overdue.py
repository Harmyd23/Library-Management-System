from fastapi import status
from ...databases import Session,get_db
from ...models import Borrowed_books
from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from ...Util.config import Database_url

def mark_as_overdue():
    db_gen=get_db()
    db:Session=next(db_gen)
    try:
        now=datetime.utcnow()
        books=db.query(Borrowed_books).filter(Borrowed_books.status=="Borrowed",Borrowed_books.due_date<now).all()
        for book in books:
            book.status="Overdue"
        db.commit()
    finally:
        db.close()
    
jobstores={"default":SQLAlchemyJobStore(url=Database_url)}
scheduler=BackgroundScheduler(jobstores=jobstores)
scheduler.add_job(mark_as_overdue,"cron",hour=8,minute=0)
scheduler.start()

    


    


