from src.models.task_model import *
from tsup.youtube.youtube_upload import YoutubeUpload
from src.log import logger, addKeywordfilter
import asyncio

async def uploadTask(taskid=None, uploadsetting=None, account=None, video=None):
    youtubevideoid = None
    logger.debug(f"start to youtube upload video:\r{video}")

    upload = YoutubeUpload(**uploadsetting)
    logger.debug("initial youtube upload ok")
    youtubevideoid = await upload.upload(**video)

    if youtubevideoid:
        logger.debug("video upload ok:{youtubevideoid}")
        result = TaskModel.update_task(id=taskid, status=TASK_STATUS.SUCCESS)
    else:
        logger.debug("video upload failed")
        result = TaskModel.update_task(id=taskid, status=TASK_STATUS.FAILURE)

    return youtubevideoid

 asyncio.run(await uploadTask(taskid=None, uploadsetting=None, account=None, video=None))