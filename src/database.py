from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from .UploadSession import *
import os

print('running')
conn_string = 'sqlite:///youtube.sqlite3'
if os.path.exists(os.getcwd()+os.sep+"youtube.sqlite3"):
    os.remove(os.getcwd()+os.sep+"youtube.sqlite3")

engine = create_engine(conn_string)
print('start create tables')
Base.metadata.create_all(engine)  # here we create all tables
print('finish create tables')

Session = sessionmaker(bind=engine,autoflush=True,autocommit=True)
dbsession = Session()


