#https://github.com/AsaChiri/DDRecorder/blob/f19722173dfeac975f17a10c27359f5512e9adc2/main.py#L28

import datetime
import json
import logging
import os
import sys
import time
import threading
from multiprocessing import freeze_support
from lastversion import lastversion

import utils
from MainRunner import MainThreadRunner


CURRENT_VERSION = "1.3.3"



class versionThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            latest_version = lastversion.has_update(
                repo="AsaChiri/DDRecorder", current_version=CURRENT_VERSION)
            if latest_version:
                print('DDRecorder 有更新，版本号：{} 请尽快到 https://github.com/AsaChiri/DDRecorder/releases 下载最新版'.format(str(latest_version)))
            else:
                print('DDRecorder 已是最新版本！')
        except:
            print('无法获取 DDRecorder 的版本信息，当前版本号：{}，请到 https://github.com/AsaChiri/DDRecorder/releases 检查最新版本'.format(CURRENT_VERSION))



if __name__ == "__main__":
    freeze_support()
    vt = versionThread()
    vt.start()

    if utils.is_windows():
        utils.add_path("./ffmpeg/bin")