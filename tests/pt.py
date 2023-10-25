
from peewee import Model, CharField, IntegerField,TextField,BooleanField,IntegerField,ForeignKeyField
from peewee import *
import random,os
if os.path.exists('1.sqlite3'):
    os.remove('1.sqlite3')

db_uri='1.sqlite3'

db = SqliteDatabase(db_uri)

class BaseModel(Model):
    class Meta:
        database = db
class AccountModel(BaseModel):
    id = IntegerField(primary_key=True)    
    platform = IntegerField(null=True)
    username = TextField(null=True)
    password = TextField(null=True)  
    
    
class YoutubeVideoModel(BaseModel):
    id = IntegerField(primary_key=True)        
    video_title = TextField(null=True,default=None)

class UploadSettingModel(BaseModel):
    id = IntegerField(primary_key=True)   
    timeout = IntegerField(default=20)
    account = ForeignKeyField(AccountModel, backref='account_id')
    
class TaskModel(BaseModel):
    id = IntegerField(primary_key=True)    
    status = IntegerField()

    video = ForeignKeyField(YoutubeVideoModel, backref='videos')
    setting = ForeignKeyField(UploadSettingModel, backref='settings')

    @classmethod

    def filter_tasks2(cls, status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,video_id=None,username=None):
            query=TaskModel.select()

            query = (TaskModel
                    .select(TaskModel, YoutubeVideoModel, UploadSettingModel, AccountModel)
                    .join(YoutubeVideoModel)  # Join favorite -> user (owner of favorite).
                    .switch(TaskModel)
                    .join(UploadSettingModel)  # Join favorite -> tweet
                    .join(AccountModel))   # Join tweet -> user        

        
            if video_title is not None :
                query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.

                query = (query
                .where(YoutubeVideoModel.video_title.regexp(video_title))

                )
                query=query.switch(TaskModel)  # <-- switch the "query context" back to ticket.



            try:
                result = list(query)
                # for i in result:
                #     for att in dir(i):
                #         print('======show attr=========')
                #         print(att,getattr(i,att))
                
            except cls.DoesNotExist:
                result = None  # Set a default value or perform any other action

            return result

db.create_tables([AccountModel,UploadSettingModel,YoutubeVideoModel,TaskModel])



test_accounts=[]
for i in range(1,5):
    
        account=AccountModel.create(platform=  random.choice([0,1,2,3]),   username='y1',password='p1'
        )
        test_accounts.append(account)



test_settings=[]
for i in range(1,5):
        setting=UploadSettingModel.create(id=i,timeout=5,account=random.choice(test_accounts))

        test_settings.append(setting)


test_videos=[]
for i in range(1,100):
        video=YoutubeVideoModel.create(id=i,video_title='test title'+str(random.choice(range(1,100))))
        test_videos.append(video)





tasks=[]

for i in range(1,100):

        
        t = TaskModel.create(id=i,status=1,video=random.choice(test_videos),setting=random.choice(test_settings))
        tasks.append(t)
# TaskModel.filter_tasks2( status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,video_id=None,username=None)
TaskModel.filter_tasks2( status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title='title86',video_id=None,username=None)