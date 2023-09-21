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
import os
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


from UltraDict import UltraDict
if platform.system()=='Windows':
    
    ultra = UltraDict(shared_lock=True,recurse=True)
else:
    ultra = UltraDict(recurse=True)
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

def reset_gui():

    load_setting()

    # 清空表格
    # 写入数据

    prefertags.set(setting['prefertags'])
    preferdessuffix.set(setting['preferdessuffix'])
    preferdesprefix.set(setting['preferdesprefix'])

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

def save_setting(dbm):
    global settingid

    try:
        proxy_option_value = proxy_option.get()
        # print(' proxy_option setting',proxy_option.get())
    except NameError:
        print('no  proxy_option,using existing setting',
              setting['proxy_option'])
        proxy_option_value = setting['proxy_option']
    try:
        firefox_profile_folder_path = firefox_profile_folder.get()
        print('firefox_profile_folder is ',firefox_profile_folder_path)
        setting['firefox_profile_folder'] = firefox_profile_folder_path

    except NameError:
        print('no new  firefox_profile_folder,using existing setting',
              setting['firefox_profile_folder'])
        setting['firefox_profile_folder'] = ''

    try:
        video_folder_path=video_folder.get()
    except NameError:
        print('no new  video_folder_path,using existing setting',
              setting['video_folder'])
        video_folder_path = setting['video_folder']
        print(video_folder_path)
    else:
        if video_folder_path:
            if os.path.exists(video_folder_path):
                setting['video_folder'] = video_folder_path
            else:
                print('we can not find this video foler',video_folder_path)
    try:
        channel_cookie_path=channel_cookie.get()
    except NameError:
        print('no new  channel_cookie_path,using existing setting',
              setting['channelcookiepath'])
        channel_cookie_path = setting['channelcookiepath']
        print(channel_cookie_path)
    else:
        if channel_cookie_path:
            if os.path.exists(channel_cookie_path):
                setting['channelcookiepath'] = channel_cookie_path
            else:
                print('we cannot find cookie file',channel_cookie_path)
    try:
        music_folder_path=music_folder.get()
    except NameError:
        # print('no new  music_folder,using existing setting',
            #   setting['music_folder'])
        music_folder = setting['music_folder']
        # print(music_folder)
    else:
        if music_folder_path:
            setting['music_folder'] = music_folder_path

    setting['is_record_video'] = is_record_video.get()
    setting['is_open_browser'] = is_open_browser.get()    
    setting['ratio'] = ratio.get()
    setting['debug'] = is_debug.get()

    setting['dailycount'] = dailycount.get()
    setting['channelname'] = channelname.get()
    setting['start_publish_date'] = start_publish_date.get()

    setting['preferdesprefix'] = preferdesprefix.get()
    setting['preferdessuffix'] = preferdessuffix.get()
    setting['proxy_option']=proxy_option_value
    setting['prefertags'] = prefertags.get()
    setting['publishpolicy']=publishpolicy.get()    
    if setting['publishpolicy']=='': 
        setting['publishpolicy']=1
    if setting['start_publish_date']=='': 
        setting['start_publish_date']='1'
    if setting['channelname'] is None or setting['channelname']=='' :
        print('before save setting,you need input channelname')
    else:
        if setting['video_folder'] is None or setting['video_folder']=='' :
            print('before save setting,you need input video_folder')
        else:
            if os.path.exists(channel_cookie_path):

                
                newsetting=json.dumps(setting, indent=4, separators=(',', ': '))
                if os.path.exists('./assets/config/'+setting['channelname']+".json"):
                    with open('./assets/config/'+setting['channelname']+".json", 'r') as fr:
                        exitingsetting=json.loads(fr.read())

                        if ordered(setting)==ordered(exitingsetting):
                            print('no change at all')
                        else:
                            print('new change will be saved')
                        with open('./assets/config/'+setting['channelname']+".json", 'w') as f:
                            f.write(json.dumps(setting, indent=4, separators=(',', ': ')))
                        settingid=dbm.Add_New_UploadSetting_In_Db(setting)
                        print("配置保存成功",settingid)
                        with open('latest-used-setting.txt','w+') as fw:
                            fw.write('./assets/config/'+setting['channelname']+".json")                        
                else:
                    with open('./assets/config/'+setting['channelname']+".json", 'w') as f:
 
                        f.write(json.dumps(setting, indent=4, separators=(',', ': ')))                                     
                # print('当前使用的配置为：', setting)
                
                    settingid=dbm.Add_New_UploadSetting_In_Db(setting)
                    print("配置保存成功",settingid)
                    with open('latest-used-setting.txt','w+') as fw:
                        fw.write('./assets/config/'+setting['channelname']+".json")
            else:
                print('请检查cookie文件是否存在 是否损坏',channel_cookie_path)

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

def select_thumbView_video_folder(folder_variable):
    global thumbView_video_folder_path
    try:
        thumbView_video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(thumbView_video_folder_path):
            print("You chose %s" % thumbView_video_folder_path)
            folder_variable.set(thumbView_video_folder_path)
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



def create_setting_file():
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    print('使用默认模版新建配置文件')
    default_setting_path ="./assets/config/template.json"

    global setting_file
    if os.path.exists(ROOT_DIR+os.path.sep+default_setting_path):
        print('default template exists')
        fp = open(ROOT_DIR+os.path.sep+default_setting_path, 'r', encoding='utf-8')
        setting_json = fp.read()
        fp.close()        
        setting = json.loads(setting_json)
    else:
        setting={}
    firefox_profile_folder_path = setting['firefox_profile_folder']
    firefox_profile_folder.set(firefox_profile_folder_path)

    proxy_option.set(setting['proxy_option'])
    # firefox_profile_folder.set(setting['firefox_profile_folder'])
    channel_cookie.set(setting['channelcookiepath'])
    video_folder.set(setting['video_folder'])

    prefertags.set(setting['prefertags'])
    preferdessuffix.set(setting['preferdessuffix'])
    preferdesprefix.set(setting['preferdesprefix'])
    
    dailycount.set(setting['dailycount'])
    channelname.set('hints-we use this as setting file name,you should change it')
    music_folder_path= setting['music_folder']
    publishpolicy.set(setting['publishpolicy'])
    music_folder.set(music_folder_path)
    ratio.set(setting['ratio'])    
    with open(ROOT_DIR+os.path.sep+'./assets/config/'+channelname.get()+".json", 'w') as f:

        f.write(json.dumps(setting, indent=4, separators=(',', ': ')))      

    if os.path.exists(ROOT_DIR+os.path.sep+'./assets/config/'+channelname.get()+".json"):
        print('setting file create done')

def videosMenuMangement():
    # global frame
    # frame=tk.Frame(root,width=str(width),  height=str(height),  )
    # frame.pack()
    window = tk.Tk()
    
    window.title("Airline Management System")

    window.geometry('550x450')    
    tab_control = ttk.Notebook(window)
    
    right = ttk.Frame(tab_control)
    
    left = ttk.Frame(tab_control)

    three = ttk.Frame(tab_control)

    four = ttk.Frame(tab_control)

    right1 = tk.Frame(three, width = 500, height = 500)
    right1.pack(side = tk.RIGHT)

    left1 = tk.Frame(three, width = 500, height = 500)
    left1.pack(side = tk.LEFT)

    tab_control.add(right, text='Passenger Info')
    
    tab_control.add(left, text='Airline Info')

    tab_control.add(three, text='Book Ticket')

    tab_control.add(four, text='Boarding Pass')
    tab_control.pack(expand=1, fill='both')
    window.mainloop()
def load_setting_file():
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )
    default_setting_path=''
    if os.path.exists('latest-used-setting.txt') :
        try:
            fp = open('latest-used-setting.txt', 'r', encoding='utf-8')
            default_setting_path=fp.readlines()[0]
            print('读取最近保存的配置文件',default_setting_path)


        except:
            print('读取配置文件失败 加载默认模版')
            default_setting_path ="./assets/config/demo.json"

    else:
        print('读取配置文件失败 加载默认模版')
        default_setting_path ="./assets/config/demo.json"



    print('======',ROOT_DIR+os.path.sep+default_setting_path)

    global setting_file
    setting_file = filedialog.askopenfilenames(initialdir=ROOT_DIR,initialfile=ROOT_DIR+os.path.sep+default_setting_path,title="请选择该频道配置文件", filetypes=[
        ("Json", "*.json"), ("All Files", "*")])[0]
    load_setting()
    firefox_profile_folder_path = setting['firefox_profile_folder']
    firefox_profile_folder.set(firefox_profile_folder_path)

    proxy_option.set(setting['proxy_option'])
    # firefox_profile_folder.set(setting['firefox_profile_folder'])
    channel_cookie.set(setting['channelcookiepath'])
    video_folder.set(setting['video_folder'])

    prefertags.set(setting['prefertags'])
    preferdessuffix.set(setting['preferdessuffix'])
    preferdesprefix.set(setting['preferdesprefix'])
    
    dailycount.set(setting['dailycount'])
    channelname.set(setting['channelname'])
    music_folder_path= setting['music_folder']
    publishpolicy.set(setting['publishpolicy'])
    music_folder.set(music_folder_path)
    ratio.set(setting['ratio'])



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




def select_file(title,cached,variable,limited='all'):
    file_path=''
    try:
        if limited=='json':
            file_path = filedialog.askopenfilenames(title=title, filetypes=[
                ("Json", "*.json"), ("All Files", "*")])[0]
        elif limited=='images':
            file_path = filedialog.askopenfilenames(title=title, filetypes=[
                ("JPEG", "*.jpg"),("PNG", "*.png"),("JPG", "*.jpg"),("WebP", "*.webp"), ("All Files", "*")])[0]
        else:
            file_path = filedialog.askopenfilenames(title=title, filetypes=[ ("All Files", "*")])[0]
        variable.set(file_path)
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


def changeDisplayLang(lang,window,log_frame):

    window.destroy()
    log_frame.destroy()
    root.title(i18labels("title", locale=lang, module="g"))        
    window=tk.Frame(root,width=str(width),  height=str(height+200),  )
    
    log_frame = tk.Frame(window, width = width, height = 5)
    log_frame.pack(side = tk.BOTTOM)
    st = ScrolledText.ScrolledText(log_frame,                                      
                                width = width, 
                                    height = 5, 
                                     wrap=tk.WORD,
                                    state='disabled')
    st.bind_all("<Control-c>",_copy)

    st.configure(font='TkFixedFont')
    st.grid(column=0, 
            row=0, 
            # sticky='n',
            # columnspan=4
            )
    # st.pack(padx=10, pady=10,side= tk.LEFT, fill=tk.X, expand=True)
    # Create textLogger
    text_handler = TextHandler(st)

    logger.addHandler(text_handler)    
    # print('debug message')
    # print('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    window.pack()
    render(root,window,log_frame,lang)
    logger.info(f'switch lang to locale:{lang}')

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

def downVideoMetas():
    template_url='https://raw.githubusercontent.com/wanghaisheng/tiktoka-studio-uploader-app/main/assets/youtube-videos-meta-comments.json'
    logger.info(f'start to down video metas json template from:{template_url}')
    time.sleep(3)
    logger.info('finish to down video metas json template')

    
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
    logger.info('load video metas to database .create upload task for each video')


    if metafile !='' and metafile is not None:
        
        logger.info(f'you select metafile is {metafile}')
        if  os.path.exists(metafile):
            # check_video_thumb_pair(dbm,video_folder_path,True)
            logger.info('start to load  and parse meta json')

            
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


def createuploadsession(dbm,ttkframe,metafile):
    save_setting(dbm)
    logger.info('load video metas to database .create upload task for each video')
# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        metafile

    except NameError:
        logger.error('please provide a video meta json file')
        is_createuploadsession.set(False)
       
    else:
        if metafile:
            if os.path.exists(metafile):
                # check_video_thumb_pair(dbm,video_folder_path,True)
                logger.info('start to load  and parse meta json')
                # prepareuploadsession( dbm,videopath,thumbpath,filename,start_index,setting['channelname'],settingid)
                logger.info('start to create uploading task for each video')
            else:
                is_createuploadsession.set(False)                
                print("there is no defined video dir.",is_createuploadsession.get())
                print('===',is_createuploadsession.get())


        else:
            print("pls choose file or folder")
            is_createuploadsession.set(False)

        if is_createuploadsession.get()==False:
            logger.info('show import meta to database error hints in 10 seconds')
            lab = tk.Label(ttkframe,text="创建失败，请参考日志修改文件后重新提交",bg="lightyellow",width=40)
            lab.place(x=10, y=220)       
            lab.after(10*1000,lab.destroy)
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
        
def analyse_video_meta_pair(folder,frame,right_frame,selectedMetafileformat,isThumbView=False):
    if folder=='':
        logger.info('please choose a folder first')
    else:
        logger.info(f'detecting----------{ultra.has_key(folder)}')
        if ultra.has_key(folder):
            print(pd.Timestamp.now().value-ultra[folder] ['updatedAt'])
            logger.info(f"we cached {pd.Timestamp.now().value-ultra[folder] ['updatedAt']} seconds before for  this folder {folder}")
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

        
        render_video_folder_check_results(frame,right_frame,folder,isThumbView)






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
    b_view_readme.place(x=50, y=100)    

    b_view_contact=tk.Button(frame,text=i18labels("testnetwork", locale=lang, module="g"),command=lambda: threading.Thread(target=testNetwork).start() )
    b_view_contact.place(x=50, y=200)    
    

    b_view_version=tk.Button(frame,text=i18labels("testsettingok", locale=lang, module="g"),command=lambda: threading.Thread(target=ValidateSetting).start() )
    b_view_version.place(x=50, y=300)    
def videosView(frame,ttkframe,lang):
    global videosView_video_folder
    videosView_video_folder = tk.StringVar()

    videosView_video_folder.set(setting['video_folder'])

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
    global thumbView_video_folder
    thumbView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=thumbView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_thumbView_video_folder(thumbView_video_folder)).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(thumbView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_meta_format, text='Choose the one you like to edit metadata' , wraplength=200)

    global metafileformat
    metafileformat = tk.StringVar()
    metafileformat.set('json')

    keepmetafileformat = metafileformat.get()    
    metafileformatbox = ttk.Combobox(left, width=int(width*0.01), textvariable=keepmetafileformat, state='readonly')
    # box.place(x=10, y=120)
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      

    def selectedmetafileformat(event):
        box = event.widget
        
        print('selected metafileformat is :',metafileformatbox.get())
        metafileformat.set(metafileformatbox.get())
        
        analyse_video_meta_pair(thumbView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True)
    metafileformatbox['values'] = ( 'json','xlsx', 'csv')
    metafileformatbox.current(0)
    metafileformatbox.bind("<<ComboboxSelected>>", selectedmetafileformat)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(thumbView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(thumbView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)



def openXLSX(xlsxpath):
    
    if  platform.system()=='Linux':
    
        
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'") 

    elif platform.system()=='macos':
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'") 
    else:
        os.system('start "excel" "C:\\path\\to\\myfile.xlsx"')

    
def render_video_folder_check_results(frame,right_frame,folder,isThumbView=False):
    lb_video_counts = tk.Label(frame, text='video total counts')

    lb_video_counts.grid(row = 3, column = 0,sticky='w')    

    lb_video_counts_value = tk.Label(frame, text=str(ultra[folder] ['videoCounts']))
    lb_video_counts_value.grid(row = 3, column = 1)    


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

    if isThumbView==False:
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
        # mode1.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        # mode2=tk.Radiobutton(frame,text="定时",variable=publishpolicy,value=2,command='')
        # mode2.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 
        # mode3=tk.Radiobutton(frame,text="unlisted",variable=publishpolicy,value=3,command='')
        # mode3.grid(row = 5, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 

        # mode4=tk.Radiobutton(frame,text="public&premiere",variable=publishpolicy,value=4,command='')
        # mode4.grid(row = 6, column = 0, columnspan = 3, padx=14, pady=15,sticky='ne') 

        # dailycount=tk.StringVar()

        # l_dailycount = tk.Label(frame, text=i18labels("dailyVideoLimit", locale=lang, module="g"))
        # l_dailycount.grid(row = 7, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 



        # e_dailycount = tk.Entry(frame, width=55, textvariable=dailycount)
        # e_dailycount.grid(row = 7, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 
        # start_publish_date=tk.StringVar()

        # l_start_publish_date=tk.Label(frame, text=i18labels("offsetDays", locale=lang, module="g"))
        # l_start_publish_date.grid(row = 8, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        # e_start_publish_date = tk.Entry(frame, width=55, textvariable=start_publish_date)
        # e_start_publish_date.grid(row = 8, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 

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
                                    df=pd.read_excel(os.path.join(folder,'videos-meta.xlsx'))
                                elif ultra[folder]['metafileformat']=='json':
                                    df=pd.read_json(os.path.join(folder,'videos-meta.json'))        
                                elif ultra[folder]['metafileformat']=='csv':
                                    df=pd.read_csv(os.path.join(folder,'videos-meta.csv'))   
                                # List of allowed field names
                                logger.info(f'start to check {allowedTextTypes} defined in template')

                                # Check the data dictionary for allowed fields and empty values in each entry
                                for key, entry in df.items():
                                    missing_fields = [field for field in allowedTextTypes if field not in entry.keys()]

                                    if missing_fields:
                                        print(f"The following allowed fields are missing in entry {key}: {', '.join(missing_fields)}")
                                        logger.error(f'{missing_fields} filed in defined in template,but not found in metafile,add a column named {missing_fields} in metafile')                                    

                                        passed=False

                                    else:
                                        for field in allowedTextTypes:
                                            value = entry[field]
                                            if value == "":
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
                                    for key in json.loads(df.to_json()).keys():
                                        new[key]  =json.loads(df.to_json())[key]                             
                                    
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
                    if len(bg_images)>0:
                        ultra[folder]['thumb_gen_setting']['bg_folder']=thummbnail_bg_folder_path
                        
                        ultra[folder]['thumb_gen_setting']['bg_folder_images']=bg_images
                        logger.info('Random assign bg to each video')


                        for filename in  ultra[folder]['filenames']:
                            bgpath=random.choice(bg_images)

                                            
                            if  ultra[folder]['videos'][filename]['thumbnail_local_path']==[]:
                                ultra[folder]['videos'][filename]['thumbnail_bg_image_path']=bgpath
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
    print(f'you choose metafile format is:{metafileformat.get()}')
    if metafileformat.get():
        openLocal(os.path.join(folder,'videos-meta.'+metafileformat.get()))
    else:
        logger.error(f'you dont choose a valid meta fileformat:{metafileformat.get()}')

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
            'youtube':"1280*720",
            'tiktok':"1080*1920px"

        }
        dict_16_9={
            'xhs':"1440*1080px",
            'dy':"1080*608px",
            'wx':"1080*608px",
            'youtube':"1920 * 1080",
            'tiktok':"1080*608px"


        }

        filename=video_id+ext
        filename=video_id+"_"+str(result_image_width)+"x"+str(result_image_height)+ext
        draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)

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

def setEntry(str):
    proxy_option_account.set(str) 
    print('2222',proxy_option_account.get())
    
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

    lbl15.grid(row=1,column=0, sticky=tk.W)

    txt15 = tk.Entry(newWindow,textvariable=city_user,width=int(0.01*width))
    txt15.insert(0,'')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=1, sticky=tk.W)

    lbl16 = tk.Label(newWindow, text='by country.')
    lbl16.grid(row=2,column=0, sticky=tk.W)
    txt16 = tk.Entry(newWindow,textvariable=country_user,width=int(0.01*width))
    txt16.insert(0,'')
    txt16.grid(row=2,column=1, sticky=tk.W)
    
    lb17 = tk.Label(newWindow, text='by tags.')
    lb17.grid(row=3,column=0, sticky=tk.W)
    txt17 = tk.Entry(newWindow,textvariable=proxyTags_user,width=int(0.01*width))
    txt17.insert(0,'')
    txt17.grid(row=3,column=2, sticky=tk.W)

    lb18 = tk.Label(newWindow, text='by status.')
    lb18.grid(row=4,column=0, sticky=tk.W)

    keepStatus = proxyStatus_user.get()    
    proxyStatusbox = ttk.Combobox(newWindow, width=int(width*0.01), textvariable=keepStatus, state='readonly')
    # box.place(x=10, y=120)
    proxyStatusbox.grid(row = 4, column = 2, columnspan = 3, padx=14, pady=15)    

    def selectedproxyStatus(event):
        box = event.widget
        
        print('selected status is :',box.get())
    proxyStatusbox['values'] = ('valid', 'invalid')
    proxyStatusbox.current(0)
    proxyStatusbox.bind("<<ComboboxSelected>>", selectedproxyStatus)




    

     
     

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(newWindow)
    frame_canvas.grid(row=6, column=0, pady=(5, 0), sticky='nw')
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
    btn5= tk.Button(newWindow, text="Get proxy list", padx = 0, 
                    pady = 0,command = lambda: threading.Thread(target=
                    filterProxiesLocations(newWindow,langlist,prod_engine,logger,city_user.get(),country_user.get(),proxyTags_user.get(),proxyStatusbox.get(),latest_proxy_conditions_user.get())).start())
    btn5.grid(row=5,column=0, sticky=tk.W)    
    btn6= tk.Button(newWindow, text="add selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=setEntry(proxy_str.get())).start())
    # btn5.place(x=800, y=30, anchor=tk.NE)    
    # btn6.pack(side='left')          
    btn6.grid(row=7,column=0, sticky=tk.W)

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
def saveUser(engine,platform,username,password,proxy,cookies):
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
        is_proxy_ok=pd2table(engine,'accounts',account_df,logger)
    
def  queryAccounts(newWindow,tree,engine,logger,username,platform,latest_conditions_value):



    availableProxies=[]
    now_conditions='platform:'+platform+';username:'+username

    
    if set(list(latest_conditions_value))==set(now_conditions):
        logger.info('you proxy filter conditions without any change,keep the same')

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
    socialplatform = tk.StringVar()
    password = tk.StringVar()


    l_platform = tk.Label(ttkframe, text=i18labels("platform", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_platform.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15)    


    keepplatform = socialplatform.get()    
    box = ttk.Combobox(ttkframe, width=int(width*0.01), textvariable=keepplatform, state='readonly')
    # box.place(x=10, y=120)
    box.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15)    

    def selectedplatform(event):
        box = event.widget
        
        print('selected platform is :',box.get())
    box['values'] = ('youtube', 'tiktok', 'douyin')
    box.current(0)
    box.bind("<<ComboboxSelected>>", selectedplatform)



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

    
    b_channel_cookie_gen=tk.Button(ttkframe,text="gen",command=auto_gen_cookie_file)
    # b_channel_cookie_gen.place(x=100, y=390)    
    b_channel_cookie_gen.grid(row = 6, column = 5, columnspan = 3, padx=14, pady=15)    


    
    b_save_user=tk.Button(ttkframe,text="save user",command=lambda: threading.Thread(target=saveUser(prod_engine,box.get(),username.get(),password.get(),proxy_option_account.get(),channel_cookie_user.get())).start() )
                         
    # b_save_user.place(x=10, y=420)        
    b_save_user.grid(row = 8, column = 0, columnspan = 3, padx=14, pady=15)    

    b_bulk_import_users=tk.Button(ttkframe,text="bulk import",command=lambda: threading.Thread(target=bulkImportUsers(ttkframe)).start() )
    # b_bulk_import_users.place(x=10, y=450)    
    b_bulk_import_users.grid(row = 8, column = 4, columnspan = 3, padx=14, pady=15)    

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

    keepStatus = q_platform_account.get()    
    q_platform_accountbox = ttk.Combobox(frame, width=int(width*0.01), textvariable=keepStatus, state='readonly')
    # box.place(x=10, y=120)
    q_platform_accountbox.grid(row = 1, column = 2, columnspan = 3, padx=14, pady=15)    

    def selectedq_platform_accountbox(event):
        box = event.widget
        
        print('selected status is :',box.get())
    q_platform_accountbox['values'] = ('youtube', 'tiktok')
    q_platform_accountbox.current(0)
    q_platform_accountbox.bind("<<ComboboxSelected>>", selectedq_platform_accountbox)




    
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


        
    
    b_down_video_metas_temp = tk.Button(frame, text=i18labels("downVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=downVideoMetas).start())
    b_down_video_metas_temp.grid(row = 0, column = 0, padx=14, pady=15)
    

    b_editVideoMetas = tk.Button(frame, text=i18labels("editVideoMetas", locale=lang, module="g"), command=
                                #  lambda: webbrowser.open_new("https://jsoncrack.com/editor")
                                 lambda: threading.Thread(target=webbrowser.open_new("https://jsoncrack.com/editor")).start())
    b_editVideoMetas.grid(row = 0, column = 1, padx=14, pady=15)
    


    l_import_video_metas = tk.Label(frame, text=i18labels("importVideoMetas", locale=lang, module="g"), font=(' ', 14))
    l_import_video_metas.grid(row = 2, column = 0, padx=14, pady=15)
    global video_meta_json_path
    b_imported_video_metas_file=tk.Button(frame,text="Select",command=SelectVideoMetasfile)
    b_imported_video_metas_file.grid(row = 2, column = 2, padx=14, pady=15)


    global imported_video_metas_file   
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
   except:pass
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
    proxyStatus = tk.BooleanVar()

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

    keepStatus = proxyStatus.get()    
    proxyStatusbox = ttk.Combobox(ttkframe, width=int(width*0.01), textvariable=keepStatus, state='readonly')
    # box.place(x=10, y=120)
    proxyStatusbox.grid(row = 1, column = 3, columnspan = 3, padx=14, pady=15)    

    def selectedproxyStatus(event):
        box = event.widget
        
        print('selected status is :',box.get())
    proxyStatusbox['values'] = ('valid', 'invalid')
    proxyStatusbox.current(0)
    proxyStatusbox.bind("<<ComboboxSelected>>", selectedproxyStatus)

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
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_thumbView_video_folder(metaView_video_folder)).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(metaView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    l_meta_format = tk.Label(left, text=i18labels("preferred meta file format", locale=lang, module="g"))
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    global metafileformat
    metafileformat = tk.StringVar()
    metafileformat.set('json')

    keepmetafileformat = metafileformat.get()    
    metafileformatbox = ttk.Combobox(left, width=int(width*0.01), textvariable=keepmetafileformat, state='readonly')
    # box.place(x=10, y=120)
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      

    def selectedmetafileformat(event):
        box = event.widget
        
        print('metafileformat changed to :',metafileformatbox.get())
        metafileformat.set(metafileformatbox.get())
        analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True)
        logger.info(f'reload results when metafileformat changed to :{metafileformatbox.get()}')
    metafileformatbox['values'] = ( 'json','xlsx', 'csv')
    metafileformatbox.current(0)
    metafileformatbox.bind("<<ComboboxSelected>>", selectedmetafileformat)

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(metaView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get())).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    
    
def metaView1(frame,ttkframe,lang):

    # 
    global is_debug,is_open_browser,is_record_video,start_publish_date,channelname,ratio,publishpolicy,prefertags,preferdesprefix,preferdessuffix,channel_cookie,proxy_option,firefox_profile_folder,video_folder,dailycount,music_folder
    is_debug = tk.BooleanVar()
    is_debug.set(setting['is_debug']) 

    is_open_browser = tk.BooleanVar()
    is_open_browser.set(setting['is_open_browser']) 
    is_record_video = tk.BooleanVar()
    is_record_video.set(setting['is_record_video'])

    prefertags = tk.StringVar()
    prefertags.set(setting['prefertags'])
    preferdesprefix = tk.StringVar()
    preferdesprefix.set(setting['preferdesprefix'])
    preferdessuffix = tk.StringVar()
    preferdessuffix.set(setting['preferdessuffix'])
    dailycount = tk.StringVar()
    dailycount.set(setting['dailycount'])
    music_folder = tk.StringVar()
    music_folder.set(setting['music_folder'])

    ratio = tk.StringVar()
    ratio.set(setting['ratio'])        
    video_folder = tk.StringVar()
    video_folder.set(setting['video_folder'])
    firefox_profile_folder = tk.StringVar()
    firefox_profile_folder.set(setting['firefox_profile_folder'])
    proxy_option = tk.StringVar()
    proxy_option.set(setting['proxy_option'])
    channelname = tk.StringVar()
    channelname.set(setting['channelname'])
    channel_cookie = tk.StringVar()
    channel_cookie.set(setting['channelcookiepath'])
    publishpolicy = tk.StringVar()
    publishpolicy.set(setting['publishpolicy'])
    start_publish_date = tk.StringVar()
    start_publish_date.set(setting['start_publish_date'])
    username = tk.StringVar()
    username.set(setting['username'])

    password = tk.StringVar()
    password.set(setting['password'])    
    

    
    
    

    l_prefertags = tk.Label(frame, text=i18labels("preferTags", locale=lang, module="g"))
    l_prefertags.place(x=10, y=50)
    el_prefertags = tk.Entry(frame, width=55, textvariable=prefertags)
    el_prefertags.place(x=150, y=50)

    l_preferdesprefix = tk.Label(frame, text=i18labels("descriptionPrefix", locale=lang, module="g"))
    l_preferdesprefix.place(x=10, y=70)
    e_preferdesprefix = tk.Entry(frame, width=55, textvariable=preferdesprefix)
    e_preferdesprefix.place(x=150, y=70)


    l_preferdessuffix = tk.Label(frame, text=i18labels("descriptionSuffix", locale=lang, module="g"))
    l_preferdessuffix.place(x=10, y=100)
    e_preferdessuffix = tk.Entry(frame, width=55, textvariable=preferdessuffix)
    e_preferdessuffix.place(x=150, y=100)


    l_music_folder = tk.Label(frame, text=i18labels("bgVideoFolder", locale=lang, module="g"))
    l_music_folder.place(in_=frame, x=10, y=130)
    
    el_music_folder = tk.Entry(frame, width=45, textvariable=music_folder)
    el_music_folder.place(x=150, y=130)
    
    b_music_folder=tk.Button(frame,text="Select",command=select_musics_folder)
    b_music_folder.place(x=580, y=130)        
    
    

    l_bgMucisVolume = tk.Label(frame, text=i18labels("bgMucisVolume", locale=lang, module="g"))
    l_bgMucisVolume.place(x=10, y=160)
    e_bgMucisVolume = tk.Entry(frame, width=55, textvariable=ratio)
    e_bgMucisVolume.place(x=150, y=160)
    
    l_publishpolicy = tk.Label(frame, text=i18labels("publishPolicy", locale=lang, module="g"))
    l_publishpolicy.place(x=10, y=180)
    e_publishpolicy = tk.Entry(frame, width=55, textvariable=publishpolicy)
    e_publishpolicy.place(x=150, y=180)


    l_dailycount = tk.Label(frame, text=i18labels("dailyVideoLimit", locale=lang, module="g"))
    l_dailycount.place(x=10, y=200)



    e_dailycount = tk.Entry(frame, width=55, textvariable=dailycount)
    e_dailycount.place(x=150, y=200)

    l_start_publish_date=tk.Label(frame, text=i18labels("offsetDays", locale=lang, module="g"))
    l_start_publish_date.place(x=10, y=220)
    e_start_publish_date = tk.Entry(frame, width=55, textvariable=start_publish_date)
    e_start_publish_date.place(x=150, y=220)

    


    l_channelname = tk.Label(frame, text=i18labels("channelName", locale=lang, module="g"))
    l_channelname.place(x=10, y=240)
    e_channelname = tk.Entry(frame, width=55, textvariable=channelname)
    e_channelname.place(x=150, y=240)

    l_video_folder = tk.Label(frame, text=i18labels("videoFolder", locale=lang, module="g"))
    l_video_folder.place(x=10, y=270)
    e_video_folder = tk.Entry(frame, width=45, textvariable=video_folder)
    e_video_folder.place(x=150, y=270)
    
    b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_videos_folder).start() )
    b_video_folder.place(x=580, y=270)    
    

    l_firefox_profile_folder = tk.Label(frame, text=i18labels("profileFolder", locale=lang, module="g"))
    l_firefox_profile_folder.place(x=10, y=300)
    e_firefox_profile_folder = tk.Entry(frame, width=45, textvariable=firefox_profile_folder)
    e_firefox_profile_folder.place(x=150, y=300)


    b_firefox_profile_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_profile_folder).start() )
    b_firefox_profile_folder.place(x=580, y=300)


    l_proxy_option = tk.Label(frame, text=i18labels("proxySetting", locale=lang, module="g"))
    l_proxy_option.place(x=10, y=330)
    e_proxy_option = tk.Entry(frame, width=55, textvariable=proxy_option)
    e_proxy_option.place(x=150, y=330)

    l_channel_cookie = tk.Label(frame, text=i18labels("cookiejson", locale=lang, module="g"))
    l_channel_cookie.place(x=10, y=360)
    e_channel_cookie = tk.Entry(frame, width=35, textvariable=channel_cookie)
    e_channel_cookie.place(x=150, y=360)

    b_channel_cookie=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_cookie_file).start() )
    b_channel_cookie.place(x=480, y=360)    
    
    
    b_channel_cookie_gen=tk.Button(frame,text="gen",command=auto_gen_cookie_file)
    b_channel_cookie_gen.place(x=550, y=360)    

    l_username = tk.Label(frame, text=i18labels("username", locale=lang, module="g"))
    l_username.place(x=10, y=390)
    e_username = tk.Entry(frame, width=55, textvariable=username)
    e_username.place(x=150, y=390)

    l_password = tk.Label(frame, text=i18labels("password", locale=lang, module="g"))
    l_password.place(x=10, y=420)
    e_password = tk.Entry(frame, width=55, textvariable=password)
    e_password.place(x=150, y=420)



    
    # b_readfist = tk.Button(frame, text="Read First", command=docs)
    # b_readfist.place(x=10, y=10)




    

    b_is_open_browser = tk.Checkbutton(frame, text=i18labels("is_open_browser", locale=lang, module="g"), variable=is_open_browser)
    b_is_open_browser.place(x=280, y=10)


    b_recordvideo = tk.Checkbutton(frame, text=i18labels("is_record_video", locale=lang, module="g"), variable=is_record_video)
    b_recordvideo.place(x=200, y=10)


    b_debug = tk.Checkbutton(frame, text=i18labels("debug", locale=lang, module="g"), variable=is_debug)
    b_debug.place(x=120, y=10)

    
    

    
    
        
    l_mode_2 = tk.Label(frame, text=i18labels("mode2", locale=lang, module="g"))
    l_mode_2.place(x=10, y=int(height-150))
    
    
    
    b_gen_video_metas = tk.Button(frame, text=i18labels("genVideoMetas", locale=lang, module="g"), command=lambda: threading.Thread(target=genVideoMetas).start())
    b_gen_video_metas.place(x=150, y=int(height-150))







    
    b_autothumb = tk.Button(frame, text=i18labels("load_setting_file", locale=lang, module="g"), command=lambda: threading.Thread(target=load_setting_file).start())
    b_autothumb.place(x=150, y=int(height-250))
    b_batchchangebgmusic = tk.Button(frame, text=i18labels("save_setting", locale=lang, module="g"), command=lambda: threading.Thread(target=save_setting).start())
    b_batchchangebgmusic.place(x=350,y=int(height-250))
    
    
    b_hiddenwatermark = tk.Button(frame, text=i18labels("create_setting_file", locale=lang, module="g"), command=lambda: threading.Thread(target=create_setting_file))
    b_hiddenwatermark.place(x=500,y=int(height-250))

def render(root,window,log_frame,lang):
    global doc_frame,install_frame,thumb_frame,video_frame,proxy_frame,account_frame,upload_frame,meta_frame

    tab_control = ttk.Notebook(window)
    
    doc_frame = ttk.Frame(tab_control)
    doc_frame.grid_rowconfigure(0, weight=1)
    doc_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    doc_frame.columnconfigure((0,1), weight=1)
    
    doc_frame_left = tk.Frame(doc_frame, height = height)
    doc_frame_left.grid(row=0,column=0,sticky="nsew")
    doc_frame_right = tk.Frame(doc_frame, height = height)
    doc_frame_right.grid(row=0,column=1,sticky="nsew") 



    install_frame = ttk.Frame(tab_control)
    install_frame.grid_rowconfigure(0, weight=1)
    install_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    install_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    install_frame.columnconfigure((0,1), weight=1)
    
    install_frame_left = tk.Frame(install_frame, height = height)
    install_frame_left.grid(row=0,column=0,sticky="nsew")
    install_frame_right = tk.Frame(install_frame, height = height)
    install_frame_right.grid(row=0,column=1,sticky="nsew") 





    thumb_frame = ttk.Frame(tab_control)
    thumb_frame.grid_rowconfigure(0, weight=1)
    thumb_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    thumb_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    thumb_frame.columnconfigure((0,1), weight=1)
    
    thumb_frame_left = tk.Frame(thumb_frame, height = height)
    thumb_frame_left.grid(row=0,column=0,sticky="nsew")
    thumb_frame_right = tk.Frame(thumb_frame, height = height)
    thumb_frame_right.grid(row=0,column=1,sticky="nsew") 



    video_frame = ttk.Frame(tab_control)

    video_frame.grid_rowconfigure(0, weight=1)
    video_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    video_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    video_frame.columnconfigure((0,1), weight=1)
    
    video_frame_left = tk.Frame(video_frame, height = height)
    video_frame_left.grid(row=0,column=0,sticky="nsew")
    video_frame_right = tk.Frame(video_frame, height = height)
    video_frame_right.grid(row=0,column=1,sticky="nsew") 



    proxy_frame = ttk.Frame(tab_control)
    proxy_frame.grid_rowconfigure(0, weight=1)
    proxy_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    proxy_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    proxy_frame.columnconfigure((0,1), weight=1)
    
    proxy_frame_left = tk.Frame(proxy_frame, height = height)
    proxy_frame_left.grid(row=0,column=0,sticky="nsew")
    proxy_frame_right = tk.Frame(proxy_frame, height = height)
    proxy_frame_right.grid(row=0,column=1,sticky="nsew") 
    # input_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')   

    account_frame = ttk.Frame(tab_control)
    account_frame.grid_rowconfigure(0, weight=1)
    account_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    account_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    account_frame.columnconfigure((0,1), weight=1)
    
    account_frame_left = tk.Frame(account_frame, height = height)
    account_frame_left.grid(row=0,column=0,sticky="nsew")
    account_frame_right = tk.Frame(account_frame, height = height)
    account_frame_right.grid(row=0,column=1,sticky="nsew") 

    upload_frame = ttk.Frame(tab_control)
    upload_frame.grid_rowconfigure(0, weight=1)
    # upload_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    # upload_frame.grid_columnconfigure(1, weight=2, uniform="group1")
    upload_frame.grid_columnconfigure(0, weight=1 )
    upload_frame.grid_columnconfigure(1, weight=3)

    # upload_frame.columnconfigure((0), weight=1)
    # upload_frame.columnconfigure((1), weight=2)
    
    # upload_frame.grid_columnconfigure(0, weight=1)
    # upload_frame.grid_columnconfigure(1, weight=2) 
     # Right frame occupies twice the width

    upload_frame_left = tk.Frame(upload_frame, height = height)
    upload_frame_left.grid(row=0,column=0,sticky="nsew")
    upload_frame_right = tk.Frame(upload_frame, height = height)
    upload_frame_right.grid(row=0,column=1,sticky="nse") 

    # upload_frame_right.columnconfigure((0,1,2,3,4), weight=1)
    # upload_frame_right.grid_columnconfigure((0,1,2,3,4), weight=1)

    # meta_frame = ttk.Frame(tab_control)
    # meta_frame.rowconfigure(0, weight=1)
    # meta_frame.columnconfigure((0,1), weight=1)
    # meta_frame_left = tk.Frame(meta_frame,width=int(0.5*width),height = height)
    # # meta_frame_left.pack(side = tk.LEFT)
    # meta_frame_left.grid(row=0,column=3,columnspan=3, sticky='nw')
    # meta_frame_right = tk.Frame(meta_frame,width=int(0.5*width), height = height)
    # # meta_frame_right.pack(side = tk.RIGHT)
    # meta_frame_right.grid(row=0,column=6,columnspan=3, sticky='ne')


    meta_frame = ttk.Frame(tab_control)
    meta_frame.grid_rowconfigure(0, weight=1)
    meta_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    meta_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    meta_frame.columnconfigure((0,1), weight=1)
    
    meta_frame_left = tk.Frame(meta_frame, height = height)
    meta_frame_left.grid(row=0,column=0,sticky="nsew")
    meta_frame_right = tk.Frame(meta_frame, height = height)
    meta_frame_right.grid(row=0,column=1,sticky="nsew") 


    meta_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    meta_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    meta_frame.grid_rowconfigure(0, weight=1)


    tab_control.add(doc_frame, text=i18labels("docView", locale=lang, module="g"))
    docView(doc_frame_left,doc_frame_right,lang)

    tab_control.add(install_frame, text=i18labels("installView", locale=lang, module="g"))
    installView(install_frame_left,install_frame_right,lang)


    tab_control.add(account_frame, text=i18labels("accountView", locale=lang, module="g"))
    accountView(account_frame_right,account_frame_left,lang)

    tab_control.add(proxy_frame, text=i18labels("proxyView", locale=lang, module="g"))
    proxyView(proxy_frame_left,proxy_frame_right,lang)

    tab_control.add(thumb_frame, text=i18labels("thumbView", locale=lang, module="g"))
    thumbView(thumb_frame_left,thumb_frame_right,lang)


    tab_control.add(video_frame, text=i18labels("videosView", locale=lang, module="g"))
    videosView(video_frame_left,video_frame_right,lang)


    tab_control.add(meta_frame, text=i18labels("metaView", locale=lang, module="g"))
    metaView(meta_frame_left,meta_frame_right,lang)
    # metaView(meta_frame_right,meta_frame_left,lang)


    tab_control.add(upload_frame, text=i18labels("uploadView", locale=lang, module="g"))
    uploadView(upload_frame_left,upload_frame_right,lang)

    # tab_control.pack(expand=1, fill='both')
    tab_control.grid(row=0,column=0)









    Cascade_button = tk.Menubutton(window)
    # Cascade_button.pack(side=tk.LEFT, padx="2m")
 
     # the primary pulldown
    Cascade_button.menu = tk.Menu(Cascade_button)
 
     # this is the menu that cascades from the primary pulldown....
    Cascade_button.menu.choices = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.choices.add_command(label='zh',command=lambda:changeDisplayLang('zh',window,log_frame))
    Cascade_button.menu.choices.add_command(label='en',command=lambda:changeDisplayLang('en',window,log_frame))
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



    # root.config(menu=menubar)
    # return langchoosen.get()


if __name__ == '__main__':

    gui_flag = 1

    # log_file = "log.txt"


    load_setting()
    global ROOT_DIR
    ROOT_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )



    if gui_flag:
        global root
        root = tk.Tk()
        root.geometry(window_size)
        # root.resizable(width=True, height=True)
        root.iconbitmap("assets/icon.ico")
        root.title(i18labels("title", locale='en', module="g"))        
        # Create a PanedWindow widget (vertical)
        paned_window = tk.PanedWindow(root, orient=tk.VERTICAL)
        paned_window.pack(expand=True, fill="both")

        # Configure weights for mainwindow and log_frame
        paned_window.grid_rowconfigure(0, weight=5)
        paned_window.grid_rowconfigure(1, weight=1)

        # Create the frame for the notebook
        mainwindow = ttk.Frame(paned_window)
        paned_window.add(mainwindow)
        mainwindow.grid_rowconfigure(0, weight=1)
        mainwindow.grid_columnconfigure(0, weight=1)


        


        log_frame =tk.Frame(paned_window)
        paned_window.add(log_frame)

        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)




        st = ScrolledText.ScrolledText(log_frame,                                      
                                    # width = width, 
                                    #     height = 5, 
                                        state='disabled')
        st.bind_all("<Control-c>",_copy)

        def clear_text():

            st.configure(state='normal')  # Enable text widget
            st.delete(1.0, tk.END)  # Delete all text
            st.configure(state='disabled')  # Disable text widget again
        # Create a right-click context menu
        def show_context_menu(event):
            context_menu.post(event.x_root, event.y_root)

        context_menu = tk.Menu(root, tearoff=0)
        context_menu.add_command(label="Clear All Text", command=clear_text)


        # Bind right-click event to show context menu
        st.bind("<Button-3>", show_context_menu)

        st.configure(font='TkFixedFont')
        st.grid(column=0, 
                row=0, 
                sticky='nwse',
                # columnspan=4
                )
        text_handler = TextHandler(st)

        logger.addHandler(text_handler)    


        logger.debug(f'Installation path is:{ROOT_DIR}')

        logger.info('TiktokaStudio GUI started')
        render(paned_window,mainwindow,log_frame,'en')
    #     root.update_idletasks()

    # # Set the initial size of the notebook frame (4/5 of total height)
        mainwindow_initial_percentage = 5 / 6  

        # Calculate the initial height of mainwindow based on the percentage
        initial_height = int(float(root.winfo_height()) * mainwindow_initial_percentage)
        mainwindow.config(height=initial_height)
        root.mainloop()
