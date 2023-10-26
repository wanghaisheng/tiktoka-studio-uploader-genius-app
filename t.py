import os
from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel,PLATFORM_TYPE
from src.models.account_model import AccountModel,AccountRelationship
from src.models.upload_setting_model import UploadSettingModel,BROWSER_TYPE,WAIT_POLICY_TYPE
from src.models.youtube_video_model import YoutubeVideoModel,VIDEO_SETTINGS
import random
from peewee import *

from src.models.task_model import TaskModel,TASK_STATUS
from src.customid import *
if  os.path.exists('debug.sqlite3'):
        print('remove tmp database')
        os.remove('debug.sqlite3')


mode='debug'

DATABASE_URI=f'{mode}.sqlite3'
# DATABASE_URI = f'sqlite:///{mode}.sqlite3'


db = SqliteDatabase(DATABASE_URI)

db.connect()

# t=TaskModel.filter_tasks(status=None, type=None,uploaded_at=None,setting=None,inserted_at=None,video_title=None,video_id=None,username=None,pageno=2,pagecount=100,start=None,end=None,data=None)
platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]