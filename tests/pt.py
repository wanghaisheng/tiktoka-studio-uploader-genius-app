
from peewee import Model, CharField, IntegerField,TextField,BooleanField,IntegerField,ForeignKeyField
from peewee import *
import random,os
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
            print('========show without filter========')
            print('======show attr=========')     

            for i in query:
                print(list(query))
                for att in dir(i):
                    if 'setting' in att:
                        print(att,getattr(i,att))           
                        
                    if 'video'  in att:
                        print(att,getattr(i,att))           
            print('======show ids=========')     
                    
            for i in query:
                print(i.id)
                
            print('======show fks=========')     
            for i in query:
                print(i.video,i.setting)
            query = (TaskModel
                    .select(TaskModel, YoutubeVideoModel, UploadSettingModel, AccountModel)
                    .join(YoutubeVideoModel)  # Join favorite -> user (owner of favorite).
                    .switch(TaskModel)
                    .join(UploadSettingModel)  # Join favorite -> tweet
                    .join(AccountModel))   # Join tweet -> user        
            print('========show with join========')

            for fav in query:
                print(fav.video,fav.setting)
        
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


            try:
                result = list(query)
                for i in result:
                    for att in dir(i):
                        print('======show attr=========')
                        print(att,getattr(i,att))
                    print('----------',i.video)
                    print('----------',i.setting)
                
            except cls.DoesNotExist:
                result = None  # Set a default value or perform any other action

            return result

db.create_tables([AccountModel,UploadSettingModel,YoutubeVideoModel,TaskModel])



test_accounts=[]
for i in range(1,5):
    
        account=AccountModel.create(platform=  random.choice([0,1,2,3]),   username='y1',password='p1'
        )
        test_accounts.append(account)
print('111',test_accounts)



test_settings=[]
for i in range(1,5):
        print('idnex',i)
        setting=UploadSettingModel.create(id=i,timeout=5,account=random.choice(test_accounts))

        test_settings.append(setting)

print('222',test_settings)

test_videos=[]
for i in range(1,10):
        video=YoutubeVideoModel(id=i,video_title='test title'+str(random.choice(range(1,100))))
        test_videos.append(video)

print('333',test_videos)




tasks=[]

for i in range(1,5):

        
        t = TaskModel.create(id=i,status=1,video=random.choice(test_videos),setting=random.choice(test_settings))
        tasks.append(t)
print('444',tasks)
TaskModel.filter_tasks2( status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,video_id=None,username=None)
TaskModel.filter_tasks2( status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title='test',video_id=None,username=None)