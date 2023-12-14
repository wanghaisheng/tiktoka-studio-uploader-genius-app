import sys
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from os import environ, path
from cheroot.wsgi import Server

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
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
from flask import Flask, abort, request
from json import JSONEncoder
from typing import Union
from flask import send_from_directory


if sys.platform=='darwin':
    ROOT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

print('fastserver  static files location======',ROOT_DIR,parent_dir)
# app = FastAPI()

# # Allow all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # You can replace this with specific origins if needed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.get("/")
# def howdy():
#     return {"Howdy": "World"}

# app.mount("/static", StaticFiles(directory=os.path.join(parent_dir,"static")), name="static")
# # https://www.starlette.io/staticfiles/
# # app.mount("/static", StaticFiles(directory="static",packages=['src.app']), name="static")

# # app.include_router(router)


class JsonEncoder(JSONEncoder):
    def default(self, obj) -> Union[str, int]:
        if isinstance(obj, bytes):
            try:
                return obj.decode()
            except UnicodeDecodeError:
                return obj.decode("utf-8", "ignore")

        return super(JsonEncoder, self).default(obj)

print(path.join(ROOT_DIR, "static"),'=========')
app = Flask(
    APP_NAME,
    static_folder=path.join(ROOT_DIR, "static"),
    template_folder=path.join(ROOT_DIR, "templates"),
)
app.json_encoder = JsonEncoder
app.config["JSON_SORT_KEYS"] = False
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"timeout": 30}}
app.config["SQLALCHEMY_BINDS"] = {
    "contacts": f"sqlite:///{CONTACTS_CACHE_DB_FILE}",
    "folders": f"sqlite:///{FOLDER_CACHE_DB_FILE}",
}

class ServerWithGetPort(Server):
    def get_port(self):
        if not hasattr(self, "socket"):
            return SERVER_PORT
        return self.socket.getsockname()[1]


server = ServerWithGetPort((SERVER_HOST, SERVER_PORT), app
                           )

def boot(prepare_server: bool = True) -> None:
    if prepare_server:
        server.prepare()

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
