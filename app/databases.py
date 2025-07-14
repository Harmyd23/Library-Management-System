from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from .Util.config import Database_url

database_url="postgresql://library_user:AZxfBI52Xk0iUKYgi1WuXeP6sExrsHeh@dpg-d1lag4mmcj7s73bvjktg-a.oregon-postgres.render.com/lms_db_oq4e"
engine=create_engine(database_url)
Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

def get_db():
    print("get_db is called")
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()
