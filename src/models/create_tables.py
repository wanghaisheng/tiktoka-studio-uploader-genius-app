# coding:utf-8

from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel
from src.models.account_model import AccountModel

db.connect()
# db.create_tables([ProxyModel, PlatformModel], safe=True)
db.create_tables([ProxyModel,AccountModel,PlatformModel])

PlatformModel.add_platform(PlatformModel,platform_data={
    "name":"youtube",
    "type":1,
    "server":None
    
}

)
PlatformModel.add_platform(PlatformModel,platform_data=
    {
    "name":"tiktok",
    "type":2,
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
