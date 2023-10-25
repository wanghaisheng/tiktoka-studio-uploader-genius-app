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
mode='debug'
# https://github.com/coleifer/peewee/issues/221
# 如何切换数据库

def addTestdata():


        print('inital supported platforms')
        PlatformModel.add_platform(platform_data={
        "name":"youtube",
        "type":0,
        "server":'www.youtube.com'
        
        }

        )
        PlatformModel.add_platform(platform_data=
        {
        "name":"tiktok",
        "type":1,
        "server":None
        }
        )
        PlatformModel.add_platform(platform_data=
        {
        "name":"instagram",
        "type":2,
        "server":None
        }
        )
        PlatformModel.add_platform(platform_data=
        {
        "name":"twitter",
        "type":3,
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

        test_setting={
        
        "timeout":random.choice(range(200,2000)),
        "is_open_browser":random.choice([True,False]),
        "is_debug":random.choice([True,False]),
        "is_record_video":random.choice([True,False]),
        "platform":random.choice([0,1,2,3]),
        "browser_type":random.choice(['chromium','webKit','firefox']),
        "wait_policy":random.choice([0,1,2,3,4]),
        "account":random.choice(test_users),
        }

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
        test_video={
                "video_local_path": random.choice(fule),
                "video_title": 'test title'+str(random.choice(range(1,100))),
                "video_description":'test description'+str(random.choice(range(1,100))),
                "thumbnail_local_path": random.choice(images),
                "publish_policy": random.choice([0,1,2,3,4]),
                "tags": random.choice(['t1,t2,t3']),

                }

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


        test_task={
                "type":random.choice([0,1,2,3]),
                "username":'',

                "proxy":'',
                "status":random.choice([0,1,2]),
                "uploaded_at":''

                }

        test_tasks=[]

        for i in range(1,100):
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
        if len(test_tasks)==100:
                return test_tasks,test_setting,test_videos,test_users
        else:
                return None
def removedata():
     AccountModel.delete()
     UploadSettingModel.delete()
     YoutubeVideoModel.delete()
     TaskModel.delete()