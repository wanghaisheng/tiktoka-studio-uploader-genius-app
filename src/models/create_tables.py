# coding:utf-8

from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel
from src.models.account_model import AccountModel,AccountRelationship
from src.models.upload_setting_model import UploadSettingModel
from src.models.youtube_video_model import YoutubeVideoModel

from src.models.task_model import TaskModel
from src.customid import *

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
test_users=[{
                "platform":0,
                "username":"y1",
                "password":"p1"
        },
                
        {
                "platform":0,
                "username":"y2",
                "password":"p2"
        },
                
        {
                "platform":1,
                "username":"t1",
                "password":"p1"
        },
                
        {
                "platform":2,
                "username":"i1",
                "password":"p1"
        }                
]
ids=[]
for u in test_users:
    id=AccountModel.add_account(
            account_data=u
                    

    )
    ids.append(id)

print('000000',ids)
if ids[0] is not None:
        AccountRelationship.add_AccountRelationship_by_id(main_id=ids[0],otherid=ids[1])
        # for id in ids:
        #         hexstr=CustomID(custom_id=id).to_hex()
        #         print('bin id',id)
        #         print('bin id after hexstr',hexstr)
        #         hexstrtobin=CustomID(custom_id=hexstr).to_bin()
        #         print('restore',hexstrtobin)