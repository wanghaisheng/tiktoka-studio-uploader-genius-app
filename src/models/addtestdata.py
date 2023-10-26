import os
from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel,PLATFORM_TYPE
from src.models.account_model import AccountModel,AccountRelationship
from src.models.upload_setting_model import UploadSettingModel,BROWSER_TYPE,WAIT_POLICY_TYPE
from src.models.youtube_video_model import YoutubeVideoModel,VIDEO_SETTINGS
import random

from src.models.task_model import TaskModel,TASK_STATUS
from src.customid import *
if  os.path.exists('debug.sqlite3'):
        print('remove tmp database')
        os.remove('debug.sqlite3')



# https://github.com/coleifer/peewee/issues/221
# 如何切换数据库
class TestData:
    def __init__(self):
        
        self.test_tasks=None
        self.test_setting=None
        self.test_videos=None
        self.test_users=None
    
    def addTestdata(self):
        with db.bind_ctx([ProxyModel,AccountModel,AccountRelationship,PlatformModel,UploadSettingModel,YoutubeVideoModel,TaskModel]):


                print('inital supported platforms')
                PlatformModel.add_platform(platform_data={
                "name":"youtube",
                "type":1,
                "server":'www.youtube.com'

                }

                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"tiktok",
                "type":2,
                "server":None
                }
                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"instagram",
                "type":3,
                "server":None
                }
                )


                PlatformModel.add_platform(platform_data=
                {
                "name":"twitter",
                "type":4,
                "server":None
                }
                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"facebook",
                "type":5,
                "server":None
                }
                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"douyin",
                "type":6,
                "server":None
                }
                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"视频号",
                "type":7,
                "server":None
                }
                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"小红书",
                "type":8,
                "server":None
                }
                )
                PlatformModel.add_platform(platform_data=
                {
                "name":"unknown",
                "type":100,
                "server":None
                }
                )
                print('add test datas')



                test_users=[]
                for i in range(1,20):
                        account=AccountModel.add_account(
                                account_data={
                                "platform":random.choice([0,1,2,3]),
                                "username":"user "+str(i),
                                "password":"pass "+str(i)


                }

                                        

                        )
                        test_users.append(account)

                print('accounts',test_users)
                if test_users[0] is not None:
                        AccountRelationship.add_AccountRelationship_by_id(main_id=test_users[0],otherid=test_users[1])

                # test_setting={
                
                # "timeout":random.choice(range(200,2000)),
                # "is_open_browser":random.choice([True,False]),
                # "is_debug":random.choice([True,False]),
                # "is_record_video":random.choice([True,False]),
                # "platform":random.choice([0,1,2,3]),
                # "browser_type":random.choice(['chromium','webKit','firefox']),
                # "wait_policy":random.choice([0,1,2,3,4]),
                # "account":random.choice(test_users),
                # }

                test_settings=[]
                for i in range(1,20):
                        setting=UploadSettingModel.add_uploadsetting(
                                setting_data={
                
                "timeout":random.choice(range(200,2000)),
                "is_open_browser":random.choice([True,False]),
                "is_debug":random.choice([True,False]),
                "is_record_video":random.choice([True,False]),
                "platform":random.choice([0,1,2,3]),
                "browser_type":random.choice(['chromium','webKit','firefox']),
                "wait_policy":random.choice([0,1,2,3,4])        },account=random.choice(test_users)
                                        

                        )
                        test_settings.append(setting)

                print('test_settings',test_settings)

                fule=["D:\/Download\/audio-visual\/saas\/tiktoka\/tiktoka-studio-uploader-genius\/tests\/videos\/vertical\\1.mp4"]
                images=[
                                "D:/Download/audio-visual/saas/tiktoka/tiktoka-studio-uploader-genius/tests/videos/vertical\\1.png"
                        ]
                # test_video={
                #         "video_local_path": random.choice(fule),
                #         "video_title": 'test title'+str(random.choice(range(1,100))),
                #         "video_description":'test description'+str(random.choice(range(1,100))),
                #         "thumbnail_local_path": random.choice(images),
                #         "publish_policy": random.choice([0,1,2,3,4]),
                #         "tags": random.choice(['t1,t2,t3']),

                #         }

                test_videos=[]
                for i in range(1,50):
                        video=YoutubeVideoModel.add_video(
                                video_data={
                        "video_local_path": random.choice(fule),
                        "video_title": 'test title'+str(random.choice(range(1,100))),
                        "video_description":'test description'+str(random.choice(range(1,100))),
                        "thumbnail_local_path": random.choice(images),
                        "publish_policy": random.choice([0,1,2,3,4]),
                        "tags": random.choice(['t1,t2,t3']),

                        }

                                        

                        )
                        print('add video ok',video.video_title)
                        test_videos.append(video)

                print('test_videos',test_videos)


                # test_task={
                #         "type":random.choice([0,1,2,3]),
                #         "username":'',

                #         "proxy":'',
                #         "status":random.choice([0,1,2]),
                #         "uploaded_at":''

                #         }

                test_tasks=[]

                for i in range(1,120):
                        t=TaskModel.add_task( 
                                task_data={
                        "type":random.choice([0,1,2,3]),
                        "username":'',

                        "proxy":'',
                        "status":random.choice([0,1,2]),

                        },tasksetting=random.choice(test_settings),taskvideo=random.choice(test_videos)
                                        

                        )
                        test_tasks.append(t)
                print('test_tasks',test_tasks)
                self.test_tasks=test_tasks
                self.test_setting=test_settings
                self.test_videos=test_videos
                self.test_users=test_users
                                
                if len(test_tasks)==100:
                        print('test data  inserted done')
                        return test_tasks,test_settings,test_videos,test_users
                else:
                        return None,None,None,None
    def removedata(self):
        with db.bind_ctx([ProxyModel,AccountModel,AccountRelationship,PlatformModel,UploadSettingModel,YoutubeVideoModel,TaskModel]):
            if self.test_users:
                list_of_ids = [r.id for r in self.test_users]
                print(f'{len(list_of_ids)} account to be deleted:{self.test_users}')                        
                query=AccountModel.delete().where(AccountModel.id.in_(list_of_ids))
                query.execute()

            if self.test_setting:
                list_of_ids = [r.id for r in self.test_setting]
                print(f'{len(list_of_ids)} setting to be deleted:{self.test_setting}')                        

                query=UploadSettingModel.delete().where(UploadSettingModel.id.in_(list_of_ids))
                query.execute()
                
            if self.test_videos:
                list_of_ids = [r.id for r in self.test_videos]
                print(f'{len(list_of_ids)} video to be deleted:{self.test_videos}')                        

                query=YoutubeVideoModel.delete().where(YoutubeVideoModel.id.in_(list_of_ids))
                query.execute()

            if self.test_tasks:
                list_of_ids = [r.id for r in self.test_tasks]
                print(f'{len(list_of_ids)} task to be deleted:{self.test_tasks}')                        

                query=TaskModel.delete().where(TaskModel.id.in_(list_of_ids))
                query.execute()

            print('test data is deleted')
    def cleardata(self):
        with db.bind_ctx([ProxyModel,AccountModel,AccountRelationship,PlatformModel,UploadSettingModel,YoutubeVideoModel,TaskModel]):
            nrows = AccountRelationship.delete().execute()
            nrows = AccountModel.delete().execute()
            nrows = ProxyModel.delete().execute()
            nrows = PlatformModel.delete().execute()
            nrows = UploadSettingModel.delete().execute()
            nrows = YoutubeVideoModel.delete().execute()
            nrows = TaskModel.delete().execute()

            print('all data is deleted')