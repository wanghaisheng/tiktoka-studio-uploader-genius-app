from tsup.youtube.youtube_upload import YoutubeUpload
from datetime import datetime, date, timedelta
import asyncio
from src.log import logger, addKeywordfilter
from src.models.task_model import *


# # for cookie issue,
# upload = Upload(
# )
async def uploadTask(taskid=None, uploadsetting=None, account=None, video=None):
    youtubevideoid = None
    logger.debug(f"start to youtube upload video:\r{video}")

    upload = YoutubeUpload(**uploadsetting)
    logger.debug("initial youtube upload ok")
    youtubevideoid = await upload.upload(**video)
    print(f"upload return:{youtubevideoid}")
    if youtubevideoid is None:
        logger.debug("video upload failed")
        print(f"{taskid} video upload failed")
    else:
        logger.debug("video upload ok:{youtubevideoid}")
        print(f"{taskid} video upload ok")

    return youtubevideoid
