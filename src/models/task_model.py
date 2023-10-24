from peewee import TextField, BlobField, BooleanField,IntegerField,ForeignKeyField
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
    prorioty= BooleanField(default=False) 
    video = ForeignKeyField(YoutubeVideoModel, backref='videos')
    # video upload use which proxy
    proxy = TextField(null=True)
    # video upload to
    username = TextField(null=True)

    setting = ForeignKeyField(UploadSettingModel, backref='settings')

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
        return task
        
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
            task.save() 
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

    def filter_tasks(cls, status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,video_id=None,username=None):
        # result=list(TaskModel.select())
        # for i in result:
        #     print(i.__data__)
        #     print(i.inserted_at)
        #     print(i.video_id)
        #     print(i.setting_id)



        query = (TaskModel
                .select(TaskModel, YoutubeVideoModel, UploadSettingModel, AccountModel)
                .join(YoutubeVideoModel)  # Join favorite -> user (owner of favorite).
                .switch(TaskModel)
                .join(UploadSettingModel)  # Join favorite -> tweet
                .join(AccountModel)
                )   # Join tweet -> user        
        print('999999999',query)
        print('999999999',len(list(query)))

        for i in list( query):
            print(i.__data__)
            print(i.inserted_at)
            print(i.video_id)
            print(i.setting_id)
        # 如果存在video 相关的查询参数，先找到对应的video id集合
        if video_title=='':
            video_title=None
        if status=='':
            status=None
        if video_id=='':
            video_id=None
        if username=='':
            username=None
        if video_title is not None :
            print('ding ding video title')
            query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.

            query = (query
            # .join(YoutubeVideoModel,on=(TaskModel.video_id == YoutubeVideoModel.id))
            # .where(YoutubeVideoModel.video_title.regexp(video_title))
            .where(YoutubeVideoModel.video_title==video_title)

            )
            query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.

        print('1')

        if video_id is not None:
            query = query.join(YoutubeVideoModel,on=(TaskModel.video == YoutubeVideoModel.id)).where(YoutubeVideoModel.youtube_video_id == video_id)
            query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.

        print('3')        
        # 如果存在account 相关的查询参数，先找到对应的 setting id集合
        if username is not None:
            query = query.join(UploadSettingModel,on=(TaskModel.setting == UploadSettingModel.id)).join(AccountModel,on=(UploadSettingModel.account == AccountModel.id)).where(AccountModel.username.regexp(username))

            query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.
        print('2')





  
        if status is not None:
            query = query.where(cls.status == status)
        print('5')

        if inserted_at is not None:
            query = query.where(cls.inserted_at == inserted_at)
        if uploaded_at is not None:
            query = query.where(cls.uploaded_at == uploaded_at)
        if type is not None:
            query = query.where(cls.type == type)

        print('8')

        print('9',(query))

        try:
            result = list(query)
            print(len(result))
            # if len(result)==0:
            #     result=list(TaskModel.select())
            # for i in result:
            #     for att in dir(i):
            #         print(f'=======att========{att}')
            #         print(att,getattr(i,att))
                # print('----------',i.video)
                # print('----------',i.setting)
            
        except cls.DoesNotExist:
            result = None  # Set a default value or perform any other action

        return result
