# coding:utf-8

from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel,PLATFORM_TYPE
from src.models.account_model import AccountModel,AccountRelationship
from src.models.upload_setting_model import UploadSettingModel,BROWSER_TYPE,WAIT_POLICY_TYPE
from src.models.youtube_video_model import YoutubeVideoModel,VIDEO_SETTINGS

from src.models.task_model import TaskModel,TASK_STATUS
from src.customid import *
import random
mode='debug'
db.connect()
# db.create_tables([ProxyModel, PlatformModel], safe=True)
db.create_tables([ProxyModel,AccountModel,AccountRelationship,PlatformModel,UploadSettingModel,YoutubeVideoModel,TaskModel])
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

if mode=='debug':
        print('add test datas')
        test_user={
                        "platform":random.choice([0,1,2,3]),
                        "username":"y1",
                        "password":"p1"


        }


        accounts=[]
        for i in range(1,20):
                account=AccountModel.add_account(
                        account_data=test_user
                                

                )
                accounts.append(account)

        print('000000',accounts)
        if accounts[0] is not None:
                AccountRelationship.add_AccountRelationship_by_id(main_id=accounts[0],otherid=accounts[1])

        test_setting={
        
        "timeout":random.choice(range(200,2000)),
        "is_open_browser":random.choice([True,False]),
        "is_debug":random.choice([True,False]),
        "is_record_video":random.choice([True,False]),
        "platform":random.choice([0,1,2,3]),
        "browser_type":random.choice(['chromium','webKit','firefox']),
        "wait_policy":random.choice([0,1,2,3,4]),
        "account":random.choice(accounts),
        }

        settings=[]
        for i in range(1,20):
                setting=UploadSettingModel.add_uploadsetting(
                        setting_data=test_setting,account=random.choice(accounts)
                                

                )
                settings.append(setting)



        test_video={
                "video_local_path": random.choice(['D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\tests\videos\vertical\1.mp4','D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\tests\videos\horizon\OP.mp4']),
                "video_title": 'test title'+str(random.choice(range(1,100))),
                "video_description":'test description'+str(random.choice(range(1,100))),
                "thumbnail_local_path": random.choice(['D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\tests\videos\vertical\1.png','D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\tests\videos\horizon\OP.png']),
                "publish_policy": random.choice([0,1,2,3,4]),
                "tags": random.choice(['t1,t2,t3']),

                }

        videos=[]
        for i in range(1,50):
                video=YoutubeVideoModel.add_video(
                        video_data=test_video
                                

                )
                videos.append(setting)



        test_task={
                "type":'',
                "username":'',

                "proxy":'',
                "status":random.choice([0,1,2]),
                "uploaded_at":''

                }

        tasks=[]

        for i in range(1,100):
                t=TaskModel.add_task( 
                        task_data=test_task,tasksetting=random.choice(settings),taskvideo=random.choice(videos)
                                

                )
                tasks.append(t)