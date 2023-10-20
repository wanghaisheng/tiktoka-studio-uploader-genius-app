from peewee import Model, BlobField, TextField,IntegerField,ForeignKeyField
from src.models import BaseModel,db
import config
import time
from src.customid import CustomID
from src.models.youtube_video_model import YoutubeVideoModel
from src.models.platform_model import PLATFORM_TYPE
from src.models.upload_setting_model import UploadSettingModel
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
    videoid = ForeignKeyField(YoutubeVideoModel, backref='video_id',to_field="id")
    
    settingid = ForeignKeyField(UploadSettingModel, backref='setting_id',to_field="id")

    inserted_at = IntegerField()
    uploaded_at = IntegerField(null=True)
    @classmethod

    def add_task(cls,task_data):


        task = TaskModel(**task_data)
        task.insert_date = int(time.time())  # Update insert_date
        # task.id = CustomID().to_bin()
        task.id = CustomID().to_bin()

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

    def filter_tasks(cls, status=None, type=None,uploaded_at=None, videoid=None,inserted_at=None):
        query = cls.select()
        print('all platfroms are ',list(query))
        if videoid is not None:
            query = query.where(cls.videoid == videoid)

        
        if status is not None:
            query = query.where(cls.task == status)

        if inserted_at is not None:
            query = query.where(cls.server == inserted_at)
        if uploaded_at is not None:
            query = query.where(cls.server == uploaded_at)
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
