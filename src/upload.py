from tsup.youtube.youtube_upload import YoutubeUpload
from datetime import datetime, date, timedelta
import asyncio
from src.log import logger
from src.models.task_model import *
import traceback

# # for cookie issue,
# upload = Upload(
# )
async def uploadTask(taskid=None, uploadsetting=None, account=None, video=None):
    youtubevideoid = None
    logger.debug(f"===================Start==========================")

    logger.debug(f"start task {taskid} to youtube upload video:\r{video}")
    try:
        upload = YoutubeUpload(**uploadsetting)
        logger.debug(f"initial youtube upload ok:{uploadsetting}")
        isok,youtubevideoid = await upload.upload(**video)
        print(f"upload return:{youtubevideoid} for task {CustomID(custom_id=taskid).to_hex()}")
        logger.debug(f"=====================END========================")
        return youtubevideoid,taskid

    except Exception as e:
        e=traceback.print_exc()
        logger.error(f"upload failed:{e}")
        return None,taskid
    # if youtubevideoid is None:
    #     logger.debug("video upload failed")
    #     print(f"{taskid} video upload failed")
    #     print("update task status to failure")
    #     result = TaskModel.update_task(
    #         id=CustomID(custom_id=taskid).to_bin(),
    #         status=TASK_STATUS.FAILURE,
    #     )
    #     print("end to update task status to failure")

    # else:
    #     logger.debug("video upload ok:{youtubevideoid}")
    #     print(f"{taskid} video upload ok")
    #     print("update task status to success")

    #     result = TaskModel.update_task(
    #         id=CustomID(custom_id=taskid).to_bin(),
    #         status=TASK_STATUS.SUCCESS,
    #     )
    #     print("end to update task status to success")

