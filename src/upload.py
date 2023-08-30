from .UploadSession import UploadSession
from tsup.youtube.youtube_upload import YoutubeUpload
from tsup.youtube.models.youtube_models import YoutubeVideo,UploadSetting

from datetime import datetime,date,timedelta
import asyncio

# # for cookie issue,
# upload = Upload(
# )

async def startUpload(profilepath="",proxy_option="",watcheveryuploadstep=True,CHANNEL_COOKIES='',username='',password='',recordvideo=True):
    uploadSetting=UploadSetting(
        # use r"" for paths, this will not give formatting errors e.g. "\n"
        root_profile_directory="",
        proxy_option=proxy_option,
        headless=False,
        debug=True,
        use_stealth_js=False,
        # if you want to silent background running, set watcheveryuploadstep false
        CHANNEL_COOKIES=CHANNEL_COOKIES,
        username=username,
        browserType="firefox",
        closewhen100percent="go next after copyright check success",
        password=password,
        recordvideo=True)



    upload = YoutubeUpload(uploadSetting)

    return upload
async def instantpublish(uploadSession:UploadSession,upload:YoutubeUpload):

    await upload.upload(
        video_local_path=uploadSession.videopath,
        video_title=uploadSession.title,
        video_description=uploadSession.des,
        thumbnail_locapath=uploadSession.thumbpath,
        tags=uploadSession.tags,
        wait_policy=False,
        release_date=uploadSession.publish_date,
        publish_policy=1
    )


async def privatedraft(uploadSession:UploadSession,upload:YoutubeUpload):
    await upload.upload(
        video_local_path=uploadSession.videopath,
        video_title=uploadSession.title,
        video_description=uploadSession.des,
        thumbnail_locapath=uploadSession.thumbpath,
        tags=uploadSession.tags,
        wait_policy=False,
        release_date=uploadSession.publish_date,
        publishpolicy=0
    )





async def scheduletopublish_specific_date(uploadSession:UploadSession,upload:YoutubeUpload):
        # mode a:release_offset exist,publishdate exist will take date value as a starting date to schedule videos
        # mode b:release_offset not exist, publishdate exist , schedule to this specific date
        # mode c:release_offset not exist, publishdate not exist,daily count to increment schedule from tomorrow
        # mode d: offset exist, publish date not exist, daily count to increment with specific offset schedule from tomorrow         

    # publish_date = datetime.strftime(publish_date, "%Y-%m-%d %H:%M:%S")
    await upload.upload(
        video_local_path=uploadSession.videopath,
        video_title=uploadSession.title,
        video_description=uploadSession.des,
        thumbnail_locapath=uploadSession.thumbpath,
        tags=uploadSession.tags,
        wait_policy=False,
        release_date=uploadSession.publish_date,
        publishpolicy=2

    )




async def bulk_scheduletopublish_specific_date(videos:list,upload:YoutubeUpload) -> None:
    """ concurrently upload for multiple video files."""
    print('this is a schedule video task',videos)
    for video in videos:
        tasks = []

        tasks.append(
            scheduletopublish_specific_date(uploadSession=video, upload=upload)
        )
        await asyncio.gather(*tasks)


async def bulk_privatedraft(videos:list,upload:YoutubeUpload) -> None:
    """ concurrently upload for multiple video files."""
    print('this is a private video task',videos)

    for video in videos:
        tasks = []

        tasks.append(
            privatedraft(uploadSession=video, upload=upload)
        )
        await asyncio.gather(*tasks)

async def bulk_instantpublish(videos:list,upload:YoutubeUpload) -> None:
    """ concurrently upload for multiple video files."""
    print('this is a public video task',videos)

    for video in videos:
        tasks = []
        tasks.append(
            instantpublish(uploadSession=video, upload=upload)
        )
        await asyncio.gather(*tasks)

