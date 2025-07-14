from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from .Util.config import Database_url

database_url=Database_url
engine=create_engine(database_url, connect_args={"connect_timeout": 5})
Sessionlocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

def get_db():
    #print("get_db is called")
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()
