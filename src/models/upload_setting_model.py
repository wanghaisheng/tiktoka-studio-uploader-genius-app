from peewee import ForeignKeyField, TextField, BooleanField, IntegerField,BlobField
from src.models import BaseModel,db
from src.models.platform_model import PLATFORM_TYPE
from src.models.account_model import AccountModel
import time
from src.customid import CustomID

class BROWSER_TYPE:

    CHROMIUM = 0
    FIREFOX = 1
    WEBKIT = 2

    BROWSER_TYPE_TEXT = [
        (CHROMIUM, "chromium"),
        (FIREFOX, "firefox"),
        (WEBKIT, "webKit"),
    ]
class WAIT_POLICY_TYPE:

    uploading = 0
    processing = 1
    check = 2

    WAIT_POLICY_TYPE_TEXT = [
        (uploading, "go next after uploading success"),
        (processing, "go next after processing success"),
        (check, "go next after copyright check success"),
    ]

    
class UploadSettingModel(BaseModel):
    id = BlobField(primary_key=True)    
    timeout = IntegerField(default=200000)
    is_open_browser = BooleanField(default=True)
    is_debug = BooleanField(default=True)
    platform = IntegerField(default=PLATFORM_TYPE.YOUTUBE)
    inserted_at = IntegerField()

    browser_type = IntegerField(default=BROWSER_TYPE.FIREFOX)
    account = ForeignKeyField(AccountModel, backref='account_id')
    is_record_video = BooleanField(default=True)

    wait_policy=IntegerField(default=WAIT_POLICY_TYPE.check)
    @classmethod

    def add_uploadsetting(cls,setting_data,account):

        
        setting = UploadSettingModel(**setting_data)
        
        setting.inserted_at = int(time.time())  # Update insert_date
        setting.account=account
        setting.id = CustomID().to_bin()

        setting.save(force_insert=True) 
        print('setting add ok',setting.id)
        
            # for user in SettingModel.select():
            #     print(user.name)
            # return True
        return setting

    @classmethod

    def get_uploadsetting_by_id(cls,id):
        return cls.get_or_none(cls.id == id)

    @classmethod
    def update_uploadsetting(cls,id, **kwargs):
        try:
            uploadsetting = cls.get(cls.id == id)
            for key, value in kwargs.items():
                setattr(uploadsetting, key, value)
            uploadsetting.save() 
            return uploadsetting
        except cls.DoesNotExist:
            return None
    @classmethod

    def delete_uploadsetting(cls,id):
        try:
            uploadsetting = cls.get(cls.id == id)
            uploadsetting.delete_instance()
            return True
        except cls.DoesNotExist:
            return False
    @classmethod

    def filter_uploadsettings(cls, platform=None, browser_type=None, timeout=None,pageno=None,pagecount=None,start=None,end=None,data=None,ids=None,sortby=None):
        query = cls.select()

        if platform is not None:
            query = query.where(cls.platform == platform)

        if browser_type is not None:
            query = query.where(cls.browser_type == browser_type)

        if timeout is not None:
            query = query.where(cls.timeout == timeout)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_uploadsetting = proxy.uploadsetting  # This will fetch the associated Uploadsetting

        try:
            result = list(query)
            
        except cls.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result
