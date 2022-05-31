from .database import dbsession
from .UploadSession import UploadSession, UploadSetting
import json
import sqlalchemy
""" This file will have all function that make any direct query or manipulation in the database. So we can use this funtions as interface of the database. With this we have a single place to edit when some database code should change. 
"""


def Add_New_UploadSession_In_Db(uploadsession) -> None:
    """ This function insert video object in database
    """
    # newUploadSessionDetails = UploadSession(
    #     url=url,
    #     title=title,
    #     thumbnail=thumbnail,
    #     downloadPercent=downloadPercent,
    #     videoquality=str(videoquality),
    #     savefile=savefile,
    # )
    result=dbsession.add(uploadsession)
    dbsession.flush()
    print('add uploadsession result',uploadsession.id)

    # and don't forget to commit your changes
    try:
        dbsession.commit()
    except sqlalchemy.exc.SQLAlchemyError  as e:
        dbsession.rollback()
    print('new upload session',uploadsession.id)
    return uploadsession.id

def Add_New_UploadSetting_In_Db(uploadsetting) -> None:
    """ This function insert video object in database
    """
    newUploadSettingDetails = UploadSetting(
        channelname=uploadsetting["channelname"],
        firefox_profile_folder=uploadsetting["firefox_profile_folder"],
        video_folder=uploadsetting["video_folder"],
        dailycount=uploadsetting["dailycount"],
        preferdesprefix=uploadsetting["preferdesprefix"],
        preferdessuffix=uploadsetting["preferdessuffix"],
        proxy_option=uploadsetting["proxy_option"],
        start_publish_date=uploadsetting["start_publish_date"],
        publishpolicy=uploadsetting["publishpolicy"],
        ratio=uploadsetting["ratio"],
        music_folder=uploadsetting["music_folder"],
        channelcookiepath=uploadsetting["channelcookiepath"],
        prefertags=uploadsetting["prefertags"],
    )
    print(newUploadSettingDetails)
    result=dbsession.add(newUploadSettingDetails)
    dbsession.flush()
    # print('add newUploadSettingDetails result',newUploadSettingDetails.id)

    # and don't forget to commit your changes
    try:
        dbsession.commit()
        print('add new setting to sqlite')
        print('add result',newUploadSettingDetails.id)

    except sqlalchemy.exc.SQLAlchemyError  as e:
        dbsession.rollback()
        # print('rollback')

    return newUploadSettingDetails.id
def Url_In_Database(url) -> bool:
    return (dbsession.query(dbsession.query(UploadSession).filter(UploadSession.domain == url).exists()).scalar())


def Query_UploadSetting_In_db(id) -> list:
    data = dbsession.query(UploadSetting).filter(UploadSetting.id == id).first()
    if data:
        return data
    else:
        return []
def Query_undone_videos_in_channel(uploadsessionid) -> list:
    data = dbsession.query(UploadSession).filter(UploadSession.id == uploadsessionid,UploadSession.status == False).all()
    if data:
        return data
    else:
        return []
def Query_video_status_in_channel(videopath,channelname,settingid) -> list:
    print(videopath,channelname,settingid,'????????????????')
    data = dbsession.query(UploadSession).filter(UploadSession.videopath == videopath,UploadSession.channelname == channelname,UploadSession.uploadSettingid==settingid).first()
    if data:
        status=data.status
        return True,status
    else:
        return False,False
def Query_subdomain_In_db(url) -> list:
    data = dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
    if data:
        subdomains=data.subdomains 
        return json.loads(subdomains)
    else:
        return []

def Update_uploadsetting_In_Db(setting,channelname) -> None:
    print('========',setting,channelname)
    data = dbsession.query(UploadSetting).filter(UploadSetting.channelname == channelname).first()
    print('is data here=========== ')
    settingid=''
    if data:    
        data.json = json.dumps(setting)
        dbsession.merge(data)
    else:
        data=UploadSetting()
        # data.json = json.dumps(setting)
        # settingid=data.id
        data=setting
        dbsession.add(data)    
    # and don't forget to commit your changes
    dbsession.flush()

    try:
        dbsession.commit()
        settingid=data.id

    except sqlalchemy.exc.SQLAlchemyError  as e:
        dbsession.rollback()
    return settingid

def Query_urls_list_In_Db(url) -> list:
    data = dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
    if data:
        urls_list=data.urls_list
        return json.loads(urls_list)
    else:
        return []    
def Update_urls_list_In_Db(urls_list, url) -> None:
    data = dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
    if data:
# There is another less obvious way though. To save as String by json.dumps(my_list) and then while retrieving just do json.loads(my_column). But it will require you to set the data in a key-value format and seems a bit in-efficient compared to the previous solution.

        data.urls_list = json.dumps(urls_list)
        dbsession.merge(data)
    else:
        data=UploadSession()
        data.urls_list = urls_list
        dbsession.merge(data)        

    dbsession.flush()

    # and don't forget to commit your changes
    try:
        dbsession.commit()
    except sqlalchemy.exc.SQLAlchemyError  as e:
        dbsession.rollback()


def Update_kv_In_Db(k,v,url) -> None:
    data = dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
    data.k = v
    dbsession.merge(data)

    dbsession.flush()

    # and don't forget to commit your changes
    try:
        dbsession.commit()
    except sqlalchemy.exc.SQLAlchemyError  as e:
        dbsession.rollback()
