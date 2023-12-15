import sys
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from os import environ, path
from cheroot.wsgi import Server
from server_thread import ServerThread

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from uploadergenius.log import logger

# from uploadergenius.server.api.account import router
from uploadergenius.settings.constants import (
    APP_NAME,
    ROOT_DIR,
    CLIENT_ROOT,
    CONTACTS_CACHE_DB_FILE,
    DEACTIVATE_SENTRY,
    DEBUG,
    DEBUG_SENTRY,
    FOLDER_CACHE_DB_FILE,
    SERVER_HOST,
    SERVER_PORT,
    SESSION_TOKEN,
)



from uploadergenius.server.models import db
from uploadergenius.server.models.proxy_model import ProxyModel
from uploadergenius.server.models.platform_model import PlatformModel,PLATFORM_TYPE
from uploadergenius.server.models.account_model import AccountModel,AccountRelationship
from uploadergenius.server.models.upload_setting_model import UploadSettingModel,BROWSER_TYPE,WAIT_POLICY_TYPE
from uploadergenius.server.models.youtube_video_model import YoutubeVideoModel,VIDEO_SETTINGS

from uploadergenius.server.models.task_model import TaskModel,TASK_STATUS
from uploadergenius.utils.customid import *

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def howdy():
    return {"Howdy": "World"}

# https://www.starlette.io/staticfiles/
app.mount("/static", StaticFiles(packages=[('uploadergenius.server.app',"static")]), name="static")


print(path.join(ROOT_DIR, "static"),'=========')
print(f'try to start server {SERVER_HOST}:{SERVER_PORT}')

server = ServerThread(app, host=SERVER_HOST, port=SERVER_PORT,debug=True)
# server.is_alive
# import requests

# print(f"http://{server.host}:{server.port}")
# response = requests.get(f"http://{server.host}:{server.port}/")
# response.raise_for_status()

print(f'start server {server.host}:{server.port}')
def boot(prepare_server: bool = True) -> None:


    logger.debug(f"App client root is: {CLIENT_ROOT}")
    logger.debug(f"App session token is: {SESSION_TOKEN}")
    logger.debug(f"App server port: http://{SERVER_HOST}:{SERVER_PORT}")


    from uploadergenius import secrets  # noqa: F401

    # API views



    db.connect()
    # db.create_tables([ProxyModel, PlatformModel], safe=True)
    db.create_tables([ProxyModel,AccountModel,AccountRelationship,PlatformModel,UploadSettingModel,YoutubeVideoModel,TaskModel])



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
