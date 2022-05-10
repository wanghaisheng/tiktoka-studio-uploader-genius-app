from ytb_up import *
from datetime import datetime,date,timedelta
import asyncio

# # for cookie issue,
# upload = Upload(
# )

def startUpload(profilepath="",proxy_option="",watcheveryuploadstep=True,CHANNEL_COOKIES='',username='',password='',recordvideo=True):

    upload = Upload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            root_profile_directory=profilepath,
            proxy_option=proxy_option,
            watcheveryuploadstep=watcheveryuploadstep,
            # if you want to silent background running, set watcheveryuploadstep false
            CHANNEL_COOKIES=CHANNEL_COOKIES,
            username=username,
            password=password,
            recordvideo=recordvideo
            # for test purpose we need to check the video step by step ,
        )
    return upload
def instantpublish(upload:Upload,video):

    asyncio.run(upload.upload(
        videopath=video.videopath,
        title=video.title,
        description=video.des,
        thumbnail=video.thumbpath,
        tags=video.tags,
        closewhen100percentupload=True,
        publish_date=video.publish_date,
        publishpolicy=1
    ))

def privatedraft(upload:Upload,video):
    asyncio.run(upload.upload(
        videopath=video.videopath,
        title=video.title,
        description=video.des,
        thumbnail=video.thumbpath,
        tags=video.tags,
        closewhen100percentupload=True,
        publish_date=video.publish_date,
        publishpolicy=0
    ))





def scheduletopublish_specific_date(video):
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         

    # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
    asyncio.run(upload.upload(
        videopath=video.videopath,
        title=video.title,
        description=video.des,
        thumbnail=video.thumbpath,
        tags=video.tags,
        closewhen100percentupload=True,
        publish_date=video.publish_date,
        publishpolicy=2

    ))


