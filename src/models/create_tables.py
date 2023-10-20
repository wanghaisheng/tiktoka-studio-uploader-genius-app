# coding:utf-8

from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel
from src.models.account_model import AccountModel

db.connect()
# db.create_tables([ProxyModel, PlatformModel], safe=True)
db.create_tables([ProxyModel,AccountModel,PlatformModel])
print('inital supported platforms')
PlatformModel.add_platform(PlatformModel,platform_data={
    "name":"youtube",
    "type":0,
    "server":None
    
}

)
PlatformModel.add_platform(PlatformModel,platform_data=
    {
    "name":"tiktok",
    "type":1,
    "server":None
}
)
PlatformModel.add_platform(PlatformModel,platform_data=
    {
    "name":"instagram",
    "type":2,
    "server":None
}
)
PlatformModel.add_platform(PlatformModel,platform_data=
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
for u in test_users:
    AccountModel.add_account(
            AccountModel,account_data=u
                    

    )