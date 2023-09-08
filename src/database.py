from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from .UploadSession import *
import os
import pandas as pd

def rmEngine(name):
    if os.path.exists(os.getcwd()+os.sep+f"{name}.sqlite3"):
        os.remove(os.getcwd()+os.sep+f"{name}.sqlite3")    
def createEngine(name):
    conn_string = f'sqlite:///{name}.sqlite3'
    # if os.path.exists(os.getcwd()+os.sep+f"{name}.sqlite3"):
    #     os.remove(os.getcwd()+os.sep+f"{name}.sqlite3")

    engine = create_engine(conn_string)
    print(f'start create {name} database for {name} purpose')
    # Base.metadata.create_all(engine)  # here we create all tables
    # print(f'finish create tables for  {name} database')

    return engine
def createSessonMaker(engine):
    Session = sessionmaker(bind=engine)
    dbsession = Session()
    return dbsession
if os.path.exists(os.getcwd()+os.sep+"test.sqlite3"):
    print('detected test database exists,clear the old  and create a new')
    os.remove(os.getcwd()+os.sep+"test.sqlite3")




def pd2table(engine,table_name,df,logger,if_exists='append',dtype=None):

    try:
        with engine.begin() as conn:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False,dtype=dtype)
            logger.info(f"insert data to {table_name}>>> seems All good.")
            return True
    except Exception as e:
        logger.error(f"insert data to {table_name}>>> seems went wrong!{e}")
        return False
def  query2df(engine,query,logger):

    try:
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        logger.error(f"query  to {query}>>> seems went wrong!{e}")
        return None

dbsession_test=createSessonMaker('test')
dbsession_pro=createSessonMaker('prod')
