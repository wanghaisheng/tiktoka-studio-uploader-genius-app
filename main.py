#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import threading
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.editor import concatenate_videoclips,concatenate_audioclips,TextClip,CompositeVideoClip
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex
import moviepy.audio.fx.all  as afx
import moviepy.video.fx.all as vfx
# here put the import lib
from jsonschema import validate
from jsonschema import ValidationError
import json
import jsons
import tkinter as tk
import webbrowser
from tkinter import OptionMenu, filedialog,ttk
import pandas as pd
import os,queue
import base64
import subprocess
import sys
import random
import os
import time
# import multiprocessing.dummy as mp
import concurrent
from glob import glob
from src.dbmanipulation import *
from src.UploadSession import *
from PIL import Image,ImageTk
import multiprocessing as mp
from src.upload import *
from src.ai_detector import AiThumbnailGenerator
from src.tooltip import Tooltip
from datetime import datetime,date,timedelta
import asyncio
import requests
import re
import calendar
from tsup.utils.webdriver.setupPL import checkRequirments
import logging
from src.database import createEngine,pd2table,query2df,rmEngine
from src.gpt_thumbnail import draw_text_on_image,validateSeting
try:
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk # Python 2.x
    import ScrolledText
import pyperclip as clip
import platform
from easy_i18n.t import Ai18n
from pystray import MenuItem as item
import pystray

from UltraDict import UltraDict
if platform.system()=='Windows':
    
    ultra = UltraDict(shared_lock=True,recurse=True)
    settings = UltraDict(shared_lock=True,recurse=True)
    tmp = UltraDict(shared_lock=True,recurse=True)
else:
    ultra = UltraDict(recurse=True)
    settings = UltraDict(recurse=True)
    tmp = UltraDict(shared_lock=True,recurse=True)
tmp['uploadaddaccounts']={}
settings['zh']={
		"title": "TiktokaStudio 视频批量上传助手测试版",
		"select_musics_folder": "选择背景音樂文件夹",
		"select_videos_folder": "选择视频文件夹",
		"setups": "安装配置",
		"select_cookie_file": "选择cookie json",
		"select_profile_folder": "选择profile文件夹",
		"settings": "配置",
		"createuploadsession": "创建上传任务",
		"autothumb": "自动生成缩略图",
		"testupload": "开始上传前測試",
		"videosMenu": "视频管理",
		"docView": "帮助",		
		"installView": "安装配置",
		"accountView": "账号",
		"proxyView": "代理",
		"thumbView": "缩略图",
		"logView": "日志",

		"videosView": "视频",
		"metaView": "元数据",
		"uploadView": "上传",
		"tagsView": "标签",
		"desView": "视频描述",
		"scheduleView": "发布日期",

		"loglevel": "loglevel",

		"upload": "开始上传",
		"batchchangebgmusic": "批量替换背景音乐",
		"is_open_browser": "静默模式",
		"is_record_video": "录像模式",
		"debug": "开启日志",
		"start-loading-setting": "开始读取最近保存的配置文件",
		"loading-default-setting": "读取配置文件失败 加载默认模版",

		"hiddenwatermark": "添加隐形水印",
		
		"downVideoMetas":"下载视频元信息json模板",
		"toolkits":"工具箱",
		"mode1":"模式1",
		"mode2":"模式2",
		"mode3":"模式3",
		
		"save_setting": "保存配置",
		"testsettingok": "测试配置",
		"testnetwork": "测试网络",
		"version":"版本",
		"version_str":"V0.1.16\\n1.source code for this GUI:https://github.com/wanghaisheng/tiktoka-studio-uploader-app \\n2.core lib for this GUI: https://github.com/wanghaisheng/tiktoka-studio-uploader",

		"docs":"说明文档",
		"docs_str":"安装配置篇\\n1.安装\\n2.配置\\n导入默认配置后可以通过测试网络、测试安装、测试配置文件来知晓具体情况\\n1.从文件夹生成视频元数据规则\\n r1:尝试使用ffmpeg读取视频元数据,从其中获取视频标题、描述、制作日期、制作地点、字幕文件等信息。\\n r2:r1未命中则读取文件名称作为视频名称,如果视频名称超过20个字符,则将视频名称作为视频描述\\n r3:如果存在字幕文件,尝试从字幕总结出视频描述,如果不存在多语种字幕，尝试使用外部工具翻译多语种字幕\\n r4:如果存在同名的图片文件,则将其作为缩略图，如果没有则使用自动提取关键帧工具生成缩略图底图供后续封面图生成使用\\n r5:如果设置了每日发布的数量，则自动按照数量从次日起安排视频定时公开的日期\\n如果没有设置每日发布的数量，则根据发布策略的值来决定视频是立即公开还是私有发布。1.如果是多个账户,你需要为每个账号准备一个cookie,然后每个账户配置一个单独的配置文件\\n2.安装浏览器插件Cookie-Editor,登录youtube,导出cookie3.免版权的音乐可以在\\nhttps://icons8.com/music/\\n=====================\\n1.首次使用请选择对应的配置模板,比如默认private、public和schedule,文件路径为软件安装路径下的assets/config/setting-template.json,请按照自己的情况修改,修改完成后点击保存\\n文件和文件夹 你可以通过菜单里的浏览器配置、视频素材来点选,你也可以自行在文本框中填写\\n首选标签：这一批上传的视频我们想设置一些通用的标签,在这里设置,其他的标签请放在视频文件名中即可\\n视频描述前缀:一般而言频道的视频描述都会有个模板,类似作文里总分总结构\\n视频描述后缀:一般是一些免责声明之类\\n发布策略:0表示上传为私有,1表示上传后立马公开2表示定时公开 当你选了2,可配合每日发布数量来自动设置对应视频公开的日期,起始日期默认为上传日期+1\\n频道名称:只是用来保存配置文件\\ncookie json:请使用浏览器插件导出并保存\\n2.第二步需要检查素材,因为目前上传逻辑中只有支持视频和缩略图名字一样才能进行上传\\n背景音乐批量替换:请设置好免费音乐所在文件夹,可先对1个视频处理,调节背景音乐音量为最佳效果\\n 3.点击上传即可",
		"contact":"联系我",
		"contact_str":"1.发送邮件到admin@tiktokastudio.com\\n",

		"contact_str_group":"2.扫码加入讨论组参与讨论",
		"contact_str_personal":"3.特殊情况,299元红包可添加私人微信",
		"chooseLang": "语言:",
		"genVideoMetas":"从视频文件夹生成视频元信息",
		"helpcenter":"帮助中心",
		"importVideoMetas":"导入视频元信息json文件",

		"validateVideoMetas":"验证视频元信息json文件",
		"editVideoMetas":"纯手动编辑视频元信息json文件",
		"username": "账号名称",
		"password": "账号密码",

		"testinstall": "测试安装",
		"load_setting_file": "加载配置文件",
		"create_setting_file": "新建配置文件",

		"cookiejson": "cookie json 文件",
		"proxySetting": "代理配置",
		"profileFolder": "profile文件夹",
		"videoFolder": "视频文件夹",
		"channelName": "频道名称",
		"offsetDays": "起始发布日期-当日(天数)",
		"dailyVideoLimit": "每日公开视频数量",
		"publishPolicy": "发布策略",
		"bgMucisVolume": "背景音乐音量",
		"descriptionSuffix": "视频描述后缀",
		"descriptionPrefix": "视频描述前缀",
		"preferTags": "首选标签",
		"bgVideoFolder": "背景音乐文件夹",
		"chooseCookie": "请选择该频道对应cookie文件",
		"chooseChannelSetting": "请选择该频道配置文件"
	}
settings['en']={
		"title": "TiktokaStudio Video Bulk Upload GUI Demo",
		"select_musics_folder''": "choose music folder",
		"select_videos_folder": "choose video folder",
		"setups": "setups",
		"select_cookie_file": "choose cookie json",
		"select_profile_folder": "choose profile folder",
		"settings": "settings",
		"createuploadsession": "create uploadsession",
		"autothumb": "auto thumbnail",
		"testupload": "test video upload ",
		"videosMenu": "视频管理",
		"docView": "Docs",		
		"installView": "Setup",
		"accountView": "Accounts",
		"proxyView": "Proxies",
		"thumbView": "Thumbnails",
		"videosView": "Videos",
		"metaView": "Metas",
		"uploadView": "Upload",
		"upload": "start upload",
		"batchchangebgmusic": "batch replace audio",
		"is_open_browser": "silent mode",
		"is_record_video": "recording",
		"genVideoMetas":"gen  video metas",
		"helpcenter":"helpcenter",
		"importVideoMetas":"import video metajson file",
		"editVideoMetas":"edit video metajson file",
		"username": "username",
		"password": "password",
		"save_setting": "save config",
		"chooseLang": "Lang",
		"contact":"contact",
		"contact_str":"1.Email send to admin@tiktokastudio.com\\n",
		"debug": "debug",
		"loglevel": "loglevel",
		"validateVideoMetas":"validate meta json",
		"logView": "Logs",
		"tagsView": "tags",
		"desView": "des",
		"scheduleView": "schedule",

		"start-loading-setting": "start loading latest used setting file",
		"loading-default-setting": "loading failed,use default setting template",
		"contact_str_group":"2.Join discussion group",
		"contact_str_personal":"3.Pay $99 to add personal wechat",
		"version":"version",
		"version_str":"V0.1.16\\n1.source code for this GUI:https://github.com/wanghaisheng/tiktoka-studio-uploader-app \\n2.core lib for this GUI: https://github.com/wanghaisheng/tiktoka-studio-uploader",
		"hiddenwatermark": "add hidden watermark",
		"docs_str":"安装配置篇\\n1.安装\\n2.配置\\n导入默认配置后可以通过测试网络、测试安装、测试配置文件来知晓具体情况\\n1.从文件夹生成视频元数据规则\\n r1:尝试使用ffmpeg读取视频元数据,从其中获取视频标题、描述、制作日期、制作地点、字幕文件等信息。\\n r2:r1未命中则读取文件名称作为视频名称,如果视频名称超过20个字符,则将视频名称作为视频描述\\n r3:如果存在字幕文件,尝试从字幕总结出视频描述,如果不存在多语种字幕，尝试使用外部工具翻译多语种字幕\\n r4:如果存在同名的图片文件,则将其作为缩略图，如果没有则使用自动提取关键帧工具生成缩略图底图供后续封面图生成使用\\n r5:如果设置了每日发布的数量，则自动按照数量从次日起安排视频定时公开的日期\\n如果没有设置每日发布的数量，则根据发布策略的值来决定视频是立即公开还是私有发布。1.如果是多个账户,你需要为每个账号准备一个cookie,然后每个账户配置一个单独的配置文件\\n2.安装浏览器插件Cookie-Editor,登录youtube,导出cookie3.免版权的音乐可以在\\nhttps://icons8.com/music/\\n=====================\\n1.首次使用请选择对应的配置模板,比如默认private、public和schedule,文件路径为软件安装路径下的assets/config/setting-template.json,请按照自己的情况修改,修改完成后点击保存\\n文件和文件夹 你可以通过菜单里的浏览器配置、视频素材来点选,你也可以自行在文本框中填写\\n首选标签：这一批上传的视频我们想设置一些通用的标签,在这里设置,其他的标签请放在视频文件名中即可\\n视频描述前缀:一般而言频道的视频描述都会有个模板,类似作文里总分总结构\\n视频描述后缀:一般是一些免责声明之类\\n发布策略:0表示上传为私有,1表示上传后立马公开2表示定时公开 当你选了2,可配合每日发布数量来自动设置对应视频公开的日期,起始日期默认为上传日期+1\\n频道名称:只是用来保存配置文件\\ncookie json:请使用浏览器插件导出并保存\\n2.第二步需要检查素材,因为目前上传逻辑中只有支持视频和缩略图名字一样才能进行上传\\n背景音乐批量替换:请设置好免费音乐所在文件夹,可先对1个视频处理,调节背景音乐音量为最佳效果\\n 3.点击上传即可",
		"testsettingok": "test config",
		"testinstall": "test install",
		"testnetwork": "test network",
		"load_setting_file": "load setting",
		"docs": "Read First",
		"cookiejson": "cookie json",
		"proxySetting": "proxy",
		"profileFolder": "profile folder",
		"videoFolder": "video folder",
		"create_setting_file": "new setting file",
		"downVideoMetas":"download metajson template",
		"toolkits":"toolkits",
		"mode1":"mode 1",
		"mode2":"mode 2",
		"mode3":"mode 3",
		"channelName": "channel name",
		"offsetDays": "days offset",
		"dailyVideoLimit": "daily publish count",
		"publishPolicy": "publish policy",
		"bgMucisVolume": "music volumn",
		"descriptionSuffix": "preferred des suffix",
		"descriptionPrefix": "preferred des prefix",
		"preferTags": "preferred tags",
		"bgVideoFolder": "free music folder",
		"chooseCookie": "select specific cookie file",
		"chooseChannelSetting": "select channel setting file"
	}


config = {
    "load_path": "./locales", # 指定在 /locales 下找对应的翻译 json文件
    "default_module": "global", # 指定默认的全局模块，你可以为比如用户模块，订单模块单独设置翻译，如果不指定 module 则会去全局模块查找。
}
videoassetsfilename='videos-assets.json'
a_i18n = Ai18n(locales=["en", "zh"], config=config)

i18labels= a_i18n.translate
window_size='1024x720'
height=720
width=1024
supported_video_exts=['.flv', '.mp4', '.avi']
supported_thumb_exts=['.jpeg', '.png', '.jpg','webp']
supported_des_exts=['.des', '.txt']
supported_meta_exts=['.json', '.xls','.xlsx','.csv']      

# Logging configuration
logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')        

# Add the handler to logger

logger = logging.getLogger()         
checkvideopaircounts=0
checkvideocounts=0
test_engine=createEngine('test')
prod_engine=createEngine('prod')
window=None
# after import or define a_i18n and t
# add translation dictionary manually.
# dbname = "reddit_popular"
# Open the database and make sure there is a table with appopriate indices
availableScheduleTimes = [
"0:00",
"0:15",
"0:30",
"0:45",
"1:00",
"1:15",
"1:30",
"1:45",
"2:00",
"2:15",
"2:30",
"2:45",
"3:00",
"3:15",
"3:30",
"3:45",
"4:00",
"4:15",
"4:30",
"4:45",
"5:00",
"5:15",
"5:30",
"5:45",
"6:00",
"6:15",
"6:30",
"6:45",
"7:00",
"7:15",
"7:30",
"7:45",
"8:00",
"8:15",
"8:30",
"8:45",
"9:00",
"9:15",
"9:30",
"9:45",
"10:00",
"10:15",
"10:30",
"10:45",
"11:00",
"11:15",
"11:30",
"11:45",
"12:00",
"12:15",
"12:30",
"12:45",
"13:00",
"13:15",
"13:30",
"13:45",
"14:00",
"14:15",
"14:30",
"14:45",
"15:00",
"15:15",
"15:30",
"15:45",
"16:00",
"16:15",
"16:30",
"16:45",
"17:00",
"17:15",
"17:30",
"17:45",
"18:00",
"18:15",
"18:30",
"18:45",
"19:00",
"19:15",
"19:30",
"19:45",
"20:00",
"20:15",
"20:30",
"20:45",
"21:00",
"21:15",
"21:30",
"21:45",
"22:00",
"22:15",
"22:30",
"22:45",
"23:00",
"23:15",
"23:30",
"23:45"] 


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)
        


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame,root,row=0,column=0):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText.ScrolledText(frame, state='disabled')
        
        self.scrolled_text.bind_all("<Control-c>",self.copy)



        # Bind right-click event to show context menu
        # https://stackoverflow.com/questions/30668425/tkinter-right-click-popup-unresponsive-on-osx
        MAC_OS = False
        if sys.platform == 'darwin':
            MAC_OS = True
        if MAC_OS:
            self.scrolled_text.bind('<Button-2>', self.show_context_menu)
        else:
            self.scrolled_text.bind('<Button-3>', self.show_context_menu)        

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Clear All Text", command=self.clear_text)
            
        self.scrolled_text.grid(row=row, column=column, columnspan=2,sticky='nswe')
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)
    def clear_text(self):

        self.scrolled_text.configure(state='normal')  # Enable text widget
        self.scrolled_text.delete(1.0, tk.END)  # Delete all text
        self.scrolled_text.configure(state='disabled')  # Disable text widget again
    # Create a right-click context menu
    def show_context_menu(self,event):
        self.context_menu.post(event.x_root, event.y_root)


    def copy(self,event):
        try:
            string = event.widget.selection_get()
            clip.copy(string)
        except:
            pass
    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)

class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06

    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text
        self.max_length = 250


    def emit(self, record):
        msg = self.format(record)
        if len(msg) > self.max_length:
            lines = []
            while len(msg) > self.max_length:
                lines.append(msg[:self.max_length])
                msg = msg[self.max_length:]
            lines.append(msg)
            msg= '\n'.join(lines)

        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)

def url_ok(url,proxy_option=''):


    try:
        if not proxy_option=='':
            

            # proxies = {
            #    'http': 'http://proxy.example.com:8080',
            #    'https': 'http://secureproxy.example.com:8090',
            # }
            if 'http:' in proxy_option:

                proxies = {
                'http': proxy_option
                }                
            elif 'https:' in proxy_option:

                proxies = {
                'https': proxy_option,
                }                
            elif 'socks' in proxy_option:
                proxies = {
                'http': proxy_option,
                'https': proxy_option,
                }
            else:
                proxy_option='http://'
                proxies = {
                'http': proxy_option,
                'https': proxy_option,
                }            
            print('use proxy',proxy_option)
            response = requests.head(url,proxies=proxies)
            print('google access is ok use {proxy_option}')
        else:
            response = requests.head(url)
            print('we cant  access google without proxy')

    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        print('we cant  access google')
        
        return False
    else:
        print('status code',response.status_code)
        if response.status_code == 200:
            print('we cant  access google')
            return True
        else:
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False


def isfilenamevalid(filename):
    # print(imagename)
    invalid = '…,<>:."/\|?*!$\'\"#'

    for char in invalid:

        filename = filename.replace(char, '')
    if len(filename) > 260:
        filename = filename[:259]
    return filename


def fix_size(old_image_path, new_image_path, canvas_width=1080, canvas_height=720):
    """Edited from https://stackoverflow.com/questions/44231209/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black"""
    im = Image.open(old_image_path)
    x, y = im.size

    ratio = x / y
    desired_ratio = canvas_width / canvas_height

    w = max(canvas_width, x)
    h = int(w / desired_ratio)
    if h < y:
        h = y
        w = int(h * desired_ratio)

    mode = im.mode
    print(mode)
    if len(mode) == 1:  # L, 1
        new_background = (0)
    if len(mode) == 3:  # RGB
        new_background = (0, 0, 0)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (0, 0, 0, 0)
    new_im = Image.new(mode, (w, h), new_background)
    new_im.paste(im, ((w - x) // 2, (h - y) // 2))
    img = new_im.resize((canvas_width, canvas_height))
    if mode == 'RGBA':
        img = img.convert('RGB')
    img.save(new_image_path)


def load_setting():

    global setting

    if os.path.exists('latest-used-setting.txt') :
        try:
            fp = open('latest-used-setting.txt', 'r', encoding='utf-8')
            settingfile=fp.readlines()[0]

            fp = open(settingfile, 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
        except:
            print(i18labels("loading-default-setting", locale='en', module="g"))
            fp = open("./assets/config/demo.json", 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
    else:
        print(i18labels("loading-default-setting", locale='en', module="g"))
        fp = open("./assets/config/demo.json", 'r', encoding='utf-8')
        setting_json = fp.read()
        fp.close()        
    setting = json.loads(setting_json)
    return setting



def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
# 加载剧本

settingid=0
# 保存配置


def select_profile_folder():
    global firefox_profile_folder_path
    try:
        firefox_profile_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')

        if os.path.exists(firefox_profile_folder_path):
            firefox_profile_folder_path = str(firefox_profile_folder_path)
            print("You chose %s" % firefox_profile_folder_path)
            firefox_profile_folder.set(firefox_profile_folder_path)
        else:
            print('please choose a valid profile folder')

            # setting['firefox_profile_folder'] = firefox_profile_folder
    except:
        print('please choose a valid profile folder')

def select_tabview_video_folder(folder_variable,cache_var):
    global thumbView_video_folder_path
    try:
        thumbView_video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(thumbView_video_folder_path):
            print("You chose %s" % thumbView_video_folder_path)
            folder_variable.set(thumbView_video_folder_path)
            ultra[cache_var]=thumbView_video_folder_path         
            print("You chose %s" % folder_variable.get())

        else:
            print('please choose a valid video folder')

    except:
        print('please choose a valid video folder')

def openLocal(folder):
    try:
        
        webbrowser.open('file:///' + folder)
    except:
        logger.error(f'please choose a valid video folder:\n{folder}')



def select_videosView_video_folder():
    global videosView_video_folder_path
    try:
        videosView_video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(videosView_video_folder_path):
            print("You chose %s" % videosView_video_folder_path)
            videosView_video_folder.set(videosView_video_folder_path)
            print("You chose %s" % videosView_video_folder.get())

        else:
            print('please choose a valid video folder')

    except:
        print('please choose a valid video folder')

def select_videos_folder():
    global video_folder_path
    try:
        video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(video_folder_path):
            print("You chose %s" % video_folder_path)
            video_folder.set(video_folder_path)
            setting['video_folder'] = video_folder_path
        else:
            print('please choose a valid video folder')

    except:
        print('please choose a valid video folder')
def select_folder(dict,value):
    global music_folder_path
    try:
        music_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')


        if os.path.exists(music_folder_path):
            print("You chose %s" % music_folder_path)
            dict = music_folder_path
            value.set(music_folder_path)
        else:
            print('please choose a valid music folder')
    except:
        print('please choose a valid music folder')

docsopen=False
def docs(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    print('open docmentations')
    label_helptext_setting = tk.Label(newWindow, text = i18labels("docs_str", locale='en', module="g").replace('\\n','\n'),justify='left', wraplength=450)
    label_helptext_setting.pack()
    
def version(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # print(type(i18labels("version_str", locale='en', module="g")))
    # print(str(i18labels("version_str", locale='en', module="g")))
    # if '\\n' in i18labels("version_str", locale='en', module="g"):
    print('111111111111')
    # print(type("First line\n and this is the second"))
    # print("First line\n and this is the second")
    # if '\n' in "First line\n and this is the second":
    #     print('22222222222')    
    label_helptext_setting = tk.Label(newWindow, 
                                      text = i18labels("version_str", locale='en', module="g").replace('\\n','\n'),
                                    #   text = "First line\n and this is the second",
                                      justify='left')
    label_helptext_setting.pack()


def contact(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # due to \n in json string should in \\n, so read it from json  need to convert to original 
    label_helptext_setting = tk.Label(newWindow, text = i18labels("contact_str", locale=lang, module="g").replace('\\n','\n'),anchor='e',justify='left', wraplength=450)
    label_helptext_setting.pack()

    group = tk.Label(newWindow, text =i18labels("contact_str_group", locale=lang, module="g"),anchor='e',justify='left')
    group.pack()
    path_group = './assets/feishu-chatgroup.jpg'
    img_group = Image.open(path_group)
    photo_group = ImageTk.PhotoImage(img_group)
    
    label_group = tk.Label(newWindow,image=photo_group,height=400, width=256)
    label_group.pack()

    personal = tk.Label(newWindow, text = i18labels("contact_str_personal", locale=lang, module="g").replace('\\n','\n'),anchor='e',justify='left')
    personal.pack()
    path_personal = './assets/wechat.jpg'
    img_personal = Image.open(path_personal)
    photo_personal = ImageTk.PhotoImage(img_personal)#在root实例化创建，否则会报错
    
    label_personal = tk.Label(newWindow,image=photo_personal,height=400, width=256)
    label_personal.pack()

    newWindow.mainloop()

def get_record_video():
    is_record_video=record_video.get()
def get_is_open_browser():
    is_open_browser=open_browser.get()

def install():
    # subprocess.check_call([sys.executable, "-m", "playwright ", "install"])
    subprocess.check_call(["playwright ", "install"])

def testInstallRequirements():
    print('check install requirments')
    checkRequirments()
def testNetwork():
    print('start to test network and proxy setting')
    if proxy_option.get() is None:
        url_ok('www.youtube.com')
        print('you can access google without proxy setting')
    else:
        # print('please check your proxy setting\nsocks5://127.0.0.1:1080\nhttp://proxy.example.com:8080\n222.165.235.2:80\n')
    
        print('your proxy setting is ',proxy_option.get())
        if  proxy_option.get()=='':

            print('you should provide valid your proxy setting,format as follows \nsocks5://127.0.0.1:1080\nhttp://proxy.example.com:8080\n222.165.235.2:80\n')
        else:
            if url_ok('www.youtube.com',proxy_option=proxy_option.get()):        
                print('your  proxy is running ok')
            else:
                print('you should provide valid your proxy setting,format as follows \nsocks5://127.0.0.1:1080\nhttp://proxy.example.com:8080\n222.165.235.2:80\n')
    print('netwrork and proxy test is done')
def ValidateSetting():
    print('start to validate your upload settings')
    time.sleep(4)
    print('end to validate your upload settings')






def auto_gen_cookie_file():
    
    print('call tsup gen cookie api')


def select_thumb_template_file(folder):
    global thumbnail_template_file_path
    try:
        thumbnail_template_file_path = filedialog.askopenfilenames(title="请选择 template文件", filetypes=[
            ("Json", "*.json"), ("All Files", "*")])[0]

        thumbnail_template_file.set(thumbnail_template_file_path)
        # ultra[folder]['thumb_gen_template']=thumbnail_template_file_path
    except:
        print('please select a valid template json file')




def select_file(title,cached,variable,limited='all',parent=None):
    file_path=''
    try:
        if limited=='json':
            file_path = filedialog.askopenfilenames(title=title, filetypes=[
                ("Json", "*.json"), ("All Files", "*")],parent=parent)[0]
        elif limited=='images':
            file_path = filedialog.askopenfilenames(title=title, filetypes=[
                ("JPEG", "*.jpg"),("PNG", "*.png"),("JPG", "*.jpg"),("WebP", "*.webp"), ("All Files", "*")],parent=parent)[0]
        else:
            file_path = filedialog.askopenfilenames(title=title, filetypes=[ ("All Files", "*")],parent=parent)[0]
        variable.set(file_path)
        if cached is not None:
            cached=file_path
    except:
        print('please select a valid  file')


def select_cookie_file(channel_cookie_user):

    global channel_cookie_path
    try:
        channel_cookie_path = filedialog.askopenfilenames(title="请选择该频道对应cookie文件", filetypes=[
            ("Json", "*.json"), ("All Files", "*")])[0]

        channel_cookie_user.set(channel_cookie_path)
        setting['channelcookiepath'] = channel_cookie_path
    except:
        print('please select a valid cookie json file')


# 清理残留文件

def threadusing_free_musichelper(numbers):

    using_free_music(numbers[0],numbers[1])

def using_free_music(setting,inputmp4):

    if os.path.exists(inputmp4):

        print('video exists', inputmp4)
    else:
        print('video not found')
    try:
        music_folder =setting['music_folder']
    except:
        music_folder='assets/freemusic'

    else:

        music_folder = setting['music_folder']
    if os.path.exists(music_folder):
        print('there are free music folder',music_folder)
    else:
        print('choose valid free music folder',music_folder)

    freemusic = []

    for ext in ('*.mp3', '*.wav','*.wma','*.ogg','*.aac'):
        freemusic.extend(glob(os.path.join(music_folder, ext)))
        
    if len(freemusic) > 0:    
        soundeffect = random.choice(freemusic)
        print('randomly choose a background music',soundeffect)
        ext = os.path.splitext(soundeffect)[1]
        videoext= os.path.splitext(inputmp4)[1]
        videofilename= os.path.splitext(inputmp4)[0]

        print('videoext',videoext)
        print('videofilename',videofilename)
        oldvideofiles=[]

        audioclip = AudioFileClip(soundeffect)
        if not os.path.exists(videofilename+'-old'+videoext):
            os.rename(inputmp4, videofilename+'-old'+videoext)
        videoclip = VideoFileClip(videofilename+'-old'+videoext)
        if audioclip.duration>videoclip.duration:
            audioclip =audioclip.subclip(0,videoclip.duration)
        else:
            audioclip = vfx.loop( audioclip, duration=videoclip.duration)
        if setting['ratio']:
            pass
        else:
            setting['ratio']=1
        # audioclip = audioclip.fx( afx.volumex, float(setting['ratio']))
        # audioclip.write_audiofile(videofilename+'.mp3')

        # audioclip = volumex(audioclip,setting['ratio'])          
        videoclip = videoclip.set_audio(audioclip)

        videoclip.write_videofile(videofilename+'.mp4', threads=0, audio=True)
        if not videoclip == None:
            print('force close clip')
            audioclip.close()

            videoclip.close()

            del audioclip 
            del videoclip 
 
            import gc 
            gc.collect()

           
        # time.sleep(2) 
        print('start cleaning old video file')
        if os.path.exists(videofilename+'-old'+videoext):
            os.remove(videofilename+'-old'+videoext)
def init_worker(mps, fps, cut):
    global memorizedPaths, filepaths, cutoff
    global DG

    print("process initializing", mp.current_process())
    memorizedPaths, filepaths, cutoff = mps, fps, cut
    DG = 1##nx.read_gml("KeggComplete.gml", relabel = True)
def changeLoglevel(level,window,log_frame):
    values = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

    if level=='DEBUG':
        logging.basicConfig(filename='test.log',
            level=logging.DEBUG, 
            format='%(asctime)s - %(levelname)s - %(message)s')   
    elif level=='INFO':
        logging.basicConfig(filename='test.log',
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
    elif level=='WARNING':
        logging.basicConfig(filename='test.log',
            level=logging.WARNING, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
    elif level=='ERROR':
        logging.basicConfig(filename='test.log',
            level=logging.ERROR, 
            format='%(asctime)s - %(levelname)s - %(message)s') 
    elif level=='CRITICAL':
        logging.basicConfig(filename='test.log',
            level=logging.CRITICAL, 
            format='%(asctime)s - %(levelname)s - %(message)s') 



def hiddenwatermark():
    print('add hiddenwatermark to each video for  copyright theft')
def batchchangebgmusic():

    # use all available CPUs
    # p = mp.Pool(initializer=init_worker, initargs=(memorizedPaths,
    #                                                filepaths,
    #                                                cutoff))
    folder =setting['video_folder']    
    oldvideofiles=[]
    videofiles = []

    if os.path.isdir(folder):
        print('this is a directory',folder)

        for ext in ('*.flv', '*.mp4', '*.avi'):
            videofiles.extend(glob(os.path.join(folder, ext)))
        print('detecting videos in folder',folder,videofiles)
        if len(videofiles) > 0:
            arguments=[]
            for i,f in enumerate(videofiles):
                videofilename= os.path.splitext(f)[0]
                videoext= os.path.splitext(f)[1]
                if not videofilename.endswith('-old'):
                    using_free_music(setting,f)
                    # arguments.append((setting,f)) 

            print('awaiting convert files',videofiles)                                                   
            # degreelist = range(100000) ##
    #         for _ in p.imap_unordered(threadusing_free_musichelper, arguments, chunksize=500):
    #             pass
    # p.close()
    # p.join()


    # print('start cleaning old video files')
    # oldvideofiles=[]

    # if os.path.isdir(folder):

    #     for ext in ('*.flv', '*.mp4', '*.avi'):
    #         oldvideofiles.extend(glob(os.path.join(folder, ext)))
    #     # print('this is a directory',folder)
  
    # for f in oldvideofiles:   
    #     videofilename= os.path.splitext(f)[0]

    #     if  videofilename.endswith('-old'):
    #         print('start cleaning old video file',f)
    #         if os.path.exists(f.replace('-old','')):
    #             os.remove( f)
    print('finish cleaning old video files')
def changebgmusic():
    folder =setting['video_folder']    
    if os.path.isdir(folder):
        print('this is a directory',folder)

        videofiles = []
        for ext in ('*.flv', '*.mp4', '*.avi'):
            videofiles.extend(glob(os.path.join(folder, ext)))
        print('detecting videos in folder',folder,videofiles)
        if len(videofiles) > 0:
            # for i,f in enumerate(videofiles):

            #     videofiles.append(f)    
            print('awaiting convert files',videofiles)
            start = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                # while True:
                tasks = [using_free_music(x) for x in videofiles]
                for task, future in [(i, executor.submit(i)) for i in tasks]:
                    try:
                        # print(future.result(timeout=1))
                        print('ok')
                    except concurrent.futures.TimeoutError:
                        print("this took too long...")
            #             # task.interrupt()
            end = time.time()
            print("批量替换took {} seconds\n".format(end-start))



def b64e(s):
    return base64.b64encode(s.encode()).decode()


def autothumb():

    save_setting()
# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        video_folder_path = setting['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            print("sure, it was defined dir.",video_folder_path)

            check_video_thumb_pair(video_folder_path,False)
        else:
            print("pls choose file or folder")
def editVideoMetas():
    print('go to web json editor to edit prepared video metas in json format')


def SelectVideoMetasfile():
    logger.debug('start to import prepared video metas in json format')
    try:
        video_meta_json_path = filedialog.askopenfilenames(title="choose video meta json file", filetypes=[
        ("Json", "*.json"), ("All Files", "*")])[0]
        imported_video_metas_file.set(video_meta_json_path)

    except:
        logger.error('you should choose a valid path')
    # setting['channelcookiepath'] = channel_cookie_path
    logger.debug('finished to import prepared video metas in json format')
def proxyaddView(newWindow):
    btn6= tk.Button(newWindow, text="add selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=setEntry(proxy_str.get())).start())     
    btn6.grid(row=9,column=0, sticky=tk.W)
    

    
    

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(newWindow)
    frame_canvas.grid(row=7, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)     

    # for scrolling vertically
    # for scrolling vertically
    yscrollbar = tk.Scrollbar(frame_canvas)
    yscrollbar.pack(side = tk.RIGHT, fill = 'both')
    
    langlist = tk.Listbox(frame_canvas, selectmode = "multiple",
                yscrollcommand = yscrollbar.set)
    langlist.pack(padx = 10, pady = 10,
            expand = tk.YES, fill = "both")

    btn5= tk.Button(newWindow, text="Get proxy list", padx = 0, 
                    pady = 0,command = lambda: threading.Thread(target=
                    filterProxiesLocations(newWindow,langlist,prod_engine,logger,city_user.get(),country_user.get(),proxyTags_user.get(),proxyStatusbox.get(),latest_proxy_conditions_user.get())).start())
    btn5.grid(row=6,column=2, sticky=tk.W)    
    def CurSelet(event):
        listbox = event.widget
        # values = [listbox.get(idx) for idx in listbox.curselection()]
        selection=listbox.curselection()
        # picked = listbox.get(selection[1])
        print(selection,list(selection),listbox.get(0))
        tmp=''
        for i in list(selection):
            tmp=tmp+listbox.get(i)+';'
        proxy_str.set(tmp)
        print('000000',proxy_str.get())
        if len(list(selection))==3:
            lbl15 = tk.Label(newWindow, text='you have reached 3 proxy limit for one account.dont select anymore')
            lbl15.grid(row=6,column=0, sticky=tk.W)
            lbl15.after(5*1000,lbl15.destroy)        
        
        elif len(list(selection))>3:
            print('you should choose no more than 3 proxy for one account')
            lbl15 = tk.Label(newWindow, text='you should choose no more than 3 proxy for one account.please remove')
            lbl15.grid(row=6,column=0, sticky=tk.W)
            lbl15.after(3*1000,lbl15.destroy)
        else:
            lbl15 = tk.Label(newWindow, text='you can add at least 1 and max 3 proxy for one account.')
            lbl15.grid(row=6,column=0, sticky=tk.W)
            lbl15.after(500,lbl15.destroy)

    langlist.bind('<<ListboxSelect>>',CurSelet)    


def chooseAccountsView(newWindow,parentchooseaccounts):
    chooseAccountsWindow = tk.Toplevel(newWindow)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title('which accounts in which platform you want upload')
    account_var = tk.StringVar()





    # Create a label for the platform dropdown
    platform_label = ttk.Label(chooseAccountsWindow, text="Select Platform:")
    platform_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    # Create a Combobox for the platform selection
    platform_var = tk.StringVar()
    platform_var.set("choose one:")
    platform_combo = ttk.Combobox(chooseAccountsWindow, textvariable=platform_var)
    platform_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(chooseAccountsWindow)
    frame_canvas.grid(row=4, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)     

    # for scrolling vertically
    yscrollbar = tk.Scrollbar(frame_canvas)
    yscrollbar.pack(side = tk.RIGHT, fill = 'both')
    
    langlist = tk.Listbox(frame_canvas, selectmode = "multiple",
                yscrollcommand = yscrollbar.set)
    langlist.pack(padx = 10, pady = 10,
            expand = tk.YES, fill = "both")

    btn6= tk.Button(chooseAccountsWindow, text="remove selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=remove_selected_accounts).start())     
    btn6.grid(row=5,column=1, sticky=tk.W)
    lbl16 = tk.Label(chooseAccountsWindow, text='selected user')
    lbl16.grid(row=6,column=0, sticky=tk.W)
    txt16 = tk.Entry(chooseAccountsWindow,textvariable=account_var)
    txt16.insert(0,'')
    txt16.grid(row=6,column=2, 
            #    width=width,
               columnspan=8,
            #    rowspan=3,
               sticky='nswe')    
    def on_platform_selected(event):
        selected_platform = platform_var.get()
        # Clear the current selection in the account dropdown
        # account_var.set("")
        # account_var.set("Select Accounts:")        

        if selected_platform:
            # Connect to the SQLite database
            table_name='accounts'
            # Execute a query to retrieve the dynamic platform list
            query="SELECT DISTINCT platform FROM accounts"
            engine=prod_engine
            platform_rows = query2df(engine,query,logger)


            # Extract platform names and set them as options in the platform dropdown
            if platform_rows is None:
                platform_combo["values"]=[]
                button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

            else:
                platform_names = [row.platform for row in platform_rows.itertuples()]
                logger.info(f'query results of existing platforms is {platform_names}')


                # Execute a query to retrieve accounts based on the selected platform
                query=f"SELECT username FROM {table_name} WHERE platform = '{selected_platform}'"
                if  len(platform_names)==0:
                    platform_combo["values"]=[]
                    button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                    button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
                    
                else:
                    tmp_accounts=''
                    platform_combo["values"]=platform_names
                    for platform in platform_names:
                        
                        if tmp['uploadaddaccounts'].has_key(platform):
                            logger.info(f'you have cached account for this platform {platform}')
                        else:
                            tmp['uploadaddaccounts'][platform]=[]
                    
                    print('all added accounts',tmp['uploadaddaccounts'])



                    engine=prod_engine
                    account_rows = query2df(engine,query,logger)
                    # Extract account names and set them as options in the account dropdown

                    if account_rows is None:
                        langlist.delete(0,tk.END)
                        button1 = ttk.Button(chooseAccountsWindow, text=f"try to add accounts for {selected_platform} first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                        button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

                    else:                
                        account_names = [row.username for row in account_rows.itertuples()]
                        logger.info(f'we found {len(account_names)} record matching ')

                        langlist.delete(0,tk.END)
                        i=0
                        for row in account_names:

                            langlist.insert(tk.END, row)
                            langlist.itemconfig(int(i), bg = "lime")                        

    
    # Bind the platform selection event to the on_platform_selected function
    platform_combo.bind("<<ComboboxSelected>>", on_platform_selected)


    # Create a label for the account dropdown
    account_label = ttk.Label(chooseAccountsWindow, text="Select Account(one or many):")
    account_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)


    # Initialize the platform dropdown by calling the event handler
    on_platform_selected(None)

    def remove_selected_accounts():
        selected_accounts=tmp['uploadaddaccounts']['selected']
        print('you want to remove these selected accounts',selected_accounts)
        # print('previous selected accounts',tmp['uploadaddaccounts'])
        # print('update selected accounts',account_var.get())
        if len(selected_accounts)==0:
            lbl15 = tk.Label(chooseAccountsWindow, text='you have not selected  accounts at all.choose one or more')
            lbl15.grid(row=4,column=2, sticky=tk.W)
            lbl15.after(5*1000,lbl15.destroy)        
        
        # elif selected_accounts==tmp['uploadaddaccounts'][platform_var.get()]:
        #     lbl15 = tk.Label(chooseAccountsWindow, text='you have not selected new accounts at all')
        #     lbl15.grid(row=6,column=0, sticky=tk.W)
        #     lbl15.after(5*1000,lbl15.destroy)        
        
        else:
            for item in selected_accounts:
                logger.info(f'you want to remove this selected account {item}')
                if item in tmp['uploadaddaccounts'][platform_var.get()]:
                    tmp['uploadaddaccounts'][platform_var.get()].remove(item)
                    logger.info(f'this account {item} removed success')
                    lbl15 = tk.Label(chooseAccountsWindow, text=f'this account {item} removed success')
                    lbl15.grid(row=4,column=2, sticky=tk.W)
                    lbl15.after(5*1000,lbl15.destroy)   
                else:
                    logger.info(f'you cannot remove this account {item}, not added before')
                    lbl15 = tk.Label(chooseAccountsWindow, text=f'this account {item} not added before')
                    lbl15.grid(row=4,column=2, sticky=tk.W)
                    lbl15.after(5*1000,lbl15.destroy)   
        show_str=str(tmp['uploadaddaccounts'])
        if tmp['uploadaddaccounts'].has_key('selected'):
            new=dict(tmp['uploadaddaccounts'])
            new.pop('selected')
            show_str=str(new)
        account_var.set(show_str)
        parentchooseaccounts.set(show_str)

    def add_selected_accounts(event):
        listbox = event.widget
        values = [listbox.get(idx) for idx in listbox.curselection()]
        tmp['uploadaddaccounts']['selected']=values
        # print('selected accounts',values)
        # print('previous selected accounts',tmp['uploadaddaccounts'])
        # print('update selected accounts',account_var.get())
        if len(list(values))==0:
            logger.info('you have not selected  accounts at all.choose one or more')
            lbl15 = tk.Label(chooseAccountsWindow, text='you have not selected  accounts at all.choose one or more')
            lbl15.grid(row=4,column=2, sticky=tk.W)
            lbl15.after(5*1000,lbl15.destroy)        
        
        elif values==tmp['uploadaddaccounts'][platform_var.get()]:
            logger.info('you have not selected new accounts at all')
            lbl15 = tk.Label(chooseAccountsWindow, text='you have not selected new accounts at all')
            lbl15.grid(row=4,column=2, sticky=tk.W)
            lbl15.after(5*1000,lbl15.destroy)        
        
        else:
            for item in values:
                if item in tmp['uploadaddaccounts'][platform_var.get()]:
                    logger.info(f'this account {item} added before')                    
                    lbl15 = tk.Label(chooseAccountsWindow, text=f'this account {item} added before')
                    lbl15.grid(row=4,column=2, sticky=tk.W)
                    lbl15.after(5*1000,lbl15.destroy)   
                else:
                    tmp['uploadaddaccounts'][platform_var.get()].append(item)
                    logger.info(f'this account {item} added successS')
                    lbl15 = tk.Label(chooseAccountsWindow, text=f'this account {item} added successS')
                    lbl15.grid(row=4,column=2, sticky=tk.W)
                    lbl15.after(5*1000,lbl15.destroy)   
            
        show_str=str(tmp['uploadaddaccounts'])
        if tmp['uploadaddaccounts'].has_key('selected'):
            new=dict(tmp['uploadaddaccounts'])
            new.pop('selected')
            show_str=str(new)
        account_var.set(show_str)
        parentchooseaccounts.set(show_str)
    langlist.bind('<<ListboxSelect>>',add_selected_accounts)    


def filterUserPlatform(engine=prod_engine,platform=None,username=None,newWindow=None):

    availableProxies=[]
    now_conditions='platform:'+platform+';username:'+username


    if username is not None and username !='' and 'input' not in username:
    # or platform is not None and platform !='' :
        query = f"SELECT * FROM accounts where"
        clause=[]
        if username is not None and username !='':
            clause.append(f" username regexp '{username}'")
        if platform is not None and platform !='':
            clause.append(f" platform regexp '{platform}'")


        query=query+' AND '.join(clause)+" ORDER by inserted_at DESC"

    else:
        query = f"SELECT * FROM accounts ORDER by inserted_at DESC"


    try:
        logger.info(f'start a new query:\n {query}')
        
        table_name='accounts'
        tableexist_query_sqlite=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"

        tableexist=query2df(engine,tableexist_query_sqlite,logger)
        if  tableexist is None and newWindow is not None:
            hints='there is no  records for query.add accounts before then try again'
                
            lbl15 = tk.Label(newWindow,bg="lightyellow", text=hints)
            lbl15.grid(row=6,column=2, sticky=tk.W)
            lbl15.after(2000,lbl15.destroy)                
        else:
            platform_rows_query=f"SELECT DISTINCT platform FROM {table_name}"
            platform_rows=query2df(engine,platform_rows_query,logger)
            platform_names = [row[0] for row in platform_rows]
            db_rows = query2df(engine,query,logger)
    except Exception as e:
        print(f'sql run exception :{e}')



def isPairedMetas(r,videofilename,meta_exts_list,dict,meta_name):
    logger.info(f'start to check {meta_name} for video: {videofilename}')
    print(f'before check:\n{jsons.dump(dict[meta_name])}')

    for ext in meta_exts_list:
        metapath = os.path.join(r, videofilename+ext)
        if  os.path.exists(metapath):     
            logger.info(f'this  {meta_name} exist:\n {metapath}')
            if dict[meta_name] is not None and metapath not in dict[meta_name]:
                if dict[meta_name].has_key(videofilename)==False:
                    dict[meta_name][videofilename]=[]
                    logger.info(f'intial {meta_name} for {videofilename}:\n')

                dict[meta_name][videofilename].append(metapath)
                print(f'append result:\n{dict[meta_name][videofilename]}')
                if meta_name=='thumbFilePaths':
                    dict['videos'][videofilename]['thumbnail_local_path'].append(metapath)
                if meta_name=='desFilePaths':
                    with open(metapath,'r') as f:
                        contents=f.readlines()
                        dict['videos'][videofilename]['video_description']=contents               
    print(f'after check:\n{jsons.dump(dict[meta_name])}')
    tmpjson=os.path.join(r, videofilename+'.json')
    if os.path.exists(tmpjson):
        logger.info(f'update to {videofilename} meta json')
        with open(tmpjson,'w') as f:
            f.write(jsons.dumps(dict['videos'][videofilename]))        
    else:
        logger.info(f'create a fresh {videofilename} meta json')
        with open(tmpjson,'a') as f:
            f.write(jsons.dumps(dict['videos'][videofilename]))
        
def analyse_video_meta_pair(folder,frame,right_frame,selectedMetafileformat,isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True):
    if folder=='':
        logger.info('please choose a folder first')
    else:
        logger.info(f'detecting----------{ultra.has_key(folder)}')
        if ultra.has_key(folder):
            print(pd.Timestamp.now().value-ultra[folder] ['updatedAt'])
            logger.info(f"we cached {pd.Timestamp.now().value-ultra[folder] ['updatedAt']} seconds before for  this folder {folder}")
            
            b_delete_folder_cache=tk.Button(frame,text="remove cache data to re-gen",command=lambda: threading.Thread(target=ultra[folder].unlink()).start() )
            b_delete_folder_cache.grid(row = 6, column = 1,sticky='w', padx=14, pady=15)  
        else:
            logger.info(f"create cached data for this folder:\n{folder}")
            ultra[folder]={'videoCounts':0,'thumbCounts':0,'desCounts':0,
                        'metaCounts':0,'updatedAt':pd.Timestamp.now().value,
                        'filenames':[],
                        'videoFilePaths':[],
                            'thumbFilePaths':{},
                            'desFilePaths':{},
                            'metaFilePaths':{},  
                            "thumb_gen_setting":{
                            "mode":3,
                            "render_style":'cord',
                            "result_image_width": "",
                            "result_image_height": "",                        
                            # "bg_image": "",  
                            "template_path":"",     
                            "bg_folder":"",
                            "bg_folder_images":[],                         
                            "template":  {},

                            },
                                    "des_gen_setting":{
                                        "prefix":"",
                                        "suffix":"",
                                        "mode":"manually from .des file or append prefix suffix with des file or auto summary from subtitle or auto summary from tts"
                                    },
                                    "schedule_gen_setting":{
                                        'daily_limit':4,
                                        'offset':1
                                    },
                                    "tag_gen_setting":{
                                        'preferred':"",
                                        'mode':"manually from .tag file or manually +preferred or just preferred or api or auto"
                                    },
                        
                            'videos':{},
                            'videosmeta':{}

                        } 

            ultra[folder].dump()   

        for r, d, f in os.walk(folder):
            videos=[]        
            with os.scandir(r) as i:
# how to deal sub-folder and fodler
# if folder has no video but got 1 subfolder has 1 video, where to put metafiles
                for entry in i:
                    if entry.is_file():
                        filename = os.path.splitext(entry.name)[0]

                        ext = os.path.splitext(entry.name)[1]
                        if ext in supported_video_exts:

                            if ultra[folder] ['filenames']!=[] and filename in ultra[folder] ['filenames']:
                                logger.info(f'we found same filename diff ext video:{filename},please rename or remove')
                            else:
                                ultra[folder] ['filenames'].append(filename)


                                videopath = os.path.join(r, entry.name)
                                ultra[folder] ['videoFilePaths'].append(videopath)
                                # default single video meta json
                                video={'video_local_path':videopath,
                                    "video_filename":entry.name,
                                    "video_title":'',
                                        "heading":"",
                                        "subheading":"",
                                        "extraheading":"",
                                    "video_description":"",
                                        "thumbnail_bg_image_path": "",

                                    "thumbnail_local_path":[],
                                    "release_date":"",
                                    "release_date_hour":"10:15",
                                        "is_not_for_kid": True,
                                        "categories": 3,
                                        "comments_ratings_policy": 1,
                                        "is_age_restriction": False,
                                        "is_paid_promotion": False,
                                        "is_automatic_chapters": True,
                                        "is_featured_place": True,
                                        "video_language": "",
                                        "captions_certification": 0,
                                        "video_film_date": "",
                                        "video_film_location": "",
                                        "license_type": 0,
                                        "is_allow_embedding": True,
                                        "is_publish_to_subscriptions_feed_notify": True,
                                        "shorts_remixing_type": 0,
                                        "is_show_howmany_likes": True,
                                        "is_monetization_allowed": True,
                                        "first_comment": "",
                                        "subtitles": "",
                                        "is_not_for_kid": True,
                                        "categories": '',
                                        "comments_ratings_policy": 1,
                                    'tags':''}
                                ultra[folder] ['videos'][filename]=video
                                videos.append(video)
                                ultra[folder] ['videos'][filename]['video_local_path']=videopath
                                ultra[folder] ['videos'][filename]['video_title']=filename
                                ultra[folder] ['videoCounts']+=1
                                print(videopath,'==',ext,'counts now:',ultra[folder] ['videoCounts'],type(ultra[folder] ['videoCounts'])) 

                                # if ultra[folder]['thumbFilePaths'].has_key(filename)==False:
                                #     ultra[folder]['thumbFilePaths'][filename]=[]
                                isPairedMetas(r,filename,supported_thumb_exts,ultra[folder],'thumbFilePaths')
                                isPairedMetas(r,filename,supported_des_exts,ultra[folder],'desFilePaths')
                                isPairedMetas(r,filename,supported_meta_exts,ultra[folder],'metaFilePaths')
                    else:
                        print('is folder',r,d,i)


        if ultra[folder] ['videoCounts']==0:
            logger.info(f"we could not find any video, video counts is {ultra[folder] ['videoCounts']},supported ext includes:\n{'.'.join(supported_video_exts)}")
        ultra[folder] ['thumbCounts']=len(ultra[folder] ['thumbFilePaths'])
        ultra[folder] ['desCounts']=len(ultra[folder] ['desFilePaths'])
        ultra[folder] ['metaCounts']=len(ultra[folder] ['metaFilePaths'])
        ultra[folder]['updatedAt']=pd.Timestamp.now().value
        print('---------\n',type(ultra[folder]),type(jsons.dump(ultra[folder])),jsons.dump(ultra[folder]))
        tmpjson=os.path.join(folder,videoassetsfilename)

        if os.path.exists(tmpjson):
            with open(tmpjson,'w') as f:
                f.write(jsons.dumps(ultra[folder]))        
        else:
            with open(tmpjson,'a') as f:
                f.write(jsons.dumps(ultra[folder]))        

        ultra[folder]['metafileformat']=selectedMetafileformat
        if selectedMetafileformat=='xlsx':
            df_metas = pd.read_json(jsons.dumps(ultra[folder]['videos']), orient = 'index')

            metaxls=os.path.join(folder,'videos-meta.xlsx')
            df_metas.to_excel(metaxls)
        elif selectedMetafileformat=='csv':
            df_metas = pd.read_json(jsons.dumps(ultra[folder]['videos']), orient = 'index')

            metacsv=os.path.join(folder,'videos-meta.csv')

            df_metas.to_csv(metacsv)
        else:
            df_metas = pd.read_json(jsons.dumps(ultra[folder]['videos']), orient = 'records')

            # json is the default ,there is always a videometa.json file after folder check
            metajson=os.path.join(folder,'videos-meta.json')

            df_metas.to_json(metajson)

        
        render_video_folder_check_results(frame,right_frame,folder,isThumbView,isDesView,isTagsView,isScheduleView)






def check_video_thumb_pair(dbm,folder,session):
    # print(f'detecting----------{folder}')

    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            print('detecting----------',r)
            videopair=0

            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    # print(filename,'==',ext) 

                    start_index=1
                    if ext in ('.flv', '.mp4', '.avi'):
                        videopath = os.path.join(r, entry.name)
                        count=0
                        exist_image_ext=''
                        for image_ext in ['.jpeg', '.png', '.jpg','webp']:
                            thumbpath = os.path.join(r, filename+image_ext)

                            if not os.path.exists(thumbpath):     
                                count+=1
                            else:
                                exist_image_ext=image_ext  
                        if count==len(['.jpeg', '.png', '.jpg']):
                            no=random.choice(['001','002','003'])
                            if not os.path.exists(os.path.join(r, filename+'-'+no+'.jpg')):   
                                generator = AiThumbnailGenerator(videopath)

                                thumbpath=os.path.join(r, filename+'-'+no+'.jpg')                                
                                print('generated thumbnail is',thumbpath)
                        else:
                            thubmpath=os.path.join(r,filename+exist_image_ext)
                            print('thumbnail is there.if you need create,pls delete the old one')
                        if session:
                            print( videopath,thumbpath,filename,start_index,setting['channelname'],settingid)

                            prepareuploadsession( dbm,videopath,thumbpath,filename,start_index,setting['channelname'],settingid)
                            print('all video added to task list,you should start uploading next ')
                        else:
                            print('save video meta json to local disk')
                        start_index=start_index+1
                        videopair+=1

                if videopair==0:
                    print('we could not find any video,prefer format mp4,mkv,flv,mov')



def prepareuploadsession(dbm,videopath,thumbpath,filename,start_index,channelname,settingid):
    global uploadsessionid
    isadded,isuploaded=dbm.Query_video_status_in_channel(videopath,channelname,settingid)
              
    # filename = os.path.splitext(f)[0]
    if isadded:

        if isuploaded:
            print('task completed', isuploaded, videopath)
        else:

            print('task added but not uploaded')

    else:
        print('task not added before')
        
        tags = setting['prefertags']
        
        
        preferdesprefix = setting['preferdesprefix']
        preferdessuffix = setting['preferdessuffix']
        filename=filename.split(os.sep)[-1]
        des =filename
        if preferdesprefix:

            des=preferdesprefix+'========\n'+des
        if preferdessuffix:
            des=des+'=========\n'+preferdessuffix
        des=des[:4900]
        title = isfilenamevalid(filename)
        if len(filename) > 100:
            title = filename[:90]
        nowtime = time.time()
        videoid = b64e(filename)

        olddata = UploadSession()
        olddata.uploadSettingid=settingid
        olddata.videoid = videoid
        olddata.channelname=setting['channelname']
        publishpolicy=setting['publishpolicy']
        start_publish_date=setting['start_publish_date']
        olddata.publishpolicy=publishpolicy
        today = date.today()
        publish_date =datetime(today.year, today.month, today.day, 20, 15)

        if publishpolicy == 0:
            olddata.publish_date = publish_date
        elif publishpolicy == 1:
            olddata.publish_date = publish_date
        else:
            # Oct 19, 2021
            start_index = int(start_publish_date)+start_index
            maxdays=calendar._monthlen(today.year, today.month)

            monthoffset=int(int(start_index)/maxdays)
            startingday=today.day
            dayoffset=int(int(start_index)/int(setting['dailycount']))
            if today.day+1>maxdays:
                monthoffset=1
                startingday=today.day+1-maxdays
            publish_date =datetime(today.year, today.month+monthoffset, startingday+1+dayoffset, 20, 15)



            olddata.publish_date = publish_date
        olddata.thumbpath = thumbpath
        olddata.title= title
        olddata.des= des
        olddata.videopath = videopath
        olddata.tags= tags
        olddata.status = False
        uploadsessionid=dbm.Add_New_UploadSession_In_Db(olddata)
        print('add 1 new videos ',filename,'for upload session',uploadsessionid)



def exportcsv(dbm):
    videos=dbm.Query_undone_videos_in_channel()


def importundonefromcsv(dbm):
    videos=dbm.Query_undone_videos_in_channel()



def testupload(dbm,ttkframe):
    print('we got setting proxy ,',setting['proxy_option'])
    try:
        uploadsessionid
        if uploadsessionid is None:
            print('weir error',uploadsessionid)
            createuploadsession(dbm,ttkframe)
    except:

        print('before upload,you need create upload session first')
        createuploadsession(dbm,ttkframe)

    videos=dbm.Query_undone_videos_in_channel()
    print('there is ',len(videos),' video need to uploading for task ')

    if len(videos)>0:
        publicvideos=[]
        privatevideos=[]
        othervideos=[]
        if url_ok('http://www.google.com'):
            print('network is fine,there is no need for proxy ')
            setting['proxy_option']=""
            print('start browser in headless mode',is_open_browser)

        else:
            print('google can not be access ')

            print('we need for proxy ',setting['proxy_option'])   
            print('start browser in headless mode',is_open_browser,setting['proxy_option'])
        upload =  YoutubeUpload(
                root_profile_directory=setting['firefox_profile_folder'],
                proxy_option=setting['proxy_option'],
                is_open_browser=is_open_browser,
                debug=True,
                use_stealth_js=False,
                # if you want to silent background running, set watcheveryuploadstep false
                channel_cookie_path=setting['channelcookiepath'],
                username=setting['username'],
                browser_type='firefox',
                wait_policy="go next after copyright check success",
                password=setting['password'],
                is_record_video=setting['is_record_video']

                # for test purpose we need to check the video step by step ,
            )

        for video in videos:
            
            if int(video.publishpolicy)==1:
                print('add public uploading task video',video.videopath)
                
                publicvideos.append(video)
            elif int(video.publishpolicy)==0:
                print('add private uploading task video',video.videopath)

                privatevideos.append(video)
            else:
                print('add schedule uploading task video',video.videopath)

                othervideos.append(video)
        if len(publicvideos)>0:
            print('start public uploading task')
            asyncio.run(bulk_instantpublish(videos=publicvideos,upload=upload))
        if len(privatevideos)>0:
            print('start private uploading task')

            asyncio.run(bulk_privatedraft(videos=privatevideos,upload=upload))
        if len(othervideos)>0:
            print('start schedule uploading task')

            asyncio.run(bulk_scheduletopublish_specific_date(videos=othervideos,upload=upload))


def upload(mode='prod'):
    print('we got setting proxy ,',setting['proxy_option'])
    dbm=DBM('prod')
    
    try:
        uploadsessionid
        if uploadsessionid is None:
            print('weir error',uploadsessionid)
            # createuploadsession()
    except:

        print('before upload,you need create upload session first')
        # createuploadsession()

    videos=dbm.Query_undone_videos_in_channel()
    print('there is ',len(videos),' video need to uploading for task ')

    if len(videos)>0:
        publicvideos=[]
        privatevideos=[]
        othervideos=[]
        if url_ok('http://www.google.com'):
            print('network is fine,there is no need for proxy ')
            setting['proxy_option']=""
            print('start browser in headless mode',is_open_browser)

        else:
            print('google can not be access ')

            print('we need for proxy ',setting['proxy_option'])   
            print('start browser in headless mode',is_open_browser,setting['proxy_option'])
        upload =  YoutubeUpload(
                root_profile_directory=setting['firefox_profile_folder'],
                proxy_option=setting['proxy_option'],
                is_open_browser=is_open_browser,
                debug=True,
                use_stealth_js=False,
                # if you want to silent background running, set watcheveryuploadstep false
                channel_cookie_path=setting['channelcookiepath'],
                username=setting['username'],
                browser_type='firefox',
                wait_policy="go next after copyright check success",
                password=setting['password'],
                is_record_video=setting['is_record_video']

                # for test purpose we need to check the video step by step ,
            )

        for video in videos:
            
            if int(video.publishpolicy)==1:
                print('add public uploading task video',video.videopath)
                
                publicvideos.append(video)
            elif int(video.publishpolicy)==0:
                print('add private uploading task video',video.videopath)

                privatevideos.append(video)
            else:
                print('add schedule uploading task video',video.videopath)

                othervideos.append(video)
        if len(publicvideos)>0:
            print('start public uploading task')
            asyncio.run(bulk_instantpublish(videos=publicvideos,upload=upload))
        if len(privatevideos)>0:
            print('start private uploading task')

            asyncio.run(bulk_privatedraft(videos=privatevideos,upload=upload))
        if len(othervideos)>0:
            print('start schedule uploading task')

            asyncio.run(bulk_scheduletopublish_specific_date(videos=othervideos,upload=upload))

def docView(frame,ttkframe,lang):
    b_view_readme=tk.Button(frame,text=i18labels("docs", locale=lang, module="g"),command=lambda: threading.Thread(target=docs(frame,lang)).start() )
    b_view_readme.place(x=50, y=100)    

    b_view_contact=tk.Button(frame,text=i18labels("contact", locale=lang, module="g"),command=lambda: threading.Thread(target=contact(frame,lang)).start() )
    b_view_contact.place(x=50, y=200)    
    

    b_view_version=tk.Button(frame,text=i18labels("version", locale=lang, module="g"),command=lambda: threading.Thread(target=version(frame,lang)).start() )
    b_view_version.place(x=50, y=300)   

def installView(frame,ttkframe,lang):
    b_view_readme=tk.Button(frame,text=i18labels("testinstall", locale=lang, module="g"),command=lambda: threading.Thread(target=testInstallRequirements).start() )
    b_view_readme.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)      

    b_view_contact=tk.Button(frame,text=i18labels("testnetwork", locale=lang, module="g"),command=lambda: threading.Thread(target=testNetwork).start() )
    b_view_contact.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    

    b_view_version=tk.Button(frame,text=i18labels("testsettingok", locale=lang, module="g"),command=lambda: threading.Thread(target=ValidateSetting).start() )
    b_view_version.grid(row = 2, column = 1, sticky='w', padx=14, pady=15)      
    
    locale_tkstudio = tk.StringVar()


    l_lang = tk.Label(ttkframe, text=i18labels("chooseLang", locale=lang, module="g"))
    # l_lang.place(x=10, y=90)
    l_lang.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15)    
    try:
        settings['locale']
        print(f"cache locale exist {settings['locale']}")
        locale_tkstudio.set(settings['locale'])
    except:
        print('keep the default locale placeholder')
        # locale_tkstudio_box.set("Select From Langs")
        locale_tkstudio.set("Select From Langs")    
    def display_selected_item_index(event): 
        try:
            settings['locale']
            print(f"cache locale exist {settings['locale']}")
            locale_tkstudio.set(settings['locale'])
        except:
            print('keep the default locale')
            # locale_tkstudio_box.set("Select From Langs")
            locale_tkstudio.set("Select From Langs")
    def locale_tkstudioOptionCallBack(*args):
        print(locale_tkstudio.get())
        print(locale_tkstudio_box.current())
        settings['locale']=locale_tkstudio.get()
        print(f"save locale to cache { settings['locale']}")        
        changeDisplayLang(locale_tkstudio.get())



    locale_tkstudio.trace('w', locale_tkstudioOptionCallBack)


    locale_tkstudio_box = ttk.Combobox(ttkframe, textvariable=locale_tkstudio)
    locale_tkstudio_box.config(values =('en', 'zh'))
    # locale_tkstudio_box.set(locale_tkstudio.get())    
    locale_tkstudio_box.grid(row = 4, column = 1, columnspan = 3, padx=14, pady=15)    
    locale_tkstudio_box.bind("<<ComboboxSelected>>", display_selected_item_index)  


      
def videosView(frame,ttkframe,lang):
    global videosView_video_folder
    videosView_video_folder = tk.StringVar()

    # videosView_video_folder.set(setting['video_folder'])

    l_video_folder = tk.Label(frame, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.place(x=10, y=20)
    e_video_folder = tk.Entry(frame, width=45, textvariable=videosView_video_folder)
    e_video_folder.place(x=150, y=20)
    b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_videosView_video_folder).start() )
    b_video_folder.place(x=580, y=20)    

    l_mode_1 = tk.Label(frame, text=i18labels("toolkits", locale=lang, module="g"))
    l_mode_1.place(x=10, y=int(height-250))
    
    
    b_autothumb = tk.Button(frame, text=i18labels("autothumb", locale=lang, module="g"), command=lambda: threading.Thread(target=autothumb).start())
    b_autothumb.place(x=150, y=int(height-250))
    b_batchchangebgmusic = tk.Button(frame, text=i18labels("batchchangebgmusic", locale=lang, module="g"), command=lambda: threading.Thread(target=batchchangebgmusic).start())
    b_batchchangebgmusic.place(x=350,y=int(height-250))
    
    
    b_hiddenwatermark = tk.Button(frame, text=i18labels("hiddenwatermark", locale=lang, module="g"), command=lambda: threading.Thread(target=hiddenwatermark))
    b_hiddenwatermark.place(x=500,y=int(height-250))

def thumbView(left,right,lang):
    # global thumbView_video_folder
    thumbView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=thumbView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     


    def e_video_folderCallBack(*args):
        thumbView_video_folder.set(ultra['thumbView_video_folder'])



    thumbView_video_folder.trace('w', e_video_folderCallBack)

    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(thumbView_video_folder,'thumbView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(thumbView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_meta_format, text='Choose the one you like to edit metadata' , wraplength=200)

    metafileformat = tk.StringVar()



    metafileformat.set("Select From format")


    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values = ( 'json','xlsx', 'csv'))
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        analyse_video_meta_pair(thumbView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True,isDesView=False,isTagsView=False,isScheduleView=False)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')
    metafileformat.trace('w', metafileformatCallBack)

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(thumbView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=
                                   lambda: threading.Thread(target=analyse_video_meta_pair(
                                       thumbView_video_folder.get(),left,right,metafileformatbox.get(),
                                       isThumbView=True,isDesView=False,isTagsView=False,isScheduleView=False)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)



def openXLSX(xlsxpath):
    
    if  platform.system()=='Linux':
    
        
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'") 

    elif platform.system()=='macos':
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'") 
    else:
        os.system('start "excel" "C:\\path\\to\\myfile.xlsx"')

    
def render_video_folder_check_results(frame,right_frame,folder,isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True):
    lb_video_counts = tk.Label(frame, text='video total counts')

    lb_video_counts.grid(row = 3, column = 0,sticky='w')    

    lb_video_counts_value = tk.Label(frame, text=str(ultra[folder] ['videoCounts']))
    lb_video_counts_value.grid(row = 3, column = 1)    


    if isThumbView==True:
        lb_video_thumb_pairs_counts = tk.Label(frame, text='video-thum paired')
        lb_video_thumb_pairs_counts.grid(row = 4, column = 0,sticky='w')    
        Tooltip(lb_video_thumb_pairs_counts, text='if there is the same filename image exist for video,we take it as paired' , wraplength=200)



        lb_video_thumb_pairs_counts_value = tk.Label(frame, text=str(ultra[folder] ['thumbCounts']))
        lb_video_thumb_pairs_counts_value.grid(row = 4, column = 1)      


        lb_video_thumb_missing_file_pairs_counts = tk.Label(frame, text='missing file')
        lb_video_thumb_missing_file_pairs_counts.grid(row = 4, column = 2)      

        missing_video_thumb_file_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] ['thumbCounts']

        lb_missing_video_thumb_file_pairs_counts = tk.Label(frame, text=str(missing_video_thumb_file_pairs_counts))
        lb_missing_video_thumb_file_pairs_counts.grid(row = 4, column = 3)      
    #  subtitles missing file


        label_str='Gen'
        if missing_video_thumb_file_pairs_counts>0:
            label_str='Update'



        b_gen_thumb=tk.Button(frame,text=label_str,command=lambda: threading.Thread(target=render_thumb_gen(right_frame,True,folder)).start() )
        b_gen_thumb.grid(row = 4, column = 4)     
        Tooltip(b_gen_thumb, text='Click below button to Learn more' , wraplength=200)

    if isDesView==True:
        lb_video_des_pairs_counts = tk.Label(frame, text='video-des paired')
        lb_video_des_pairs_counts.grid(row = 5, column = 0,sticky='w')    



        lb_video_des_pairs_counts_value = tk.Label(frame, text=str(ultra[folder] ['desCounts']))
        lb_video_des_pairs_counts_value.grid(row =5, column = 1)    


        lb_video_des_missing_pairs_counts = tk.Label(frame, text='missing paired')
        lb_video_des_missing_pairs_counts.grid(row = 5, column = 2)    

        missing_video_des_missing_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] ['desCounts']

        lb_video_des_missing_pairs_counts_value = tk.Label(frame, text=str(missing_video_des_missing_pairs_counts))
        lb_video_des_missing_pairs_counts_value.grid(row = 5, column = 3)    
        label_str='Gen'
        if missing_video_des_missing_pairs_counts>0:
            label_str='Update'

        b_gen_des=tk.Button(frame,text=label_str,command=lambda: threading.Thread(target=render_des_gen(right_frame,True,folder)).start() )
        b_gen_des.grid(row = 5, column = 4)    


    if isScheduleView==True:


        lb_video_schedule_pairs_counts = tk.Label(frame, text='video-schedule paired')
        lb_video_schedule_pairs_counts.grid(row = 6, column = 0,sticky='w')    



        lb_video_schedule_pairs_counts_value = tk.Label(frame, text=str(ultra[folder] ['metaCounts']))
        lb_video_schedule_pairs_counts_value.grid(row = 6, column = 1)    


        lb_video_schedule_missing_pairs_counts = tk.Label(frame, text='missing paired')
        lb_video_schedule_missing_pairs_counts.grid(row = 6, column = 2)    

        missing_video_schedule_missing_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] ['metaCounts']

        lb_video_schedule_missing_pairs_counts_value = tk.Label(frame, text=str(missing_video_schedule_missing_pairs_counts))
        lb_video_schedule_missing_pairs_counts_value.grid(row = 6, column = 3)    
        label_str='Gen'
        if missing_video_schedule_missing_pairs_counts>0:
            label_str='Update'

        b_gen_schedule=tk.Button(frame,text=label_str,command=lambda: threading.Thread(target=render_update_schedule(right_frame,True)).start() )
        b_gen_schedule.grid(row = 6, column = 4,sticky='nesw')    

    if isTagsView:
        lb_video_tags_pairs_counts = tk.Label(frame, text='video-tags paired')
        lb_video_tags_pairs_counts.grid(row = 7, column = 0,sticky='w')    



        lb_video_tags_pairs_counts_value = tk.Label(frame, text=str(ultra[folder] ['metaCounts']))
        lb_video_tags_pairs_counts_value.grid(row = 7, column = 1)    


        lb_video_tags_missing_pairs_counts = tk.Label(frame, text='missing paired')
        lb_video_tags_missing_pairs_counts.grid(row = 7, column = 2)    

        missing_video_tags_missing_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] ['metaCounts']

        lb_video_tags_missing_pairs_counts_value = tk.Label(frame, text=str(missing_video_tags_missing_pairs_counts))
        lb_video_tags_missing_pairs_counts_value.grid(row = 7, column = 3)    
        label_str='Gen'
        if missing_video_tags_missing_pairs_counts>0:
            label_str='Update'
        b_gen_thumb=tk.Button(frame,text=label_str,command=lambda: threading.Thread(target=render_update_tags(right_frame,True)).start() )
        b_gen_thumb.grid(row = 7, column = 4,sticky='nesw')    


    if isDesView==True and isScheduleView==True and isTagsView==True and isThumbView==True:
        lb_video_meta_pairs_counts = tk.Label(frame, text='video-meta paired')
        lb_video_meta_pairs_counts.grid(row = 8, column = 0,sticky='w')    



        lb_video_meta_pairs_counts_value = tk.Label(frame, text=str(ultra[folder] ['metaCounts']))
        lb_video_meta_pairs_counts_value.grid(row = 8, column = 1)    


        lb_video_meta_missing_pairs_counts = tk.Label(frame, text='missing paired')
        lb_video_meta_missing_pairs_counts.grid(row = 8, column = 2)    

        missing_video_meta_missing_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] ['metaCounts']

        lb_video_meta_missing_pairs_counts_value = tk.Label(frame, text=str(missing_video_meta_missing_pairs_counts))
        lb_video_meta_missing_pairs_counts_value.grid(row = 8, column = 3)    
        label_str='Gen'
        if missing_video_meta_missing_pairs_counts>0:
            label_str='Update'

        b_gen_meta=tk.Button(frame,text=label_str,command=lambda: threading.Thread(target=render_update_meta(right_frame,True)).start() )
        b_gen_meta.grid(row = 8, column = 4,sticky='nesw')    
def render_des_gen(frame,isneed,folder):
    if isneed==True:
        if len(frame.winfo_children())>0:
            for widget in frame.winfo_children():
                widget.destroy()        
        global thumbnail_metas_file,thummbnail_bg_folder,thummbnail_bg_file,thumbnail_template_file
        thumbnail_metas_file = tk.StringVar()        
        thummbnail_bg_folder = tk.StringVar()        
        thummbnail_bg_file = tk.StringVar()      

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')     


        desmode = tk.IntVar()
        # thumbmode.set(1)

        lab = tk.Label(new_canvas,text="请选择你的视频描述从何而来",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw') 
   
        thumbmode1=tk.Radiobutton(new_canvas,text="手动准备",variable=desmode,value=1,command=lambda:render_des_update_view(new_canvas,folder,desmode,frame))
        thumbmode1.grid(row = 1, column = 1,  padx=14, pady=15,sticky='nw') 
        thumbmode2=tk.Radiobutton(new_canvas,text=" 批量生成",variable=desmode,value=2,command=lambda:render_des_update_view(new_canvas,folder,desmode,frame))
        thumbmode2.grid(row = 1, column = 2,  padx=14, pady=15,sticky='nw') 

        # thumbmode.trace_add('write', render_thumb_update_view(new_canvas,folder,thumbmode))




def render_des_update_view(frame,folder,thumbmode,previous_frame=None):
    print('thumbmode',type(thumbmode.get()),thumbmode.get())    
    lang='en'

    if len(frame.winfo_children())>0:
        for widget in frame.winfo_children():
            widget.destroy()      
   
    if thumbmode.get() ==1:
        lbl15 = tk.Label(frame, text='两种选择')
        lbl15.grid(row=0,column=0,padx=14, pady=15,sticky='w') 
       
        lbl15 = tk.Label(frame, text='1.手动准备视频描述，填充到元数据对应字段即可，元数据格式支持xlsx json csv',wraplength=600)
        lbl15.grid(row=1,column=0, sticky='w')

        lbl15 = tk.Label(frame, text='2.\r',wraplength=600)
        lbl15.grid(row=2,column=0, sticky='w')



        b_check_metas_=tk.Button(frame,text="edit videometa with local editor",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 6, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_check_metas_, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)

        if ultra[folder]['metafileformat']=='json':
            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 5, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_edit_thumb_metas, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)
        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 4, column = 0, padx=14, pady=15,sticky='nswe')      


        b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateThumbnailGenMetas(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_file.get(),thummbnail_bg_folder.get()))
        b_update_metas_.grid(row = 7, column = 0,  padx=14, pady=15,sticky='nswe') 

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_des_gen(previous_frame,True,folder))
        b_return.grid(row = 8, column =0)   

    else:

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_des_gen(previous_frame,True,folder))
        b_return.grid(row = 0, column =1)   


        lab = tk.Label(frame,text="Step2:是否使用统一前缀后缀",bg="lightyellow",width=30)
        lab.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw')         
        descriptionPrefix=tk.StringVar()
        descriptionSuffix=tk.StringVar()

        l_preferdesprefix = tk.Label(frame, text=i18labels("descriptionPrefix", locale=lang, module="g"))
        l_preferdesprefix.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        e_preferdesprefix = tk.Entry(frame, width=55, textvariable=descriptionPrefix)
        e_preferdesprefix.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 


        l_preferdessuffix = tk.Label(frame, text=i18labels("descriptionSuffix", locale=lang, module="g"))
        l_preferdessuffix.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        e_preferdessuffix = tk.Entry(frame, width=55, textvariable=descriptionSuffix)
        e_preferdessuffix.grid(row = 1, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 

        mode = tk.StringVar()
        mode.set("4")

        lab = tk.Label(frame,text="Step1:请选择视频描述主体从何而来",bg="lightyellow",width=30)
        lab.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode1=tk.Radiobutton(frame,text="视频文件名称",variable=mode,value="1",command='')
        mode1.grid(row = 5, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode2=tk.Radiobutton(frame,text="视频字幕总结",variable=mode,value="2",command='')
        mode2.grid(row = 6, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode3=tk.Radiobutton(frame,text="视频音频总结",variable=mode,value="3",command='')
        mode3.grid(row = 7, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode4=tk.Radiobutton(frame,text="从视频描述文件中来",variable=mode,value="4",command='')
        mode4.grid(row = 8, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode5=tk.Radiobutton(frame,text="从元数据中来",variable=mode,value="5",command='')
        mode5.grid(row = 9, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 


        
        lab = tk.Label(frame,text="Step3:请编辑视频元数据",bg="lightyellow",width=30)
        lab.grid(row = 7, column = 0,  padx=14, pady=15,sticky='nw')         




        b_check_metas_=tk.Button(frame,text="edit videometa",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 8, column = 0, padx=14, pady=15,sticky='nswe') 
        if ultra[folder]['metafileformat']=='json':

            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 8, column = 1, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_edit_thumb_metas, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)
        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 8, column = 2, padx=14, pady=15,sticky='nswe')    
        lab = tk.Label(frame,text="Step4:生成视频描述",bg="lightyellow",width=30)
        lab.grid(row = 9, column = 0,  padx=14, pady=15,sticky='nw')         


        b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateThumbnailGenMetas(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_file.get(),thummbnail_bg_folder.get()))
        b_update_metas_.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nswe') 
        



        b_gen_thumb_=tk.Button(frame,text="gen thumb",command=lambda: genThumbnailFromTemplate(folder,thumbnail_template_file.get(),mode))
        b_gen_thumb_.grid(row = 11, column =0, padx=14, pady=15,sticky='nswe') 


        b_check_metas_=tk.Button(frame,text="check metajson",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_check_metas_.grid(row = 12, column = 0, padx=14, pady=15,sticky='nswe') 


def render_update_tags(frame,isneed):
    if isneed==True:
        lang='en'
        prefertags=tk.StringVar()
        if len(frame.winfo_children())>0:
            for widget in frame.winfo_children():
                widget.destroy()
        l_prefertags = tk.Label(frame, text=i18labels("preferTags", locale=lang, module="g"))
        l_prefertags.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        el_prefertags = tk.Entry(frame, width=55, textvariable=prefertags)
        el_prefertags.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 



        publishpolicy = tk.IntVar()
        # publishpolicy.set(4)

        lab = tk.Label(frame,text="where to auto gen tags",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode0=tk.Radiobutton(frame,text="rapidtags",variable=publishpolicy,value=0,command='')
        mode0.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode1=tk.Radiobutton(frame,text="openai",variable=publishpolicy,value=1,command='')

        b_import_thumb_metas_=tk.Button(frame,text="Step4:更新视频元数据文件",command=lambda: genThumbnailFromTemplate(videosView_video_folder.get(),thumbnail_template_file.get(),mode.get()))
        b_import_thumb_metas_.grid(row = 9, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 

def render_update_schedule(frame,isneed):
    if isneed==True:
        lang='en'
        prefertags=tk.StringVar()
        if len(frame.winfo_children())>0:
            for widget in frame.winfo_children():
                widget.destroy()




        publishpolicy = tk.IntVar()
        # publishpolicy.set(4)

        lab = tk.Label(frame,text="请选择你的发布策略",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode0=tk.Radiobutton(frame,text="私有",variable=publishpolicy,value=0,command='')
        mode0.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode1=tk.Radiobutton(frame,text="公开",variable=publishpolicy,value=1,command='')
        mode1.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode2=tk.Radiobutton(frame,text="定时",variable=publishpolicy,value=2,command='')
        mode2.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode3=tk.Radiobutton(frame,text="unlisted",variable=publishpolicy,value=3,command='')
        mode3.grid(row = 5, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 

        mode4=tk.Radiobutton(frame,text="public&premiere",variable=publishpolicy,value=4,command='')
        mode4.grid(row = 6, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 

        dailycount=tk.StringVar()

        l_dailycount = tk.Label(frame, text=i18labels("dailyVideoLimit", locale=lang, module="g"))
        l_dailycount.grid(row = 7, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 



        e_dailycount = tk.Entry(frame, width=55, textvariable=dailycount)
        e_dailycount.grid(row = 7, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 
        start_publish_date=tk.StringVar()

        l_start_publish_date=tk.Label(frame, text=i18labels("offsetDays", locale=lang, module="g"))
        l_start_publish_date.grid(row = 8, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        e_start_publish_date = tk.Entry(frame, width=55, textvariable=start_publish_date)
        e_start_publish_date.grid(row = 8, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 

        b_import_thumb_metas_=tk.Button(frame,text="Step4:更新视频元数据文件",command=lambda: genThumbnailFromTemplate(videosView_video_folder.get(),thumbnail_template_file.get(),mode.get()))
        b_import_thumb_metas_.grid(row = 9, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
def render_update_meta(frame,isneed):
    if isneed==True:
        lang='en'
        prefertags=tk.StringVar()
        if len(frame.winfo_children())>0:
            for widget in frame.winfo_children():
                widget.destroy()
        
        lab = tk.Label(frame,text="batch modify video metas",bg="lightyellow",width=30)
        # dropdown platform   so they can have diff fields
        l_prefertags = tk.Label(frame, text=i18labels("is_not_for_kid", locale=lang, module="g"))
        l_prefertags.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        el_prefertags = tk.Entry(frame, width=55, textvariable=prefertags)
        el_prefertags.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 

        categories=tk.StringVar()

        l_categories = tk.Label(frame, text=i18labels("categories", locale=lang, module="g"))
        l_categories.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        el_categories = tk.Entry(frame, width=55, textvariable=categories)
        el_categories.grid(row = 1, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 


        is_paid_promotion = tk.BooleanVar()
        # publishpolicy.set(4)

        lab.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode0=tk.Radiobutton(frame,text="私有",variable=is_paid_promotion,value=True,command='')
        mode0.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        mode1=tk.Radiobutton(frame,text="私有",variable=is_paid_promotion,value=False,command='')
        mode1.grid(row = 2, column = 1, columnspan = 3, padx=14, pady=15,sticky='ne') 

            # "is_age_restriction": false,
            # "is_paid_promotion": false,
            # "is_automatic_chapters": true,
            # "is_featured_place": true,
            # "video_language": "",
            # "captions_certification": 0,
            # "video_film_date": "",
            # "video_film_location": "",
            # "license_type": 0,
            # "is_allow_embedding": true,
            # "is_publish_to_subscriptions_feed_notify": true,
            # "shorts_remixing_type": 0,
            # "is_show_howmany_likes": true,
            # "is_monetization_allowed": true,
            # "first_comment": "xxxx",
            # "subtitles": "",
            # "is_not_for_kid": true,
            # "categories": 10,
            # "comments_ratings_policy": 1,

        b_import_thumb_metas_=tk.Button(frame,text="Step4:更新视频元数据文件",command=lambda: genThumbnailFromTemplate(videosView_video_folder.get(),thumbnail_template_file.get(),mode.get()))
        b_import_thumb_metas_.grid(row = 9, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 

def check_folder_thumb_bg(folder):
    supported_thumb_exts=['.jpeg', '.png', '.jpg','webp']
    bg_images=[]
    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:

            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]

                    ext = os.path.splitext(entry.name)[1]
                    if ext in supported_thumb_exts:
                        filepath=os.path.join(r,filename+ext)
                        bg_images.append(filepath)
    if len(bg_images)==0:
        logger.info(f'please choose another bg folder,there is no image found:\n{folder}')
    return bg_images

def check_fields_and_empty_values(data_dict, allowed_fields):
    for key, entry in data_dict.items():
        missing_fields = [field for field in allowed_fields if field not in entry.keys()]

        if missing_fields:
            print(f"The following allowed fields are missing in entry {key}: {', '.join(missing_fields)}")
            return False

        empty_fields = any(entry[field] == "" for field in allowed_fields)

        if empty_fields:
            print(f"There are empty values in one or more of the allowed fields in entry {key}.")
            return False

    return True
def ValidateThumbnailGenMetas(folder,thumbnail_template_file_path,mode_value,thummbnail_bg_folder_path,frame=None):
    passed=True
    bg_images=[]
    if mode_value and mode_value is not None:
        ultra[folder]['thumb_gen_setting']['mode']=mode_value

        if mode_value==1:
            logger.info('extract first frame of video,this extension is not supported yet')
        elif mode_value==2:
            logger.info('extract random key frame of video,this extension is not supported yet')
        elif mode_value==3:
            if thumbnail_template_file_path is None or thumbnail_template_file_path=='':
                logger.error('please choose a thumbtemplate first')
            

            else:
                logger.info(f'start to load thumbnail gen setting json from::\r{thumbnail_template_file_path}')

                if os.path.exists(thumbnail_template_file_path):
                    try:
                        # fp = open(thumbnail_template_file_path, 'r', encoding='utf-8')
                        # setting_json = fp.read()                    
                        setting=json.load(open(thumbnail_template_file_path, 'r', encoding='utf-8')) 
                        templateschema = {
                                        "$schema": "http://json-schema.org/draft-04/schema#",
                                        "type": "object",
                                        "properties": {
                                            "width": {
                                            "type": "integer"
                                            },
                                            "height": {
                                            "type": "integer"
                                            },
                                            "texts": {
                                            "type": "array",
                                            "items": [
                                                {
                                                "type": "object",
                                                "properties": {
                                                    "textType": {
                                                    "type": "string"
                                                    },
                                                    "fontFile": {
                                                    "type": "string"
                                                    },
                                                    "x": {
                                                    "type": "integer"
                                                    },
                                                    "y": {
                                                    "type": "integer"
                                                    },
                                                    "width": {
                                                    "type": "integer"
                                                    },
                                                    "height": {
                                                    "type": "integer"
                                                    },
                                                    "topLeft": {
                                                    "type": "string"
                                                    },
                                                    "topRight": {
                                                    "type": "string"
                                                    },
                                                    "bottomLeft": {
                                                    "type": "string"
                                                    },
                                                    "bottomRight": {
                                                    "type": "string"
                                                    },
                                                    "fontSize": {
                                                    "type": "integer"
                                                    },
                                                    "fontName": {
                                                    "type": "string"
                                                    },
                                                    "gridSize": {
                                                    "type": "integer"
                                                    },
                                                    "isdrawborder": {
                                                    "type": "boolean"
                                                    },                                                    
                                                    "bordersize": {
                                                    "type": "integer"
                                                    },                                                    
                                                    "bordercolor": {
                                                    "type": "string"
                                                    },


                                                    "nearestGridSerialNumber": {
                                                    "type": "integer"
                                                    },
                                                    "fontcolor": {
                                                    "type": "string"
                                                    }
                                                },
                                                "required": [
                                                    "textType",
                                                    "fontFile",
                                                    "x",
                                                    "y",
                                                    "width",
                                                    "height",
                                                    "topLeft",
                                                    "topRight",
                                                    "bottomLeft",
                                                    "bottomRight",
                                                    "fontSize",
                                                    "fontName",
                                                    "gridSize",
                                                    "nearestGridSerialNumber",
                                                    "fontcolor"
                                                ]
                                                }
                                            ]
                                            }
                                        },
                                        "required": [
                                            "width",
                                            "height",
                                            "texts"
                                        ]
                                        }

                        try:
                            logger.info('start to validate template')
                            print(f'start to validate template:\r{setting}')

                            validate(setting, schema=templateschema)
                                #    validate template format ,contain videoID  contain text type ,hints for user to edit temporary
                            ultra[folder]['thumb_gen_setting']['template']=setting['texts']
                            ultra[folder]['thumb_gen_setting']['result_image_width']=setting['width']
                            ultra[folder]['thumb_gen_setting']['result_image_height']=setting['height']
                            ultra[folder]['thumb_gen_setting']['template_path']=thumbnail_template_file_path

                            logger.info(f'validate thumbnail gen template passed')



                            logger.info('start to validate metadata for thumbgen setting')
                            allowedTextTypes=[]
                            for item in setting['texts']:
                                allowedTextTypes.append(item['textType'])
                            df=None                            
                            if len(allowedTextTypes)==0:
                                logger.error('it seemed textType in the template is empty')
                                passed=False
                            else:

                                if ultra[folder]['metafileformat']=='xlsx':
                                    df=pd.read_excel(os.path.join(folder,'videos-meta.xlsx'), index_col=[0])
                                    df.replace('nan', '')
                                    
                                    dfdict=df.iterrows()
                                elif ultra[folder]['metafileformat']=='json':
                                    df=pd.read_json(os.path.join(folder,'videos-meta.json'))  
                                    df.replace('nan', '')
                                    
                                    dfdict=df.items()      
                                elif ultra[folder]['metafileformat']=='csv':
                                    df=pd.read_csv(os.path.join(folder,'videos-meta.csv'), index_col=[0])
                                    df.replace('nan', '')
                                    
                                    dfdict=df.iterrows()
   
                                # List of allowed field names
                                print('reading video meta\r',df)
                                
                                logger.info(f'start to check {allowedTextTypes} defined in template')

                                # Check the data dictionary for allowed fields and empty values in each entry
                                for key, entry in dfdict:
                                    missing_fields = [field for field in allowedTextTypes if field not in entry.keys()]

                                    if missing_fields:
                                        print(f"The following allowed fields are missing in entry {key}: {', '.join(missing_fields)}")
                                        logger.error(f'{missing_fields} filed in defined in template,but not found in metafile,add a column named {missing_fields} in metafile')                                    

                                        passed=False

                                    else:
                                        for field in allowedTextTypes:
                                            value = entry[field]
                                            if not value  or pd.isna(value) or value == "":
                                                logger.error(f'{field} value is empty in entry {key}.')   
                                                passed=False
                                             
                                            else:
                                                logger.info(f'{field} value is {value} in entry {key}.')                                                
                                                # ultra[folder]['videos'][key][field]=value
                            if passed==True:
                                logger.info('validate metadata for thumbgen setting passed')
                                if df is not None:
                                    logger.info('start to update user submited metafile to video assets')
                                    # df.to_json()==str  直接赋值 这个key的值就是str 后面没法拿video的字段值
                                    # print('==1==',type(ultra[folder]['videos']))
                                    # print('==2==',ultra[folder]['videos'])


                                    # print('==3==',type(json.loads(df.to_json())))
                                    # print('==4==',json.loads(df.to_json()))
                                    new=UltraDict()
                                    tmpdict=None
                                    
                                    if ultra[folder]['metafileformat']=='xlsx':
                                        tmpdict=json.loads(df.to_json(orient = 'index'))   


                                    elif ultra[folder]['metafileformat']=='json':
                                        tmpdict=json.loads(df.to_json())   
                                        
 
                                    elif ultra[folder]['metafileformat']=='csv':
                                        tmpdict=json.loads(df.to_json(orient = 'index'))   

                                    for key in tmpdict.keys():
                                        new[key]  =tmpdict[key]   
                                    
                         
                                    
                                    # new=json.loads(df.to_json())
                                    # 如果不先 new一个UltraDict 而是仅仅凭借json.loads(df.to_json() python 内置的dict类型直接赋值，就会出错
                                    # 奇怪的是这种方法不行，得像上面那样遍历每一个key 赋值以后才行
                                    try:
                                        ultra[folder]['videos']=new
                                    except Exception as e:
                                        print(f'wohhha {e}')
                                    logger.info('update user submited metafile to video assets passed')

                            else:
                                logger.error('validate metadata for thumbgen setting failed')

                        
                        except ValidationError as e:
                            logger.error(f'validate thumbnail gen template failed')

                            logger.error(f'this thumb template json dont follow json schema format,check the error msg:\n{e}')
                            passed=False
                    except Exception as e:
                        logger.error(f'this thumb template json can not be loaded and parsed,check the error msg:\n{e}')
                        passed=False
                else:
                    logger.error("template json is not found")
                    passed =False
                    
                logger.info('start to validate bg folder')
     
                if os.path.exists(thummbnail_bg_folder_path):

                    bg_images=check_folder_thumb_bg(thummbnail_bg_folder_path)
                    logger.info(f'bg folder image list :{bg_images}')
                    if len(bg_images)>0:
                        ultra[folder]['thumb_gen_setting']['bg_folder']=thummbnail_bg_folder_path
                        
                        ultra[folder]['thumb_gen_setting']['bg_folder_images']=bg_images


                        for filename in  ultra[folder]['filenames']:
                            bgpath=random.choice(bg_images)
                            if  ultra[folder]['videos'][filename]['thumbnail_local_path'] in [[],'[]']:
                                ultra[folder]['videos'][filename]['thumbnail_bg_image_path']=bgpath
                                logger.info(f"Random assign bg:{bgpath} to  video:{filename}")
                                
                            else:
                                logger.info(f"{ultra[folder]['videos'][filename]} has got thumbnail setup:\r{ultra[folder]['videos'][filename]['thumbnail_local_path']}")


                        logger.info('validate bg folder passed')


                        

                    else:
                        logger.error('validate bg folder failed')
                        passed=False

                        logger.info(f'there is no images under {thummbnail_bg_folder_path}.please choose another folder')
                else:
                    logger.error('validate bg folder failed')
                    
                    logger.error('please choose a valid thummbnail_bg_folder_path ')   
                    passed=False       
        else: 

            logger.error(f'no valid mode:{mode_value}')



    else:
        logger.info('mode value is none')
        passed=False
    print(f'passed is {passed}')
    if passed==True:
        

        
        lab = tk.Label(frame,text="validation passed, go to gen thumbnail",bg="lightyellow")
        lab.grid(row = 10, column = 1,  padx=14, pady=15,sticky='nw')     
        lab.after(5000,lab.destroy)    
        print(f'sync total video assets with thumb gen video meta {ultra[folder]["videos"]}')

        totaljson=os.path.join(folder,videoassetsfilename)

        if os.path.exists(totaljson):
            with open(totaljson,'w') as f:
                f.write(jsons.dumps(ultra[folder]))        
        else:
            with open(totaljson,'a') as f:
                f.write(jsons.dumps(ultra[folder]))    
    else:
        print('pass failed')
    return passed
def openVideoMetaFile(folder):
    print(f"you choose metafile format is:{ultra[folder]['metafileformat']}")
    if ultra[folder]['metafileformat']:
        openLocal(os.path.join(folder,'videos-meta.'+ultra[folder]['metafileformat']))
    else:
        logger.error(f"you dont choose a valid meta fileformat:{ultra[folder]['metafileformat']}")

def genThumbnailFromTemplate(folder,thumbnail_template_file_path,mode_value,thummbnail_bg_folder_path,frame=None):

    passed=ValidateThumbnailGenMetas(folder,thumbnail_template_file_path,mode_value,thummbnail_bg_folder_path,frame)


    print('read video meta')

 
    print('read thumb gen settings')

    template_data=validateSeting(ultra[folder]['thumb_gen_setting']     )
    video_data = ultra[folder]['videos']
    render_style=template_data.get("render_style") 
    result_image_width=int(template_data.get('result_image_width'))
    result_image_height=int(template_data.get('result_image_height'))        
    output_folder=folder
    for video_id, video_info in video_data.items():
        print('1',video_info)
        thumb_gen_setting = template_data.get("template", [])

        ext='.png'
        dict_9_16={
            'xhs':"1080*1440px",
            'dy':"1080*1920px",
            'wx':"1080*1260px",
            'youtube':"1920*1080px",
            'tiktok':"1080*1920px"

        }
        dict_16_9={
            'xhs':"1440*1080px",
            'dy':"1080*608px",
            'wx':"1080*608px",
            'youtube':"1280*720px",
            'tiktok':"1080*608px"


        }
        # 如果想同时为一个视频生成多个平台的缩略图，需要准备不同尺寸的背景图，那么这些背景图读进来会放在bg_images，就不能用原来的随机分配一张到文件里了，
        # 在渲染的时候从bg_images里读取尺寸要求相同的背景图即可
        filename=video_id+ext
        # filename=video_id+"_"+str(result_image_width)+"x"+str(result_image_height)+ext
        outputpath=draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)
        video_data[video_id]['thumbnail_local_path'].append(outputpath)
        if result_image_width > result_image_height:
            basedir=output_folder+os.sep+'16-9'
            os.makedirs(basedir, exist_ok=True)

            # 16:9 aspect ratio        
            for key,value in dict_16_9.items():
                output_folder=basedir+os.sep+key
                os.makedirs(output_folder, exist_ok=True)
                filename=video_id+ext
                value=value.replace("px","")
                result_image_width=value.split("*")[0]
                result_image_height=value.split("*")[-1]
                filename=video_id+"_"+value.replace("*","x")+ext
                result_image_width=int(result_image_width)
                result_image_height=int(result_image_height)


                draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)
        else:
            # 9:16 aspect ratio    
            basedir=output_folder+os.sep+'9-16'

            os.makedirs(basedir, exist_ok=True)
            for key,value in dict_9_16.items():
                output_folder=basedir+os.sep+key
                os.makedirs(output_folder, exist_ok=True)
                filename=video_id+ext
                value=value.replace("px","")
                result_image_width=value.split("*")[0]
                result_image_height=value.split("*")[-1]
                filename=video_id+"_"+value.replace("*","x")+ext
                result_image_width=int(result_image_width)
                result_image_height=int(result_image_height)

                draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)



def render_thumb_gen(frame,isneed,folder):
    if isneed==True:
        if len(frame.winfo_children())>0:
            for widget in frame.winfo_children():
                widget.destroy()        
        global thumbnail_metas_file,thummbnail_bg_folder,thummbnail_bg_file,thumbnail_template_file
        thumbnail_metas_file = tk.StringVar()        
        thummbnail_bg_folder = tk.StringVar()        
        thummbnail_bg_file = tk.StringVar()      

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')     


        thumbmode = tk.IntVar()
        # thumbmode.set(1)

        lab = tk.Label(new_canvas,text="请选择你的缩略图从何而来",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw') 
   
        thumbmode1=tk.Radiobutton(new_canvas,text="手动准备",variable=thumbmode,value=1,command=lambda:render_thumb_update_view(new_canvas,folder,thumbmode,frame))
        thumbmode1.grid(row = 1, column = 1,  padx=14, pady=15,sticky='nw') 
        thumbmode2=tk.Radiobutton(new_canvas,text=" 批量生成",variable=thumbmode,value=2,command=lambda:render_thumb_update_view(new_canvas,folder,thumbmode,frame))
        thumbmode2.grid(row = 1, column = 2,  padx=14, pady=15,sticky='nw') 

        # thumbmode.trace_add('write', render_thumb_update_view(new_canvas,folder,thumbmode))




def render_thumb_update_view(frame,folder,thumbmode,previous_frame=None):
    print('thumbmode',type(thumbmode.get()),thumbmode.get())    

    if len(frame.winfo_children())>0:
        for widget in frame.winfo_children():
            widget.destroy()      
   
    if thumbmode.get() ==1:
        lbl15 = tk.Label(frame, text='两种选择')
        lbl15.grid(row=0,column=0,padx=14, pady=15,sticky='w') 
       
        lbl15 = tk.Label(frame, text='1.手动准备缩略图文件，需放在视频所在文件夹下，且与视频文件同名,完成后再次检测即可',wraplength=600)
        lbl15.grid(row=1,column=0, sticky='w')

        lbl15 = tk.Label(frame, text='2.如果缩略图后文件与视频不在同一个文件夹或者缩略图文件为自定义命名，\r需手动编辑视频元数据中缩略图文件路径,编辑完成后可再次进行检测\r',wraplength=600)
        lbl15.grid(row=2,column=0, sticky='w')



        b_check_metas_=tk.Button(frame,text="edit videometa with local editor",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 6, column = 0, padx=14, pady=15,sticky='nswe') 
        if ultra[folder]['metafileformat']=='json':

            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 5, column = 0, padx=14, pady=15,sticky='nswe') 
            Tooltip(b_edit_thumb_metas, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)
        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 4, column = 0, padx=14, pady=15,sticky='nswe')      


        b_update_metas_=tk.Button(frame,text="validate meta",command='validate thumbpath is there')
        b_update_metas_.grid(row = 7, column = 0,  padx=14, pady=15,sticky='nswe') 

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_thumb_gen(previous_frame,True,folder))
        b_return.grid(row = 8, column =0)   

    else:
        mode = tk.IntVar()
        mode.set(3)
        lab = tk.Label(frame,text="Step1:请选择你的缩略图生成模式",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw')    
        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_thumb_gen(previous_frame,True,folder))
        b_return.grid(row = 1, column = 2,  padx=14, pady=15,sticky='e')              
        mode1=tk.Radiobutton(frame,text="选择视频第一帧作为缩略图背景图",variable=mode,value=1,command='')
        mode1.configure(state = tk.DISABLED)
        Tooltip(mode1, text='you dont install this extension yet' , wraplength=200)

        mode1.grid(row = 2, column = 0,  padx=14, pady=15,sticky='nw') 
        mode2=tk.Radiobutton(frame,text="视频任意关键帧作为背景图",variable=mode,value=2,command='')
        mode2.configure(state = tk.DISABLED)
        Tooltip(mode2, text='you dont install this extension yet' , wraplength=200)

        mode2.grid(row = 2, column = 1,  padx=14, pady=15,sticky='nw') 
        mode3=tk.Radiobutton(frame,text="文件夹中随机一张图片作为背景图",variable=mode,value=3,command='')
        mode3.grid(row = 3, column = 0,  padx=14, pady=15,sticky='nw') 
        Tooltip(mode3, text='please select the bg image folder ' , wraplength=200)


        b_thumbnail_bg_folder=tk.Button(frame,text="select",command=lambda: threading.Thread(target=select_folder(ultra[folder]['thumb_gen_setting']['bg_folder'],thummbnail_bg_folder)).start() )
        b_thumbnail_bg_folder.grid(row = 3, column = 2, padx=14, pady=15,sticky='nswe') 
        e_thumbnail_bg_folder = tk.Entry(frame, textvariable=thummbnail_bg_folder)
        e_thumbnail_bg_folder.grid(row = 3, column =1, padx=14, pady=15,sticky='nswe') 

        lab = tk.Label(frame,text="Step2:请选择你的缩略图模板",bg="lightyellow",width=30)
        lab.grid(row = 5, column = 0,  padx=14, pady=15,sticky='nw')         

        b_check_metas_=tk.Button(frame,text="edit metajson",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 6, column = 1, padx=14, pady=15,sticky='nswe')   
        

        b_edit_thumb=tk.Button(frame,text="create thumbnails template with editor",command=lambda: webbrowser.open_new('file:///{base_dir}/template.html'.format(base_dir=ROOT_DIR)))

        b_edit_thumb.grid(row = 6, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_edit_thumb, text='figure out  heading,subheading,extra text position,font,fontclolor use editor.you can update the json manually to set heading,subheading,extra type,adjust font name and font file ,because fontcolor,fontsize is auto detected, it need to be verify.and set a default bg image for all the videos to use' , wraplength=200)


        thumbnail_template_file = tk.StringVar()        


        b_thumbnail_template_file=tk.Button(frame,text="select",command=lambda: threading.Thread(target=select_file('select thumb template json file',ultra[folder]['thumb_gen_setting']['template_path'],thumbnail_template_file,'json')).start() )
        b_thumbnail_template_file.grid(row = 6, column = 2,  padx=14, pady=15,sticky='nswe') 
        e_thumbnail_template_file = tk.Entry(frame, textvariable=thumbnail_template_file)
        e_thumbnail_template_file.grid(row = 6, column = 1, padx=14, pady=15,sticky='nswe') 
        
        lab = tk.Label(frame,text="Step3:请编辑视频元数据",bg="lightyellow",width=30)
        lab.grid(row = 7, column = 0,  padx=14, pady=15,sticky='nw')         




        b_check_metas_=tk.Button(frame,text="edit videometa",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 8, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_check_metas_, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)

        if ultra[folder]['metafileformat']=='json':

            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 8, column = 1, padx=14, pady=15,sticky='nswe') 
            Tooltip(b_edit_thumb_metas, text='if you dont have json editor locally,try this' , wraplength=200)
        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 8, column = 2, padx=14, pady=15,sticky='nswe')    
        lab = tk.Label(frame,text="Step4:生成缩略图",bg="lightyellow",width=30)
        lab.grid(row = 9, column = 0,  padx=14, pady=15,sticky='nw')         


        b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateThumbnailGenMetas(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_folder.get(),frame))
        b_update_metas_.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nswe') 
        



        b_gen_thumb_=tk.Button(frame,text="gen thumb",command=lambda: genThumbnailFromTemplate(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_folder.get(),frame))
        b_gen_thumb_.grid(row = 11, column =0, padx=14, pady=15,sticky='nswe') 


        b_check_metas_=tk.Button(frame,text="check metajson",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_check_metas_.grid(row = 12, column = 0, padx=14, pady=15,sticky='nswe') 


def printValues(choices):
    for name, var in choices.items():
        print("%s: %s" % (name, var.get()))

def setEntry(str,var):
    var.set(str) 
    
def chooseProxies(ttkframe,username):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)
    
    
    newWindow.title('proxy selection')

    if username=='':
        username='this user account'

    label = tk.Label(newWindow,
                text = f"Select the proxies for {username} below : ",
                font = ("Times New Roman", 10),
                padx = 10, pady = 10)
    # label.pack()
    label.grid(row=0,column=0, sticky=tk.W)
    
 
    
    global city_user,country_user,proxyTags_user,proxyStatus_user,proxy_str
    city_user = tk.StringVar()
    country_user = tk.StringVar()
    proxyTags_user = tk.StringVar()
    proxyStatus_user = tk.BooleanVar()
    global latest_proxy_conditions_user
    latest_proxy_conditions_user = tk.StringVar()
    lbl15 = tk.Label(newWindow, text='by city.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')
    proxy_str = tk.StringVar()

    lbl15.grid(row=1,column=0, sticky=tk.W,  padx=14, pady=15)    

    txt15 = tk.Entry(newWindow,textvariable=city_user)
    txt15.insert(0,'')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=1, sticky=tk.W,  padx=14, pady=15)    

    lbl16 = tk.Label(newWindow, text='by country.')
    lbl16.grid(row=2,column=0, sticky=tk.W,  padx=14, pady=15)    
    txt16 = tk.Entry(newWindow,textvariable=country_user)
    txt16.insert(0,'')
    txt16.grid(row=2,column=1, sticky=tk.W,  padx=14, pady=15)    
    
    lb17 = tk.Label(newWindow, text='by tags.')
    lb17.grid(row=3,column=0, sticky=tk.W,  padx=14, pady=15)    
    txt17 = tk.Entry(newWindow,textvariable=proxyTags_user)
    txt17.insert(0,'')
    txt17.grid(row=3,column=1, sticky=tk.W,  padx=14, pady=15)    

    lb18 = tk.Label(newWindow, text='by status.')
    lb18.grid(row=4,column=0, sticky=tk.W,  padx=14, pady=15)    


    proxyStatus = tk.StringVar()


    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set("Select From Status")
    proxyStatus.trace('w', proxyStatusCallBack)


    proxyStatusbox = ttk.Combobox(newWindow, textvariable=proxyStatus)
    proxyStatusbox.config(values = ('valid', 'invalid'))
    proxyStatusbox.grid(row = 4, column = 1,  padx=14, pady=15)    



    

     
     

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(newWindow)
    frame_canvas.grid(row=6, column=1,columnspan=2,  sticky='nw',  padx=14, pady=15)    
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)     

    # for scrolling vertically
    # for scrolling vertically
    yscrollbar = tk.Scrollbar(frame_canvas)
    yscrollbar.pack(side = tk.RIGHT, fill = 'both')
     
    langlist = tk.Listbox(frame_canvas, selectmode = "multiple",
                yscrollcommand = yscrollbar.set)
    langlist.pack(padx = 10, pady = 10,
            expand = tk.YES, fill = "both")

    def CurSelet(event):
        listbox = event.widget
        # values = [listbox.get(idx) for idx in listbox.curselection()]
        selection=listbox.curselection()
        # picked = listbox.get(selection[1])
        print(selection,list(selection),listbox.get(0))
        tmp=''
        for i in list(selection):
            tmp=tmp+listbox.get(i)+';'
        proxy_str.set(tmp)
        print('000000',proxy_str.get())
        if len(list(selection))==3:
            lbl15 = tk.Label(newWindow, text='you have reached 3 proxy limit for one account.dont select anymore')
            lbl15.grid(row=6,column=2, sticky=tk.W)
            lbl15.after(5*1000,lbl15.destroy)        
        
        elif len(list(selection))>3:
            print('you should choose no more than 3 proxy for one account')
            lbl15 = tk.Label(newWindow, text='you should choose no more than 3 proxy for one account.please remove')
            lbl15.grid(row=6,column=2, sticky=tk.W)
            lbl15.after(3*1000,lbl15.destroy)
        else:
            lbl15 = tk.Label(newWindow, text='you can add at least 1 and max 3 proxy for one account.')
            lbl15.grid(row=6,column=2, sticky=tk.W)
            lbl15.after(500,lbl15.destroy)

    langlist.bind('<<ListboxSelect>>',CurSelet)
    btn5= tk.Button(newWindow, text="Get proxy list", padx = 0, 
                    pady = 0,command = lambda: threading.Thread(target=
                    filterProxiesLocations(newWindow,langlist,prod_engine,logger,city_user.get(),country_user.get(),proxyTags_user.get(),proxyStatusbox.get(),latest_proxy_conditions_user.get())).start())
    btn5.grid(row=5,column=2, sticky=tk.W)    
    btn6= tk.Button(newWindow, text="add selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=setEntry(proxy_str.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn6.pack(side='left')          
    btn6.grid(row=7,column=2, sticky=tk.W)

def bulkImportUsers(ttkframe):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)
    #缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0,1), weight=1)

    newWindow.title('user bulk import')
    
    input_canvas = tk.Frame(newWindow)
    input_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')    
    

    lbl15 = tk.Label(input_canvas, text='input account info with \\n separator')
    lbl15.grid(row=0,column=0, sticky=tk.W)
    

        
    
    
    
    from tkinter.scrolledtext import ScrolledText
    textfield = ScrolledText(input_canvas, wrap=tk.WORD)
    textfield.grid(row = 1, column = 0, columnspan = 5, padx=14, pady=15)
    textfield.bind_all("<Control-c>",_copy)

    
    b_choose_proxy=tk.Button(input_canvas,text="load  from file",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_choose_proxy.grid(row=2,column=0, sticky=tk.W)

    
    
    hints='bulk pull sessionid and cookies'

    b_bulk_pull_cookies=tk.Button(ttkframe,text=hints,command=lambda: threading.Thread(target=bulkImportUsers(ttkframe)).start() )
    # b_bulk_import_users.place(x=10, y=450)    
    b_bulk_pull_cookies.grid(row = 9, column = 4, columnspan = 3, padx=14, pady=15)        
    
    res_canvas = tk.Frame(newWindow,width=int(0.5*width))
    res_canvas.grid(row=0, column=10,pady=(5, 0), sticky='ne')    
    
        
    global vid
    vid = tk.StringVar()
    lbl15 = tk.Label(res_canvas, text='Filter by Username.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(res_canvas, width=11,textvariable=vid)
    txt15.insert(0,'input username')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=0,column=1, sticky=tk.W)
    
    
    btn5= tk.Button(res_canvas, text="Get user list", padx = 10, pady = 10,command = lambda: threading.Thread(target=filterProxiesLocations(prod_engine,logger,vid.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn5.pack(side='left')       
    btn5.grid(row=0,column=5, sticky=tk.W)    
    
    
    
    # treeview_flight
    tree = ttk.Treeview(res_canvas, height = 20, column = 8)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 1, column = 0, columnspan = 20, padx=14, pady=15)

    tree.heading('#0', text = 'Account No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'username')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'password')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'platform')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'proxies')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'Cookiefile')
    tree.column('#5', anchor = 'center', width = 80)
    tree.heading('#6', text = 'create. Time')
    tree.column('#6', anchor = 'center', width = 80)
    tree.heading('#7', text = 'updated. Time')
    tree.column('#7', anchor = 'center', width = 80)
def saveUser(engine,platform,username,password,proxy,cookies,if_exists=None):
    if not if_exists in ['append','replace']:
        if_exists='append'
    if platform is None:
        logger.info('please choose a platform')
    if username is None:
        logger.error('please provide  a username')
    else:    
        if password is None:
            logger.info('you dont provide password')        
            if cookies is None:
                logger.error('please provide a cookie file without  password')        
                  
        list_platform=[platform]
        list_ids=[pd.Timestamp.now().value ]
        list_username=[username]
        list_password=[password]
        list_proxy=[proxy]
        list_cookies=[cookies]
        list_inserted_ats=[datetime.now()]
        account_df= pd.DataFrame({'username':list_username,'id':list_ids,"platform":list_platform,'password':list_password,'cookies':list_cookies,"proxy":list_proxy,'inserted_at':list_inserted_ats})
            
        print('1000000000',account_df)

        account_df['updated_at']=None  
        is_proxy_ok=pd2table(engine,'accounts',account_df,logger,if_exists=if_exists)
    
def  queryAccounts(newWindow,tree,engine,logger,username,platform,latest_conditions_value):



    availableProxies=[]
    now_conditions='platform:'+platform+';username:'+username

    
    if set(list(latest_conditions_value))==set(now_conditions):
        logger.info('you account filter conditions without any change,keep the same')

    else:    
        if username is not None and username !='' and 'input' not in username:
        # or platform is not None and platform !='' :
            query = f"SELECT * FROM accounts where"
            clause=[]
            if username is not None and username !='':
                clause.append(f" username regexp '{username}'")
            if platform is not None and platform !='':
                clause.append(f" platform regexp '{platform}'")


            query=query+' AND '.join(clause)+" ORDER by inserted_at DESC"

        else:
            query = f"SELECT * FROM accounts ORDER by inserted_at DESC"


        try:
            logger.info(f'start a new query:\n {query}')
            
            table_name='accounts'
            tableexist_query=f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME= '{table_name}'"
            tableexist_query_sqlite=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"

            tableexist=query2df(engine,tableexist_query_sqlite,logger)
            if  tableexist is None:
                hints='there is no  records for query.add proxy before then try again'
                    
                lbl15 = tk.Label(newWindow,bg="lightyellow", text=hints)
                lbl15.grid(row=6,column=2, sticky=tk.W)
                lbl15.after(2000,lbl15.destroy)                
            else:
                
                db_rows = query2df(engine,query,logger)
                
                records = tree.get_children()                
                if db_rows is not None:
                    logger.info(f'we found {len(db_rows)} record matching ')
                    i=0
                    for element in records:
                        tree.delete(element) 
                    for row in db_rows.itertuples():
                        tree.insert(
                            "", 0, text=row.id, values=(row.username,row.password,row.platform,row.proxy, row.cookies, row.inserted_at, row.updated_at)
                        )                    
                        

                        
                    
                    latest_proxy_conditions_user.set(now_conditions)
                    logger.info(f'search and display finished:\n{query}')
                else:
                    logger.info(f'there is no matching records for query:\n{query}')
                    hints=''
                    query = f"SELECT * FROM accounts"
                    if query2df(engine,query,logger) is not None and len( query2df(engine,query,logger))>0:
                        hints='there is no matching records for query. try to set another condition'
                    else:
                        hints='there is no  records for query.add proxy before then try again'
                        
                    lbl15 = tk.Label(newWindow,bg="lightyellow", text=hints)
                    lbl15.grid(row=6,column=2, sticky=tk.W)
                    lbl15.after(2000,lbl15.destroy)
        except Exception as e:
            logger.error(f'search failed error:{e}') 

def accountView(frame,ttkframe,lang):

    global proxy_option_account

    channel_cookie_user= tk.StringVar()
    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()


    l_platform = tk.Label(ttkframe, text=i18labels("platform", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_platform.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15)    




    def socialplatformOptionCallBack(*args):
        print(socialplatform.get())
        print(socialplatform_box.current())

    socialplatform = tk.StringVar()
    socialplatform.set("Select From Platforms")
    socialplatform.trace('w', socialplatformOptionCallBack)


    socialplatform_box = ttk.Combobox(ttkframe, textvariable=socialplatform)
    socialplatform_box.config(values =('youtube', 'tiktok', 'douyin'))
    socialplatform_box.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15)    


    # def selectedplatform(event):
    #     box = event.widget
    #     print('selected platform is :',box.get())
    #     keepplatform=box.get()
    #     box_platform.current()    
        
    # box_platform['values'] = ('youtube', 'tiktok', 'douyin')
    # index=box_platform['values'].index(keepplatform)
    # box_platform.current(index)    

    # box_platform.bind("<<ComboboxSelected>>", selectedplatform)



    l_username = tk.Label(ttkframe, text=i18labels("username", locale=lang, module="g"))
    # l_username.place(x=10, y=150)
    l_username.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15)    

    e_username = tk.Entry(ttkframe, width=int(width*0.01), textvariable=username)
    # e_username.place(x=10, y=180)
    e_username.grid(row = 2, column = 5, columnspan = 3, padx=14, pady=15)    

    l_password = tk.Label(ttkframe, text=i18labels("password", locale=lang, module="g"))
    # l_password.place(x=10, y=210)
    e_password = tk.Entry(ttkframe, width=int(width*0.01), textvariable=password)
    # e_password.place(x=10, y=240)

    l_password.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15)    
    e_password.grid(row = 3, column = 5, columnspan = 3, padx=14, pady=15)    


    l_proxy_option = tk.Label(ttkframe, text=i18labels("proxySetting", locale=lang, module="g"))
    # l_proxy_option.place(x=10, y=270)
    
    l_proxy_option.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15)    

    e_proxy_option = tk.Entry(ttkframe, textvariable=proxy_option_account)
    # e_proxy_option.place(x=10, y=300)
    e_proxy_option.grid(row = 5, column = 3, columnspan = 3, padx=14, pady=15)    

    b_choose_proxy=tk.Button(ttkframe,text="choose",command=lambda: threading.Thread(target=chooseProxies(ttkframe,username.get())).start() )
    
    # b_choose_proxy.place(x=50, y=270)    
    b_choose_proxy.grid(row = 4, column = 3, columnspan = 2, padx=14, pady=15)    




    l_channel_cookie = tk.Label(ttkframe, text=i18labels("cookiejson", locale=lang, module="g"))
    # l_channel_cookie.place(x=10, y=330)
    l_channel_cookie.grid(row = 6, column = 0, columnspan = 3, padx=14, pady=15)    

    e_channel_cookie = tk.Entry(ttkframe, textvariable=channel_cookie_user)
    # e_channel_cookie.place(x=10, y=360)
    e_channel_cookie.grid(row = 7, column = 3, columnspan = 3, padx=14, pady=15)    

    b_channel_cookie=tk.Button(ttkframe,text="Select",command=lambda: threading.Thread(target=select_cookie_file(channel_cookie_user)).start() )
    # b_channel_cookie.place(x=10, y=390)    
    b_channel_cookie.grid(row = 6, column = 3, columnspan = 2, padx=14, pady=15)    

    
    b_channel_cookie_gen=tk.Button(ttkframe,text="pull",command=auto_gen_cookie_file)
    # b_channel_cookie_gen.place(x=100, y=390)    
    b_channel_cookie_gen.grid(row = 6, column = 5, columnspan = 3, padx=14, pady=15)    
    def if_existsOptionCallBack(*args):
        print(if_exists.get())
        print(if_exists_box.current())

    if_exists = tk.StringVar()
    if_exists.set("if the same account exists")
    if_exists.trace('w', if_existsOptionCallBack)


    if_exists_box = ttk.Combobox(ttkframe, textvariable=if_exists)
    if_exists_box.config(values =('replace', 'append'))
    if_exists_box.grid(row = 9, column = 5, columnspan = 3, padx=14, pady=15)    
    
    b_save_user=tk.Button(ttkframe,text="save user",command=lambda: threading.Thread(target=saveUser(prod_engine,socialplatform.get(),username.get(),password.get(),proxy_option_account.get(),channel_cookie_user.get(),if_exists=if_exists.get())).start() )
                         
    # b_save_user.place(x=10, y=420)        
    b_save_user.grid(row = 10, column = 0, columnspan = 3, padx=14, pady=15)    

    b_bulk_import_users=tk.Button(ttkframe,text="bulk import",command=lambda: threading.Thread(target=bulkImportUsers(ttkframe)).start() )
    # b_bulk_import_users.place(x=10, y=450)    
    b_bulk_import_users.grid(row = 10, column = 4, columnspan = 3, padx=14, pady=15)    

        
    

    global q_username_account,latest_user_conditions_user,q_platform_account
    q_username_account = tk.StringVar()
    q_platform_account = tk.StringVar()

    latest_user_conditions_user=tk.StringVar()
    lbl15 = tk.Label(frame, text='By username.')
    # lbl15.place(x=430, y=15, anchor=tk.NE)
    lbl15.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15)    
    txt15 = tk.Entry(frame, width=11,textvariable=q_platform_account)
    txt15.insert(0,'input username')
    txt15.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15)    


    lb18 = tk.Label(frame, text='By platform.')
    lb18.grid(row=0,column=3, sticky=tk.W)


    q_platform = tk.StringVar()


    def q_platformOptionCallBack(*args):
        print(q_platform.get())
        print(q_platform_accountbox.current())

    q_platform.set("Select From Platforms")
    q_platform.trace('w', q_platformOptionCallBack)


    q_platform_accountbox = ttk.Combobox(frame, textvariable=q_platform)
    q_platform_accountbox.config(values =('youtube', 'tiktok', 'douyin'))
    q_platform_accountbox.grid(row = 1, column = 2, columnspan = 3, padx=14, pady=15)    




    
    # txt15.place(x=580, y=15, anchor=tk.NE)
    btn5= tk.Button(frame, text="Get Info", command = lambda: threading.Thread(target=queryAccounts(ttkframe,tree,prod_engine,logger,q_platform_account.get(),q_platform_account.get(),latest_user_conditions_user.get())).start())
    # btn5.place(x=800, y=15, anchor=tk.NE)    

    btn5.grid(row = 0, column =3, columnspan = 5, padx=14, pady=15)    




    # treeview_flight
    tree = ttk.Treeview(frame, height = 20,column = 8)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 2, column = 0, columnspan = 10, padx=14, pady=15)

    tree.heading('#0', text = 'Account No.')
    tree.column('#0', anchor = 'center', width = 90)
    tree.heading('#1', text = 'username')
    tree.column('#1', anchor = 'center', width = 90)
    tree.heading('#2', text = 'password')
    tree.column('#2', anchor = 'center', width = 90)
    tree.heading('#3', text = 'platform')
    tree.column('#3', anchor = 'center', width = 90)
    tree.heading('#4', text = 'proxies')
    tree.column('#4', anchor = 'center', width = 90)
    tree.heading('#5', text = 'Cookiefile')
    tree.column('#5', anchor = 'center', width = 90)
    tree.heading('#6', text = 'create. Time')
    tree.column('#6', anchor = 'center', width = 90)
    tree.heading('#7', text = 'updated. Time')
    tree.column('#7', anchor = 'center', width = 90)


    
    
def  queryTasks(tree,engine,logger,vid):



    query = "SELECT * FROM uploadtasks ORDER by inserted_at DESC"
    print('vid',vid,type(vid))
    if vid is not None and vid !='' and  not "input" in vid:
        query=f"SELECT * FROM uploadtasks  where id={vid}"
    try:
        db_rows = query2df(engine,query,logger)
        records = tree.get_children()
        for element in records:
            tree.delete(element) 
        for row in db_rows.itertuples():
            tree.insert(
                "", 0, text=row.id, values=(row.video_title,row.video_description,row.status,row.release_date, row.release_date_hour, row.publish_policy, row.uploaded_at, row.video_local_path)
            )
    except:
        print('keep the same')    


def getBool(var): # get rid of the event argument
    print(var.get())
    value=var.get()

def createTaskMetas(left,right):
    creatTaskWindow = tk.Toplevel(right)
    creatTaskWindow.geometry(window_size)
    username = tk.StringVar()

    # creatTaskWindow.focus_force()
    # creatTaskWindow.grab_set()
    
    creatTaskWindow.title('create tasks from scratch')

    if username=='':
        username='this user account'

    label = tk.Label(creatTaskWindow,
                text = f"If you are new,try to start from a folder with videos",
                font = ("Times New Roman", 10),
                padx = 10, pady = 10)
    # label.pack()
    label.grid(row=0,column=0, sticky=tk.W)
    
 
    
    global videometafile,country_user,uploadsettingid,proxyStatus_user,choosedAccounts
    videometafile = tk.StringVar()
    uploadsettingid = tk.StringVar()
    choosedAccounts = tk.StringVar()
    global latest_proxy_conditions_user
    latest_proxy_conditions_user = tk.StringVar()
    lbl15 = tk.Label(creatTaskWindow, text='load video metas from file')
    lbl15.grid(row=1,column=0, padx=14, pady=15, sticky=tk.W)

    txt15 = tk.Entry(creatTaskWindow,textvariable=videometafile)
    txt15.insert(0,'')
    b_thumbnail_template_file=tk.Button(creatTaskWindow,text="select",command=lambda: threading.Thread(target=select_file('select video meta  file','',videometafile,'all',creatTaskWindow)).start() )
    b_thumbnail_template_file.grid(row = 1, column = 2,  padx=14, pady=15,sticky='nswe')     
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=1, sticky=tk.W)

    button1 = ttk.Button(creatTaskWindow, text="Start from video folder", command=lambda: (creatTaskWindow.withdraw(),tab_control.select(5)))
    button1.grid(row=1,column=3, sticky=tk.W)

    uploadStrategy = tk.StringVar()
    uploadStrategy.set("start from template")


    # uploadStrategybox = ttk.Combobox(creatTaskWindow, textvariable=uploadStrategy)
    # uploadStrategybox.config(values = ('平均分配','随机分配','智能元数据分配'))
    # uploadStrategybox.grid(row = 3, column = 2, padx=14, pady=15)    


    
    # lb17 = tk.Label(creatTaskWindow, text='load upload setting')
    # lb17.grid(row=3,column=0, sticky=tk.W)
    # txt17 = tk.Entry(creatTaskWindow,textvariable=uploadsettingid)
    # txt17.insert(0,'')
    # txt17.grid(row=3,column=1, sticky=tk.W)





    
    lb17 = tk.Label(creatTaskWindow, text='choose accounts')
    lb17.grid(row=4,column=0, padx=14, pady=15,  sticky=tk.W)
    txt17 = tk.Entry(creatTaskWindow,textvariable=choosedAccounts)
    txt17.insert(0,'')
    txt17.grid(row=4,column=1, sticky=tk.W)


    button1 = ttk.Button(creatTaskWindow, text="ADD", command=lambda:chooseAccountsView(creatTaskWindow,choosedAccounts))
    button1.grid(row=4,column=2, sticky=tk.W)


    lb18 = tk.Label(creatTaskWindow, text='Runs on.')
    lb18.grid(row=5,column=0,  padx=14, pady=15, sticky=tk.W)


    deviceType = tk.StringVar()


    def deviceTypeCallBack(*args):
        print(deviceType.get())
        print(deviceTypebox.current())
        if 'browser' in deviceType.get():
            browserType = tk.StringVar()

            browserType.set("Select From Browsers")
            def browserTypeCallBack(*args):
                print(browserType.get())
                print(browserTypebox.current())
            browserType.trace('w', browserTypeCallBack)

            browserTypebox = ttk.Combobox(creatTaskWindow, textvariable=browserType)
            browserTypebox.config(values = ('firefox', 'webkit','chrome'))
            browserTypebox.grid(row = 5, column = 2,padx=14, pady=15, sticky='w')   


    deviceType.set("Select From device")
    deviceType.trace('w', deviceTypeCallBack)


    deviceTypebox = ttk.Combobox(creatTaskWindow, textvariable=deviceType)
    deviceTypebox.config(values = ('embed browser', 'adspower','phone emulator','iphone','android'))
    deviceTypebox.grid(row = 5, column = 1, padx=14, pady=15, sticky='w')   

    is_open_browser = tk.BooleanVar()
    is_open_browser.set(True)
    is_open_browser.trace('w', lambda *_: print("The value is_open_browser was changed"))    
    l_is_open_browser = tk.Label(creatTaskWindow, text='静默模式')

    l_is_open_browser.grid(row = 6, column = 0,  padx=14, pady=15,sticky='w') 
    checkbutton = tk.Checkbutton(creatTaskWindow, text="是", variable=is_open_browser,command = lambda:getBool(is_open_browser))
    checkbutton.grid(row=6, column=1, padx=14, pady=15, sticky='w')

    is_debug = tk.BooleanVar()
    is_debug.set(True)
    l_is_debug = tk.Label(creatTaskWindow, text='是否调试')
    is_debug.trace('w', lambda *_: print("The value is_debug was changed"))    

    l_is_debug.grid(row = 9, column = 0,  padx=14, pady=15,sticky='w') 
    checkbutton = tk.Checkbutton(creatTaskWindow, text="是", variable=is_debug,command =lambda: getBool(is_debug))
    checkbutton.grid(row=9, column=1, padx=14, pady=15, sticky='w')

    is_record_video = tk.BooleanVar()
    is_record_video.set(True)
    is_record_video.trace('w', lambda *_: print("The value is_record_video was changed"))    

    l_is_record_video = tk.Label(creatTaskWindow, text='是否录制视频')
    l_is_record_video.grid(row=7, column=0, padx=14, pady=15, sticky='w')


    checkbutton = tk.Checkbutton(creatTaskWindow, text="是", variable=is_record_video,command = lambda:getBool(is_record_video))
    checkbutton.grid(row=7, column=1, padx=14, pady=15, sticky='w')


    wait_policy = tk.IntVar()
    wait_policy.set(3)
    l_wait_policy = tk.Label(creatTaskWindow, text='视频处理等待机制')
    wait_policy.trace('w', lambda *_: print("The value wait_policy was changed"))    

    l_wait_policy.grid(row = 8, column = 0, padx=14, pady=15,sticky='w') 
    mode0=tk.Radiobutton(creatTaskWindow,text="after processing success",variable=wait_policy,value=1,command=lambda: getBool(wait_policy))
    mode0.grid(row = 8, column = 1, padx=14, pady=15,sticky='w') 
    mode1=tk.Radiobutton(creatTaskWindow,text="after uploading success",variable=wait_policy,value=2,command=lambda: getBool(wait_policy))
    mode1.grid(row = 8, column = 2, padx=14, pady=15,sticky='w') 
    mode1=tk.Radiobutton(creatTaskWindow,text="after copyright check success",variable=wait_policy,value=3,command=lambda: getBool(wait_policy))
    mode1.grid(row = 8, column = 3, padx=14, pady=15,sticky='w') 
    btn6= tk.Button(creatTaskWindow, text="gen task meta file", padx = 10, pady = 10,command = lambda: threading.Thread(target=setEntry(account_var.get(),choosedAccounts)).start())     
    btn6.grid(row=10,column=1, sticky=tk.W)
    def uploadStrategyCallBack(*args):
        print(uploadStrategy.get())
        # print(uploadStrategybox.current())
        # if uploadStrategybox.current()==0 or uploadStrategy.get()=='单帐号' :
        #     pass







    uploadStrategy.trace('w', uploadStrategyCallBack)

    # uploadPlatform = tk.StringVar()
    # uploadPlatform.set("choose target platform")


    # uploadPlatformbox = ttk.Combobox(creatTaskWindow, textvariable=uploadPlatform)
    # uploadPlatformbox.config(values = ('tiktok', 'youtube','xhs'))
    # uploadPlatformbox.grid(row = 3, column = 3, padx=14, pady=15)    
    # def uploadPlatformboxCallBack(*args):
    #     print(uploadPlatform.get())
    #     print(uploadPlatformbox.current())

    # uploadPlatform.trace('w', uploadPlatformboxCallBack)

    
def genVideoMetas():
    dbm=DBM('prod')
    save_setting(dbm)
# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        video_folder_path = setting['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            if os.path.exists(video_folder_path):
                check_video_thumb_pair(dbm,video_folder_path,False)
            else:
                print("there is no defined video dir.")
        else:
            print("pls choose file or folder")
    print('save metas to json /csv excel format for later processing')

def validateMetafile(engine,ttkframe,metafile):
    logger.info('load task metas to database .create upload task for each video')


    if metafile !='' and metafile is not None:
        
        logger.info(f'you select task metafile is {metafile}')
        if  os.path.exists(metafile):
            # check_video_thumb_pair(dbm,video_folder_path,True)
            logger.info('start to load  and parse meta file')

            
            settingidsdict={}
            try:
                data = json.load(open(metafile))
            # df = pd.read_json(metafile)     
            except:
                logger.error(f'{metafile} cannot be read') 
            else:
                try:
                    settings=data["uploadSetting"]

                    for setting in settings:
                        logger.info(f'setting json is {setting}')

                        for key in ['proxy_option','channel_cookie_path']:
                            if setting.get(key)==None:
                                logger.error(f" this field {key} is required in given setting json data")
                                raise ValueError(f"this field {key} is required  in given data")
                                
                        for key in ['timeout','timeout','debug','wait_policy','is_record_video','username','password']:
                            if setting.get(key)==None:
                                logger.info(f"no {key} filed provide in given setting json data,we can use default value")

                        if setting.get('browser_type')==None:
                            setting['browser_type']='firefox'        
                            logger.info('we use browser_type =firefox')
                        else:
                            if type(setting.get('browser_type'))!=str:
                                logger.error('browser_type should be one of "chromium", "firefox", "webkit"')
                            else:
                                if not setting.get('browser_type') in ["chromium", "firefox", "webkit"]:
                                    logger.error('browser_type should be one of"chromium", "firefox", "webkit"')

                        if setting.get('platform')==None:
                            setting['platform']='youtube'        
                            logger.info('you dont specify platform field,we use default youtube')
                        else:
                            if type(setting.get('platform'))!=str:
                                logger.error('platform should be one of "youtube", "tiktok", "douyin"')
                            else:
                                if not setting.get('platform') in ["youtube", "tiktok", "douyin"]:
                                    logger.error('platform should be one of "youtube", "tiktok", "douyin"')


                        if setting.get('timeout')==None:
                            setting['timeout']=200000
                            logger.info("you dont specify timeout field,we use default 200*1000")
                        else:
                            if type(setting.get('timeout'))!=int:
                                logger.error('timeout should be integer,such as 20*1000=20000, 20 seconds')
                        if setting.get('is_open_browser')==None:
                            setting['is_open_browser']=True
                            logger.info("you dont specify is_open_browser field,we use default True")
                            
                        else:
                            
                            if type(setting.get('is_open_browser'))==bool:
                                pass
                            elif type(setting.get('is_open_browser'))==str and setting.get('is_open_browser').lower() not in ['true','false']:

                                logger.error(f'is_open_browser is {setting.get("is_open_browser")} of {type(setting.get("is_open_browser"))},it should be bool, true or false')

                        if setting.get('debug')==None:
                            setting['debug']=True
                            logger.info("you dont specify debug field,we use default True")
                            
                        else:
                            
                            if type(setting.get('debug'))==bool:
                                pass
                            elif type(setting.get('debug'))==str and setting.get('debug').lower() not in ['true','false']:

                                logger.error(f'debug is {setting.get("debug")} of {type(setting.get("debug"))},it should be bool, true or false')

               
                        if setting.get('wait_policy')==None:
                            setting['wait_policy']=2        
                            logger.info("you dont specify wait_policy field,we use default 2")
                        else:
                            if type(setting.get('wait_policy'))!=int:
                                logger.error('wait_policy should be one of 0,1,2')
                            else:
                                if not setting.get('wait_policy') in [0,1,2]:
                                    logger.error('wait_policy should be one of 0,1,2')

                        if setting.get('is_record_video')==None:
                            setting['is_record_video']=True        
                            logger.info("you dont specify is_record_video field,we use default True")
                            
                        else:
                            
                            if type(setting.get('is_record_video'))==bool:
                                pass
                            elif type(setting.get('is_record_video'))==str and setting.get('is_record_video').lower() not in ['true','false']:

                                logger.error(f'is_record_video is {setting.get("is_record_video")} of {type(setting.get("is_record_video"))},it should be bool, true or false')


                        df_setting=    pd.json_normalize(setting)

                        newid=pd.Timestamp.now().value  
                        if setting.get('id')==None:
                            df_setting['id']=newid  
                            logger.info(f"you dont specify id field,we generate a new {newid} for this setting")
                            
                            settingidsdict[newid]=newid   
                            logger.info(f"setting old id and new ids mapping dicts is {settingidsdict}")

                        else:
                            if type(setting['id'])==str:
                                try:
                                    setting['id']=int(setting['id'])
                                    
                                except Exception as e:
                                    logger.error(f'setting["id"] should be a int value')
                            settingidsdict[setting['id']]=newid                               
                            logger.info(f"you  specify id field,we add a mapping to {setting['id']}  of {type({setting['id']} )}a new {newid} for this setting")
                            df_setting['id']=newid  

                            logger.info(f"setting old id and new ids mapping dicts is {settingidsdict}")

                        df_setting['inserted_at']=datetime.now()           

                        logger.info('start to check whether setting duplicate or save as new')

                        table_name = "uploadsetting"
                        
                        is_setting_ok=pd2table(engine,table_name,df_setting,logger,if_exists='replace')

                    query = 'SELECT * FROM uploadsetting'
                    # Display the results
                    df=query2df(engine,query,logger)
                    print(df.columns)
                    print(df.head(3))

            # prepareuploadsession( dbm,videopath,thumbpath,filename,start_index,setting['channelname'],settingid)

                except Exception as e:
                    logger.error(f'there is no uploadSetting key in  your metajson:{e}')
                try:
                    videos=data["videos"]
                    logger.info(f'we found {len(videos)} videos to be load in db')
                    
                    for idx,video in enumerate(videos):
                        logger.info(f'start to process {str(idx)}th\n:{video} ')
                    
                        for key in ['video_local_path','video_title','video_description','thumbnail_local_path','publish_policy','tags']:
                            if video.get(key)==None:
                                logger.error(f"these {key} field is required,No target{key} in given video json data")
                                raise ValueError(f"these {key} field is required,No target{key} in given video json data")
                            if key in['video_local_path','thumbnail_local_path']:
                                if os.path.exists(video.get(key))==False:
                                    logger.error(f"these {key} field is required,and check whether local file exists")
                                    raise ValueError(f"these {key} field is required,and check whether local file exists")
                        for key in ['video_film_date','video_film_location','first_comment','subtitles']:
                            video[key]=None 
                            logger.info(f'now we have no rules about {key} validation ')

                        for key in ['is_allow_embedding','is_publish_to_subscriptions_feed_notify',
                                    'is_automatic_chapters','is_featured_place', 'is_not_for_kid',
                                    'is_show_howmany_likes',
                                    'is_monetization_allowed']:

                            if video.get(key)==None:
                                video[key]=True 
                                logger.info(f"This field {key} is optional in given video json data,we can use default true")
                            else:
                                if video.get(key) not in ['true','false']:
                                    logger.error(f'{key} should be bool, true or false') 


                        for key in ['is_age_restriction','is_paid_promotion']:
                            if video.get(key)==None:
                                video[key]=False 

                                logger.info(f"This field {key} is optional in given video json data,we can use default false")
                            else:
                                if video.get(key) not in ['true','false']:
                                    logger.error(f'{key} should be bool, true or false') 

                        if video.get('categories')==None:
                            video['categories']=None      
                            logger.info('we use categories =none')
                        else:
                            if type(video.get('categories'))!=int:
                                logger.error('categories should be one of 0,1,....,14')
                            else:
                                if not video.get('categories') in range(0,15):
                                    logger.error('categories should be one of 0,1,2,3..........,14')

                        if video.get('license_type')==None:
                            video['license_type']=0       
                            logger.info('we use license_type =0')
                        else:
                            if type(video.get('license_type'))!=int:
                                logger.error('license_type should be one of 0,1')
                            else:
                                if not video.get('license_type') in range(0,2):
                                    logger.error('license_type should be one of 0,1')
                        if video.get('shorts_remixing_type')==None:
                            video['shorts_remixing_type']=0       
                            logger.info('we use shorts_remixing_type =0')
                        else:
                            if type(video.get('shorts_remixing_type'))!=int:
                                logger.error('shorts_remixing_type should be one of 0,1,2')
                            else:
                                if not video.get('shorts_remixing_type') in range(0,3):
                                    logger.error('shorts_remixing_type should be one of 0,1,2')
                        if video.get('comments_ratings_policy')==None:
                            video['comments_ratings_policy']=1       
                            logger.info('we use comments_ratings_policy =1')
                        else:
                            if type(video.get('comments_ratings_policy'))!=int:
                                logger.error('comments_ratings_policy should be one of 0,1,2,3,4,5')
                            else:
                                if not video.get('comments_ratings_policy') in range(0,6):
                                    logger.error('comments_ratings_policy should be one of 0,1,2,3,4,5')



                        if video.get('captions_certification')==None:
                            video['captions_certification']=0       
                            logger.info('we use captions_certification =0')
                        else:
                            if type(video.get('captions_certification'))!=int:
                                logger.error('captions_certification should be one of 0,1,2,3,4,5')
                            else:
                                if not video.get('captions_certification') in range(0,6):
                                    logger.error('captions_certification should be one of 0,1,2,3,4,5')
                        if video.get('video_language')==None:
                            video['video_language']=None       
                            logger.info('we use video_language =none')
                        else:
                            if type(video.get('video_language'))!=int:
                                logger.error('video_language should be one of 0,1,2,3,4...23')
                            else:
                                if not video.get('video_language') in range(0,24):
                                    logger.error('video_language should be one of 0,1,2,3,4...23')

                        if video.get('publish_policy')==None:
                            video['publish_policy']=0       
                            logger.info('we use publish_policy =0')
                        else:
                            if type(video.get('publish_policy'))!=int:
                                logger.error('publish_policy should be one of 0,1,2,3,4')
                            else:
                                if not video.get('publish_policy') in [0,1,2,3,4]:
                                    logger.error('publish_policy should be one of 0,1,2,3,4')
                                else:
                                    # check release date and datehour exists
                                    if video.get('publish_policy')==2:
                                        if video.get('release_date')==None:
                                            video['release_date']=None      
                                            logger.info('we use release_date ==none')  
                                        else:
                                            if video.get('release_date_hour')==None:     
                                                logger.info('we use default release_date_hour 10:15')    
                                            elif video.get('release_date_hour') not in availableScheduleTimes:
                                                logger.error(f'we use choose one from {availableScheduleTimes}') 
                        if video.get('release_date')==None:
                            nowdate=datetime.now() 
                            video['release_date']=nowdate      
                            logger.info(f'we use release_date =={nowdate }')  
                        else:
                            if video.get('release_date_hour')==None:    
                                video['release_date_hour']="10:15"   
                                logger.info('we use default release_date_hour 10:15')    
                            elif video.get('release_date_hour') not in availableScheduleTimes:
                                logger.error(f'we use choose one from {availableScheduleTimes}')    
                        if video.get('release_date_hour')==None:     
                            video['release_date_hour']="10:15"   
                            logger.info('we use default release_date_hour 10:15')    
                        elif video.get('release_date_hour') not in availableScheduleTimes:
                            logger.error(f'we use choose one from {availableScheduleTimes}')  
                        if video.get('tags')==None:
                            video['tags']=None      
                            logger.info('we use tags =[]')
                        else:
                            if type(video.get('tags'))==str and "," in video.get('tags'):
                                logger.info(f'tags is ok:{video.get("tags")}')                                

                            else:
                                logger.error('tags should be a list of keywords such as "one,two" ')

                        logger.info(f'length of settingidsdict is {len(settingidsdict)}')
                        df_video=pd.json_normalize(video)                        
                        if len(settingidsdict)>1:       
                            if video.get('uploadSettingid')==None:
    
                                logger.error('we need explicitly specify  uploadSettingid in each video ')
                            else:

                                if  settingidsdict[video.get('uploadSettingid')]:
                                    df_video['upload_setting_id']=settingidsdict[video.get('uploadSettingid')]
                                else:       
                                    logger.error(f'please check {video.get("uploadSettingid")} is saved sucess in db')
                        elif len(settingidsdict)==1:       
                            logger.info(f'there is only one setting:{list(settingidsdict.items())}')
                            # there is two case, 
                            # 1.user input a setting id,we gen a new as value in the dict,key is the old
                            # 2. user give no id, we gen a new as key and value in the dict
                            df_video['upload_setting_id']= list(settingidsdict.keys())[0]
                           
                        else:

                            logger.error('we need at least 1 uploadsetting saved sucess in db')

                        newid=pd.Timestamp.now().value  
                        df_video['id']=newid
                        df_video['youtube_video_id']=None
                        df_video['inserted_at']=datetime.now()           
                        df_video['updated_at']=None           
                        df_video['uploaded_at']=None    
       
                        df_video['status']=False         
                        # print('videos',videos)   
                        logger.info(f'start to check {str(idx)}th video whether  duplicate or save as new')

                        table_name = "uploadtasks"
                        

                        is_video_ok=pd2table(engine,table_name,df_video,logger,if_exists='append')
                        if is_video_ok:
                            logger.info(f'save {str(idx)}th video ok:{df_video["video_title"]}')
                            
                    query = 'SELECT * FROM uploadtasks'
                    # Display the results
                    df=query2df(engine,query,logger)

                    logger.info(f'there is {len(df.index)} records in table {table_name}')      
                    lab = tk.Label(ttkframe,text="validation pass,try to create upload task next",bg="green",width=40)
                    lab.place(x=10, y=220)       
                    lab.after(5*1000,lab.destroy)                                        
                                                 
                except Exception as e:
                    logger.error(f'there is no videos in  your metajson.check metajson docs for reference:{e}')                
                


        else:
            logger.error("you choosed video meta json file is missing or broken.")
            lab = tk.Label(ttkframe,text="please choose a valid json file",bg="lightyellow",width=40)
            lab.place(x=10, y=220)       
            lab.after(10*1000,lab.destroy)
    else:
        logger.error('please provide a video meta json file')
        lab = tk.Label(ttkframe,text="please choose a  json file",bg="lightyellow",width=40)
        lab.place(x=10, y=220)       
        lab.after(10*1000,lab.destroy)       

def uploadView(frame,ttkframe,lang):

    # treeview_flight
    tree = ttk.Treeview(ttkframe, height = 20, column = 9)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 3, column =3,columnspan=50,padx=14, pady=15,sticky='w')

    tree.heading('#0', text = 'Task No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'Video title')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'Description')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'Status')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'release. Date')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'release. Time')
    tree.column('#5', anchor = 'center', width = 80)
    
    tree.heading('#6', text = 'publish type')
    tree.column('#6', anchor = 'center', width = 80)
    tree.heading('#7', text = 'upload. Time')
    tree.column('#7', anchor = 'center', width = 80)
    tree.heading('#8', text = 'local path')
    tree.column('#8', anchor = 'center', width = 80)


    
    
        
    global vid
    vid = tk.StringVar()
    lbl15 = tk.Label(ttkframe, text='Enter vid.')
    lbl15.grid(row = 0, column = 3,sticky='w')
    txt15 = tk.Entry(ttkframe, textvariable=vid)
    txt15.insert(0,'input task id')
    txt15.grid(row = 1, column = 3,sticky='w',columnspan=2)

    channelname = tk.StringVar()
    lbl16 = tk.Label(ttkframe, text='Enter channelname.')
    lbl16.grid(row = 0, column = 6,sticky='w')
    txt16 = tk.Entry(ttkframe,textvariable=channelname)
    txt16.insert(0,'input channelname')
    txt16.grid(row = 1, column = 6,sticky='w',columnspan=2)

    releasedata = tk.StringVar()
    lbl17 = tk.Label(ttkframe, text='Enter releasedata.')
    lbl17.grid(row = 0, column = 9,sticky='w')
    txt17 = tk.Entry(ttkframe, textvariable=releasedata)
    txt17.insert(0,'input releasedata')
    txt17.grid(row = 1, column = 9,sticky='w',columnspan=2)


    btn5= tk.Button(ttkframe, text="Get Info", command = lambda: threading.Thread(target=queryTasks(tree,prod_engine,logger,vid.get())).start())
    btn5.grid(row = 0, column = 12,  padx=14, pady=15)


        
    
    b_down_video_metas_temp = tk.Button(frame, text=i18labels("createTaskMetas", locale=lang, module="g"),
                                         command=lambda: threading.Thread(target=createTaskMetas(frame,ttkframe)).start())
    b_down_video_metas_temp.grid(row = 0, column = 0, padx=14, pady=15,sticky='w')
    

    b_editVideoMetas = tk.Button(frame, text=i18labels("editVideoMetas", locale=lang, module="g"), command=
                                #  lambda: webbrowser.open_new("https://jsoncrack.com/editor")
                                 lambda: threading.Thread(target=webbrowser.open_new("https://jsoncrack.com/editor")).start())
    b_editVideoMetas.grid(row = 0, column = 1, padx=14, pady=15,sticky='w')
    


    l_import_video_metas = tk.Label(frame, text=settings[lang]['importVideoMetas'], font=(' ', 14))
    l_import_video_metas.grid(row = 2, column = 0, padx=14, pady=15,sticky='w')
    b_imported_video_metas_file=tk.Button(frame,text="Select",command=SelectVideoMetasfile)
    b_imported_video_metas_file.grid(row = 2, column = 2, padx=14, pady=15)


    imported_video_metas_file = tk.StringVar()        
    # l_imported_video_metas_file = tk.Label(ttkframe, text='thumbnail template file')

    # l_imported_video_metas_file.place(x=10, y=200)
    e_imported_video_metas_file = tk.Entry(frame, width=int(width*0.02), textvariable=imported_video_metas_file)
    e_imported_video_metas_file.grid(row = 2, column = 1, padx=14, pady=15)

  
    b_validate_video_metas = tk.Button(frame, text=i18labels("validateVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=validateMetafile(test_engine,ttkframe,imported_video_metas_file.get())).start())
    b_validate_video_metas.grid(row = 4, column = 0, padx=14, pady=15)
    b_createuploadsession = tk.Button(frame, text=i18labels("createuploadsession", locale=lang, module="g"), command=lambda: threading.Thread(target=validateMetafile(prod_engine,ttkframe,imported_video_metas_file.get())).start())
    b_createuploadsession.grid(row = 5, column = 0, padx=14, pady=15)

    # test upload  跳转到一个单独页面，录入一个视频的上传信息，点击上传进行测试。
    b_upload = tk.Button(frame, text=i18labels("testupload", locale=lang, module="g"), command=lambda: threading.Thread(target=testupload(DBM('test'),ttkframe)).start())
    b_upload.grid(row = 4, column = 1, padx=14, pady=15)

    b_upload = tk.Button(frame, text=i18labels("upload", locale=lang, module="g"), command=lambda: threading.Thread(target=upload).start())
    b_upload.grid(row = 5, column = 1, padx=14, pady=15)

    lb_youtube_counts = tk.Label(frame, text='youtube', font=(' ', 15))
    lb_youtube_counts.grid(row = 8, column = 0)

    lb_tiktok_counts = tk.Label(frame, text='tiktok', font=(' ', 15))
    lb_tiktok_counts.grid(row = 9, column =0)

    lb_total_counts = tk.Label(frame, text='all', font=(' ', 15))
    lb_total_counts.grid(row = 10, column =0)

    lb_account_counts = tk.Label(frame, text='account', font=(' ', 15))
    lb_account_counts.grid(row = 7, column = 1)

    lb_video_counts = tk.Label(frame, text='success', font=(' ', 15))
    lb_video_counts.grid(row = 7, column = 2)
    
    lb_video_queuedcounts = tk.Label(frame, text='queued', font=(' ', 15))
    lb_video_queuedcounts.grid(row = 7, column = 3)

    lb_video_failure_counts = tk.Label(frame, text='failure', font=(' ', 15))
    lb_video_failure_counts.grid(row = 7, column = 4)


    lb_youtube_success_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_youtube_success_counts_value.grid(row = 8, column = 1)

    lb_youtube_queued_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_youtube_queued_counts_value.grid(row = 8, column = 2)

    lb_youtube_failure_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_youtube_failure_counts_value.grid(row = 8, column = 3)
    
    
    lb_tiktok_success_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_tiktok_success_counts_value.grid(row = 9, column = 1)

    lb_tiktok_queued_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_tiktok_queued_counts_value.grid(row = 9, column = 2)

    lb_tiktok_failure_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_tiktok_failure_counts_value.grid(row = 9, column = 3)
    
    

    lb_total_success_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_total_success_counts_value.grid(row = 10, column =1)

    lb_total_queued_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_total_queued_counts_value.grid(row = 10, column = 2)

    lb_total_failure_counts_value = tk.Label(frame, text=str(checkvideocounts), font=(' ', 18))
    lb_total_failure_counts_value.grid(row = 10, column = 3)
    

    
def  filterProxiesLocations(newWindow,langlist,engine,logger,city,country,tags,status,latest_conditions_value):
    city=city.lower()
    country=country.lower()
    tags=tags.lower()
    availableProxies=[]
    status=1 if status=='valid' else 0
    now_conditions='city:'+city+';country:'+country+';tags:'+tags+';status:'+str(status)

    
    if set(list(latest_conditions_value))==set(now_conditions):
        logger.info('you proxy filter conditions without any change,keep the same')

    else:    
        if city is not None and city !='' or country is not None and country !='' or tags is not None and tags !='':
            query = f"SELECT * FROM proxies where"
            clause=[]
            if city is not None and city !='':
                clause.append(f" city regexp '{city}'")
            if country is not None and country !='':
                clause.append(f" country regexp '{country}'")
            if tags is not None and tags !='':
                clause.append(f" tags regexp '{tags}'")
            if status is not None:
                clause.append(f" status regexp '{status}'")

            query=query+' AND '.join(clause)+" ORDER by inserted_at DESC"

        else:
            query = f"SELECT * FROM proxies ORDER by inserted_at DESC"


        try:
            logger.info(f'start a new query:\n {query}')
            
            table_name='proxies'
            tableexist_query=f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME= '{table_name}'"
            tableexist_query_sqlite=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"

            tableexist=query2df(engine,tableexist_query_sqlite,logger)
            if  tableexist is None:
                hints='there is no  records for query.add proxy before then try again'
                    
                lbl15 = tk.Label(newWindow,bg="lightyellow", text=hints)
                lbl15.grid(row=6,column=2, sticky=tk.W)
                lbl15.after(2000,lbl15.destroy)                
            else:
                
                db_rows = query2df(engine,query,logger)
                if db_rows is not None:
                    langlist.delete(0,tk.END)
                    logger.info(f'we found {len(db_rows)} record matching ')
                    i=0
                    for row in db_rows.itertuples():

                        langlist.insert(tk.END, row.url)
                        langlist.itemconfig(int(i), bg = "lime")
                        i=i+1
                    latest_proxy_conditions_user.set(now_conditions)
                    logger.info(f'search and display finished:\n{query}')
                else:
                    logger.info(f'there is no matching records for query:\n{query}')
                    hints=''
                    query = f"SELECT * FROM proxies"
                    if query2df(engine,query,logger) is not None and len( query2df(engine,query,logger))>0:
                        hints='there is no matching records for query. try to set another condition'
                    else:
                        hints='there is no  records for query.add proxy before then try again'
                        
                    lbl15 = tk.Label(newWindow,bg="lightyellow", text=hints)
                    lbl15.grid(row=6,column=2, sticky=tk.W)
                    lbl15.after(2000,lbl15.destroy)
        except Exception as e:
            logger.error(f'search failed error:{e}') 

def  queryProxies(tree,engine,logger,city,country,tags,status,latest_conditions_value):
    city=city.lower()
    country=country.lower()
    tags=tags.lower()
    status=1 if status=='valid' else 0
    now_conditions='city:'+city+';country:'+country+';tags:'+tags+';status:'+str(status)

    
    if set(list(latest_conditions_value))==set(now_conditions):
        logger.info('you proxy filter conditions without any change,keep the same')

    else:    
        if city is not None and city !='' or country is not None and country !='' or tags is not None and tags !='':
            query = f"SELECT * FROM proxies where"
            clause=[]
            if city is not None and city !='':
                clause.append(f" city regexp '{city}'")
            if country is not None and country !='':
                clause.append(f" country regexp '{country}'")
            if tags is not None and tags !='':
                clause.append(f" tags regexp '{tags}'")
            if status is not None:
                clause.append(f" status regexp '{status}'")

            query=query+' AND '.join(clause)+" ORDER by inserted_at DESC"

        else:
            query = f"SELECT * FROM proxies ORDER by inserted_at DESC"


        try:
            logger.info(f'start a new query:\n {query}')

            db_rows = query2df(engine,query,logger)
            if db_rows is not None:
                records = tree.get_children()
                for element in records:
                    tree.delete(element) 
                for row in db_rows.itertuples():
                    tree.insert(
                        "", 0, text=row.id, values=(row.url,row.status,row.city,row.country,row.tags, row.inserted_at,row.updated_at)
                    )
                latest_conditions.set(now_conditions)
                logger.info(f'search and display finished:\n{query}')
            else:
                logger.info(f'there is no matching records for query:\n{query}')
        except Exception as e:
            logger.error(f'search failed error:{e}')
def updateproxies(engine,proxies_list_raw,logger):
    
    print('check proxy whether valid and its city country')
def saveproxies(engine,proxies_list_raw,logger):
    proxies_list=[]
    if proxies_list_raw and not 'proxy list should be one proxy oneline,and each proxy in such format' in proxies_list_raw:
        proxies_list=proxies_list_raw.split('\n')
        proxies_list=list(set(proxies_list))
        proxies_list=list(filter(None, proxies_list))
        logger.info(f'detected {len(proxies_list) } records to be added')
        
        
        tags=[]
        servers=[]
        for idx,ele in enumerate(proxies_list):
            logger.info(f'start to pre-process {str(idx)} record: {type(ele)}')
            if ";" in ele:
                logger.info(f'split into url:\n{ele.split(";")[0]}\ntags:\n{ele.split(";")[-1]}')

                url=ele.split(";")[0]
                tag=ele.split(";")[-1]

                if url:
                    logger.info(f'check url format {url}')    
                    servers.append(url)  
                    logger.info(f'check tag format {tag}')    

                    tags.append(tag)          
            else:

                if url:
                    print('check url format ',url)    
                    servers.append(url)  
                    tags.append(None)          
            logger.info(f'end to validate {str(idx)} record: {type(url)}')



        ids=[]
        status=[]
        cities=[]
        countries=[]
        inserted_ats=[]
        for i in range(0,len(servers)):
            newid=pd.Timestamp.now().value  
            ids.append(newid)
            status.append('1')
            cities.append(None)
            countries.append(None)
            inserted_ats.append(datetime.now() )     
            
        proxies_df= pd.DataFrame({'url':servers,'id':ids,'status':status,'city':cities,"country":countries,'inserted_at':inserted_ats,'tags':tags})
            

        proxies_df['updated_at']=None  
        print(proxies_df)         
        is_proxy_ok=pd2table(engine,'proxies',proxies_df,logger)
    else:
        logger.info('you should input valid proxy list and try again')
def returnProxy_textfield(event):
    proxy_textfield_str.set(event.widget.get("1.0", "end-1c"))
    print(proxy_textfield_str.get())
    return proxy_textfield_str.get()


def _copy(event):
    try:
        string = event.widget.selection_get()
        clip.copy(string)
    except:
        pass

def proxyView(frame,ttkframe,lang):

    
 


    lbl15 = tk.Label(frame, text='copy proxy info here')
    lbl15.grid(row=0,column=0, sticky=tk.W)
    

        
    global proxy_textfield_str
    proxy_textfield_str = tk.StringVar()
    global latest_conditions
    latest_conditions = tk.StringVar()




    
    from tkinter.scrolledtext import ScrolledText
    proxy_textfield = ScrolledText(frame, wrap=tk.WORD)
    proxy_textfield.grid(row = 3, column = 0, columnspan =2, padx=0, pady=15)
    proxy_textfield.insert(tk.END,'proxy list should be one proxy oneline,and each proxy in such format:\nsocks5://127.0.0.1:1080;tiktok\nsocks5://127.0.0.1:1088;youtube')
    proxy_textfield.bind("<Return>", returnProxy_textfield)
    proxy_textfield.bind_all("<Control-c>",_copy)

    b_save_proxy=tk.Button(frame,text="save proxy",command=lambda: threading.Thread(target=saveproxies(prod_engine,proxy_textfield.get("1.0", tk.END),logger)).start() )
    b_save_proxy.grid(row=5,column=0, sticky=tk.W)
    
    b_check_proxy=tk.Button(frame,text="check proxy",command=lambda: threading.Thread(target=updateproxies(prod_engine,proxy_textfield.get("1.0", tk.END),logger)).start() )
    b_check_proxy.grid(row=5,column=1, sticky=tk.W)    
    

    b_clear_texts=tk.Button(frame,text="clear all texts",command=lambda: threading.Thread(target=proxy_textfield.delete(1.0,tk.END)).start() )
    b_clear_texts.grid(row=4,column=1, sticky=tk.W)
    
    b_choose_proxy=tk.Button(frame,text="load  from file",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_choose_proxy.grid(row=4,column=0, sticky=tk.W)



    
    # res_canvas.rowconfigure(0, weight=1)
    # res_canvas.columnconfigure((0,1), weight=1)
        
    global city,country,proxyTags,proxyStatus
    city = tk.StringVar()
    country = tk.StringVar()
    proxyTags = tk.StringVar()

    lbl15 = tk.Label(ttkframe, text='by city.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(ttkframe,textvariable=city,width=int(0.01*width))
    txt15.insert(0,'Los')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=0, sticky=tk.W)

    lbl16 = tk.Label(ttkframe, text='by country.')
    lbl16.grid(row=0,column=1, sticky=tk.W)
    txt16 = tk.Entry(ttkframe,textvariable=country,width=int(0.01*width))
    txt16.insert(0,'USA')
    txt16.grid(row=1,column=1, sticky=tk.W)
    
    lb17 = tk.Label(ttkframe, text='by tags.')
    lb17.grid(row=0,column=2, sticky=tk.W)
    txt17 = tk.Entry(ttkframe,textvariable=proxyTags,width=int(0.01*width))
    txt17.insert(0,'youtube')
    txt17.grid(row=1,column=2, sticky=tk.W)

    lb18 = tk.Label(ttkframe, text='by status.')
    lb18.grid(row=0,column=3, sticky=tk.W)


    proxyStatus = tk.StringVar()


    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set("Select From Status")
    proxyStatus.trace('w', proxyStatusCallBack)


    proxyStatusbox = ttk.Combobox(ttkframe, textvariable=proxyStatus)
    proxyStatusbox.config(values = ('valid', 'invalid'))
    proxyStatusbox.grid(row = 1, column = 3, columnspan = 3, padx=14, pady=15)    





    btn5= tk.Button(ttkframe, text="Get proxy list", padx = 0, pady = 0,command = lambda: threading.Thread(target=queryProxies(tree,prod_engine,logger,city.get(),country.get(),proxyTags.get(),proxyStatusbox.get(),latest_conditions.get())).start())
    btn5.grid(row=2,column=0, sticky=tk.W)    
    
    
    
    # treeview_flight
    tree = ttk.Treeview(ttkframe, height = 20, column = 8)
    tree["column"]=('#0','#1','#2','#3','#4','#5','#6','#7')
    tree.grid(row = 3, column = 0, columnspan = 20, padx=14, pady=15)

    tree.heading('#0', text = 'proxy No.')
    tree.column('#0', anchor = 'center', width = 70)
    tree.heading('#1', text = 'URL')
    tree.column('#1', anchor = 'center', width = 60)
    tree.heading('#2', text = 'Status')
    tree.column('#2', anchor = 'center', width = 60)
    tree.heading('#3', text = 'City')
    tree.column('#3', anchor = 'center', width = 80)
    tree.heading('#4', text = 'Country')
    tree.column('#4', anchor = 'center', width = 80)
    tree.heading('#5', text = 'tags')
    tree.column('#5', anchor = 'center', width = 80)
    tree.heading('#6', text = 'create. Time')
    tree.column('#6', anchor = 'center', width = 80)
    tree.heading('#7', text = 'updated. Time')
    tree.column('#7', anchor = 'center', width = 80)
    # tree.heading('#8', text = 'local path')
    # tree.column('#8', anchor = 'center', width = 80)    
    
    # viewing_records()

def metaView(left,right,lang):
    global metaView_video_folder
    metaView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    


    e_video_folder = tk.Entry(left,textvariable=metaView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(metaView_video_folder,'metaView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(metaView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    global metafileformat
    

    metafileformat = tk.StringVar()


    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
    metafileformat.set("Select From format")
    metafileformat.trace('w', metafileformatCallBack)


    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values = ( 'json','xlsx', 'csv'))
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    


    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(metaView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    


def tagsView(left,right,lang):
    tagView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=tagView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(tagView_video_folder,'tagView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(tagView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_meta_format, text='Choose the one you like to edit metadata' , wraplength=200)

    metafileformat = tk.StringVar()



    metafileformat.set("Select From format")


    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values = ( 'json','xlsx', 'csv'))
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        analyse_video_meta_pair(tagView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=False,isDesView=False,isTagsView=True,isScheduleView=False)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')
    metafileformat.trace('w', metafileformatCallBack)

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(tagView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(tagView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=False,isDesView=False,isTagsView=True,isScheduleView=False)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)



def desView(left,right,lang):
    desView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=desView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(desView_video_folder,'desView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(desView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_meta_format, text='Choose the one you like to edit metadata' , wraplength=200)

    metafileformat = tk.StringVar()



    metafileformat.set("Select From format")


    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values = ( 'json','xlsx', 'csv'))
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        analyse_video_meta_pair(desView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')
    metafileformat.trace('w', metafileformatCallBack)

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(desView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(desView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)



def scheduleView(left,right,lang):
    scheduleView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=scheduleView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(scheduleView_video_folder,'scheduleView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(scheduleView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_meta_format, text='Choose the one you like to edit metadata' , wraplength=200)

    metafileformat = tk.StringVar()



    metafileformat.set("Select From format")


    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values = ( 'json','xlsx', 'csv'))
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        analyse_video_meta_pair(scheduleView_video_folder.get(),left,right,metafileformatbox.get(),
                                isThumbView=False,isDesView=False,isTagsView=False,isScheduleView=True)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')
    metafileformat.trace('w', metafileformatCallBack)

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(scheduleView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(scheduleView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=False,isDesView=False,isTagsView=False,isScheduleView=True)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)



def logView(log_tab_frame,log_frame,root,lang):

    
    debugLevel = tk.StringVar()

    debugLevel.set("Debug Level:")
    def browserTypeCallBack(*args):
        print(debugLevel.get())
        print(debugLevelbox.current())
    def log_filterCallBack(*args):
        print(log_filter.get())

    debugLevel.trace('w', browserTypeCallBack)

    debugLevelbox = ttk.Combobox(log_tab_frame, textvariable=debugLevel)
    debugLevelbox.config(values = ('DEBUG', 'INFO','ERROR'))
    debugLevelbox.grid(row = 0, column = 0,padx=14, pady=15, sticky='w')   
    log_filter=tk.StringVar()
    e_log_filter = tk.Entry(log_tab_frame,textvariable=log_filter)
    log_filter.set('log filter')
    log_filter.trace('w', log_filterCallBack)

    e_log_filter.grid(row = 0, column = 1,padx=14, pady=15, sticky='nswe')   

    st =ConsoleUi(log_tab_frame,root,row=1,column=0)
    logger.debug(f'Installation path is:{ROOT_DIR}')

    logger.info('TiktokaStudio GUI started')
def hide_log_frame():
    log_frame.grid_forget()

def show_log_frame():
    log_frame.grid(row=1, column=0, sticky="nsew")

def on_tab_change(event):
    selected_tab = tab_control.index(tab_control.select())
    if selected_tab == 11:  # Assuming you want to hide the log frame when the first tab is selected
        hide_log_frame()
    else:
        show_log_frame()

def addTab(tab_control):

    # Create a ttk.Frame within the notebook
    doc_frame = ttk.Frame(tab_control)
    doc_frame.grid(row=0, column=0, sticky="nsew")

    # Create left and right frames within doc_frame
    doc_frame_left = tk.Frame(doc_frame)
    doc_frame_left.grid(row=0, column=0, sticky="nsew")

    doc_frame_right = tk.Frame(doc_frame)
    doc_frame_right.grid(row=0, column=1, sticky="nsew")

    # Add content to doc_frame_left and doc_frame_right
    # You can add widgets and content here as needed

    # Configure the notebook columns to take half of the available width
    tab_control.grid_columnconfigure(0, weight=1)
    tab_control.grid_columnconfigure(1, weight=1)

    # Configure the doc_frame columns to take half of the available width initially
    doc_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(1, weight=1, uniform="group1")

    # Set the initial weight for the right column to be half of the left column
    doc_frame.grid_columnconfigure(0, weight=1, minsize=400)  # Adjust minsize as needed
    doc_frame.grid_columnconfigure(1, weight=2)
    return doc_frame,doc_frame_left,doc_frame_right

def render(root,window,log_frame,lang):
    global doc_frame,install_frame,thumb_frame,video_frame,proxy_frame,account_frame,upload_frame,meta_frame,tab_control

    tab_control = ttk.Notebook(window)
    tab_control.bind("<<NotebookTabChanged>>", on_tab_change)
    tab_control.grid_columnconfigure(0, weight=1)
    tab_control.grid_columnconfigure(1, weight=1)
    # lefts=[]
    # rights=[]
    # for view in ['installView','accountView','proxyView','videosView','thumbView',
                 
    #              'tagsView','desView','scheduleView','metaView',
    #              'uploadView','docView']:

    #     subtab_frame,left,right=addTab(tab_control)
    #     lefts.append(left)
    #     rights.append(right)

    #     tab_control.add(subtab_frame, 
    #                     text=settings[lang][view])
    doc_frame = ttk.Frame(tab_control)
    doc_frame.grid_rowconfigure(0, weight=1)
    doc_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    doc_frame.grid_columnconfigure(1, weight=2)
    doc_frame.grid(row=0, column=0, sticky="nsew")
    
    doc_frame_left = tk.Frame(doc_frame, height = height)
    doc_frame_left.grid(row=0,column=0,sticky="nsew")
    doc_frame_right = tk.Frame(doc_frame, height = height)
    doc_frame_right.grid(row=0,column=1,sticky="nsew") 



    install_frame = ttk.Frame(tab_control)
    install_frame.grid_rowconfigure(0, weight=1)
    install_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    install_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    install_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    install_frame.grid_columnconfigure(1, weight=2)
    install_frame.grid(row=0, column=0, sticky="nsew")

    
    install_frame_left = tk.Frame(install_frame, height = height)
    install_frame_left.grid(row=0,column=0,sticky="nsew")
    install_frame_right = tk.Frame(install_frame, height = height)
    install_frame_right.grid(row=0,column=1,sticky="nsew") 





    thumb_frame = ttk.Frame(tab_control)
    thumb_frame = ttk.Frame(tab_control)
    thumb_frame.grid_rowconfigure(0, weight=1)
    thumb_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    thumb_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    thumb_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    thumb_frame.grid_columnconfigure(1, weight=2)
    thumb_frame.grid(row=0, column=0, sticky="nsew")
    thumb_frame_left = tk.Frame(thumb_frame)
    thumb_frame_left.grid(row=0,column=0,sticky="nswe")
    thumb_frame_right = tk.Frame(thumb_frame)
    thumb_frame_right.grid(row=0,column=1,sticky="nswe") 
    
    thumb_frame_left = tk.Frame(thumb_frame, height = height)
    thumb_frame_left.grid(row=0,column=0,sticky="nsew")
    thumb_frame_right = tk.Frame(thumb_frame, height = height)
    thumb_frame_right.grid(row=0,column=1,sticky="nsew") 




    tags_frame = ttk.Frame(tab_control)
    tags_frame = ttk.Frame(tab_control)
    tags_frame.grid_rowconfigure(0, weight=1)
    tags_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    tags_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    tags_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    tags_frame.grid_columnconfigure(1, weight=2)
    tags_frame.grid(row=0, column=0, sticky="nsew")
    tags_frame_left = tk.Frame(tags_frame)
    tags_frame_left.grid(row=0,column=0,sticky="nswe")
    tags_frame_right = tk.Frame(tags_frame)
    tags_frame_right.grid(row=0,column=1,sticky="nswe") 
    tags_frame_left = tk.Frame(tags_frame, height = height)
    tags_frame_left.grid(row=0,column=0,sticky="nsew")
    tags_frame_right = tk.Frame(tags_frame, height = height)
    tags_frame_right.grid(row=0,column=1,sticky="nsew") 



    des_frame = ttk.Frame(tab_control)
    des_frame = ttk.Frame(tab_control)
    des_frame.grid_rowconfigure(0, weight=1)
    des_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    des_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    des_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    des_frame.grid_columnconfigure(1, weight=2)
    des_frame.grid(row=0, column=0, sticky="nsew")
    des_frame_left = tk.Frame(des_frame)
    des_frame_left.grid(row=0,column=0,sticky="nswe")
    des_frame_right = tk.Frame(des_frame)
    des_frame_right.grid(row=0,column=1,sticky="nswe") 
    
    des_frame_left = tk.Frame(des_frame, height = height)
    des_frame_left.grid(row=0,column=0,sticky="nsew")
    des_frame_right = tk.Frame(des_frame, height = height)
    des_frame_right.grid(row=0,column=1,sticky="nsew") 



    schedule_frame = ttk.Frame(tab_control)
    schedule_frame = ttk.Frame(tab_control)
    schedule_frame.grid_rowconfigure(0, weight=1)
    schedule_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    schedule_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    schedule_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    schedule_frame.grid_columnconfigure(1, weight=2)
    schedule_frame.grid(row=0, column=0, sticky="nsew")
    schedule_frame_left = tk.Frame(schedule_frame)
    schedule_frame_left.grid(row=0,column=0,sticky="nswe")
    schedule_frame_right = tk.Frame(schedule_frame)
    schedule_frame_right.grid(row=0,column=1,sticky="nswe") 
    
    schedule_frame_left = tk.Frame(schedule_frame, height = height)
    schedule_frame_left.grid(row=0,column=0,sticky="nsew")
    schedule_frame_right = tk.Frame(schedule_frame, height = height)
    schedule_frame_right.grid(row=0,column=1,sticky="nsew") 
    video_frame = ttk.Frame(tab_control)
    video_frame = ttk.Frame(tab_control)
    video_frame.grid_rowconfigure(0, weight=1)
    video_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    video_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    video_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    video_frame.grid_columnconfigure(1, weight=2)
    video_frame.grid(row=0, column=0, sticky="nsew")
    video_frame_left = tk.Frame(video_frame)
    video_frame_left.grid(row=0,column=0,sticky="nswe")
    video_frame_right = tk.Frame(video_frame)
    video_frame_right.grid(row=0,column=1,sticky="nswe") 

    
    video_frame_left = tk.Frame(video_frame, height = height)
    video_frame_left.grid(row=0,column=0,sticky="nsew")
    video_frame_right = tk.Frame(video_frame, height = height)
    video_frame_right.grid(row=0,column=1,sticky="nsew") 



    proxy_frame = ttk.Frame(tab_control)
    proxy_frame.grid_rowconfigure(0, weight=1)
    proxy_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    proxy_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    proxy_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    proxy_frame.grid_columnconfigure(1, weight=2)
    proxy_frame.grid(row=0, column=0, sticky="nsew")
    
    proxy_frame_left = tk.Frame(proxy_frame, height = height)
    proxy_frame_left.grid(row=0,column=0,sticky="nsew")
    proxy_frame_right = tk.Frame(proxy_frame, height = height)
    proxy_frame_right.grid(row=0,column=1,sticky="nsew") 
    # input_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')   

    account_frame = ttk.Frame(tab_control)
    account_frame.grid_rowconfigure(0, weight=1)
    account_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    account_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    account_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    account_frame.grid_columnconfigure(1, weight=2)
    account_frame.grid(row=0, column=0, sticky="nsew")
    
    account_frame_left = tk.Frame(account_frame, height = height)
    account_frame_left.grid(row=0,column=0,sticky="nsew")
    account_frame_right = tk.Frame(account_frame, height = height)
    account_frame_right.grid(row=0,column=1,sticky="nsew") 

    upload_frame = ttk.Frame(tab_control)
    upload_frame.grid_rowconfigure(0, weight=1)
    upload_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    upload_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    upload_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    upload_frame.grid_columnconfigure(1, weight=2)
    upload_frame.grid(row=0, column=0, sticky="nsew")
    upload_frame_left = tk.Frame(upload_frame)
    upload_frame_left.grid(row=0,column=0,sticky="nswe")
    upload_frame_right = tk.Frame(upload_frame)
    upload_frame_right.grid(row=0,column=1,sticky="nswe") 



    meta_frame = ttk.Frame(tab_control)
    meta_frame.grid_rowconfigure(0, weight=1)
    meta_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    meta_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    meta_frame.grid_columnconfigure(0, weight=1,
                                      minsize=int(0.5*width)

                                      )
    meta_frame.grid_columnconfigure(1, weight=2)
    meta_frame.grid(row=0, column=0, sticky="nsew")
    meta_frame_left = tk.Frame(meta_frame)
    meta_frame_left.grid(row=0,column=0,sticky="nswe")
    meta_frame_right = tk.Frame(meta_frame)
    meta_frame_right.grid(row=0,column=1,sticky="nswe") 




    tab_control.add(install_frame, 
                     text=settings[lang]['installView'])
                    
    installView(install_frame_left,install_frame_right,lang)


    tab_control.add(account_frame, 
                     text=settings[lang]['accountView'])
                    
    accountView(account_frame_right,account_frame_left,lang)

    tab_control.add(proxy_frame,
                    text=settings[lang]['proxyView'])

    proxyView(proxy_frame_left,proxy_frame_right,lang)

    tab_control.add(video_frame, text=settings[lang]['videosView']
                    )
    videosView(video_frame_left,video_frame_right,lang)

    tab_control.add(thumb_frame, 
                     text=settings[lang]['thumbView'])
                    

    thumbView(thumb_frame_left,thumb_frame_right,lang)

    tab_control.add(tags_frame, 
                     text=settings[lang]['tagsView'])
                    

    tagsView(tags_frame_left,tags_frame_right,lang)
    tab_control.add(des_frame, 
                     text=settings[lang]['desView'])
                    

    desView(des_frame_left,des_frame_right,lang)


    tab_control.add(schedule_frame, 
                     text=settings[lang]['scheduleView'])
                    

    scheduleView(schedule_frame_left,schedule_frame_right,lang)

    tab_control.add(meta_frame, 
                     text=settings[lang]['metaView'])
    metaView(meta_frame_left,meta_frame_right,lang)
    # metaView(meta_frame_right,meta_frame_left,lang)


    tab_control.add(upload_frame, text=settings[lang]['uploadView'])
    uploadView(upload_frame_left,upload_frame_right,lang)
    

    tab_control.add(doc_frame, text=settings[lang]['docView'])

    docView(doc_frame_left,doc_frame_right,lang)
    # tab_control.pack(expand=1, fill='both')
    tab_control.grid(row=0,column=0,sticky='nswe')



    log_tab_frame = ttk.Frame(tab_control)
    # log_frame.grid_rowconfigure((0,1), weight=1)
    # log_frame.grid_columnconfigure((0,1), weight=1 )
    log_tab_frame.grid_rowconfigure(1, weight=1)
    
    log_tab_frame.grid_columnconfigure(1, weight=1)
    logView(log_tab_frame,log_frame,root,lang)

    tab_control.add(log_tab_frame, text=settings[lang]['logView'],sticky='nswe')







    Cascade_button = tk.Menubutton(window)
    # Cascade_button.pack(side=tk.LEFT, padx="2m")
 
     # the primary pulldown
    Cascade_button.menu = tk.Menu(Cascade_button)
 
     # this is the menu that cascades from the primary pulldown....
    Cascade_button.menu.choices = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.choices.add_command(label='zh',command=lambda:changeDisplayLang('zh'))
    Cascade_button.menu.choices.add_command(label='en',command=lambda:changeDisplayLang('en'))
    Cascade_button.menu.add_cascade(label= i18labels("chooseLang", locale=lang, module="g"),
                                    
                                     menu=Cascade_button.menu.choices)    
    
    Cascade_button.menu.loglevel = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.loglevel.add_command(label='DEBUG',command=lambda:changeLoglevel('DEBUG',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='INFO',command=lambda:changeLoglevel('INFO',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='WARNING',command=lambda:changeLoglevel('WARNING',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='ERROR',command=lambda:changeLoglevel('ERROR',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='CRITICAL',command=lambda:changeLoglevel('CRITICAL',window,log_frame))

    
    Cascade_button.menu.add_cascade(label= i18labels("loglevel", locale=lang, module="g"),
                                    
                                     menu=Cascade_button.menu.loglevel)    

    menubar = tk.Menu(window)

    menubar.add_cascade(label=i18labels("settings", locale=lang, module="g"), menu=Cascade_button.menu)    



    root.config(menu=menubar)
    # return langchoosen.get()

def start(lang,root=None):

    # load_setting()
    global ROOT_DIR
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    global paned_window,log_frame,mainwindow,text_handler

    root.geometry(window_size)
    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title(settings[lang]['title'])        

    # Create a PanedWindow widget (vertical)
    paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
    # paned_window.pack(expand=True, fill="both")
    paned_window.grid(row=0, column=0, sticky="nsew")

    # # Configure weights for mainwindow and log_frame
    paned_window.grid_rowconfigure(0, weight=3)
    paned_window.grid_rowconfigure(1, weight=1)

    # Create the frame for the notebook
    mainwindow = ttk.Frame(paned_window)
    paned_window.add(mainwindow)
    mainwindow.grid(row=0, column=0, sticky="nsew")

    mainwindow.grid_rowconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(1, weight=1)


    


    log_frame =tk.Frame(paned_window)
    paned_window.add(log_frame)
    log_frame.grid(row=1, column=0, sticky="nsew")

    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)


    st =ConsoleUi(log_frame,root)

    logger.debug(f'Installation path is:{ROOT_DIR}')

    logger.info('TiktokaStudio GUI started')
    render(root,mainwindow,log_frame,lang)
    root.update_idletasks()

# # Set the initial size of the notebook frame (4/5 of total height)
    mainwindow_initial_percentage = 5 / 6  

    # Calculate the initial height of mainwindow based on the percentage
    initial_height = int(float(root.winfo_height()) * mainwindow_initial_percentage)
    mainwindow.config(height=initial_height)
def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list
def changeDisplayLang(lang):
    # widget_list = all_children(mainwindow)
    # for item in widget_list:
    #     print('233,',item)
    #     item.pack_forget()     
    mainwindow.destroy()
    # del text_handler   

    # widget_list = all_children(log_frame)
    # for item in widget_list:
    #     print('234,',item)
    #     item.pack_forget()    
    # log_frame= None
    log_frame.destroy()
    
    # widget_list = all_children(paned_window)
    # for item in widget_list:
    #     print('235,',item)
    #     item.pack_forget()        
    paned_window.destroy()
    
    
    # root.quit()    
    
    start(lang)
    logger.info(f'switch lang to locale:{lang}')
    
    root.mainloop()




def quit_window(icon, item):
    icon.stop()
    root.destroy()

def show_window(icon, item):
    icon.stop()
    root.after(0,root.deiconify)

def withdraw_window():  
    root.withdraw()
    image = Image.open("assets/icon.ico")
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run_detached()
if __name__ == '__main__':
    global root
    root = tk.Tk()
    start('en',root)

    # root.protocol('WM_DELETE_WINDOW', withdraw_window)
    
    root.mainloop()


        
