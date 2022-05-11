from ytb_up import *
from datetime import datetime,date,timedelta
import asyncio
from src.upload import *
from src.UploadSession import UploadSession

profilepath =''
CHANNEL_COOKIES = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\cookies\aww.json'

videopath = r'D:\Download\audio-visual\objection_engine\hello.mp4'
tags = ['ba,baaa,bababa']
publish_date = ''
# if you use some kinda of proxy to access youtube, 
proxy_option = "socks5://127.0.0.1:1080"

# for cookie issue,
title = 'bababala'
title=title[:95]
username = "antivte"
password = ""
description = '========================'
driverpath = r'D:\Download\audio-visual\make-reddit-video\autovideo\assets\driver\geckodriver-v0.30.0-win64\geckodriver.exe'
thumbnail = r'D:\Download\audio-visual\make-reddit-video\auddit\assets\ace\ace-attorney_feature.jpg'

upload=YTB_UP_AUTO(profilepath=profilepath,CHANNEL_COOKIES=CHANNEL_COOKIES,
proxy_option=proxy_option,
username='',
password='',
watcheveryuploadstep=True,
recordvideo=True

)
video=UploadSession()
video.channelname=''
video.des='==='
video.title='------'
video.tags=tags
video.publish_date=publish_date

upload.instantpublish(video)