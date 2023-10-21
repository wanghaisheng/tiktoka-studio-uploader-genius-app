from peewee import Model, BlobField, TextField,IntegerField,ForeignKeyField
from src.models import BaseModel,db
import config
import time
from src.customid import CustomID
from src.models.youtube_video_model import YoutubeVideoModel
from src.models.platform_model import PLATFORM_TYPE
from src.models.upload_setting_model import UploadSettingModel
from src.models.account_model import AccountModel
class TASK_STATUS:
    PENDING = 0
    FAILURE = 1
    SUCCESS=2
    PLATFORM_TYPE_TEXT = [
        (PENDING, "pending"),
        (FAILURE, "failure"),
        (SUCCESS, "success"),
    ]


class TaskModel(BaseModel):
    id = BlobField(primary_key=True)    
    type= IntegerField(default=PLATFORM_TYPE.YOUTUBE)
    status = IntegerField(default=TASK_STATUS.PENDING)
    video = ForeignKeyField(YoutubeVideoModel, backref='tasks')
    
    setting = ForeignKeyField(UploadSettingModel, backref='tasks')

    inserted_at = IntegerField()
    uploaded_at = IntegerField(null=True)
    @classmethod

    def add_task(cls,task_data,taskvideo,tasksetting):


        task = TaskModel(**task_data)
        task.inserted_at = int(time.time())  # Update insert_date
        # task.id = CustomID().to_bin()
        task.id = CustomID().to_bin()
        task.video=taskvideo
        task.setting=tasksetting
        task.save(force_insert=True) 
        
        print('task add ok',task.id)
        
            # for user in TaskModel.select():
            #     print(user.name)
            # return True
    @classmethod

    def get_task_by_id(cls, task_id):
        return cls.get_or_none(cls.id == task_id)
    @classmethod

    def update_task(cls, task_id, **kwargs):
        try:
            task = cls.get(cls.id == task_id)
            for key, value in kwargs.items():
                setattr(task, key, value)
            task.save(force_insert=True) 
            return task
        except cls.DoesNotExist:
            return None
    @classmethod

    def delete_task( cls,task_id):
        try:
            task = cls.get(cls.id == task_id)
            task.delete_instance()
            return True
        except cls.DoesNotExist:
            return False
    @classmethod

    def filter_tasks(cls, status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,username=None):
        # 如果存在video 相关的查询参数，先找到对应的video id集合
        if video_title is not None:
            query = query.join(YoutubeVideoModel).where(YoutubeVideoModel.video_title == video_title)

        # if type=='youtube' or type==0:
        #     query = query.join(YoutubeVideoModel).where(YoutubeVideoModel.video_title == video_title)
        # 如果存在account 相关的查询参数，先找到对应的 setting id集合
        if username is not None:
            query = query.join(UploadSettingModel).join(AccountModel).where(AccountModel.username == username)
        
        query = cls.select()
        print('all platfroms are ',list(query))
        # if video_title is not None:
        #     query = query.where(cls.video.v == video)

        
        if setting is not None:
            query = query.where(cls.setting == setting)
        
        if status is not None:
            query = query.where(cls.status == status)

        if inserted_at is not None:
            query = query.where(cls.inserted_at == inserted_at)
        if uploaded_at is not None:
            query = query.where(cls.uploaded_at == uploaded_at)
        if type is not None:
            query = query.where(cls.type == type)
            # # Assuming 'proxy_id' is the ID of the proxy you want to work with

            # proxy = ProxyModel.get(ProxyModel.id == proxy_id)
            # associated_task = proxy.task  # This will fetch the associated Account

        try:
            result = list(query)
            
        except cls.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result
