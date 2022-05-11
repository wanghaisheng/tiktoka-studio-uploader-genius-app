from xmlrpc.client import boolean
from sqlalchemy import (
    Column, 
    Integer,
    String,
    Boolean,
    TIMESTAMP
)
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class UploadSession(Base):
    __tablename__ = 'uploadSession'
    id = Column(Integer, primary_key=True, autoincrement=True)
    videoid= Column(String, nullable=False )
    uploadSettingid= Column(Integer, nullable=False )
    videopath = Column(String, nullable=False )
    thumbpath = Column(String, nullable=False )
    title =Column(String, nullable=False )
    des =Column(String, nullable=False )
    channelname =Column(String, nullable=False )

    tags =Column(String, nullable=False )
    publish_date =Column(String, nullable=False )
    publishpolicy=Column(String, nullable=False )
    status = Column(Boolean, nullable=False)
    inserted_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now)    
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now)    


class UploadSetting(Base):
    __tablename__ = 'uploadSetting'
    id = Column(Integer, primary_key=True, autoincrement=True)
    json= Column(String, nullable=False )
    channelname = Column(String, nullable=False )
    firefox_profile_folder = Column(String, nullable=True )
    video_folder = Column(String, nullable=False )
    dailycount =Column(String, nullable=True )
    preferdesprefix =Column(String, nullable=True )
    preferdessuffix =Column(String, nullable=True )
    proxy_option =Column(String, nullable=False )
    start_publish_date =Column(String, nullable=True )
    publishpolicy = Column(String, nullable=False)
    ratio = Column(String, nullable=True)
    music_folder = Column(String, nullable=True)
    channelcookiepath = Column(String, nullable=False)
    prefertags = Column(String, nullable=False)
    inserted_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now)    
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False, default=datetime.now)    

