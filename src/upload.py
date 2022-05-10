from ytb_up import Upload
from datetime import datetime,date,timedelta
import asyncio

class YTB_UP_AUTO:
    def __init__(self, profilepath='',CHANNEL_COOKIES='',proxy_option='',username='',password='',watcheveryuploadstep=True,recordvideo=True):
        self.profilepath=profilepath
        self.CHANNEL_COOKIES=CHANNEL_COOKIES
        self.password=password
        self.watcheveryuploadstep=watcheveryuploadstep
        self.username=username
        self.proxy_option=proxy_option
        self.recordvideo=recordvideo

        self.upload = Upload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            root_profile_directory=self.profilepath,
            proxy_option=self.proxy_option,
            watcheveryuploadstep=self.watcheveryuploadstep,
            # if you want to silent background running, set watcheveryuploadstep false
            CHANNEL_COOKIES=self.CHANNEL_COOKIES,
            username=self.username,
            password=self.password,
            recordvideo=True
            # for test purpose we need to check the video step by step ,
        )

    def instantpublish(self,video):

        asyncio.run(self.upload.upload(
            videopath=video.videopath,
            title=video.title,
            description=video.des,
            thumbnail=video.thumbpath,
            tags=video.tags,
            closewhen100percentupload=True,
            publish_date=video.publish_date,
            publishpolicy=1
        ))

    def privatedraft(self,video):
        asyncio.run(self.upload.upload(
            videopath=video.videopath,
            title=video.title,
            description=video.des,
            thumbnail=video.thumbpath,
            tags=video.tags,
            closewhen100percentupload=True,
            publish_date=video.publish_date,
            publishpolicy=0
        ))





    def scheduletopublish_specific_date(self,video):
            # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
            # mode b:release_offset not exist, publishdate exist , schedule to this specific date
            # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
            # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         

        # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
        asyncio.run(self.upload.upload(
            videopath=video.videopath,
            title=video.title,
            description=video.des,
            thumbnail=video.thumbpath,
            tags=video.tags,
            closewhen100percentupload=True,
            publish_date=video.publish_date,
            publishpolicy=2

        ))


