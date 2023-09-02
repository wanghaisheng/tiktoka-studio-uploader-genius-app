from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from .UploadSession import *
import os



def createSessonMaker(name):
    conn_string = f'sqlite:///{name}.sqlite3'
    if os.path.exists(os.getcwd()+os.sep+f"{name}.sqlite3"):
        os.remove(os.getcwd()+os.sep+f"{name}.sqlite3")

    engine = create_engine(conn_string)
    print(f'start create {name} database')
    Base.metadata.create_all(engine)  # here we create all tables
    print(f'finish create {name} tables')

    Session = sessionmaker(bind=engine)
    dbsession = Session()
    return dbsession


dbsession_test=createSessonMaker('test')
dbsession_pro=createSessonMaker('prod')
