from tsup.youtube.youtube_upload import YoutubeUpload
from datetime import datetime, date, timedelta
import asyncio
from src.log import logger
from src.models.task_model import *


# # for cookie issue,
# upload = Upload(
# )
async def uploadTask(taskid=None, uploadsetting=None, account=None, video=None):
    youtubevideoid = None
    logger.debug(f"start to youtube upload video:\r{video}")

    upload = YoutubeUpload(**uploadsetting)
    logger.debug("initial youtube upload ok")
    isok,youtubevideoid = await upload.upload(**video)
    print(f"upload return:{youtubevideoid}")


    return youtubevideoid
