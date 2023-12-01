import os
from src.models import db
from src.models.proxy_model import ProxyModel
from src.models.platform_model import PlatformModel, PLATFORM_TYPE
from src.models.account_model import AccountModel, AccountRelationship
from src.models.upload_setting_model import (
    UploadSettingModel,
    BROWSER_TYPE,
    WAIT_POLICY_TYPE,
)
from src.models.youtube_video_model import *
import random
from src.utils import showinfomsg, find_key

from src.models.task_model import TaskModel, TASK_STATUS
from src.customid import *



platforms = list(dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT).keys())
platforms = platforms * 5

policys = list(dict(WAIT_POLICY.WAIT_POLICY_TEXT).keys())
taskstatus = list(dict(TASK_STATUS.TASK_STATUS_TEXT).keys())
browsers = list(dict(BROWSER_TYPE.BROWSER_TYPE_TEXT).keys())
categories = list(dict(VIDEO_CATEGORIES_OPTIONS.VIDEO_CATEGORIES_OPTIONS_TEXT).keys())


# https://github.com/coleifer/peewee/issues/221
# 如何切换数据库
class TestData:
    def __init__(self):
        self.test_tasks = None
        self.test_setting = None
        self.test_videos = None
        self.test_users = None

    def addTestdata(self):
        with db.bind_ctx(
            [
                ProxyModel,
                AccountModel,
                AccountRelationship,
                PlatformModel,
                UploadSettingModel,
                YoutubeVideoModel,
                TaskModel,
            ]
        ):
            print("inital supported platforms")
            PlatformModel.add_platform(
                platform_data={
                    "name": "youtube",
                    "type": 1,
                    "server": "www.youtube.com",
                }
            )
            PlatformModel.add_platform(
                platform_data={"name": "tiktok", "type": 2, "server": None}
            )
            PlatformModel.add_platform(
                platform_data={"name": "instagram", "type": 3, "server": None}
            )

            PlatformModel.add_platform(
                platform_data={"name": "twitter", "type": 4, "server": None}
            )
            PlatformModel.add_platform(
                platform_data={"name": "facebook", "type": 5, "server": None}
            )
            PlatformModel.add_platform(
                platform_data={"name": "douyin", "type": 6, "server": None}
            )
            PlatformModel.add_platform(
                platform_data={"name": "视频号", "type": 7, "server": None}
            )
            PlatformModel.add_platform(
                platform_data={"name": "小红书", "type": 8, "server": None}
            )
            PlatformModel.add_platform(
                platform_data={"name": "unknown", "type": 100, "server": None}
            )
            print("add test datas")

            test_users = []
            test_users_ids = []

            for i in range(0, 100):
                account = AccountModel.add_account(
                    account_data={
                        "platform": random.choice(platforms),
                        "username": "user " + str(i),
                        "password": "pass " + str(i),
                    }
                )

                test_users.append(account)
                test_users_ids.append(CustomID(custom_id=account.id).to_hex())
            print(f"accounts {len(test_users)}")
            if test_users[0] is not None:
                t = test_users_ids
                for mainid in test_users_ids:
                    n = random.choice([0, 1, 2, 3, 4, 5])
                    print("n", n)

                    print("t", t.remove(mainid))
                    print(f"bind {n} account to {mainid}")
                    otherids = random.sample(t, n)
                    result = AccountModel.update_account(
                        id=CustomID(custom_id=mainid).to_bin(), link_accounts=otherids
                    )
                    print(f"update bind {n} accounts to {mainid}")

                    for otherid in otherids:
                        AccountRelationship.add_AccountRelationship_by_main_id(
                            main_id=CustomID(custom_id=mainid).to_bin(),
                            otherid=CustomID(custom_id=otherid).to_bin(),
                        )

            test_settings = []
            for i in range(0, 20):
                user = random.choice(test_users)
                setting = UploadSettingModel.add_uploadsetting(
                    setting_data={
                        "timeout": random.choice(range(200, 2000)),
                        "is_open_browser": random.choice([True, False]),
                        "is_debug": random.choice([True, False]),
                        "is_record_video": random.choice([True, False]),
                        "platform": user.platform,
                        "browser_type": random.choice(browsers),
                        "wait_policy": random.choice(policys),
                    },
                    account=user,
                )
                test_settings.append(setting)

            print(f"settings {len(test_settings)}")

            fule = [
                "D:\/Download\/audio-visual\/saas\/tiktoka\/tiktoka-studio-uploader-genius\/tests\/videos\/vertical\\1.mp4"
            ]
            images = [
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

            test_videos = []
            for i in range(1, 50):
                video_data = {
                    "video_local_path": random.choice(fule),
                    "video_title": "test title" + str(random.choice(range(1, 100))),
                    "video_description": "test description"
                    + str(random.choice(range(1, 100))),
                    "thumbnail_local_path": random.choice(images),
                    "publish_policy": random.choice(policys),
                    "tags": random.choice(["t1,t2,t3"]),
                    "categories": random.choice(categories),
                }
                print("add video ", video_data)

                video = YoutubeVideoModel.add_video(video_data=video_data)
                print("add video ok", video.video_title)
                test_videos.append(video)

            print(f"videos {len(test_videos)}")

            # test_task={
            #         "type":random.choice([0,1,2,3]),
            #         "username":'',

            #         "proxy":'',
            #         "status":random.choice([0,1,2]),
            #         "uploaded_at":''

            #         }

            test_tasks = []

            for i in range(1, 120):
                setting = random.choice(test_settings)
                user = setting.account
                t = TaskModel.add_task(
                    task_data={
                        "platform": user.platform,
                        "username": "",
                        "proxy": "",
                        "status": random.choice(taskstatus),
                    },
                    tasksetting=setting,
                    taskvideo=random.choice(test_videos),
                )
                test_tasks.append(t)
            print(f"tasks {len(test_tasks)}")
            self.test_tasks = test_tasks
            self.test_setting = test_settings
            self.test_videos = test_videos
            self.test_users = test_users

            if len(test_tasks) == 119:
                print("test data  inserted done")
                # showinfomsg(message="test data  inserted done", DURATION=2000)
                return test_tasks, test_settings, test_videos, test_users
            else:
                return None, None, None, None

    def removedata(self):
        with db.bind_ctx(
            [
                ProxyModel,
                AccountModel,
                AccountRelationship,
                PlatformModel,
                UploadSettingModel,
                YoutubeVideoModel,
                TaskModel,
            ]
        ):
            if self.test_users:
                list_of_ids = [r.id for r in self.test_users]
                print(f"{len(list_of_ids)} account to be deleted:{self.test_users}")
                query = AccountModel.delete().where(AccountModel.id.in_(list_of_ids))
                query.execute()

            if self.test_setting:
                list_of_ids = [r.id for r in self.test_setting]
                print(f"{len(list_of_ids)} setting to be deleted:{self.test_setting}")

                query = UploadSettingModel.delete().where(
                    UploadSettingModel.id.in_(list_of_ids)
                )
                query.execute()

            if self.test_videos:
                list_of_ids = [r.id for r in self.test_videos]
                print(f"{len(list_of_ids)} video to be deleted:{self.test_videos}")

                query = YoutubeVideoModel.delete().where(
                    YoutubeVideoModel.id.in_(list_of_ids)
                )
                query.execute()

            if self.test_tasks:
                list_of_ids = [r.id for r in self.test_tasks]
                print(f"{len(list_of_ids)} task to be deleted:{self.test_tasks}")

                query = TaskModel.delete().where(TaskModel.id.in_(list_of_ids))
                query.execute()

            print("test data is deleted")

    def cleardata(self):
        with db.bind_ctx(
            [
                ProxyModel,
                AccountModel,
                AccountRelationship,
                PlatformModel,
                UploadSettingModel,
                YoutubeVideoModel,
                TaskModel,
            ]
        ):
            nrows = AccountRelationship.delete().execute()
            logger.debug(f"{nrows} AccountRelationship deleted")
            nrows = AccountModel.delete().execute()
            logger.debug(f"{nrows} AccountModel deleted")

            nrows = ProxyModel.delete().execute()
            logger.debug(f"{nrows} ProxyModel deleted")

            nrows = PlatformModel.delete().execute()
            logger.debug(f"{nrows} PlatformModel deleted")

            nrows = UploadSettingModel.delete().execute()

            logger.debug(f"{nrows} UploadSettingModel deleted")
            nrows = YoutubeVideoModel.delete().execute()
            logger.debug(f"{nrows} YoutubeVideoModel deleted")

            nrows = TaskModel.delete().execute()
            logger.debug(f"{nrows} TaskModel deleted")

            print("all data is deleted")
