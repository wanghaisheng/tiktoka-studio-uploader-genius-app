from .database import dbsession_test,dbsession_pro
from .UploadSession import UploadSession, UploadSetting
import json
import sqlalchemy
import time

from src.models.proxy_model import ProxyModel
""" This file will have all function that make any direct query or manipulation in the database. So we can use this funtions as interface of the database. With this we have a single place to edit when some database code should change. 
"""

import hashlib
import binascii
from src.customid import  CustomID

class SQLSerialGenerator:
    def __init__(self, val=b''):
        if isinstance(val, str):
            val = binascii.unhexlify(val)
        self.val = val

    def to_bin(self):
        return self.val
# 被数据库所使用的两个ID，短ID与长ID
POST_ID_GENERATOR = SQLSerialGenerator  # 代表SQL自动生成
LONG_ID_GENERATOR = CustomID    
def generate_unique_hash(data):
    if type(data)==dict:
        data=json.dumps(data)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
def append_id(values):
    """
    若有ID生成器，那么向values中添加生成出的值，若生成器为SQL Serial，则什么都不做
    :param values:
    :return:
    """
    if LONG_ID_GENERATOR != SQLSerialGenerator:
        values['id'] = CustomID().to_bin()

class DBM:
    #例如empCount就是类变量
    def __init__(self, mode):
        if mode=='test':
            self.dbsession = dbsession_test
        else:
            self.dbsession = dbsession_pro            

    def Add_New_UploadSession_In_Db(self,uploadsession) -> None:
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
        result=self.dbsession.add(uploadsession)
        self.dbsession.flush()
        print('add uploadsession result',uploadsession.id)

        # and don't forget to commit your changes
        try:
            self.dbsession.commit()
        except sqlalchemy.exc.SQLAlchemyError  as e:
            self.dbsession.rollback()
        print('new upload session',uploadsession.id)
        return uploadsession.id

    def Add_New_UploadSetting_In_Db(self,uploadsetting) -> None:
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
        result=self.dbsession.add(newUploadSettingDetails)
        self.dbsession.flush()
        # print('add newUploadSettingDetails result',newUploadSettingDetails.id)

        # and don't forget to commit your changes
        try:
            self.dbsession.commit()
            print('add new setting to sqlite')
            print('add result',newUploadSettingDetails.id)

        except sqlalchemy.exc.SQLAlchemyError  as e:
            self.dbsession.rollback()
            # print('rollback')

        return newUploadSettingDetails.id
    def Url_In_Database(self,url) -> bool:
        return (self.dbsession.query(self.dbsession.query(UploadSession).filter(UploadSession.domain == url).exists()).scalar())


    def Query_UploadSetting_In_db(self,id) -> list:
        data = self.dbsession.query(UploadSetting).filter(UploadSetting.id == id).first()
        if data:
            return data
        else:
            return []
    def Query_undone_videos_in_channel(self) -> list:
        data = self.dbsession.query(UploadSession).filter(UploadSession.status == False).all()
        if data:
            return data
        else:
            return []
    def Query_video_status_in_channel(self,videopath,channelname,settingid) -> list:
        print(videopath,channelname,settingid,'????????????????')
        data = self.dbsession.query(UploadSession).filter(UploadSession.videopath == videopath,UploadSession.channelname == channelname,UploadSession.uploadSettingid==settingid).first()
        if data:
            status=data.status
            return True,status
        else:
            return False,False
    def Query_subdomain_In_db(self,url) -> list:
        data = self.dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
        if data:
            subdomains=data.subdomains 
            return json.loads(subdomains)
        else:
            return []

    def Update_uploadsetting_In_Db(self,setting,channelname) -> None:
        print('========',setting,channelname)
        data = self.dbsession.query(UploadSetting).filter(UploadSetting.channelname == channelname).first()
        print('is data here=========== ')
        settingid=''
        if data:    
            data.json = json.dumps(setting)
            self.dbsession.merge(data)
        else:
            data=UploadSetting()
            # data.json = json.dumps(setting)
            # settingid=data.id
            data=setting
            self.dbsession.add(data)    
        # and don't forget to commit your changes
        self.dbsession.flush()

        try:
            self.dbsession.commit()
            settingid=data.id

        except sqlalchemy.exc.SQLAlchemyError  as e:
            self.dbsession.rollback()
        return settingid

    def Query_urls_list_In_Db(self,url) -> list:
        data = self.dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
        if data:
            urls_list=data.urls_list
            return json.loads(urls_list)
        else:
            return []    
    def Update_urls_list_In_Db(self,urls_list, url) -> None:
        data = self.dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
        if data:
    # There is another less obvious way though. To save as String by json.dumps(my_list) and then while retrieving just do json.loads(my_column). But it will require you to set the data in a key-value format and seems a bit in-efficient compared to the previous solution.

            data.urls_list = json.dumps(urls_list)
            self.dbsession.merge(data)
        else:
            data=UploadSession()
            data.urls_list = urls_list
            self.dbsession.merge(data)        

        self.dbsession.flush()

        # and don't forget to commit your changes
        try:
            self.dbsession.commit()
        except sqlalchemy.exc.SQLAlchemyError  as e:
            self.dbsession.rollback()


    def Update_kv_In_Db(self,k,v,url) -> None:
        data = self.dbsession.query(UploadSession).filter(UploadSession.domain == url).first()
        data.k = v
        self.dbsession.merge(data)

        self.dbsession.flush()

        # and don't forget to commit your changes
        try:
            self.dbsession.commit()
        except sqlalchemy.exc.SQLAlchemyError  as e:
            self.dbsession.rollback()

    def add_proxy(self,proxy_data)-> None:
        unique_hash = generate_unique_hash(proxy_data)
        existing_proxy = ProxyModel.query.filter(ProxyModel.unique_hash == unique_hash).first()

        if existing_proxy is None:
            proxy = ProxyModel(
                id=CustomID().to_bin(),
                inserted_at=int(time.time()),
                **proxy_data,
                unique_hash=unique_hash
            )
            self.dbsession.add(proxy)
            self.dbsession.commit()
            return True
        else:
            return False

    def get_proxy_by_id(proxy_id):
        return ProxyModel.query.get(proxy_id)

    def update_proxy(self,proxy_id, **kwargs):
        proxy = ProxyModel.query.get(proxy_id)

        if proxy:
            for key, value in kwargs.items():
                setattr(proxy, key, value)
            self.dbsession.commit()
            return proxy
        else:
            return None

    def delete_proxy(self,proxy_id):
        proxy = ProxyModel.query.get(proxy_id)

        if proxy:
            proxy.is_deleted = True
            self.dbsession.commit()
            return True
        else:
            return False

    def bulk_add_proxies(self,proxy_list):
        inserted_proxies = []

        for proxy_data in proxy_list:
            unique_hash = generate_unique_hash(proxy_data)
            existing_proxy = ProxyModel.query.filter(ProxyModel.unique_hash == unique_hash).first()

            if existing_proxy is None:
                proxy = ProxyModel(
                    id=CustomID().to_bin(),
                    inserted_at=int(time.time()),
                    **proxy_data,
                    unique_hash=unique_hash
                )
                self.dbsession.add(proxy)
                inserted_proxies.append(proxy)

        self.dbsession.commit()
        return inserted_proxies

    def filter_proxies(self,country=None, state=None, city=None, tags=None, status=None, network_type=None):
        query = ProxyModel.query

        if country is not None:
            query = query.filter(ProxyModel.country == country)

        if state is not None:
            query = query.filter(ProxyModel.state == state)

        if city is not None:
            query = query.filter(ProxyModel.city == city)

        if tags is not None:
            query = query.filter(ProxyModel.tags == tags)

        if status is not None:
            query = query.filter(ProxyModel.status == status)

        if network_type is not None:
            query = query.filter(ProxyModel.proxy_validate_network_type == network_type)

        return query.all()
