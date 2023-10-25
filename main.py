#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.api.account import router
  # Assuming filter_accounts is the function defined in api.py
from playhouse.shortcuts import model_to_dict
from pathlib import Path,PureWindowsPath,PurePath
from src.models.addtestdata import *
# Initialize FastAPI
app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# here put the import lib
from jsonschema import validate
from jsonschema import ValidationError
import json
import jsons
import tkinter as tk
import webbrowser
from tkinter import OptionMenu, filedialog,ttk,Message,Toplevel

import pandas as pd
import os,queue
import base64
import subprocess
import sys
import random
import os
import time
from  src.models.create_tables import *
from src.models.proxy_model import *
from src.models.account_model import *
from src.comboxToolip import ComboboxTip
from src.models.platform_model import *
from src.models.upload_setting_model import *
from src.models.task_model import *
from src.models.youtube_video_model import *
# import multiprocessing.dummy as mp
import concurrent
from glob import glob
from src.dbmanipulation import *
from src.UploadSession import *
from src.bg_music import using_free_music
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
from src.checkIp import CheckIP
from src.models.create_tables import *
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
    tmp = UltraDict(shared_lock=True,recurse=True)
else:
    ultra = UltraDict(recurse=True)
    tmp = UltraDict(recurse=True)    
ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

videoassetsfilename='videos-assets.json'
settingfilename='settings.json'
locale='en'
window_size='1024x720'
height=720
width=1024
supported_video_exts=['.flv', '.mp4', '.avi']
supported_thumb_exts=['.jpeg', '.png', '.jpg','webp']
supported_des_exts=['.des']
supported_tag_exts=['.tags']
supported_schedule_exts=['.schedule']
supported_meta_exts=['.json', '.xls','.xlsx','.csv']      



# Add the handler to logger
logging.basicConfig(filename='test.log',
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s')   
logger = logging.getLogger()    

test_engine=createEngine('test')
prod_engine=createEngine('prod')
window=None

availableScheduleTimes =[]

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
        # level='is_debug'
        # level=level.lower()
        # if level=='is_debug':
        #     # Logging configuration
        #     logging.basicConfig(filename='test.log',
        #         level=logging.DEBUG, 
        #         format='%(asctime)s - %(levelname)s - %(message)s')    
        # elif level=='info':
        #     # Logging configuration
        #     logging.basicConfig(filename='test.log',
        #         level=logging.INFO, 
        #         format='%(asctime)s - %(levelname)s - %(message)s')              
        # elif level=='WARNING':
        #     # Logging configuration
        #     logging.basicConfig(filename='test.log',
        #         level=logging.WARNING, 
        #         format='%(asctime)s - %(levelname)s - %(message)s')   
        # elif level=='ERROR':
        #     # Logging configuration
        #     logging.basicConfig(filename='test.log',
        #         level=logging.ERROR, 
        #         format='%(asctime)s - %(levelname)s - %(message)s')   
        # elif level=='CRITICAL':
        #     # Logging configuration
        #     logging.basicConfig(filename='test.log',
        #         level=logging.CRITICAL, 
        #         format='%(asctime)s - %(levelname)s - %(message)s')   
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
def load_locales():

    folder_path = ROOT_DIR+os.sep+'locales'+os.sep

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Filter the list to include only JSON files
    json_files = [f for f in file_list if f.endswith('.json')]

    # Loop through the JSON files and read their contents
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        with open(file_path, 'r') as file:
            data = json.load(file)

def load_setting():
    global settings
    settingfile=os.path.join(ROOT_DIR,settingfilename)
    failed=False
    if os.path.exists(settingfile) :
        try:

            fp = open(settingfile, 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
            settings = json.loads(setting_json)

        except:
            failed=True

    else:
        failed=True
    if failed==True:
        logger.info('start initialize settings with default')
        print('start initialize settings with default')

        try:
            settings
        except:

            if platform.system()!='Windows':
                settings = UltraDict(recurse=True)
            else:
                settings = UltraDict(shared_lock=True,recurse=True)
                
        settings['lastuselang']='en'
        settings['zh']=json.loads(open(os.path.join(ROOT_DIR+os.sep+'locales','zh.json'), 'r', encoding='utf-8').read())
        settings['en']=json.loads(open(os.path.join(ROOT_DIR+os.sep+'locales','en.json'), 'r', encoding='utf-8').read())
        logger.info('end to initialize settings with default')
    # print(settings)



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




def select_tabview_video_folder(folder_variable,cache_var):
    global thumbView_video_folder_path
    try:
        thumbView_video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
        if os.path.exists(thumbView_video_folder_path):
            folder_variable.set(thumbView_video_folder_path)
            ultra[cache_var]=thumbView_video_folder_path         
            print(f"You chose {folder_variable.get()} for {cache_var}")
            tmp[cache_var]=folder_variable.get()
            otherfolders=['thumbView_video_folder','tagView_video_folder','scheduleView_video_folder','desView_video_folder','metaView_video_folder']
            for i in otherfolders.remove(folder_variable):
                if i =='' or i is None:
                    tmp[i]=folder_variable.get()
            tmp['lastfodler']=folder_variable.get()
            print('==',tmp)
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
    label_helptext_setting = tk.Label(newWindow, text = settings[locale]['docs_str'].replace('\\n','\n'),justify='left', wraplength=450)
    label_helptext_setting.pack()
    
def version(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)

    label_helptext_setting = tk.Label(newWindow, 
                                      text = settings[locale]['version_str'].replace('\\n','\n'),
                                    #   text = "First line\n and this is the second",
                                      justify='left')
    label_helptext_setting.pack()


def contact(frame,lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # due to \n in json string should in \\n, so read it from json  need to convert to original 
    label_helptext_setting = tk.Label(newWindow, text =settings[locale]['contact_str'].replace('\\n','\n'),anchor='e',justify='left', wraplength=450)
    label_helptext_setting.pack()

    group = tk.Label(newWindow, text =settings[locale]['contact_str_group'],anchor='e',justify='left')
    group.pack()
    path_group = './assets/feishu-chatgroup.jpg'
    img_group = Image.open(path_group)
    photo_group = ImageTk.PhotoImage(img_group)
    
    label_group = tk.Label(newWindow,image=photo_group,height=400, width=256)
    label_group.pack()

    personal = tk.Label(newWindow, text = settings[locale]['contact_str_personal'].replace('\\n','\n'),anchor='e',justify='left')
    personal.pack()
    path_personal = './assets/wechat.jpg'
    img_personal = Image.open(path_personal)
    photo_personal = ImageTk.PhotoImage(img_personal)#在root实例化创建，否则会报错
    
    label_personal = tk.Label(newWindow,image=photo_personal,height=400, width=256)
    label_personal.pack()

    newWindow.mainloop()



def install():
    # subprocess.check_call([sys.executable, "-m", "playwright ", "install"])
    subprocess.check_call(["playwright ", "install"])

def testInstallRequirements():
    print('check install requirments')
    checkRequirments()
def testNetwork():
    print('start to test network and proxy setting')

    fnull = open(os.devnull, 'w')
    return1 = subprocess.call('ping www.whoer.net', shell = True, stdout = fnull, stderr = fnull)
    if return1:
        print('network not ready')
        #change_proxy()
        testNetwork()
        
    else:
        fnull.close()
        return True
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




def select_file(title,variable,cached=None,limited='all',parent=None):
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





# 清理残留文件

def threadusing_free_musichelper(numbers):

    using_free_music(numbers[0],numbers[1])


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


def b64e(s):
    return base64.b64encode(s.encode()).decode()


def autothumb():

# 文件夹下是否有视频文件

# 视频文件是否有同名的图片

    try:
        video_folder_path = tmp['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            print("sure, it was defined dir.",video_folder_path)

            # check_video_thumb_pair(video_folder_path,False)
        else:
            print("pls choose file or folder")
def editVideoMetas():
    print('go to web json editor to edit prepared video metas in json format')


def SelectMetafile(cachename,var):
    logger.debug('start to import prepared video metas in json format')
    try:
        filepath = filedialog.askopenfilenames(title="choose  meta  file", filetypes=[
        ("Json", "*.json"),("excel", "*.xls"),("csv", "*.csv"),("Excel", "*.xlsx"),("All Files", "*")])[0]
        tmp[cachename]=filepath
        var.set(filepath)
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
    
def chooseAccountsView_listbox(newWindow,parentchooseaccounts):
    chooseAccountsWindow = tk.Toplevel(newWindow)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title('Choose associated accounts in which platform')
    account_var = tk.StringVar()

    # chooseAccountsWindow.grid_columnconfigure(0, weight=1)
    # frame_canvas.grid_columnconfigure(1, weight=1)    


    # Create a label for the platform dropdown
    platform_label = ttk.Label(chooseAccountsWindow, text="Select Platform:")
    platform_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    # Create a Combobox for the platform selection
    platform_var = tk.StringVar()
    platform_var.set("choose one:")    

    def db_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]

        platform_combo['values'] = platform_names

    def db_refresh(event):
        platform_combo['values'] = db_values()
    platform_combo = ttk.Combobox(chooseAccountsWindow, textvariable=platform_var)
    platform_combo.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)
    platform_combo.bind('<FocusIn>', lambda event: db_refresh(event))
    platform_combo['values'] = db_values()

    # platform_combo.configure(values=platform_rows)
    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(chooseAccountsWindow)
    frame_canvas.grid(row=4, column=0,columnspan=10, pady=(5, 0), sticky='nw')
    frame_canvas.grid_columnconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(1, weight=1)    
    # frame_canvas.grid_rowconfigure(0, weight=1)
    # frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    # frame_canvas.grid_propagate(False)     
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame_canvas, bg='Yellow')
    canvas.grid(row=0, column=0)
    canvas.grid_columnconfigure(0, weight=1)
    canvas.grid_columnconfigure(1, weight=1)    
    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(frame_canvas, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    # Create a horizontal scrollbar linked to the canvas.
    hsbar = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL, command=canvas.xview)
    hsbar.grid(row=1, column=0, sticky=tk.EW)
    canvas.configure(xscrollcommand=hsbar.set)
    # for scrolling vertically

    langlist_frame = tk.Frame(frame_canvas)

    
    langlist = tk.Listbox(langlist_frame, selectmode = "multiple",
                xscrollcommand=hsbar.set,
                yscrollcommand = vsbar.set)
    # langlist.pack(padx = 10, pady = 10,
    #         expand = tk.YES, 
    #         fill = "both")
    langlist.grid(row=0,column=0,sticky='nswe')
        # Create canvas window to hold the buttons_frame.
    canvas.create_window((0,0), window=langlist_frame, anchor=tk.NW)

    langlist_frame.update_idletasks()  # Needed to make bbox info available.
    bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

    # Define the scrollable region as entire canvas with only the desired
    # number of rows and columns displayed.

    canvas.configure(scrollregion=bbox
                    #  , width=dw, height=dh
                     )
    
    btn6= tk.Button(chooseAccountsWindow, text="remove selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=remove_selected_row).start())     
    btn6.grid(row=5,column=0, sticky=tk.W)
    Tooltip(btn6, text='if you want remove any from selected user' , wraplength=200)
    lbl16 = tk.Label(chooseAccountsWindow, text='selected user')
    lbl16.grid(row=8,column=0, sticky=tk.W)
    txt16 = tk.Entry(chooseAccountsWindow,textvariable=account_var,width=int(int(window_size.split('x')[-1])/5))
    txt16.insert(0,'')
    txt16.grid(row=8,column=1, 
            #    width=width,
               columnspan=4,
            #    rowspan=3,
               sticky='nswe')    
    def on_platform_selected(event):
        selected_platform = platform_var.get()
        # Clear the current selection in the account dropdown

        if selected_platform:


            platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
            platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]
            print('platforms options are',platform_names)

            # Extract platform names and set them as options in the platform dropdown
            if platform_rows is None:
                platform_combo["values"]=[]
                button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

            else:
                logger.info(f'query results of existing platforms is {platform_names}')

                if  len(platform_names)==0:
                    platform_combo["values"]=[]
                    button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                    button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
                    
                else:

                    # Execute a query to retrieve accounts based on the selected platform
                    platform_combo["values"]=platform_names
                    for platform in platform_names:
                        
                        if tmp['accountlinkaccount'].has_key(platform):
                            logger.info(f'you have cached  this platform {platform}')
                        else:
                            tmp['accountlinkaccount'][platform]=''
                    
                    account_rows=AccountModel.filter_accounts(platform=getattr(PLATFORM_TYPE, selected_platform.upper()))
                    print(f'query accounts for {selected_platform} {getattr(PLATFORM_TYPE, selected_platform.upper())} ')
                    # Extract account names and set them as options in the account dropdown
                    if account_rows is None or len(account_rows)==0:
                        langlist.delete(0,tk.END)
                        showinfomsg(message=f"try to add accounts for {selected_platform} first",parent=chooseAccountsWindow)    

                    else:                
                        account_names = [row.username for row in account_rows]
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
    # on_platform_selected(None)

    
    def remove_selected_row():
        selected_accounts=tmp['accountlinkaccount']['selected']
        show_str=account_var.get()

        print('you want to remove these selected proxy',selected_accounts)
        if len(selected_accounts)==0:

            showinfomsg(message='you have not selected  proxy at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:
            existingaccounts=tmp['accountlinkaccount'][platform_var.get()].split(',')            
            logger.info(f'you want to remove this selected proxy {selected_accounts} from existing: {existingaccounts}')

            for item in selected_accounts:

                if item in existingaccounts:
                    existingaccounts.remove(item)


                    logger.info(f'this proxy {item} removed success')
                    showinfomsg(message=f'this proxy {item} removed success',parent=chooseAccountsWindow)    
                else:
                    logger.info(f'you cannot remove this proxy {item}, not added before')
                    showinfomsg(message=f'this proxy {item} not added before',parent=chooseAccountsWindow)    
            logger.info(f'end to remove,reset proxystr {existingaccounts}')
            tmp['accountlinkaccount'][platform_var.get()]= ','.join(item for item in existingaccounts if item is not None and item != "")
        show_str=str(tmp['accountlinkaccount'])
        if tmp['accountlinkaccount'].has_key('selected'):
            new=dict(tmp['accountlinkaccount'])
            new.pop('selected')
            show_str=str(new)
        account_var.set(show_str)
        parentchooseaccounts.set(show_str)

    def add_selected_accounts(event):
        listbox = event.widget
        values = [listbox.get(idx).split(':')[0] for idx in listbox.curselection()]
        selected_platform = platform_var.get()
        print('----------',type(tmp['accountlinkaccount']),type(values))
        tmp['accountlinkaccount']['selected']=values
        existingaccounts=tmp['accountlinkaccount'][platform_var.get()].split(',')
        # (youtube:y1,y2),(tiktok:t1:t2)
        show_str=account_var.get()
        if len(list(values))==0:
            logger.info('you have not selected  proxiess at all.choose one or more')
            showinfomsg(message='you have not selected  proxiess at all.choose one or more',parent=chooseAccountsWindow)    
        
        elif values==existingaccounts:
            logger.info('you have not selected new proxiess at all')
            showinfomsg(message='you have not selected new proxiess at all',parent=chooseAccountsWindow)    
        
        else:
            for item in values:
                if item in existingaccounts:
                    logger.info(f'this proxy {item} added before')                   
                    showinfomsg(message=f'this proxiess {item} added before',parent=chooseAccountsWindow)    

                else:
                    existingaccounts.append(item)
                    logger.info(f'this proxy {item} added successS')
                    showinfomsg(message=f'this proxy {item} added success',parent=chooseAccountsWindow)    
            tmp['accountlinkaccount'][platform_var.get()]= ','.join(item for item in existingaccounts if item is not None and item != "")

        show_str=str(tmp['accountlinkaccount'])
        if tmp['accountlinkaccount'].has_key('selected'):
            new=dict(tmp['accountlinkaccount'])
            new.pop('selected')
            show_str=str(new)

        account_var.set(show_str)
        parentchooseaccounts.set(show_str)
    langlist.bind('<<ListboxSelect>>',add_selected_accounts)   

    
def chooseAccountsView(newWindow,parentchooseaccounts):
    chooseAccountsWindow = tk.Toplevel(newWindow)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title('Choose associated accounts in which platform')
    account_var = tk.StringVar()
  

    # Create a label for the platform dropdown
    platform_label = ttk.Label(chooseAccountsWindow, text="Select Platform:")
    platform_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    # Create a Combobox for the platform selection
    platform_var = tk.StringVar()
    platform_var.set("choose one:")    

    lbl16 = tk.Label(chooseAccountsWindow, text='binded user')
    lbl16.grid(row=1,column=0, sticky=tk.W)
    txt16 = tk.Entry(chooseAccountsWindow,textvariable=account_var,width=int(int(window_size.split('x')[-1])/5))
    txt16.insert(0,'')
    txt16.grid(row=1,column=1, 
            #    width=width,
               columnspan=4,
            #    rowspan=3,
               sticky='nswe')    
    def db_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]

        platform_combo['values'] = platform_names

    def db_refresh(event):
        platform_combo['values'] = db_values()
    platform_combo = ttk.Combobox(chooseAccountsWindow, textvariable=platform_var)
    platform_combo.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
    platform_combo.bind('<FocusIn>', lambda event: db_refresh(event))
    platform_combo['values'] = db_values()

    # Create a frame for the canvas and scrollbar(s).
    frame2 = tk.Frame(chooseAccountsWindow, bg='Red', bd=1, relief=tk.FLAT)
    frame2.grid(row=2, column=0, rowspan=5,columnspan=5,sticky=tk.NW)

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=1)
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame2, bg='Yellow')
    canvas.grid(row=0, column=0)

    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    # Create a horizontal scrollbar linked to the canvas.
    hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
    hsbar.grid(row=1, column=0, sticky=tk.EW)
    canvas.configure(xscrollcommand=hsbar.set)

    # Create a frame on the canvas to contain the grid of buttons.
    buttons_frame = tk.Frame(canvas)
    

        
    def refreshcanvas(headers,datas):

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)
        ROWS_DISP = len(datas)+1 # Number of rows to display.
        COLS_DISP = len(headers)+1  # Number of columns to display.
        COLS=len(headers)+1
        
        ROWS=len(datas)+1



        # Add the buttons to the frame.
        add_buttons = [tk.Button() for j in range(ROWS+1)] 
        del_buttons = [tk.Button() for j in range(ROWS+1)] 
        
        # set table header


        for j,h in enumerate(headers):
            label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text=h)
            label.grid(row=0, column=j, sticky='news')                    
            if h=='operation':
                button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                button.grid(row=0, column=j, sticky='news')

                delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                delete_button.grid(row=0, column=j, sticky='news')

        for i,row in enumerate(datas):
            i=i+1
            for j in range(0,len(headers)):
                
                if headers[j]!='operation':
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=row[headers[j]])
                    label.grid(row=i ,column=j, sticky='news')         


              
            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row(rowid=datas[x]['id']))
            add_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row(rowid=datas[x]['id']))
            del_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')
                    
        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        print('=before==',COLS,COLS_DISP,ROWS,ROWS_DISP)

        for i in range(5,COLS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

            if dw>int( canvas.winfo_width()*0.2):
                COLS=i-1
        for i in range(5,ROWS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)                
            if dh>int( canvas.winfo_height()*0.2):
                ROWS=i-1

        print('=after==',COLS,COLS_DISP,ROWS,ROWS_DISP)
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

        if dw>int( root.winfo_width()/3):
            dw=int( root.winfo_width()/3)
        if dh>int( root.winfo_height()/3):
            dh=int( root.winfo_height()/3)
            print('use parent frame widht')
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        print('========',w,h,dw,dh,bbox)
    refreshcanvas(['id','platform','username','is_deleted','proxy','inserted_at','operation','operation'],[])




    def on_platform_selected(event):
        selected_platform = platform_var.get()
        # Clear the current selection in the account dropdown

        if selected_platform:


            platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
            platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]
            print('platforms options are',platform_names)

            # Extract platform names and set them as options in the platform dropdown
            if platform_rows is None:
                platform_combo["values"]=[]
                button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

            else:
                logger.info(f'query results of existing platforms is {platform_names}')

                if  len(platform_names)==0:
                    platform_combo["values"]=[]
                    button1 = ttk.Button(chooseAccountsWindow, text="try to add platforms first", command=lambda: (chooseAccountsWindow.withdraw(),newWindow.withdraw(),tab_control.select(1)))
                    button1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)
                    
                else:

                    # Execute a query to retrieve accounts based on the selected platform
                    platform_combo["values"]=platform_names
                    for platform in platform_names:
                        
                        if tmp['accountlinkaccount'].has_key(platform):
                            logger.info(f'you have cached  this platform {platform}')
                        else:
                            tmp['accountlinkaccount'][platform]=''
                    
                    account_rows=AccountModel.filter_accounts(platform=getattr(PLATFORM_TYPE, selected_platform.upper()))
                    print(f'query accounts for {selected_platform} {getattr(PLATFORM_TYPE, selected_platform.upper())} ')
                    # Extract account names and set them as options in the account dropdown
                    if account_rows is None or len(account_rows)==0:
                        # langlist.delete(0,tk.END)
                        showinfomsg(message=f"try to add accounts for {selected_platform} first",parent=chooseAccountsWindow)    

                    else:                
                        account_names = [row.username for row in account_rows]
                        logger.info(f'we found {len(account_names)} record matching ')

                        # langlist.delete(0,tk.END)
                        i=0
                        account_data=[]
                        for row in account_rows:
                            account={
                                "id":CustomID(custom_id=row.id).to_hex(),
                                "platform":row.platform,
                                "username":row.username,
                                "is_deleted":row.is_deleted,
                                "proxy":row.proxy,
                                "inserted_at":row.inserted_at
                            }
                            account_data.append(account)
                        refreshcanvas(['id','platform','username','is_deleted','proxy','inserted_at','operation','operation'],account_data)
                   

    # Bind the platform selection event to the on_platform_selected function
    platform_combo.bind("<<ComboboxSelected>>", on_platform_selected)



    
    def remove_selected_row(rowid):

        selected_platform = platform_var.get()
        existingaccounts=account_var.get()
        if existingaccounts:
            existingaccounts=eval(existingaccounts)
        else:
            existingaccounts={selected_platform:[]}

        print('you want to remove these selected account',rowid)
        if rowid==0:

            showinfomsg(message='you have not selected  account at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:


            if rowid in existingaccounts[selected_platform]:
                existingaccounts[selected_platform].remove(rowid)


                logger.info(f'this account {rowid} removed success')
                showinfomsg(message=f'this account {rowid} removed success',parent=chooseAccountsWindow)    
            else:
                logger.info(f'you cannot remove this account {rowid}, not added before')
                showinfomsg(message=f'this account {rowid} not added before',parent=chooseAccountsWindow)    
            logger.info(f'end to remove,reset account {existingaccounts}')

        account_var.set(str(existingaccounts))
        parentchooseaccounts.set(str(existingaccounts))

    def add_selected_accounts(rowid):
        

        selected_platform = platform_var.get()
        existingaccounts=account_var.get()
        if existingaccounts:
            existingaccounts=eval(existingaccounts)
        else:
            existingaccounts={selected_platform:[]}
        # (youtube:y1,y2),(tiktok:t1:t2)
        if rowid is None:
            logger.info('you have not selected new accounts at all')
            showinfomsg(message='you have not selected new accounts at all',parent=chooseAccountsWindow)    
        
        else:
            if rowid in existingaccounts[selected_platform]:
                logger.info(f'this account {rowid} added before')                   
                showinfomsg(message=f'this account {rowid} added before',parent=chooseAccountsWindow)    

            else:
                if existingaccounts[selected_platform]=='':
                    existingaccounts[selected_platform]=[]
                existingaccounts[selected_platform].append(rowid)
                logger.info(f'this account {rowid} added successS')
                showinfomsg(message=f'this account {rowid} added success',parent=chooseAccountsWindow)    

        account_var.set(str(existingaccounts))
        parentchooseaccounts.set(str(existingaccounts))



def isFilePairedMetas(r,videofilename,meta_exts_list,dict,meta_name):
    logger.info(f'start to check {meta_name} for video: {videofilename}')
    print(f'before check:\n{jsons.dump(dict[meta_name])}')

    for ext in meta_exts_list:
        logger.debug(f'start to {ext}--{meta_name}')
        print(f'start to {ext}')

        metapath = os.path.join(r, videofilename+ext)
        if  os.path.exists(metapath):     
            logger.info(f'meta filed  {meta_name} for {videofilename} is  exist:\n {metapath}')
            if dict[meta_name] is not None and metapath not in dict[meta_name]:
                if dict[meta_name].has_key(videofilename)==False:
                    dict[meta_name][videofilename]=[]
                    logger.info(f'intial {meta_name} for {videofilename}:\n')
                if not metapath in dict[meta_name][videofilename]:

                    dict[meta_name][videofilename].append(metapath)
                print(f'append result:\n{dict[meta_name][videofilename]}')
                if meta_name=='thumbFilePaths':
                    logger.info(f"found thumbfiles,start to set video metas {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}")

                    if dict['videos'][videofilename]['thumbnail_local_path'] is None or dict['videos'][videofilename]['thumbnail_local_path']=='':
                        print('video meta thumbnail is None')
                        print(f'try to add {metapath}')
                        print(dict['videos'][videofilename])
                        emptyfiles=[]
                        emptyfiles.append(metapath)
                        print('empty',emptyfiles)
                        dict['videos'][videofilename]['thumbnail_local_path']=str(emptyfiles)
                        print(dict['videos'][videofilename])
                        
                        print('update video meta thumbnail',dict['videos'][videofilename]['thumbnail_local_path'])
                        print(f"found thumbfiles,end to set video metas is None== {ext}== {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}")

                    else:
                        if type(dict['videos'][videofilename]['thumbnail_local_path'])==str:
                            dict['videos'][videofilename]['thumbnail_local_path']=eval(dict['videos'][videofilename]['thumbnail_local_path']).append(metapath)

                        else:                   
                            if not metapath in dict['videos'][videofilename]['thumbnail_local_path']:
                                dict['videos'][videofilename]['thumbnail_local_path'].append(metapath)
                        print(f"found thumbfiles,end to set video metas {ext}== {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}")
                                
                    logger.info(f"found thumbfiles,end to set video metas {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}")
                            
                elif meta_name=='desFilePaths':
                    logger.info(f"found des files,start to set video metas {type(dict['videos'][videofilename]['video_description'])},{dict['videos'][videofilename]['video_description']}")

                    with open(metapath,'r',encoding='utf-8') as f:
                        lines=f.readlines()
                        
                        contents = '\r'.join(lines)
                        contents = contents.replace('\n','')
                        dict['videos'][videofilename]['video_description']=contents 
                    logger.info(f"found des files,end to set video metas {type(dict['videos'][videofilename]['video_description'])},{dict['videos'][videofilename]['video_description']}")

                elif meta_name=='tagFilePaths':
                    logger.info(f"found tag files,start to set video metas {type(dict['videos'][videofilename]['tags'])},{dict['videos'][videofilename]['tags']}")

                    with open(metapath,'r',encoding='utf-8') as f:
                        lines=f.readlines()
                        
                        contents = '\r'.join(lines)
                        contents = contents.replace('\n','')
                        dict['videos'][videofilename]['tags']=contents       
                    logger.info(f"found tag files,end to set video metas {type(dict['videos'][videofilename]['tags'])},{dict['videos'][videofilename]['tags']}")
                                             
    print(f"after check:\n {jsons.dump(dict[meta_name])}:\n,{dict['videos'][videofilename]['thumbnail_local_path']}")
                          
    logger.info(f"after check:\n {jsons.dump(dict[meta_name])}:\n,{dict['videos'][videofilename]['thumbnail_local_path']}")
    
    tmpjson=os.path.join(r, videofilename+'.json')
    if os.path.exists(tmpjson):
        logger.info(f'update to {videofilename} meta json')
        with open(tmpjson,'w') as f:
            f.write(jsons.dumps(dict['videos'][videofilename]))        
    else:
        logger.info(f'create a fresh {videofilename} meta json')
        with open(tmpjson,'a') as f:
            f.write(jsons.dumps(dict['videos'][videofilename]))

def syncVideometa2assetsjson(selectedMetafileformat,folder):
    changed_df_metas=None
    if os.path.exists(os.path.join(folder,'videos-meta.'+selectedMetafileformat)) and ultra.has_key(folder):
        if selectedMetafileformat=='xlsx':
            changed_df_metas=pd.read_excel(os.path.join(folder,'videos-meta.xlsx'), index_col=[0])
            changed_df_metas.replace('nan', '')
            changed_df_metas=json.loads(changed_df_metas.to_json(orient = 'index'))   
        elif selectedMetafileformat=='json':
            changed_df_metas=pd.read_json(os.path.join(folder,'videos-meta.json'))  
            changed_df_metas.replace('nan', '')
            changed_df_metas=json.loads(changed_df_metas.to_json())   

        elif selectedMetafileformat=='csv':
            changed_df_metas=pd.read_csv(os.path.join(folder,'videos-meta.csv'), index_col=[0])
            changed_df_metas.replace('nan', '')
            changed_df_metas=json.loads(changed_df_metas.to_json(orient = 'index'))   
        # ultra[folder]['videos']=changed_df_metas
        # oldvideos=dict(ultra[folder]['videos'])
        tmpvideos=dict({})
        # oldvideos=json.loads(jsons.dumps(ultra[folder] ['videos'])) 
        newfilenameslist=[]
        logger.debug('start to check video file existence in the new metafile ')
        for filename,video in changed_df_metas.items():
            print('video',video,type(video))
            if os.path.exists(video['video_local_path']):
                logger.info('video file is ok')
                newfilenameslist.append(filename)
                tmpvideos[filename]=video
                
            else:
                logger.info(f"{video['video_local_path']} video file is broken or not found according to video metafile")
                # newfilenameslist.remove(filename)
                # changed_df_metas.remove(filename)        
        if ultra[folder].has_key('videos'):
            logger.info(f"=111==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")
            
            logger.info(f"=222==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")
            # ultra[folder]['videos']= {}
            # 当某个key值为空 {} 如果你要赋值一个嵌套的对象 比如json样子的数组 是没有办法直接赋值的
            # ultra[folder]['videos']= changed_df_metas
            if dict(ultra[folder]['videos'])==dict({}):
                logger.info(f"=333==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")
                
                for filename,video in tmpvideos.items():
                    ultra[folder]['videos'][filename]= video
                logger.info(f"=444==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")
            else:
                logger.info(f"=555==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")
                try:
                    ultra[folder]['videos']=tmpvideos      
                except Exception as e:
                    logger.error(e)
                logger.info(f"=5551==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")

                for filename,video in tmpvideos.items():
                    print('is_debug',filename,video)
                    ultra[folder]['videos'][filename]= video
                    # ultra[folder]['videos']=new                   
        else:
            logger.info(f"=666==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}")
        
            new=dict({})        
            for filename,video in tmpvideos.items():
                new[filename]= video
            ultra[folder]['videos']=new   
        ultra[folder]['filenames']= newfilenameslist
        if len(ultra[folder] ['filenames'])==0:
            logger.info(f"we could not find any video, video counts is {ultra[folder] ['videoCounts']},supported ext includes:\n{'.'.join(supported_video_exts)}")
        # 遍历每个视频文件，核对视频文件、缩略图等文件是否存在，核对元数据中对应字段是否存在
        ultra[folder] ['videoCounts']=len(ultra[folder] ['filenames'])    
        print(f"during sync ,detected video counts {len(ultra[folder] ['filenames'])  }")

        ultra[folder]['updatedAt']=pd.Timestamp.now().value        
        logger.debug('end to check video file existence in the new metafile ')


def creatNewfoldercache(folder):
    if ultra.has_key(folder)==False:

        ultra[folder]={'videoCounts':0,
                    'thumbFileCounts':0,
                    'thumbMetaCounts':0,

                    'desFileCounts':0,
                    'desMetaCounts':0,

                    'tagFileCounts':0,
                    'tagMetaCounts':0,
                    
                    'scheduleFileCounts':0,
                    'scheduleMetaCounts':0,
                    'metaFileCounts':0,
                    'updatedAt':pd.Timestamp.now().value,
                    'filenames':[],
                    'videoFilePaths':[],
                        'thumbFilePaths':{},
                        'desFilePaths':{},
                        'scheduleFilePaths':{},
                        'tagFilePaths':{},

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

                    }     
    else:
        logger.info(f'there is cache for {folder} already')
def scanVideofiles(folder):

        
    thumbFileCounts=0
    thumbMetaCounts=0

    desFileCounts=0
    desMetaCounts=0

    tagFileCounts=0
    tagMetaCounts=0
    metaMetaCounts=0
    scheduleFileCounts=0
    scheduleMetaCounts=0
    metaFileCounts=0
    logger.debug(f'start to scan video file existence in the {folder} ')

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
                            logger.info(f'you have prepared video metas for:{filename}')
                        else:
                            ultra[folder] ['filenames'].append(filename)


                            videopath = os.path.join(r, entry.name)
                            ultra[folder] ['videoFilePaths'].append(videopath)
                            print('this video is detected before',filename)
    #   //0 -private 1-publish 2-schedule 3-Unlisted 4-public&premiere 

                            # default single video meta json
                            video={'video_local_path':'',
                                "video_filename":'',
                                "video_title":'',
                                    "heading":"",
                                    "subheading":"",
                                    "extraheading":"",
                                "video_description":"",
                                    "thumbnail_bg_image_path": "",
                                'publish_policy':2,
                                "thumbnail_local_path":'[]',
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

                            # if old_df_metas and old_df_metas[filename]:
                            #     print('this video is detected before',type(old_df_metas[filename]),old_df_metas[filename])
                            #     print('2',oldvideos[filename],type(oldvideos[filename]))
                            #     if oldvideos[filename]==old_df_metas[filename]:
                            #         print(f'the existing videos-meta.{selectedMetafileformat} content is the same as cached')
                            #     else:
                            #         print(f'the existing videos-meta.{selectedMetafileformat} content is not the  same as cached')

                            #     video=old_df_metas[filename]
                            # ultra[folder] ['videos'][filename]=video
                            # print('this video json',ultra[folder] ['videos'][filename])
                        # 如果在第一次生成视频元数据以后，用户编辑了元数据文件，并且删除或者新增了文件夹中视频的数量，这时候源文件中并没有新增视频的元数据，再次点击检查以后，是否添加这些新增或者删除视频的信息
                        # 如果是新增 1.元数据中没有添加  前面元数据同步的话 这里是要添加的
                        # 如果是删除 1元数据中没有删除， 这里要删除掉
                            # videos.append(video)
                            # videopath=base64.b64encode(videopath.encode('utf-8'))
                            ultra[folder] ['videos'][filename]['video_local_path']=str(PurePath(videopath))
                            ultra[folder] ['videos'][filename]['video_title']=filename
                            ultra[folder] ['videos'][filename]['video_filename']=filename
                            ultra[folder] ['videos'][filename]['video_description']=filename

                            for ext in supported_thumb_exts:
                                filepath=os.path.join(r,filename+ext)
                                if os.path.exists(filepath):
                                    if filepath in ultra[folder]['videos'][filename]['thumbnail_local_path']:
                                        pass
                                    else:
                                        if type(ultra[folder]['videos'][filename]['thumbnail_local_path'])==str:
                                            ultra[folder]['videos'][filename]['thumbnail_local_path']=eval(ultra[folder]['videos'][filename]['thumbnail_local_path'])
                                            
                                            ultra[folder]['videos'][filename]['thumbnail_local_path'].append(str(PurePath(filepath)))
                                        elif ultra[folder]['videos'][filename]['thumbnail_local_path'] is None or ultra[folder]['videos'][filename]['thumbnail_local_path'] in ['','[]'] or len(ultra[folder]['videos'][filename]['thumbnail_local_path'])==0:
                                            empt=[].append(str(PurePath(filepath)))
                                            ultra[folder]['videos'][filename]['thumbnail_local_path']=str(empt)
                                        else:
                                            # filepath=base64.b64encode(filepath.encode('utf-8'))

                                            ultra[folder]['videos'][filename]['thumbnail_local_path'].append(str(PurePath(filepath)))
                                            
                            # to-do 
                            # supported_des_exts
                            # supported_tag_exts
                            
                        if ultra[folder] ['videos'][filename]['thumbnail_local_path']:
                            if type(ultra[folder] ['videos'][filename]['thumbnail_local_path'])==str:
                                ultra[folder] ['videos'][filename]['thumbnail_local_path']=eval(ultra[folder] ['videos'][filename]['thumbnail_local_path'])

                            
                            files=ultra[folder] ['videos'][filename]['thumbnail_local_path']
                            if files is not None:
                                if len(files)>0:
                                    start=False
                                    for i in files:
                                        if os.path.exists(i):      
                                            start=True
                                    if start==True:                                  
                                        thumbMetaCounts+=1
                            else:
                                print(f"detect no thumb files for video {filename}==={files}")
                        if ultra[folder] ['videos'][filename]['tags']!='':
                            tagMetaCounts+=1

                        if ultra[folder] ['videos'][filename]['video_description']!='':
                            desMetaCounts+=1

                        if ultra[folder] ['videos'][filename]['release_date']!='':
                            scheduleMetaCounts+=1

   

                        # if ultra[folder]['thumbFilePaths'].has_key(filename)==False:
                        #     ultra[folder]['thumbFilePaths'][filename]=[]
                        isFilePairedMetas(r,filename,supported_thumb_exts,ultra[folder],'thumbFilePaths')
                        isFilePairedMetas(r,filename,supported_des_exts,ultra[folder],'desFilePaths')
                        isFilePairedMetas(r,filename,supported_meta_exts,ultra[folder],'metaFilePaths')
                        isFilePairedMetas(r,filename,supported_tag_exts,ultra[folder],'tagFilePaths')
                        isFilePairedMetas(r,filename,supported_schedule_exts,ultra[folder],'scheduleFilePaths')
                else:
                    print('is folder',r,d,i)      
    if len(ultra[folder] ['filenames'])==0:
        logger.info(f"we could not find any video, video counts is {ultra[folder] ['videoCounts']},supported ext includes:\n{'.'.join(supported_video_exts)}")
    # 遍历每个视频文件，核对视频文件、缩略图等文件是否存在，核对元数据中对应字段是否存在
    ultra[folder] ['videoCounts']=len(ultra[folder] ['filenames'])    
    print(f"detected video counts {len(ultra[folder] ['filenames']) }")
    ultra[folder] ['thumbFileCounts']=len(ultra[folder] ['thumbFilePaths'])
    ultra[folder] ['thumbMetaCounts']=thumbMetaCounts

    ultra[folder] ['desFileCounts']=len(ultra[folder] ['desFilePaths'])
    ultra[folder] ['desMetaCounts']=desMetaCounts

    ultra[folder] ['metaFileCounts']=len(ultra[folder] ['metaFilePaths'])
    ultra[folder] ['metaMetaCounts']=metaMetaCounts

    ultra[folder] ['tagFileCounts']=len(ultra[folder] ['tagFilePaths'])

    ultra[folder] ['tagMetaCounts']=tagMetaCounts
    ultra[folder] ['scheduleFileCounts']=len(ultra[folder] ['scheduleFilePaths'])
    ultra[folder] ['scheduleMetaCounts']=scheduleMetaCounts
    ultra[folder]['updatedAt']=pd.Timestamp.now().value     
    logger.debug(f'end to scan video file existence in the {folder} ')

def analyse_video_meta_pair(folder,frame,right_frame,selectedMetafileformat,isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True):
    assetpath=os.path.join(folder,videoassetsfilename)    


    if folder=='':
        logger.info('please choose a folder first')
    else:
        logger.info(f'start to detecting video metas----------{ultra.has_key(folder)}')

        if ultra.has_key(folder):
            print(pd.Timestamp.now().value-ultra[folder] ['updatedAt'])
            duration_seconds = (pd.Timestamp.now().value-ultra[folder] ['updatedAt']) / 10**9  # Convert nanoseconds to seconds
            
            logger.info(f"we cached {duration_seconds} seconds before for  this folder {folder}")


        else:
            logger.info(f"create cached data for this folder:\n{folder}")
            creatNewfoldercache(folder)
        if os.path.exists(videoassetsfilename):
            logger.info('load video assets to cache')
            # os.remove(videoassetsfilename)
            assetpath=os.path.join(folder,videoassetsfilename)

            changed_df_metas=pd.read_json(assetpath)  
            changed_df_metas.replace('nan', '')
            changed_df_metas=json.loads(changed_df_metas.to_json())   


            ultra[folder]=changed_df_metas

            
            
        if os.path.exists(os.path.join(folder,'videos-meta.'+selectedMetafileformat)):
            logger.info('sync videos-meta')
            print('============sync videos-meta==============')
            # os.remove(os.path.join(folder,'videos-meta.'+selectedMetafileformat))
            syncVideometa2assetsjson(selectedMetafileformat,folder)
            print('============end sync videos-meta==============')
        print('============start scanVideofiles==============')

        scanVideofiles(folder)
        print('============end scanVideofiles==============')
        print('============start dumpMetafiles==============')

        ultra[folder]['metafileformat']=selectedMetafileformat
        dumpMetafiles(selectedMetafileformat,folder)
        print('============end dumpMetafiles==============')

        render_video_folder_check_results(frame,right_frame,folder,isThumbView,isDesView,isTagsView,isScheduleView,selectedMetafileformat)
def dumpTaskMetafiles(selectedMetafileformat,folder):
    logger.debug(f'start to dump task metas for {folder} ')
    print(f"task to be dump :{tmp['tasks']}")
    if selectedMetafileformat=='xlsx':
        df_metas = pd.read_json(jsons.dumps(tmp['tasks']), orient = 'index')

        metaxls=os.path.join(folder,'task-meta.xlsx')
            
        df_metas.to_excel(metaxls)
        logger.debug(f'end to dump task metas for {folder} to {metaxls}')
        
    elif selectedMetafileformat=='csv':
        df_metas = pd.read_json(jsons.dumps(tmp['tasks']), orient = 'index')

        metacsv=os.path.join(folder,'task-meta.csv')

        df_metas.to_csv(metacsv)
        logger.debug(f'end to dump task metas for {folder} to {metacsv} ')
        
    else:
        df_metas = pd.read_json(jsons.dumps(tmp['tasks']), orient = 'records')

        # json is the default ,there is always a videometa.json file after folder check
        metajson=os.path.join(folder,'task-meta.json')

        df_metas.to_json(metajson)
        logger.debug(f'end to dump task metas for {folder} to {metajson} ')


def dumpMetafiles(selectedMetafileformat,folder):
    logger.debug(f'start to dump video metas for {folder} ')

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
    logger.debug(f'end to dump video metas for {folder} ')
    logger.debug(f'start to dump video assets for {folder} ')

    tmpjson=os.path.join(folder,videoassetsfilename)

    if os.path.exists(tmpjson):
        with open(tmpjson,'w') as f:
            f.write(jsons.dumps(ultra[folder]))        
    else:
        with open(tmpjson,'a') as f:
            f.write(jsons.dumps(ultra[folder]))         
    logger.debug(f'end to dump video assets for {folder} ')

def dumpSetting(settingfilename):    
    folder=ROOT_DIR
    logger.info(f'start to dump TiktokaStudio settings')
    logger.debug(f'check settings before dump {settings}')
    tmpjson=os.path.join(folder,settingfilename)

    if os.path.exists(tmpjson):
        with open(tmpjson,'w') as f:
            f.write(jsons.dumps(settings))        
    else:
        with open(tmpjson,'a') as f:
            f.write(jsons.dumps(settings))         
    logger.info(f'end to dump TiktokaStudio settings')






def exportcsv(dbm):
    videos=dbm.Query_undone_videos_in_channel()


def importundonefromcsv(dbm):
    videos=dbm.Query_undone_videos_in_channel()



def testupload(dbm,ttkframe):

    videos=dbm.Query_undone_videos_in_channel()
    print('there is ',len(videos),' video need to uploading for task ')

    if len(videos)>0:
        publicvideos=[]
        privatevideos=[]
        othervideos=[]
        is_open_browser=videos[0]['is_open_browser']
        proxy_option=videos[0]['proxy_option']

        if url_ok('http://www.google.com'):
            print('network is fine,there is no need for proxy ')
            print('start browser in headless mode',is_open_browser)

        else:
            print('google can not be access ')

            print('we need for proxy ',proxy_option)   
            print('start browser in headless mode',is_open_browser,proxy_option)
        upload =  YoutubeUpload(
                root_profile_directory='',
                proxy_option=proxy_option,
                is_open_browser=is_open_browser,
                debug=True,
                use_stealth_js=False,
                # if you want to silent background running, set watcheveryuploadstep false
                channel_cookie_path=videos[0]['channelcookiepath'],
                username=videos[0]['username'],
                browser_type='firefox',
                wait_policy="go next after copyright check success",
                password=videos[0]['password'],
                is_record_video=videos[0]['is_record_video']

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


def runTask(status=status,type=platform,video_id=vid,username=username):
        task_rows=TaskModel.filter_tasks(status=status,type=platform,video_title=vtitle,video_id=vid,username=username) 
        if task_rows is None or len(task_rows)==0:
            showinfomsg(message=f"try to add accounts for {platform} first",parent=chooseAccountsWindow)    

        else:                
            logger.info(f'we found {len(task_rows)} record matching ')
            showinfomsg(message='we found {} record matching'.format(len(task_rows)))
            i=0
            task_data=[]
            for row in task_rows:

                task={
                    "id":CustomID(custom_id=row.id).to_hex(),
                    "platform":                    PLATFORM_TYPE.PLATFORM_TYPE_TEXT[row.setting.platform][1]
,
                    "username":row.username,

                    "proxy":row.proxy,
                    "video title":row.video.video_title,
                    "uploaded_at":datetime.fromtimestamp(row.uploaded_at).strftime("%Y-%m-%d %H:%M:%S") if row.uploaded_at else None, 

                    "inserted_at":datetime.fromtimestamp(row.inserted_at).strftime("%Y-%m-%d %H:%M:%S")  
                }

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
    b_view_readme=tk.Button(frame,text=settings[locale]['docs'],command=lambda: threading.Thread(target=docs(frame,lang)).start() )
    b_view_readme.place(x=50, y=100)    

    b_view_contact=tk.Button(frame,text=settings[locale]['contact'],command=lambda: threading.Thread(target=contact(frame,lang)).start() )
    b_view_contact.place(x=50, y=200)    
    

    b_view_version=tk.Button(frame,text=settings[locale]['version']
                             ,command=lambda: threading.Thread(target=version(frame,lang)).start() )
    b_view_version.place(x=50, y=300)   

def setupWizard(frame):
    ttkframe = tk.Toplevel(frame)
    ttkframe.geometry(window_size)
    ttkframe.title('Setup for')
    channel_cookie_user= tk.StringVar()
    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()


    l_platform = tk.Label(ttkframe, text=settings[locale]['testdatainstall']
                          )
    # l_platform.place(x=10, y=90)
    l_platform.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15)    

    socialplatform = tk.StringVar()
    socialplatform_box = ttk.Combobox(ttkframe, textvariable=socialplatform)


    socialplatform_box['values'] =[settings[locale]['testdatainstall'],settings[locale]['startfromfolder']]



    def socialplatformOptionCallBack(*args):
        print(socialplatform.get())
        print(socialplatform_box.current())
        if socialplatform_box.current()==0:
            test_tasks,test_setting,test_videos,test_users=addTestdata()
            if test_tasks:
                showinfomsg(message='test data is prepared')
        elif socialplatform_box.current()==1:
            ttkframe.withdraw()
            tab_control.select(5)


    socialplatform.set("Select From Platforms")
    socialplatform.trace('w', socialplatformOptionCallBack)
    socialplatform_box.bind('<FocusIn>', socialplatformOptionCallBack())


    # socialplatform_box.config(values =platform_names)
    socialplatform_box.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15)    




def installView(frame,ttkframe,lang):
    b_view_readme=tk.Button(frame,text=settings[locale]['testinstall']
                            ,command=lambda: threading.Thread(target=testInstallRequirements).start() )
    b_view_readme.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)      



    b_install_testdata=tk.Button(frame,text=settings[locale]['newuserwizard']
                            ,command=lambda: threading.Thread(target=setupWizard(frame)).start() )
    b_install_testdata.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)  


    b_install_testdata=tk.Button(frame,text=settings[locale]['testdataRemove']
                            ,command=lambda: threading.Thread(target=removedata).start() )
    b_install_testdata.grid(row = 2, column = 1, sticky='w', padx=14, pady=15)    
    # b_view_contact=tk.Button(frame,text=settings[locale]['testnetwork']
    #                          ,command=lambda: threading.Thread(target=testNetwork).start() )
    # b_view_contact.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    

    # b_view_version=tk.Button(frame,text=settings[locale]['testsettingok']
    #                          ,command=lambda: threading.Thread(target=ValidateSetting).start() )
    # b_view_version.grid(row = 2, column = 1, sticky='w', padx=14, pady=15)      
    
    locale_tkstudio = tk.StringVar()


    l_lang = tk.Label(ttkframe, text=settings[locale]['chooseLang'])
    # l_lang.place(x=10, y=90)
    l_lang.grid(row = 3, column = 0, padx=14, pady=15)    
    try:
        settings['locale']
        print(f"cache locale exist {settings['locale']}")
        locale_tkstudio.set(settings['locale'])
    except:
        print('keep the default locale placeholder')
        # locale_tkstudio_box.set("Select From Langs")
        locale_tkstudio.set("Select From Langs")    
        settings['locale']='en'
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
        locale=locale_tkstudio.get()



    locale_tkstudio.trace('w', locale_tkstudioOptionCallBack)


    locale_tkstudio_box = ttk.Combobox(ttkframe, textvariable=locale_tkstudio)
    locale_tkstudio_box.config(values =('en', 'zh'))
    # locale_tkstudio_box.set(locale_tkstudio.get())    
    locale_tkstudio_box.grid(row = 3, column = 1, padx=14, pady=15)    
    locale_tkstudio_box.bind("<<ComboboxSelected>>", display_selected_item_index)  


      
def videosView(frame,ttkframe,lang):
    global videosView_video_folder
    videosView_video_folder = tk.StringVar()

    # videosView_video_folder.set(setting['video_folder'])

    l_video_folder = tk.Label(frame, text=settings[locale]['videoFolder']
                              )
    l_video_folder.place(x=10, y=20)
    e_video_folder = tk.Entry(frame, width=45, textvariable=videosView_video_folder)
    e_video_folder.place(x=150, y=20)
    b_video_folder=tk.Button(frame,text="Select",command=lambda: threading.Thread(target=select_videosView_video_folder).start() )
    b_video_folder.place(x=580, y=20)    

    l_mode_1 = tk.Label(frame, text=settings[locale]['toolkits']
                        )
    l_mode_1.place(x=10, y=int(height-250))
    
    
    b_autothumb = tk.Button(frame, text=settings[locale]['autothumb']
                            , command=lambda: threading.Thread(target=autothumb).start())
    b_autothumb.place(x=150, y=int(height-250))
    b_batchchangebgmusic = tk.Button(frame, text=settings[locale]['batchchangebgmusic']
                                     , command=lambda: threading.Thread(target=batchchangebgmusic).start())
    b_batchchangebgmusic.place(x=350,y=int(height-250))
    
    
    b_hiddenwatermark = tk.Button(frame, text=settings[locale]['hiddenwatermark']
                                  , command=lambda: threading.Thread(target=hiddenwatermark))
    b_hiddenwatermark.place(x=500,y=int(height-250))

def thumbView(left,right,lang):
    global thumbView_video_folder
    thumbView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=settings[locale]['videoFolder'])
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=thumbView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    if thumbView_video_folder.get()!='':
        if tmp['lastfolder'] is None or tmp['lastfolder']=='':
            pass
        else:            
            if tmp['thumbView_video_folder'] is None:
                thumbView_video_folder.set(tmp['lastfolder'])        
            thumbView_video_folder.set(tmp['thumbView_video_folder'])    

    def e_video_folderCallBack(*args):
        print(f'we are dealing folder {thumbView_video_folder.get()}')
        tmp['thumbView_video_folder']=thumbView_video_folder.get()



    thumbView_video_folder.trace('w', e_video_folderCallBack)

    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(thumbView_video_folder,'thumbView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(thumbView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=settings[locale]['l_metafileformat'])
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
        # analyse_video_meta_pair(thumbView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True,isDesView=False,isTagsView=False,isScheduleView=False)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')
    metafileformat.trace('w', metafileformatCallBack)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)  
    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(thumbView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=
                                   lambda: threading.Thread(target=analyse_video_meta_pair(
                                       thumbView_video_folder.get(),left,right,metafileformatbox.get(),
                                       isThumbView=True,isDesView=False,isTagsView=False,isScheduleView=False)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)
    b_delete_folder_cache=tk.Button(left,text="remove cache data to re-gen",command=lambda: threading.Thread(target=ultra[thumbView_video_folder].unlink()).start() )
    b_delete_folder_cache.grid(row = 2, column = 1,sticky='w', padx=14, pady=15)  


def openXLSX(xlsxpath):
    
    if  platform.system()=='Linux':
    
        
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'") 

    elif platform.system()=='macos':
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'") 
    else:
        os.system('start "excel" "C:\\path\\to\\myfile.xlsx"')
def rendersubmeta(frame,right_frame,folder,pairlabel,missingfilevar,missingmetavar,func,rowno,selectedMetafileformat):
    lb_video_submeta_pairs_counts = tk.Label(frame, text=pairlabel+" paired")
    lb_video_submeta_pairs_counts.grid(row = rowno, column = 0,sticky='w',columnspan=1)     
    Tooltip(lb_video_submeta_pairs_counts, text=f'if there is the same {pairlabel}filename  exist for video,we take it as paired' , wraplength=200)

    video_submeta_pairs_counts =ultra[folder] [missingmetavar]

    lb_video_submeta_pairs_counts_value = tk.Label(frame, text=str(video_submeta_pairs_counts))
    lb_video_submeta_pairs_counts_value.grid(row = rowno, column = 0,sticky='e',padx=0)         


    lb_video_submeta_missing_file_pairs_counts = tk.Label(frame, text='missing file')
    lb_video_submeta_missing_file_pairs_counts.grid(row = rowno, column = 1,sticky='w',padx=50)             
    Tooltip(lb_video_submeta_missing_file_pairs_counts, text=f'we detect whether there is  {pairlabel}  files with the same video filename in this folder' , wraplength=200)

    missing_video_submeta_file_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] [missingfilevar]

    lb_missing_video_submeta_file_pairs_counts = tk.Label(frame, text=str(missing_video_submeta_file_pairs_counts))
    lb_missing_video_submeta_file_pairs_counts.grid(row = rowno, column = 1,sticky='e')            


    lb_video_submeta_missing_meta_pairs_counts = tk.Label(frame, text='missing meta')
    lb_video_submeta_missing_meta_pairs_counts.grid(row = rowno, column =2,sticky='w',padx=50)           
    Tooltip(lb_video_submeta_missing_meta_pairs_counts, text=f'we detect whether {pairlabel}  filed is  filled already in the video metafile' , wraplength=200)

    missing_video_submeta_meta_pairs_counts=ultra[folder] ['videoCounts']-ultra[folder] [missingmetavar]

    lb_missing_video_submeta_meta_pairs_counts = tk.Label(frame, text=str(missing_video_submeta_meta_pairs_counts))
    lb_missing_video_submeta_meta_pairs_counts.grid(row = rowno, column = 2,sticky='e')     


    label_str='Gen'
    if missing_video_submeta_file_pairs_counts>0:
        label_str='Update'



    b_gen_submeta=tk.Button(frame,text=label_str,command=lambda: threading.Thread(target=func(right_frame,True,folder,selectedMetafileformat)).start() )
    b_gen_submeta.grid(row = rowno, column = 3)     
    Tooltip(b_gen_submeta, text=f'Click  to create {pairlabel} meta files' , wraplength=200)
    
def render_video_folder_check_results(frame,right_frame,folder,isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True,selectedMetafileformat='json'):
    lb_video_counts = tk.Label(frame, text='video total counts')

    lb_video_counts.grid(row = 3, column = 0,sticky='w')    

    lb_video_counts_value = tk.Label(frame, text=str(ultra[folder] ['videoCounts']))
    lb_video_counts_value.grid(row = 3, column = 1)    




    if isThumbView==True:
        rendersubmeta(frame,right_frame,folder,'thum','thumbFileCounts','thumbMetaCounts',render_thumb_gen,4,selectedMetafileformat)


    if isDesView==True:
        rendersubmeta(frame,right_frame,folder,'des','desFileCounts','desMetaCounts',render_des_gen,5,selectedMetafileformat)



    if isScheduleView==True:
        rendersubmeta(frame,right_frame,folder,'schedule','scheduleFileCounts','scheduleMetaCounts',
                      render_schedule_gen,6,selectedMetafileformat)




    if isTagsView:
        rendersubmeta(frame,right_frame,folder,'tags','tagFileCounts','tagMetaCounts',render_tag_gen,7,selectedMetafileformat)




    # if isDesView==True and isScheduleView==True and isTagsView==True and isThumbView==True:
    #     rendersubmeta(frame,right_frame,folder,'meta','metaFileCounts','metaMetaCounts',render_update_meta,8,selectedMetafileformat)

def ValidateTagGenMetas(folder,mode_value,preferred_value,frame=None):
    passed=True
    print(f'start to validate tag gen metas,mode is {mode_value},{type(mode_value)}')
    logger.info(f'start to validate tag gen metas')

    if mode_value and mode_value is not None:
        logger.info(f'start to process mode : {mode_value},{type(mode_value)}')

        ultra[folder]['tag_gen_setting']['mode']=mode_value
        ultra[folder]['tag_gen_setting']['preferred']=preferred_value

        if mode_value==1:
            logger.info('in default we fill video tags with video filename')
        elif mode_value==2:
            logger.info('summarize description from subtitles of video,this extension is not supported yet')

        elif mode_value==3:
            logger.info('summarize description from audio of video,this extension is not supported yet')
        elif mode_value==4:
            logger.info('read description from .des .txt with same filename of video')
        elif mode_value==5:
            logger.info('it seems you want fill description of video by hands')

        else: 

            logger.error(f'no valid mode:{mode_value}')
    else:
        logger.info('mode value is none')
        passed=False
    print(f'passed is {passed}')

    if passed==True:
        logger.info(f'tag gen validation passed is {passed}')


        
        lab = tk.Label(frame,text="validation passed, go to gen tag",bg="lightyellow")
        lab.grid(row = 10, column = 1,  padx=14, pady=15,sticky='nw')     
        lab.after(5000,lab.destroy)    
        print(f'sync total video assets with tag gen video meta {ultra[folder]["videos"]}')

        totaljson=os.path.join(folder,videoassetsfilename)

        if os.path.exists(totaljson):
            with open(totaljson,'w') as f:
                f.write(jsons.dumps(ultra[folder]))        
        else:
            with open(totaljson,'a') as f:
                f.write(jsons.dumps(ultra[folder]))    
    else:
        logger.debug(f'tag gen validation failed')
    return passed
def genTag(folder,mode_value,prefer_tags,frame=None):
    passed=ValidateTagGenMetas(folder,mode_value,prefer_tags,frame=None)


    print('read video meta')

 
    print('read tag gen settings')

    template_data=ultra[folder]['tag_gen_setting'] 
    video_data = ultra[folder]['videos']
   
    for video_id, video_info in video_data.items():
        print(f'tag gen -process video-start tag body {video_id}')

        logger.info(f'tag gen -process video-start tag body {video_id}')


        if mode_value==1:
            logger.info(f'tag gen -process video-extract from video filename with # {video_id}')

            ultra[folder]['videos'][video_id]['tags']=','.join(ultra[folder]['videos'][video_id]['video_filename'].split('#').pop(0))
        elif mode_value==2:
            logger.info(f'tag gen -process video-gen from  rapidtags not supported yet {video_id}')
        elif mode_value==3:
            logger.info(f'tag gen -process video-auto gen from category and video description, not supported yet {video_id}')

        elif mode_value==4:
            logger.info(f'tag gen -process video-read from .tag file with  same video filename {video_id}')
            print(f'tag gen -process video-read from .tag file with  same video filename {video_id}')

            # ultra[folder]['videos'][video_id]['tags']=''
            for ext in supported_tag_exts:
                tagfilepath=os.path.join(folder,video_id+ext)
                if os.path.exists(tagfilepath):
                    with open(tagfilepath,'r',encoding='utf-8') as f:
                        lines=f.readlines()
                        
                        contents = '\r'.join(lines)
                        contents = contents.replace('\n','')
                        ultra[folder]['videos'][video_id]['tags']=contents 
                    logger.info(f'tag gen -set file content  to tag field:\r{tagfilepath}')

                else:
                    logger.debug(f'tag gen file broken {tagfilepath}')
                    print(f'tag gen file broken {tagfilepath}')

                ultra[folder]['videos'][video_id]['tags']
        logger.info(f'tag gen -process video-end tag body {video_id}')
        print(f'tag gen -process video-end tag body {video_id}')


        logger.info(f'tag gen -process video  start with prefer_tags {video_id}')
        if prefer_tags and prefer_tags !='':
            ultra[folder]['videos'][video_id]['tags']=prefer_tags+','+ultra[folder]['videos'][video_id]['tags']
        logger.info(f'tag gen -process video  end with prefer_tags {video_id}')

    
    lab = tk.Label(frame,text="end to gen tagcription,run check video assets again to see what happens",bg="lightyellow")
    lab.grid(row = 10, column = 1,  padx=14, pady=15,sticky='nw')     
    lab.after(5000,lab.destroy)    
    print(f'sync total video assets with tag gen video meta {ultra[folder]["videos"]}')

    logger.info('end to gen tagcription')
    logger.info('start to sync tagcription meta to video meta file')

    dumpMetafiles(ultra[folder]['metafileformat'],folder)
    logger.info('end to sync gen tagcription meta to video meta file')

    logger.info('start to sync gen tagcription meta to video assets file')
    
    syncVideometa2assetsjson(ultra[folder]['metafileformat'],folder)
    logger.info('end to sync gen tagcription meta to video assets file')

def ValidateDesGenMetas(folder,descriptionPrefix_value,mode_value,descriptionSuffix_value,frame=None):
    passed=True
    print(f'start to validate des gen metas,mode is {mode_value},{type(mode_value)}')
    logger.info(f'start to validate des gen metas')

    if mode_value and mode_value is not None:
        logger.info(f'start to process mode : {mode_value},{type(mode_value)}')

        ultra[folder]['des_gen_setting']['mode']=mode_value
        ultra[folder]['des_gen_setting']['descriptionPrefix']=descriptionPrefix_value
        ultra[folder]['des_gen_setting']['descriptionSuffix']=descriptionSuffix_value

        if mode_value==1:
            logger.info('in default we fill video description with video filename')
        elif mode_value==2:
            logger.info('summarize description from subtitles of video,this extension is not supported yet')

        elif mode_value==3:
            logger.info('summarize description from audio of video,this extension is not supported yet')
        elif mode_value==4:
            logger.info('read description from .des .txt with same filename of video')
        elif mode_value==5:
            logger.info('it seems you want fill description of video by hands')

        else: 

            logger.error(f'no valid mode:{mode_value}')
    else:
        logger.info('mode value is none')
        passed=False
    print(f'passed is {passed}')

    if passed==True:
        logger.info(f'des gen validation passed is {passed}')


        
        lab = tk.Label(frame,text="validation passed, go to gen des",bg="lightyellow")
        lab.grid(row = 10, column = 1,  padx=14, pady=15,sticky='nw')     
        lab.after(5000,lab.destroy)    
        print(f'sync total video assets with des gen video meta {ultra[folder]["videos"]}')

        totaljson=os.path.join(folder,videoassetsfilename)

        if os.path.exists(totaljson):
            with open(totaljson,'w') as f:
                f.write(jsons.dumps(ultra[folder]))        
        else:
            with open(totaljson,'a') as f:
                f.write(jsons.dumps(ultra[folder]))    
    else:
        logger.debug(f'des gen validation failed')
    return passed

def genDes(folder,descriptionPrefix_value,mode_value,descriptionSuffix_value,frame=None):
    passed=ValidateDesGenMetas(folder,descriptionPrefix_value,mode_value,descriptionSuffix_value,frame=None)


    print('read video meta')

 
    print('read des gen settings')

    template_data=ultra[folder]['des_gen_setting'] 
    video_data = ultra[folder]['videos']
   
    for video_id, video_info in video_data.items():
        logger.info(f'des gen -process video-start des body {video_id}')

        if mode_value==4:
            ultra[folder]['videos'][video_id]['video_description']=''
            for ext in supported_des_exts:
                desfilepath=os.path.join(folder,video_id+ext)
                if os.path.exists(desfilepath):
                    with open(desfilepath,'r',encoding='utf-8') as f:
                        lines=f.readlines()
                        
                        contents = '\r'.join(lines)
                        contents = contents.replace('\n','')
                        ultra[folder]['videos'][video_id]['video_description']=contents 
                    logger.info(f'des gen -set file content  to video_description field:\r{desfilepath}')

                else:
                    logger.debug(f'des gen file broken {desfilepath}')

                ultra[folder]['videos'][video_id]['video_description']
        logger.info(f'des gen -process video-end des body {video_id}')


        logger.info(f'des gen -process video  start with suffix and prefix {video_id}')
        ultra[folder]['videos'][video_id]['video_description']=descriptionPrefix_value+ultra[folder]['videos'][video_id]['video_description']+descriptionSuffix_value
        logger.info(f'des gen -process video  end with suffix and prefix {video_id}')

    
    lab = tk.Label(frame,text="end to gen description,run check video assets again to see what happens",bg="lightyellow")
    lab.grid(row = 10, column = 1,  padx=14, pady=15,sticky='nw')     
    lab.after(5000,lab.destroy)    
    print(f'sync total video assets with des gen video meta {ultra[folder]["videos"]}')

    logger.info('end to gen description')
    logger.info('start to sync description meta to video meta file')

    dumpMetafiles(ultra[folder]['metafileformat'],folder)
    logger.info('end to sync gen description meta to video meta file')

    logger.info('start to sync gen description meta to video assets file')
    
    syncVideometa2assetsjson(ultra[folder]['metafileformat'],folder)
    logger.info('end to sync gen description meta to video assets file')
def render_des_gen(frame,isneed,folder,selectedMetafileformat='json'):
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
        # desmode.trace('w',render_des_update_view(new_canvas,folder,desmode,frame))
        lab = tk.Label(new_canvas,text="请选择你的视频描述从何而来",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw') 
   
        desmode1=tk.Radiobutton(new_canvas,text="手动准备",variable=desmode,value=1,command=lambda:render_des_update_view(new_canvas,folder,desmode,frame))
        desmode1.grid(row = 1, column = 1,  padx=14, pady=15,sticky='nw') 
        desmode2=tk.Radiobutton(new_canvas,text=" 批量生成",variable=desmode,value=2,command=lambda:render_des_update_view(new_canvas,folder,desmode,frame))
        desmode2.grid(row = 1, column = 2,  padx=14, pady=15,sticky='nw') 

        # thumbmode.trace_add('write', render_thumb_update_view(new_canvas,folder,thumbmode))




def render_des_update_view(frame,folder,desmode,previous_frame=None):
    print('desmode',type(desmode.get()),desmode.get())    
    lang='en'

    if len(frame.winfo_children())>0:
        for widget in frame.winfo_children():
            widget.destroy()      
   
    if desmode.get() ==1:
        lbl15 = tk.Label(frame, text='两种选择')
        lbl15.grid(row=0,column=0,padx=14, pady=15,sticky='w') 
       
        lbl15 = tk.Label(frame, text='1.手动准备视频描述，填充到元数据对应字段即可，元数据格式支持xlsx json csv',wraplength=600)
        lbl15.grid(row=1,column=0, sticky='w')

        lbl15 = tk.Label(frame, text='2.\r',wraplength=600)
        lbl15.grid(row=2,column=0, sticky='w')



        b_check_metas_=tk.Button(frame,text="edit videometa with local editor",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 5, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_check_metas_, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)
        
        if ultra[folder]['metafileformat']=='json':

            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 6, column = 0, padx=14, pady=15,sticky='nswe') 
            Tooltip(b_check_metas_, text='For those who dont have json editor or have install issues' , wraplength=200)
        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 4, column = 0, padx=14, pady=15,sticky='nswe')      


        b_check_metas_=tk.Button(frame,text="edit videometa",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 7, column = 0, padx=14, pady=15,sticky='nswe') 

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_des_gen(previous_frame,True,folder))
        b_return.grid(row = 8, column =0)   

    else:

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_des_gen(previous_frame,True,folder))
        b_return.grid(row = 0, column =1)   


        mode = tk.IntVar()
        mode.set(1)

        lab = tk.Label(frame,text="Step1:请选择视频描述主体从何而来",bg="lightyellow",width=30)
        lab.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode1=tk.Radiobutton(frame,text="视频文件名称",variable=mode,value=1,command='')
        Tooltip(mode1, text='视频描述使用视频文件名称' , wraplength=200)

        mode1.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode2=tk.Radiobutton(frame,text="视频字幕文件总结",variable=mode,value=2,command='')
        Tooltip(mode2, text='利用字幕文件总结视频描述，字幕文件须与视频文件同名' , wraplength=200)

        mode2.grid(row = 1, column = 1, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode3=tk.Radiobutton(frame,text="视频音频总结",variable=mode,value=3,command='')
        Tooltip(mode2, text='利用视频音频部分总结视频描述' , wraplength=200)

        mode3.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode4=tk.Radiobutton(frame,text="从视频描述文件中来",variable=mode,value=4,command='')
        Tooltip(mode4, text='视频描述文件须与视频文件同名，后缀可以是.des' , wraplength=200)

        mode4.grid(row = 2, column = 1, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode5=tk.Radiobutton(frame,text="从元数据中来",variable=mode,value=5,command='')
        mode5.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        Tooltip(mode5, text='视频描述文可后续在元数据文件中手动编辑' , wraplength=200)



        lab_step2 = tk.Label(frame,text="Step2:是否使用统一前缀后缀",bg="lightyellow")
        lab_step2.grid(row = 4, column = 0,  padx=14, pady=15,sticky='nw')         
        Tooltip(lab_step2, text='可以通过设置前缀 后缀模板批量标准化频道的视频描述' , wraplength=200)

        descriptionPrefix=tk.StringVar()
        descriptionSuffix=tk.StringVar()

        l_preferdesprefix = tk.Label(frame, text=settings[locale]['descriptionPrefix']
                                     )
        l_preferdesprefix.grid(row = 5, column = 0,  padx=14, pady=15,sticky='nw') 
        e_preferdesprefix = tk.Entry(frame, width=55, textvariable=descriptionPrefix)
        e_preferdesprefix.grid(row = 5, column = 1,  padx=14, pady=15,sticky='nw') 
        Tooltip(l_preferdesprefix, text='add \r if you want line breaks' , wraplength=200)


        l_preferdessuffix = tk.Label(frame, text=settings[locale]['descriptionSuffix']
                                     )
        l_preferdessuffix.grid(row = 6, column = 0,  padx=14, pady=15,sticky='nw') 
        e_preferdessuffix = tk.Entry(frame, width=55, textvariable=descriptionSuffix)
        e_preferdessuffix.grid(row = 6, column = 1,  padx=14, pady=15,sticky='nw') 
        Tooltip(l_preferdessuffix, text='add \r if you want line breaks' , wraplength=200)
        
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


        b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateDesGenMetas(folder,descriptionPrefix.get(),mode.get(),descriptionSuffix.get(),frame))
        b_update_metas_.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nswe') 
        



        b_gen_thumb_=tk.Button(frame,text="gen descriptions",command=lambda: genDes(folder,descriptionPrefix.get(),mode.get(),descriptionSuffix.get(),frame))
        b_gen_thumb_.grid(row = 11, column =0, padx=14, pady=15,sticky='nswe') 


        b_check_metas_=tk.Button(frame,text="check metajson",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_check_metas_.grid(row = 12, column = 0, padx=14, pady=15,sticky='nswe') 

def render_tag_gen(frame,isneed,folder,selectedMetafileformat='json'):
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
        # desmode.trace('w',render_des_update_view(new_canvas,folder,desmode,frame))
        lab = tk.Label(new_canvas,text="请选择你的视频标签从何而来",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw') 
   
        desmode1=tk.Radiobutton(new_canvas,text="手动准备",variable=desmode,value=1,command=lambda:render_tag_update_view(new_canvas,folder,desmode,frame))
        desmode1.grid(row = 1, column = 1,  padx=14, pady=15,sticky='nw') 
        desmode2=tk.Radiobutton(new_canvas,text=" 批量生成",variable=desmode,value=2,command=lambda:render_tag_update_view(new_canvas,folder,desmode,frame))
        desmode2.grid(row = 1, column = 2,  padx=14, pady=15,sticky='nw') 

        # thumbmode.trace_add('write', render_thumb_update_view(new_canvas,folder,thumbmode))




def render_tag_update_view(frame,folder,desmode,previous_frame=None):
    print('tagmode',type(desmode.get()),desmode.get())    

    if len(frame.winfo_children())>0:
        for widget in frame.winfo_children():
            widget.destroy()      
   
    if desmode.get() ==1:
        lbl15 = tk.Label(frame, text='两种选择')
        lbl15.grid(row=0,column=0,padx=14, pady=15,sticky='w') 
       
        lbl15 = tk.Label(frame, text='1.手动准备视频标签，填充到元数据对应字段即可，元数据格式支持xlsx json csv',wraplength=600)
        lbl15.grid(row=1,column=0, sticky='w')

        lbl15 = tk.Label(frame, text='2.\r',wraplength=600)
        lbl15.grid(row=2,column=0, sticky='w')



        b_check_metas_=tk.Button(frame,text="edit videometa with local editor",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 5, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_check_metas_, text='fill heading,subheading,etra you want to render in clickbait thubmnail.you can overwrite the template  default bg image with a special one for this video.if you dont have a prepared one,you can use the following options to auto set this bg field' , wraplength=200)
        
        if ultra[folder]['metafileformat']=='json':

            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 6, column = 0, padx=14, pady=15,sticky='nswe') 
            Tooltip(b_check_metas_, text='For those who dont have json editor or have install issues' , wraplength=200)
        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 4, column = 0, padx=14, pady=15,sticky='nswe')      


        b_check_metas_=tk.Button(frame,text="edit videometa",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 7, column = 0, padx=14, pady=15,sticky='nswe') 

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_tag_gen(previous_frame,True,folder))
        b_return.grid(row = 8, column =0)   

    else:

        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_tag_gen(previous_frame,True,folder))
        b_return.grid(row = 0, column =1)   


        mode = tk.IntVar()
        mode.set(1)

        lab = tk.Label(frame,text="Step1:请选择视频标签从何而来",bg="lightyellow",width=30)
        lab.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode1=tk.Radiobutton(frame,text="视频文件名称中#",variable=mode,value=1,command='')
        Tooltip(mode1, text='视频标签使用视频文件名称带#的部分,比如文件名为xxxxxxxxxx#t1#t2#t3.mp4' , wraplength=200)

        mode1.grid(row = 1, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode2=tk.Radiobutton(frame,text="rapidtags",variable=mode,value=2,command='')
        Tooltip(mode2, text='利用rapidtags获取' , wraplength=200)

        mode2.grid(row = 1, column = 1, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode3=tk.Radiobutton(frame,text="自动",variable=mode,value=3,command='')
        Tooltip(mode2, text='利用视频分类和视频内容总结,推荐最佳的视频标签' , wraplength=200)

        mode3.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode4=tk.Radiobutton(frame,text="从视频标签文件中来",variable=mode,value=4,command='')
        Tooltip(mode4, text='视频描述文件须与视频文件同名，后缀必须是.tag,新建txt文件填写内容，修改后缀为tag' , wraplength=200)

        mode4.grid(row = 2, column = 1, columnspan = 3, padx=14, pady=15,sticky='nw') 
        mode5=tk.Radiobutton(frame,text="从元数据中来",variable=mode,value=5,command='')
        mode5.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        Tooltip(mode5, text='视频标签可后续在元数据文件中手动编辑' , wraplength=200)



        lab_step2 = tk.Label(frame,text="Step2:是否使用优先标签",bg="lightyellow")
        lab_step2.grid(row = 4, column = 0,  padx=14, pady=15,sticky='nw')         
        Tooltip(lab_step2, text='可以通过设置优先标签批量标准化频道的视频标签' , wraplength=200)

        preferTags=tk.StringVar()

        l_preferredTags = tk.Label(frame, text=settings[locale]['preferTags'])
        l_preferredTags.grid(row = 5, column = 0,  padx=14, pady=15,sticky='nw') 
        e_preferredTags = tk.Entry(frame, width=55, textvariable=preferTags)
        e_preferredTags.grid(row = 5, column = 1,  padx=14, pady=15,sticky='nw') 
        Tooltip(l_preferredTags, text='add \r if you want line breaks' , wraplength=200)


        
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
        lab = tk.Label(frame,text="Step4:生成视频标签",bg="lightyellow",width=30)
        lab.grid(row = 9, column = 0,  padx=14, pady=15,sticky='nw')         


        b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateTagGenMetas(folder,mode.get(),preferTags.get(),frame))
        b_update_metas_.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nswe') 
        



        b_gen_thumb_=tk.Button(frame,text="gen descriptions",command=lambda: genTag(folder,mode.get(),preferTags.get(),frame))
        b_gen_thumb_.grid(row = 11, column =0, padx=14, pady=15,sticky='nswe') 


        b_check_metas_=tk.Button(frame,text="check metajson",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_check_metas_.grid(row = 12, column = 0, padx=14, pady=15,sticky='nswe') 



def render_schedule_gen(frame,isneed,folder,selectedMetafileformat):
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

        lab = tk.Label(new_canvas,text="请选择你的发布时间从何而来",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw') 
   
        thumbmode1=tk.Radiobutton(new_canvas,text="手动准备",variable=thumbmode,value=1,command=lambda:render_schedule_update_view(new_canvas,folder,thumbmode,frame,selectedMetafileformat))
        thumbmode1.grid(row = 1, column = 1,  padx=14, pady=15,sticky='nw') 
        thumbmode2=tk.Radiobutton(new_canvas,text=" 批量生成",variable=thumbmode,value=2,command=lambda:render_schedule_update_view(new_canvas,folder,thumbmode,frame,selectedMetafileformat))
        thumbmode2.grid(row = 1, column = 2,  padx=14, pady=15,sticky='nw') 

        # thumbmode.trace_add('write', render_thumb_update_view(new_canvas,folder,thumbmode))


def render_schedule_update_view(frame,folder,thumbmode,previous_frame,selectedMetafileformat):
    def policyOptionCallBack(*args):
        schframe = ttk.Frame(frame)
        schframe.grid(row=7, column=0, sticky="nsew")

        # if mode.get() in [3,4,5]:

        l_dailycount = tk.Label(schframe, text='dailyVideoLimit')
        Tooltip(l_dailycount, text='you want to release how many video in one day' , wraplength=200)





        l_releasehour = tk.Label(schframe, text='release hour')
        Tooltip(l_releasehour, text=f"you can input like '10:15,' more available can choose from {settings[locale]['availableScheduleTimes']}" , wraplength=200)



        releasehour.set(settings[locale]['default_release_hour'])

        e_releasehour = tk.Entry(schframe, width=55, textvariable=releasehour)

        Tooltip(e_releasehour, text=f"you can input more than one with comma separator,such as 10:15,12:00,if you want publish 10 video in serial you should put 10 time here,more available can choose from {settings[locale]['availableScheduleTimes']}" , wraplength=200)

        start_publish_date.set(1)

        l_start_publish_date=tk.Label(schframe, text='offsetDays')
        Tooltip(l_start_publish_date, text='we calculate publish date from today,  default +1 is tomorrow' , wraplength=200)

        e_start_publish_date = tk.Entry(schframe, width=55, textvariable=start_publish_date)



        releasedatehourbox = ttk.Combobox(schframe, textvariable=dailycount)


        def display_selected_item_index(event): 
            print('index of this item is: {}\n'.format(releasedatehourbox.current()))
            number=dailycount.get()
            if dailycount.get()=='Select From policy':
                number=1
                randomNreleasehour=settings[locale]['default_release_hour']
            else:
                randomNreleasehour=','.join(random.sample(settings[locale]['availableScheduleTimes'], int(number)))
            releasehour.set(randomNreleasehour)
        def OptionCallBack(*args):
            # print(variable.get())
            # print(releasedatehourbox.current())
            number=dailycount.get()
            print('current dailycount ')
            if dailycount.get()=='Select From policy':
                number=1
            randomNreleasehour=','.join(random.sample(settings[locale]['availableScheduleTimes'], int(number)))
            releasehour.set(randomNreleasehour)

        dailycount.set("Select From policy")
        dailycount.trace('w', OptionCallBack)


        releasedatehourbox.config(values =list(range(1,21)))
        releasedatehourbox.bind("<<ComboboxSelected>>", display_selected_item_index)  




        # print(f'modeis {type(mode.get())} {mode.get()}')
        if mode.get() in [1,2]:
            try:
                logger.info(f'grid_remove hidden offset elements')

                l_dailycount.grid_remove()
                l_start_publish_date.grid_remove()            
                e_start_publish_date.grid_remove()   
                releasedatehourbox.grid_remove() 
                l_releasehour.grid_remove()
                e_releasehour.grid_remove()

            except:
                pass     

            try:
                logger.info(f'grid_forget hidden offset elements')

                l_dailycount.grid_forget()
                l_start_publish_date.grid_forget()            
                e_start_publish_date.grid_forget()   
                releasedatehourbox.grid_forget() 
                l_releasehour.grid_forget()
                e_releasehour.grid_forget()     
                logger.info(f'visible {l_dailycount.winfo_ismapped() }')

            except:
                pass              
 

            
            try:
                logger.info(f'destroy hidden offset elements')

                l_dailycount.destroy()
                l_start_publish_date.destroy()            
                e_start_publish_date.destroy()   
                releasedatehourbox.destroy() 
                l_releasehour.destroy()
                e_releasehour.destroy()

            except:
                pass     
        elif mode.get() in [3,4,5]:
            logger.info(f'show offset elements')

            l_dailycount.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nswe') 
            releasedatehourbox.grid(row=1, column=1, padx=10)

            l_releasehour.grid(row = 2, column = 0,  padx=14, pady=15,sticky='nswe')         
            e_releasehour.grid(row = 2, column = 1,  padx=14, pady=15,sticky='nswe') 

            l_start_publish_date.grid(row = 0, column = 0, padx=14, pady=15,sticky='nswe')             
            e_start_publish_date.grid(row = 0, column = 1, padx=14, pady=15,sticky='nswe')  


    if len(frame.winfo_children())>0:
        for widget in frame.winfo_children():
            widget.destroy()      
   
    if thumbmode.get() ==1:
        lbl15 = tk.Label(frame, text='两种选择')
        lbl15.grid(row=1,column=0,padx=14, pady=15,sticky='w') 
        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_schedule_gen(previous_frame,True,folder))
        b_return.grid(row = 0, column =1,padx=14, pady=15,sticky='w') 

        lbl15 = tk.Label(frame, text='1.手动准备发布时间文件，需放在视频所在文件夹下，且与视频文件同名,完成后再次检测即可',wraplength=600)
        lbl15.grid(row=2,column=0, sticky='nswe')

        lbl15 = tk.Label(frame, text='2.如果没有发布时间文件，需手动编辑视频元数据中发布时间字段,包括日期和时间段,编辑完成后可再次进行检测\r',wraplength=600)
        lbl15.grid(row=3,column=0, sticky='nswe')




        b_check_metas_=tk.Button(frame,text="edit videometa with local editor",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 5, column = 0, padx=14, pady=15,sticky='nswe') 
        Tooltip(b_check_metas_, text='fill release date and hour fields in meta files' , wraplength=200)
        
        if ultra[folder]['metafileformat']=='json':

            b_edit_thumb_metas=tk.Button(frame,text="edit json with online editor",command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"))
            b_edit_thumb_metas.grid(row = 6, column = 0, padx=14, pady=15,sticky='nswe') 
            Tooltip(b_check_metas_, text='For those who dont have json editor or have install issues' , wraplength=200)

        b_open_video_folder=tk.Button(frame,text="open local",command=lambda: threading.Thread(target=openLocal(folder)).start() )
        b_open_video_folder.grid(row = 4, column = 0, padx=14, pady=15,sticky='nswe')      


        b_update_metas_=tk.Button(frame,text="validate meta",command='validate thumbpath is there')
        b_update_metas_.grid(row = 7, column = 0,  padx=14, pady=15,sticky='nswe') 



    else:
        mode = tk.IntVar()
        mode.set(1)
        releasehour=tk.StringVar()
        dailycount = tk.StringVar(frame)
        start_publish_date=tk.StringVar()

        mode.trace_add('write', policyOptionCallBack)

        lab = tk.Label(frame,text="Step1:请选择你的发布时间生成策略",bg="lightyellow",width=30)
        lab.grid(row = 1, column = 0,  padx=14, pady=15,sticky='nw')    
        b_return=tk.Button(frame,text="Back to previous page",command=lambda: render_schedule_gen(previous_frame,True,folder))
        b_return.grid(row = 1, column = 2,  padx=14, pady=15,sticky='e')   


        mode1=tk.Radiobutton(frame,text="私有",variable=mode,value=1,command=policyOptionCallBack)
        # Tooltip(mode1, text='you dont install this extension yet' , wraplength=200)

        mode1.grid(row = 2, column = 0,  padx=14, pady=15,sticky='nw') 
        mode2=tk.Radiobutton(frame,text="公开",variable=mode,value=2,command=policyOptionCallBack)
        # mode2.configure(state = tk.DISABLED)
        # Tooltip(mode2, text='you dont install this extension yet' , wraplength=200)

        mode2.grid(row = 3, column = 0,  padx=14, pady=15,sticky='nw') 
        mode3=tk.Radiobutton(frame,text="定时",variable=mode,value=3,command=policyOptionCallBack)
        mode3.grid(row = 4, column = 0,  padx=14, pady=15,sticky='nw') 
        Tooltip(mode3, text='please select the bg image folder ' , wraplength=200)

        mode3=tk.Radiobutton(frame,text="unlisted",variable=mode,value=4,command=policyOptionCallBack)
        mode3.grid(row = 5, column = 0, padx=14, pady=15,sticky='nw') 

        mode4=tk.Radiobutton(frame,text="public&premiere",variable=mode,value=5,command=policyOptionCallBack)
        mode4.grid(row = 6, column = 0,  padx=14, pady=15,sticky='nw')         
 
        lab = tk.Label(frame,text="Step4:生成发布时间",bg="lightyellow",width=30)
        lab.grid(row = 9, column = 0,  padx=14, pady=15,sticky='nw')         


        # b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateThumbnailGenMetas(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_folder.get(),frame))
        # b_update_metas_.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nswe') 
        



        b_gen_thumb_=tk.Button(frame,text="gen schedule time plan",command=lambda: genScheduleSLots(folder,mode.get(),start_publish_date.get(),dailycount.get(),releasehour.get(),frame,selectedMetafileformat))
        b_gen_thumb_.grid(row = 11, column =0, padx=14, pady=15,sticky='nswe') 


        b_check_metas_=tk.Button(frame,text="check videometa",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        b_check_metas_.grid(row = 12, column = 0, padx=14, pady=15,sticky='nswe') 

def genScheduleSLots(folder,mode_value,start_publish_date_value,dailycount_value,releasehour_value,frame,selectedMetafileformat):
    logger.info('start to gen slots')
    publish_policy=[1,2,3,4,5].index(mode_value)
    # //0 -private 1-publish 2-schedule 3-Unlisted 4-public&premiere 
    today = date.today()

    date_to_publish = datetime(today.year, today.month, today.day)
    default_hour_to_publish = settings[locale]['default_release_hour']
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    start_publish_date_value=int(start_publish_date_value)
    if 'Select From policy'==dailycount_value:
        dailycount_value=1
    dailycount_value=int(dailycount_value)    
    metafilechanges=False
    if metafilechanges:
    # 检测缓存中的更新时间 和videometafile的修改时间进行比较，发生变化就同步
        syncVideometa2assetsjson(selectedMetafileformat,folder)
    video_data = ultra[folder]['videos']
    counts=len(video_data)   
    offsets=0
    avalaibleslots=[]
    releasehour_value=releasehour_value.strip()

    # text = "这是一个包含半角逗号,和全角逗号，的示例。"

    # 使用正则表达式搜索半角或全角逗号
    comma_pattern = re.compile(r'[,\uFF0C]')
    match = comma_pattern.search(releasehour_value)

    if match:
        print("字符串中包含半角或全角逗号。")    
        releasehour_value = re.sub(r'[,\uFF0C]', ',', releasehour_value)        
    if ',' in releasehour_value:

        avalaibleslots=releasehour_value.split(',')
    else:
        avalaibleslots.append(releasehour_value)   
    if dailycount_value==len(avalaibleslots):
        logger.info('your daily count and time slot matchs')
    elif dailycount_value>len(avalaibleslots) and len(avalaibleslots)==1:
        logger.info(f'your daily count is{dailycount_value} time slot is {avalaibleslots},it appears you want to publish them at the same time')
        for i in len(dailycount_value)-1:
            avalaibleslots.append(avalaibleslots[0])
    elif dailycount_value>len(avalaibleslots) and len(avalaibleslots)>1:
        logger.info(f'your daily count is{dailycount_value} time slot is {avalaibleslots},it appears you want to random choose { dailycount_value -len(avalaibleslots)} slots for the missing')
        randomslots=random.sample(settings[locale]['availableScheduleTimes'],dailycount_value-len(avalaibleslots))
        avalaibleslots+=randomslots
    elif dailycount_value  < len(avalaibleslots):
        logger.info(f'your daily count is{dailycount_value} time slot is {avalaibleslots},it appears you want to random choose { dailycount_value} slots from you specify: {avalaibleslots}  ')
        randomslots=random.sample(avalaibleslots,dailycount_value)
        avalaibleslots=randomslots
    tmpslots=    avalaibleslots        
    for video_id, video_info in video_data.items():    
        if offsets==dailycount_value:
            offsets=0
            tmpslots=avalaibleslots
        if  video_info['publish_policy'] in  [0,1]:
            logger.info(f'this video {video_id} is set to public or private without need to gen schedule')
        else:
            if  video_info['release_date']=="":
            
                video_info['release_date']=date_to_publish + timedelta(days=start_publish_date_value+offsets)
                offsets+=1
                date_hour=random.choice(tmpslots)  
                video_info['release_date_hour']=date_hour
                logger.info(f"start to assign this video {video_id},{video_info['release_date']},{video_info['release_date_hour']} ")

                tmpslots.remove(date_hour)
            else:
                logger.info(f"this video {video_id} is assigned release date{video_info['release_date']},{video_info['release_date_hour']} ")


    logger.info('sync slots to video metas')
    dumpMetafiles(selectedMetafileformat,folder)
    logger.info('sync slots to video assets')
    logger.info('sync slots to cache')
    lab = tk.Label(frame,text="assign schedules finished,you can check videometa",bg="lightyellow")
    lab.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nw')     
    lab.after(5000,lab.destroy)    
def render_update_meta(frame,isneed,folder,selectedMetafileformat='json'):
    if isneed==True:
        lang='en'
        prefertags=tk.StringVar()
        if len(frame.winfo_children())>0:
            for widget in frame.winfo_children():
                widget.destroy()
        
        lab = tk.Label(frame,text="batch modify video metas",bg="lightyellow",width=30)
        # dropdown platform   so they can have diff fields
        l_prefertags = tk.Label(frame, text=settings[locale]['is_not_for_kid']
                                )
        l_prefertags.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15,sticky='nw') 
        el_prefertags = tk.Entry(frame, width=55, textvariable=prefertags)
        el_prefertags.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15,sticky='nw') 

        categories=tk.StringVar()

        l_categories = tk.Label(frame, text=settings[locale]['categories']
                                )
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
                            if ultra[folder]['videos'][filename]['thumbnail_local_path'] is None:
                                ultra[folder]['videos'][filename]['thumbnail_local_path']=[]
                            
                            
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
        logger.info('start to add new gen thum to video meta')
        print(f"before add thumb for video {video_id} is {video_data[video_id]['thumbnail_local_path']}")
        print('test===',type(video_data[video_id]['thumbnail_local_path']),video_data[video_id]['thumbnail_local_path'])
        if type(video_data[video_id]['thumbnail_local_path'])==str:
            video_data[video_id]['thumbnail_local_path']=eval(video_data[video_id]['thumbnail_local_path'])
            video_data[video_id]['thumbnail_local_path'].append(outputpath)
        elif video_data[video_id]['thumbnail_local_path'] is None or video_data[video_id]['thumbnail_local_path'] in ['','[]'] or len(video_data[video_id]['thumbnail_local_path'])==0:
            empt=[].append(outputpath)
            video_data[video_id]['thumbnail_local_path']=str(empt)
        else:
            video_data[video_id]['thumbnail_local_path'].append(outputpath)

        print(f"after add thumb for video {video_id} is {video_data[video_id]['thumbnail_local_path']}")
        
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


                filepath=draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)
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

                filepath=draw_text_on_image(video_info,thumb_gen_setting,result_image_width,result_image_height,render_style,output_folder,filename)
    logger.info('end to gen thumbnail')
    logger.info('start to sync thumbnail meta to video meta file')

    dumpMetafiles(ultra[folder]['metafileformat'],folder)
    logger.info('end to sync gen thumbnail meta to video meta file')

    logger.info('start to sync gen thumbnail meta to video assets file')
    
    syncVideometa2assetsjson(ultra[folder]['metafileformat'],folder)
    logger.info('end to sync gen thumbnail meta to video assets file')

def render_thumb_gen(frame,isneed,folder,selectedMetafileformat='json'):
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


        b_thumbnail_template_file=tk.Button(frame,text="select",command=lambda: threading.Thread(target=select_file('select thumb template json file',thumbnail_template_file,ultra[folder]['thumb_gen_setting']['template_path'],'json')).start() )
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

def chooseProxies(ttkframe,username,parentchooseProxies):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)
    
    
    newWindow.title('proxy selection')

    if username=='':
        username='this user account'

    # label = tk.Label(newWindow,
    #             text = f"Select the proxies for {username} below : ",
    #             font = ("Times New Roman", 10),
    #             padx = 10, pady = 10)
    # # label.pack()
    # label.grid(row=0,column=0, sticky=tk.W)
    
    ttkframe=newWindow
    
    global city_user,country_user,proxyTags_user,proxyStatus_user,proxy_str
    city = tk.StringVar()
    state = tk.StringVar()
    network_type = tk.StringVar()
    country = tk.StringVar()
    proxyTags = tk.StringVar()

    lbl15 = tk.Label(ttkframe, text='by city.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(ttkframe,textvariable=city)
    txt15.insert(0,'Los')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=0, sticky=tk.W)


    l_state= tk.Label(ttkframe, text='by state.')
    l_state.grid(row=0,column=1, sticky=tk.W)
    e_state = tk.Entry(ttkframe,textvariable=state)
    e_state.insert(0,'LA')
    e_state.grid(row=1,column=1, sticky=tk.W)


    lbl16 = tk.Label(ttkframe, text='by country.')
    lbl16.grid(row=0,column=2, sticky=tk.W)
    txt16 = tk.Entry(ttkframe,textvariable=country)
    txt16.insert(0,'USA')
    txt16.grid(row=1,column=2, sticky=tk.W)
    


    l_networktype = tk.Label(ttkframe, text='by networktype.')
    l_networktype.grid(row=2,column=0, sticky=tk.W)
    e_networktype = tk.Entry(ttkframe,textvariable=network_type)
    e_networktype.insert(0,'resident')
    e_networktype.grid(row=3,column=0, sticky=tk.W)

    lb18 = tk.Label(ttkframe, text='by status.')
    lb18.grid(row=2,column=1, sticky=tk.W)
    lb17 = tk.Label(ttkframe, text='by tags.')
    lb17.grid(row=2,column=2, sticky=tk.W)
    txt17 = tk.Entry(ttkframe,textvariable=proxyTags)
    txt17.insert(0,'youtube')
    txt17.grid(row=3,column=2, sticky=tk.W)

    proxyStatus = tk.StringVar()
    proxy_str = tk.StringVar()


    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set("Select From Status")
    proxyStatus.trace('w', proxyStatusCallBack)


    proxyStatusbox = ttk.Combobox(ttkframe, textvariable=proxyStatus)
    proxyStatusbox.config(values = ('valid', 'invalid','unchecked'))
    proxyStatusbox.grid(row = 3, column = 1, padx=14, pady=15)    


     

    btn5= tk.Button(ttkframe, text="Get proxy list", padx = 0, pady = 0,command = lambda: on_platform_selected())
    btn5.grid(row=4,column=1, sticky=tk.W)    
    
    btn5= tk.Button(ttkframe, text="Reset", padx = 0, pady = 0,command = lambda:(proxyStatus.set(""),country.set(""),state.set(""),city.set(""),proxyTags.set(""),proxyStatus.set("Select From Status"),network_type.set("")))
    btn5.grid(row=4,column=2, sticky=tk.W)    
    
    lbl16 = tk.Label(newWindow, text='selected proxies')
    lbl16.grid(row=5,column=0, sticky=tk.W)
    txt16 = tk.Entry(newWindow,textvariable=proxy_str
                    #  ,width=int(int(window_size.split('x')[-1])/4)
                     )
    txt16.insert(0,'')
    txt16.grid(row=5,column=1, 
            #    width=width,
               columnspan=4,
            #    rowspan=3,
               sticky='nswe')    


   # Create a frame for the canvas and scrollbar(s).
    frame2 = tk.Frame(ttkframe, bg='Red', bd=1, relief=tk.FLAT)
    frame2.grid(row=6, column=0, rowspan=5,columnspan=5,sticky=tk.NW)

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=1)
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame2, bg='Yellow')
    canvas.grid(row=0, column=0)

    # Create a vertical scrollbar linked to the canvas.
    vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
    vsbar.grid(row=0, column=1, sticky=tk.NS)
    canvas.configure(yscrollcommand=vsbar.set)

    # Create a horizontal scrollbar linked to the canvas.
    hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
    hsbar.grid(row=1, column=0, sticky=tk.EW)
    canvas.configure(xscrollcommand=hsbar.set)

    # Create a frame on the canvas to contain the grid of buttons.
    buttons_frame = tk.Frame(canvas)
    
    def deleteRow(rowid):
        print('delete',rowid)
    
    def addRow(rowid):
        print('add',rowid)

    def chooseRow(rowid):
        print('delete',rowid)
    
    def unchooseRow(rowid):
        print('add',rowid)
        
    def refreshcanvas(headers,datas):

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)
        ROWS_DISP = len(datas)+1 # Number of rows to display.
        COLS_DISP = len(headers)+1  # Number of columns to display.
        COLS=len(headers)+1
        
        ROWS=len(datas)+1



        # Add the buttons to the frame.
        add_buttons = [tk.Button() for j in range(ROWS+1)] 
        del_buttons = [tk.Button() for j in range(ROWS+1)] 
        
        # set table header


        for j,h in enumerate(headers):
            label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text=h)
            label.grid(row=0, column=j, sticky='news')                    
            if h=='operation':
                button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                button.grid(row=0, column=j, sticky='news')

                delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                delete_button.grid(row=0, column=j, sticky='news')

        for i,row in enumerate(datas):
            i=i+1
            for j in range(0,len(headers)):
                
                if headers[j]!='operation':
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=row[headers[j]])
                    label.grid(row=i ,column=j, sticky='news')         


              
            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row(rowid=datas[x]['id']))
            add_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row(rowid=datas[x]['id']))
            del_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')
                    
        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        print('=before==',COLS,COLS_DISP,ROWS,ROWS_DISP)

        for i in range(5,COLS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

            if dw>int( canvas.winfo_width()*0.2):
                COLS=i-1
        for i in range(5,ROWS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)                
            if dh>int( canvas.winfo_height()*0.2):
                ROWS=i-1

        print('=after==',COLS,COLS_DISP,ROWS,ROWS_DISP)
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

        if dw>int( root.winfo_width()/3):
            dw=int( root.winfo_width()/3)
        if dh>int( root.winfo_height()/3):
            dh=int( root.winfo_height()/3)
            print('use parent frame widht')
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        print('========',w,h,dw,dh,bbox)
    headers=['id', 'host', 'port', 'username', 'pass', 'protocol', 'status', 'city', 'country', 'state', 'tags', 'inserted_at','operation','operation']
        
    refreshcanvas(headers,[])




    def on_platform_selected():
        # Clear the current selection in the account dropdown

        db_rows=  ProxyModel.filter_proxies(city=None if city.get()=='' else city.get(),
                                            country=None if city.get()=='' else country.get(),
                                            tags=None if proxyTags.get()=='' else proxyTags.get(),
                                            status=None if 'Select From Status' in proxyStatus.get() else proxyStatus.get() ,
                                            state=None if state.get()=='' else state.get(),
                                            network_type=None if network_type.get()=='' else network_type.get()
                                            )
        hints=None
        if db_rows is None or len(db_rows)==0:
            showinfomsg(message='there is no matching proxy records')
        else:
            logger.info(f'we found {len(db_rows)} record matching :{db_rows}')
            proxy_data=[]
            for row in db_rows:

                proxy={
                    "id":CustomID(custom_id=row.id).to_hex(),
                    "host":row.proxy_host,
                    "port":row.proxy_port,
                    "username":row.proxy_username,
                    "pass":row.proxy_password,
                    "protocol":row.proxy_protocol,
                    "status":row.status,
                    "city":row.city,
                    "country":row.country,
                    "state":row.state,
                    "tags":row.tags,
                    "inserted_at":row.inserted_at
                }
                proxy_data.append(proxy)
                header=proxy.keys()
                print(header)

            refreshcanvas(headers,proxy_data)
        


    chooseAccountsWindow=ttkframe
    def remove_selected_row(rowid):

        existingaccounts=proxy_str.get()
        if existingaccounts=='' or existingaccounts is None:
            existingaccounts=[]
        else:
            existingaccounts=eval(existingaccounts)

        print('you want to remove these selected proxies',rowid)
        if rowid==0:

            showinfomsg(message='you have not selected  proxies at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:


            if rowid in existingaccounts:
                existingaccounts.remove(rowid)


                logger.info(f'this proxies {rowid} removed success')
                showinfomsg(message=f'this proxies {rowid} removed success',parent=chooseAccountsWindow)    
            else:
                logger.info(f'you cannot remove this proxies {rowid}, not added before')
                showinfomsg(message=f'this proxies {rowid} not added before',parent=chooseAccountsWindow)    
            logger.info(f'end to remove,reset proxies {existingaccounts}')

        proxy_str.set(str(existingaccounts))
        parentchooseProxies.set(str(existingaccounts))

    def add_selected_accounts(rowid):
        print(rowid,'0000add_selected_accounts000')
        

        existingaccounts=proxy_str.get()
        if existingaccounts=='' or existingaccounts is None:
            existingaccounts=[]
        else:
            existingaccounts=eval(existingaccounts)
        if rowid is None:
            logger.info('you have not selected new proxies at all')
            showinfomsg(message='you have not selected new proxies at all',parent=chooseAccountsWindow)    
        
        else:
            if rowid in existingaccounts:
                logger.info(f'this proxies {rowid} added before')                   
                showinfomsg(message=f'this proxies {rowid} added before',parent=chooseAccountsWindow)    

            else:
                if existingaccounts=='':
                    existingaccounts=[]
                existingaccounts.append(rowid)
                logger.info(f'this proxies {rowid} added successS')
                showinfomsg(message=f'this proxies {rowid} added success',parent=chooseAccountsWindow)    

        proxy_str.set(str(existingaccounts))
        parentchooseProxies.set(str(existingaccounts))






def chooseProxies_listbox(ttkframe,username,parentchooseProxies):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)
    
    
    newWindow.title('proxy selection')

    if username=='':
        username='this user account'

    # label = tk.Label(newWindow,
    #             text = f"Select the proxies for {username} below : ",
    #             font = ("Times New Roman", 10),
    #             padx = 10, pady = 10)
    # # label.pack()
    # label.grid(row=0,column=0, sticky=tk.W)
    
    ttkframe=newWindow
    
    global city_user,country_user,proxyTags_user,proxyStatus_user,proxy_str
    city = tk.StringVar()
    state = tk.StringVar()
    network_type = tk.StringVar()
    country = tk.StringVar()
    proxyTags = tk.StringVar()

    lbl15 = tk.Label(ttkframe, text='by city.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(ttkframe,textvariable=city)
    txt15.insert(0,'Los')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=0, sticky=tk.W)


    l_state= tk.Label(ttkframe, text='by state.')
    l_state.grid(row=0,column=1, sticky=tk.W)
    e_state = tk.Entry(ttkframe,textvariable=state)
    e_state.insert(0,'LA')
    e_state.grid(row=1,column=1, sticky=tk.W)


    lbl16 = tk.Label(ttkframe, text='by country.')
    lbl16.grid(row=0,column=2, sticky=tk.W)
    txt16 = tk.Entry(ttkframe,textvariable=country)
    txt16.insert(0,'USA')
    txt16.grid(row=1,column=2, sticky=tk.W)
    


    l_networktype = tk.Label(ttkframe, text='by networktype.')
    l_networktype.grid(row=2,column=0, sticky=tk.W)
    e_networktype = tk.Entry(ttkframe,textvariable=network_type)
    e_networktype.insert(0,'resident')
    e_networktype.grid(row=3,column=0, sticky=tk.W)

    lb18 = tk.Label(ttkframe, text='by status.')
    lb18.grid(row=2,column=1, sticky=tk.W)
    lb17 = tk.Label(ttkframe, text='by tags.')
    lb17.grid(row=2,column=2, sticky=tk.W)
    txt17 = tk.Entry(ttkframe,textvariable=proxyTags)
    txt17.insert(0,'youtube')
    txt17.grid(row=3,column=2, sticky=tk.W)

    proxyStatus = tk.StringVar()
    proxy_str = tk.StringVar()


    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set("Select From Status")
    proxyStatus.trace('w', proxyStatusCallBack)


    proxyStatusbox = ttk.Combobox(ttkframe, textvariable=proxyStatus)
    proxyStatusbox.config(values = ('valid', 'invalid','unchecked'))
    proxyStatusbox.grid(row = 3, column = 1, padx=14, pady=15)    


     
     

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(newWindow)
    frame_canvas.grid(row=7, column=0,columnspan=20,sticky='nw',  padx=14, pady=15)    
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
    btn5= tk.Button(ttkframe, text="Get proxy list", padx = 0, pady = 0,command = lambda: threading.Thread(
        target=queryProxies(logger,city.get(),state.get(),country.get(),proxyTags.get(),network_type.get(),
                            proxyStatus.get(),ttkframe,tree=None,langlist=langlist)).start())
    btn5.grid(row=4,column=1, sticky=tk.W)    
    
    btn5= tk.Button(ttkframe, text="Reset", padx = 0, pady = 0,command = lambda:(proxyStatus.set(""),country.set(""),state.set(""),city.set(""),proxyTags.set(""),proxyStatus.set("Select From Status"),network_type.set("")))
    btn5.grid(row=4,column=2, sticky=tk.W)    
    
    btn6= tk.Button(newWindow, text="remove selected", padx = 10, pady = 10,command = lambda: threading.Thread(target=remove_selected_row).start())     
    btn6.grid(row=8,column=6, sticky=tk.W)
    lbl16 = tk.Label(newWindow, text='selected proxies')
    lbl16.grid(row=8,column=0, sticky=tk.W)
    txt16 = tk.Entry(newWindow,textvariable=proxy_str
                    #  ,width=int(int(window_size.split('x')[-1])/4)
                     )
    txt16.insert(0,'')
    txt16.grid(row=8,column=1, 
            #    width=width,
               columnspan=4,
            #    rowspan=3,
               sticky='nswe')    



    tmp['accountaddproxies']={}
    
    def remove_selected_row():
        selected_accounts=tmp['accountaddproxies']
        show_str=proxy_str.get()

        print('you want to remove these selected proxy',selected_accounts)
        if len(selected_accounts)==0:
            showinfomsg(message='you have not selected  proxy at all.choose one or more') 
        
        else:
            existingaccounts=proxy_str.get().split(',')
            logger.info(f'you want to remove this selected proxy {selected_accounts} from existing: {existingaccounts}')

            for item in selected_accounts:

                if item in existingaccounts:
                    existingaccounts.remove(item)


                    logger.info(f'this proxy {item} removed success')
                    showinfomsg(message=f'this proxy {item} removed success')
                else:
                    logger.info(f'you cannot remove this proxy {item}, not added before')
                    showinfomsg(message=f'this proxy {item} not added before')
            logger.info(f'end to remove,reset proxystr {existingaccounts}')
            show_str= ','.join(item for item in existingaccounts if item is not None and item != "")

        proxy_str.set(show_str)
        parentchooseProxies.set(show_str)

    def add_selected_accounts(event):
        listbox = event.widget
        values = [listbox.get(idx).split(':')[1] for idx in listbox.curselection()]

        tmp['accountaddproxies']=values
        existingaccounts=proxy_str.get().split(',')
        show_str=proxy_str.get()
        if len(list(values))==0:
            logger.info('you have not selected  proxiess at all.choose one or more')
            showinfomsg(message='you have not selected  proxiess at all.choose one or more')
        
        elif values==existingaccounts:
            logger.info('you have not selected new proxiess at all')
            showinfomsg(message='you have not selected new proxiess at all')
        
        else:
            for item in values:
                if item in existingaccounts:
                    logger.info(f'this proxy {item} added before')                   
                    showinfomsg(message=f'this proxiess {item} added before') 

                else:
                    existingaccounts.append(item)
                    logger.info(f'this proxy {item} added successS')
                    showinfomsg(message=f'this proxy {item} added successS')

                    if show_str=='':
                        show_str=item
                    else:
                        show_str= show_str+','+item

        proxy_str.set(show_str)
        parentchooseProxies.set(show_str)
    langlist.bind('<<ListboxSelect>>',add_selected_accounts)   




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
def saveUser(platform,username,password,proxy,cookies,linkaccounts=None):

    if platform is None:
        logger.error('please choose a platform')
        showinfomsg(message='please choose a platform first')
    if username is None:
        logger.error('please provide  a username')
        showinfomsg(message='please provide  a username')

    else:    
        if password is None:
            logger.info('you dont provide password')        
            if cookies is None:
                logger.error('please provide a cookie file without  password')     
                showinfomsg(message='please provide a cookie file without  password')

        # Define a list of proxy IDs associated with the account
        proxy_ids = proxy
        # [1, 2, 3]  # Replace with the actual IDs of the proxies

        # Serialize the list of proxy IDs to JSON
        # proxy_ids_json = json.dumps(proxy_ids)
        user_data=           {
            'platform': platform,
            'username': username,
            'password': password,
            'cookies': cookies,
            'proxy': proxy_ids
        }
        # Create the user and associate the proxy IDs
        userid = AccountModel.add_account(user_data)

        if userid:

            if linkaccounts !=None:
                accounts=eval(linkaccounts)
                for key,value in enumerate(accounts):
                    if len(value.split(','))!=0:
                        for id in  value.split(','):
                            r=AccountRelationship.add_AccountRelationship_by_username(main_username=userid,otherusername=id)
                            if r:
                                print(f'bind {id} to {username} as side account')
            showinfomsg(message='this account added ok')
        else:

            showinfomsg(message='this account added failed')

    
def  queryAccounts(newWindow,tree,logger,username,platform):
    if username=='':
        username=None
    if platform=='':
        platform=None        
    else:
        platform=getattr(PLATFORM_TYPE, platform.upper())
        print(f'query accounts for {platform} {getattr(PLATFORM_TYPE, platform.upper())} ')

    account_rows=AccountModel.filter_accounts(username=username,platform=platform) 

    logger.info(f'we found {len(account_rows)} record matching ')

    if len(account_rows)==0:
        showinfomsg(message=f'we found {len(account_rows)} record matching ')
    else:                
        records = tree.get_children()                
        if records is not None:
            for element in records:
                tree.delete(element) 
        for row in account_rows:
            id=CustomID(custom_id=row.id).to_hex()

            tree.insert(
                "", 0, text=id, values=(row.username,row.password,row.platform,row.proxy, row.cookies, row.inserted_at)
            )                    
            

                
            
        logger.info(f'Account search and display finished')


def accountView(frame,ttkframe,lang):

    global proxy_option_account,channel_cookie_user

    channel_cookie_user= tk.StringVar()
    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()


    l_platform = tk.Label(ttkframe, text=settings[locale]['l_platform']
                          )
    # l_platform.place(x=10, y=90)
    l_platform.grid(row = 0, column = 0, columnspan = 3, padx=14, pady=15)    

    socialplatform = tk.StringVar()
    socialplatform_box = ttk.Combobox(ttkframe, textvariable=socialplatform)


    def socialplatformdb_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]

        socialplatform_box['values'] = platform_names

    def socialplatformdb_refresh(event):
        socialplatform_box['values'] = socialplatformdb_values()

    socialplatform_box['values'] = socialplatformdb_values()



    def socialplatformOptionCallBack(*args):
        print(socialplatform.get())
        print(socialplatform_box.current())

    socialplatform.set("Select From Platforms")
    socialplatform.trace('w', socialplatformOptionCallBack)
    socialplatform_box.bind('<FocusIn>', lambda event: socialplatformdb_refresh(event))


    # socialplatform_box.config(values =platform_names)
    socialplatform_box.grid(row = 0, column = 5, columnspan = 3, padx=14, pady=15)    



    l_username = tk.Label(ttkframe, text=settings[locale]['username']
                          )
    # l_username.place(x=10, y=150)
    l_username.grid(row = 2, column = 0, columnspan = 3, padx=14, pady=15)    

    e_username = tk.Entry(ttkframe, width=int(width*0.01), textvariable=username)
    # e_username.place(x=10, y=180)
    e_username.grid(row = 2, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    




    l_password = tk.Label(ttkframe, text=settings[locale]['password']
                          )
    e_password = tk.Entry(ttkframe, width=int(width*0.01), textvariable=password)

    l_password.grid(row = 3, column = 0, columnspan = 3, padx=14, pady=15)    
    e_password.grid(row = 3, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    

    linkAccounts=tk.StringVar()


    l_linkAccounts = tk.Label(ttkframe, text=settings[locale]['linkAccounts']
                          )
    e_linkAccounts = tk.Entry(ttkframe, width=int(width*0.01), textvariable=linkAccounts)

    l_linkAccounts.grid(row = 4, column = 0, columnspan = 3, padx=14, pady=15)    
    e_linkAccounts.grid(row = 4, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')   

    b_choose_account=tk.Button(ttkframe,text="Link",command=lambda: threading.Thread(target=lambda:chooseAccountsView(ttkframe,linkAccounts)).start() )
    Tooltip(b_choose_account, text='if you want to associate any account as the backup accounts' , wraplength=200)

    b_choose_account.grid(row = 4, column = 9, columnspan = 2, padx=14, pady=15)    
    l_proxy_option = tk.Label(ttkframe, text=settings[locale]['proxySetting']
                              )
    
    l_proxy_option.grid(row = 5, column = 0, columnspan = 3, padx=14, pady=15)    

    e_proxy_option = tk.Entry(ttkframe, textvariable=proxy_option_account)
    e_proxy_option.grid(row = 5, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    

    b_choose_proxy=tk.Button(ttkframe,text="Link",command=lambda: threading.Thread(target=chooseProxies(ttkframe,username.get(),proxy_option_account)).start() )
    
    b_choose_proxy.grid(row = 5, column = 9, columnspan = 2, padx=14, pady=15)    




    l_channel_cookie = tk.Label(ttkframe, text='cookies' 
                                # settings[locale]['select_cookie_file']
                                )
    # l_channel_cookie.place(x=10, y=330)
    l_channel_cookie.grid(row = 6, column = 0, columnspan = 3, padx=14, pady=15)    

    e_channel_cookie = tk.Entry(ttkframe, textvariable=channel_cookie_user)
    # e_channel_cookie.place(x=10, y=360)
    e_channel_cookie.grid(row = 6, column = 5, columnspan = 3, padx=14, pady=15,sticky='w')    

    b_channel_cookie=tk.Button(ttkframe,text="Select",command=lambda: threading.Thread(target=select_file('select cookie file for account',channel_cookie_user,cached=None)).start() )
    # b_channel_cookie.place(x=10, y=390)    
    b_channel_cookie.grid(row = 6, column = 9, columnspan = 2, padx=14, pady=15)    

    
    b_channel_cookie_gen=tk.Button(ttkframe,text="pull",command=auto_gen_cookie_file)
    # b_channel_cookie_gen.place(x=100, y=390)    
    b_channel_cookie_gen.grid(row = 6, column = 12, columnspan = 2, padx=14, pady=15)    
 
    
    b_save_user=tk.Button(ttkframe,text="save user",command=lambda: threading.Thread(target=saveUser(socialplatform.get(),username.get(),password.get(),proxy_option_account.get(),channel_cookie_user.get(),linkAccounts.get())).start() )
                         
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
    lbl15.grid(row = 0, column = 0, padx=14, pady=15,sticky='w')    
    txt15 = tk.Entry(frame, width=11,textvariable=q_platform_account)
    txt15.insert(0,'')
    txt15.grid(row = 1, column = 0, padx=14, pady=15,sticky='w')    


    lb18 = tk.Label(frame, text='By platform.')
    lb18.grid(row=0,column=1, sticky=tk.W)


    q_platform = tk.StringVar()
    q_platform_accountbox = ttk.Combobox(frame, textvariable=q_platform)

    def q_platformb_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]

        q_platform_accountbox['values'] = platform_names

    def q_platformdb_refresh(event):
        q_platform_accountbox['values'] = q_platformb_values()

    q_platform_accountbox['values'] = q_platformb_values()


    def q_platformOptionCallBack(*args):
        print(q_platform.get())
        print(q_platform_accountbox.current())

    q_platform.set("Select From Platforms")
    q_platform.trace('w', q_platformOptionCallBack)


    q_platform_accountbox['values'] = q_platformb_values()

    q_platform_accountbox.bind('<FocusIn>', lambda event: q_platformdb_refresh(event))    
    q_platform_accountbox.grid(row = 1, column = 1, padx=14, pady=15,sticky='w')    




    
    # txt15.place(x=580, y=15, anchor=tk.NE)
    btn5= tk.Button(frame, text="Get Info", command = lambda:queryAccounts(username=q_username_account.get(),platform=q_platform.get()) )
    # btn5.place(x=800, y=15, anchor=tk.NE)    

    btn5.grid(row = 1, column =3, padx=14, pady=15)    


    btn5= tk.Button(frame, text="Reset", padx = 0, pady = 0,command = lambda:(q_platform.set(''),q_platform_account.set('')))
    btn5.grid(row=1,column=5, sticky=tk.W)    

    # Create a frame for the canvas and scrollbar(s).
    chooseAccountsWindow=frame
    frame2 = tk.Frame(chooseAccountsWindow, bg='Red', bd=1, relief=tk.FLAT)
    frame2.grid(row=2, column=0, rowspan=5,columnspan=15,sticky=tk.NW)

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=1)
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame2, bg='Yellow')
    canvas.grid(row=0, column=0)

        
    def refreshcanvas(headers,datas):

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)
        ROWS_DISP = len(datas)+1 # Number of rows to display.
        COLS_DISP = len(headers)+1  # Number of columns to display.
        COLS=len(headers)+1
        
        ROWS=len(datas)+1



        # Add the buttons to the frame.
        add_buttons = [tk.Button() for j in range(ROWS+1)] 
        del_buttons = [tk.Button() for j in range(ROWS+1)] 
        
        # set table header


        for j,h in enumerate(headers):
            label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text=h)
            label.grid(row=0, column=j, sticky='news')                    
            if h=='operation':
                button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                button.grid(row=0, column=j, sticky='news')

                delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                delete_button.grid(row=0, column=j, sticky='news')

        for i,row in enumerate(datas):
            i=i+1
            for j in range(0,len(headers)):
                
                if headers[j]!='operation':
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=row[headers[j]])
                    label.grid(row=i ,column=j, sticky='news')         


              
            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row(rowid=datas[x]['id']))
            add_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row(rowid=datas[x]['id']))
            del_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')
                    
        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        print('=before==',COLS,COLS_DISP,ROWS,ROWS_DISP)

        for i in range(5,COLS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

            if dw>int( canvas.winfo_width()*0.2):
                COLS=i-1
        for i in range(5,ROWS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)                
            if dh>int( canvas.winfo_height()*0.2):
                ROWS=i-1

        print('=after==',COLS,COLS_DISP,ROWS,ROWS_DISP)
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

        if dw>int( root.winfo_width()/3):
            dw=int( root.winfo_width()/3)
        if dh>int( root.winfo_height()/3):
            dh=int( root.winfo_height()/3)
            print('use parent frame widht')
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        print('========',w,h,dw,dh,bbox)
    tab_headers=['id','platform','username','pass','is_deleted','proxy','inserted_at','operation','operation']
    refreshcanvas(tab_headers,[])




    def queryAccounts(username,platform):
        print('account view -query accounts',username,platform)
        if username=='':
            username=None
        if platform=='' or 'SELECT FROM PLATFORMS' in platform.upper():
            platform=None        
        else:
            try:
                platform=int(platform)
            except:
                print(f'query accounts for {platform} {getattr(PLATFORM_TYPE, platform.upper())} ')

                platform=getattr(PLATFORM_TYPE, platform.upper())
        selected_platform=platform

        account_rows=AccountModel.filter_accounts(platform=selected_platform,username=username)
        # Extract account names and set them as options in the account dropdown
        if account_rows is None or len(account_rows)==0:
            # langlist.delete(0,tk.END)
            showinfomsg(message=f"try to add accounts for {selected_platform} first",parent=chooseAccountsWindow)    

        else:                
            account_names = [row.username for row in account_rows]
            logger.info(f'we found {len(account_names)} record matching ')

            # langlist.delete(0,tk.END)
            i=0
            account_data=[]
            for row in account_rows:
                account={
                    "id":CustomID(custom_id=row.id).to_hex(),
                    "platform":                    PLATFORM_TYPE.PLATFORM_TYPE_TEXT[row.platform][1]
,
                    "username":row.username,

                    "pass":row.password,
                    "is_deleted":row.is_deleted,
                    "proxy":row.proxy,
                    "inserted_at":datetime.fromtimestamp(row.inserted_at).strftime("%Y-%m-%d %H:%M:%S")  
                }
                account_data.append(account)
            refreshcanvas(tab_headers,account_data)
        
        
                
            logger.info(f'Account search and display finished')
                    


    # Bind the platform selection event to the on_platform_selected function



    
    def remove_selected_row(rowid):



        print('you want to remove these selected account',rowid)
        if rowid==0:

            showinfomsg(message='you have not selected  account at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:


            if rowid :
                rowid=CustomID(custom_id=rowid).to_bin()
                result=AccountModel.update_account(id=rowid,is_deleted=True)

                if result:
                    logger.info(f'this account {rowid} removed success')
                    showinfomsg(message=f'this account {rowid} removed success',parent=chooseAccountsWindow)    
                else:
                    logger.info(f'you cannot remove this account {rowid}, not added before')
                    showinfomsg(message=f'this account {rowid} not added before',parent=chooseAccountsWindow)    
            logger.info(f'end to remove,reset account {rowid}')


    def update_selected_row(rowid):
        # showinfomsg(message='not supported yet',parent=chooseAccountsWindow)    
        chooseAccountsWindow = tk.Toplevel(frame)
        chooseAccountsWindow.geometry(window_size)
        chooseAccountsWindow.title('Edit and update account info ')
        rowid=CustomID(custom_id=rowid).to_bin()

        result=AccountModel.get_account_by_id(id=rowid)
        from playhouse.shortcuts import model_to_dict
        result = model_to_dict(result)
        print('----------',result)

        i=1
        newresult=result
        rowkeys={}
        for key,value in result.items():
            # print('current key',key,value)
            if key=='id':
                value=CustomID(custom_id=value).to_hex()
            if key=='platform':
                value=  PLATFORM_TYPE.PLATFORM_TYPE_TEXT[value][1]
            if value==None:
                value=''                        
            if key=='inserted_at':
                value=datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")                
            if not  key  in ['id','inserted_at','unique_hash','platform']:
            
                label= tk.Label(chooseAccountsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text=key)
                label.grid(row=i ,column=0, sticky='news')         
                entry = tk.Entry(chooseAccountsWindow)
        
                entry.insert(0, value)
                entry.grid(row=i ,column=1, sticky='news')   
                rowkeys[i]=key
                def callback(event):

                    x = event.widget.grid_info()['row']
                    print(f'current input changes for {rowkeys[x]}',event.widget.get())   

                    newresult[rowkeys[x]]=event.widget.get()
                    if rowkeys[x]=='is_deleted':
                        print('is deleted',type(event.widget.get()))
                        value='0'
                        if event.widget.get()=='0':
                            value=False
                        elif event.widget.get()=='1':
                            value=True                        
                        newresult[rowkeys[x]]=value

                    print('============update row',newresult)

                # variable.trace('w', lambda:setEnty())    
                entry.bind("<KeyRelease>", callback)

            else:

                label = tk.Label(chooseAccountsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text=key)
                label.grid(row=i ,column=0, sticky='news')         
                variable=tk.StringVar()
                variable.set(value)
                entry = tk.Entry(chooseAccountsWindow,textvariable=variable)
                entry.grid(row=i ,column=1, sticky='news') 
                entry.config(state='disabled')
            i=i+1

        btn5= tk.Button(chooseAccountsWindow, text="save", padx = 0, pady = 0,command = lambda:AccountModel.update_account(id=rowid,account_data=newresult))
        btn5.grid(row=i+1,column=2, sticky=tk.W)    


    
    
def  queryTasks(tree,logger,status,platform,username,video_title):


    if status==''or 'input' in status:
        status=None
    if platform=='' or 'input' in platform:
        platform=None        
    else:
        platform=getattr(PLATFORM_TYPE, platform.upper())
        print(f'query tasks for {platform} {getattr(PLATFORM_TYPE, platform.upper())} ')

    task_rows=TaskModel.filter_tasks(status=status,type=platform) 

    logger.info(f'we found {len(task_rows)} record matching ')

    if len(task_rows)==0:
        showinfomsg(message=f'we found {len(task_rows)} record matching ')
    else:                
        records = tree.get_children()                
        if records is not None:
            for element in records:
                tree.delete(element) 
        for row in task_rows:
            id=CustomID(custom_id=row.id).to_hex()
            video=row.video
            setting=row.setting
            account=setting.account
            print('======',video,account,setting)
            platform=PLATFORM_TYPE.PLATFORM_TYPE_TEXT[row.type][1]
            status=TASK_STATUS.PLATFORM_TYPE_TEXT[row.status][1]
            tree.insert(
                "", 0, text=id, values=(status,platform)
            )                    
            

                
            
        logger.info(f'Account search and display finished')  


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
    b_thumbnail_template_file=tk.Button(creatTaskWindow,text="select",command=lambda: threading.Thread(target=select_file('select video meta  file',videometafile,'','all',creatTaskWindow)).start() )
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

    multiAccountsPolicy=tk.StringVar()


    def multiAccountsPolicyCallBack(*args):
        print(multiAccountsPolicy.get())
        print(multiAccountsPolicybox.current())



    multiAccountsPolicy.set("Select From policy")
    multiAccountsPolicy.trace('w', multiAccountsPolicyCallBack)


    multiAccountsPolicybox = ttk.Combobox(creatTaskWindow, textvariable=multiAccountsPolicy)
    multiAccountsPolicybox.config(values = ('单平台单账号', '单平台主副账号','单平台多账号随机发布','单平台多账号平均发布'))
    multiAccountsPolicybox.grid(row = 4, column = 3, padx=14, pady=15, sticky='w')   

    lb18 = tk.Label(creatTaskWindow, text='Runs on.')
    lb18.grid(row=5,column=0,  padx=14, pady=15, sticky=tk.W)


    deviceType = tk.StringVar()
    browserType = tk.StringVar()

    def deviceTypeCallBack(*args):
        print(deviceType.get())
        print(deviceTypebox.current())
        if 'browser' in deviceType.get():

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
    btn6= tk.Button(creatTaskWindow, text="gen task meta file", padx = 10, pady = 10,command = lambda: threading.Thread(
        target=genUploadTaskMetas(
            videometafile.get(),
            choosedAccounts.get(),
            multiAccountsPolicy.get(),
            deviceType.get(),browserType.get(),
            is_open_browser.get(),wait_policy.get(),is_debug.get(),is_record_video.get(),creatTaskWindow)).start())     
    btn6.grid(row=10,column=1, sticky=tk.W)
    def uploadStrategyCallBack(*args):
        print(uploadStrategy.get())
        # print(uploadStrategybox.current())
        # if uploadStrategybox.current()==0 or uploadStrategy.get()=='单帐号' :
        #     pass







    uploadStrategy.trace('w', uploadStrategyCallBack)


def has_more_than_one_one(lst):
    # Check if there is more than one element equal to 1 and all others are 0
    return lst.count(1) > 1 and all(x == 0 for x in lst)

    # # Example usage:
    # my_list = [0, 1, 0, 1, 0]  # Replace this with your list
    # result = has_more_than_one_one(my_list)
def has_one_large_value(lst):
    # Check if there is exactly one element greater than 1 and all others are 0
    return lst.count(0) == len(lst) - 1 and any(x > 1 for x in lst)

    # # Example usage:
    # my_list = [0, 2, 0, 0, 0]  # Replace this with your list
    # result = has_one_large_value(my_list)
def has_more_than_one_large_value(lst):
    # Check if there is more than one element greater than 1 and all others are 0
    return lst.count(0) == len(lst) - lst.count(0) - 1

    # # Example usage:
    # my_list = [0, 2, 0, 3, 0]  # Replace this with your list
    # result = has_more_than_one_large_value(my_list)

def has_one_and_zeros(lst):
    # Check if there is exactly one 1 and all others are 0
    return lst.count(1) == 1 and all(x == 0 for x in lst)

    # # Example usage:
    # my_list = [0, 0, 1, 0, 0]  # Replace this with your list
    # result = has_one_and_zeros(my_list)
def more_than_one_large_element(lst):
    # Check if there are more than one elements greater than 1
    return lst.count(x > 1 for x in lst) > 1

    # # Example usage:
    # my_list = [2, 3, 0, 0, 1]  # Replace this with your list
    # result = more_than_one_large_element(my_list)
def extends_accounts(accounts,videocount,mode='equal'):
    # Your lists
    # videos = [1, 2, 3, 4, 5]  # Replace with your list1
    # accounts = ['A', 'B', 'C']  # Replace with your list2

    n = videocount
    m = len(accounts)

    
    ratio = n / m

    extended_list2 = []

    for _ in range(n):
        if ratio.is_integer():
            # If n/m is an integer, repeat elements from list2
            extended_list2.append(accounts[_ % m])
        else:
            # If n/m is not an integer, choose a random element from list2
            extended_list2.append(random.choice(accounts))    
    if mode=='equal':
        return extended_list2
    elif mode=='random':
        return [random.choice(accounts)  for x in range(0,m)]    
    else:
        print(f'mode:{mode} not supported yet') 
def load_meta_file(filepath):
    videometafilepath=filepath
    if videometafilepath !='' and videometafilepath is not None:
        filename = os.path.splitext(videometafilepath)[0]
        folder=os.path.dirname(videometafilepath)
        ext = os.path.splitext(videometafilepath)[1].replace('.','')
        logger.info(f'you select video metafile is {videometafilepath}')
        if  os.path.exists(videometafilepath):
            # check_video_thumb_pair(dbm,video_folder_path,True)
            logger.info('start to load  and parse meta file')

            tmpdict={}
            if ext=='xlsx':
                df=pd.read_excel(videometafilepath, index_col=[0])
                df.replace('nan', '')
                tmpdict=json.loads(df.to_json(orient = 'index'))   

                dfdict=df.iterrows()
            elif ext=='json':
                df=pd.read_json(videometafilepath)  
                df.replace('nan', '')
                tmpdict=json.loads(df.to_json())   

                dfdict=df.items()      
            elif ext=='csv':
                df=pd.read_csv(videometafilepath, index_col=[0])
                df.replace('nan', '')
                tmpdict=json.loads(df.to_json(orient = 'index'))   

                dfdict=df.iterrows()
            return tmpdict
        else:
            logger.error(f'{filepath}is not not exist or broken' )  
           
            return None
    else:
        logger.error(f'{filepath}is not provide' )  
        return None
def genUploadTaskMetas(videometafilepath,choosedAccounts_value,multiAccountsPolicy_value,deviceType_value,browserType_value,is_open_browser_value,wait_policy_value,is_debug_value,is_record_video_value,frame):     
    
    if multiAccountsPolicy_value=='单平台单账号':
        # ('单平台单账号', '单平台主副账号','单平台多账号随机发布','单平台多账号平均发布')
        multiAccountsPolicy_value=0
    elif multiAccountsPolicy_value=='单平台主副账号':
        multiAccountsPolicy_value=1
    elif multiAccountsPolicy_value=='单平台多账号随机发布':
        multiAccountsPolicy_value=2
    elif multiAccountsPolicy_value=='单平台多账号平均发布':
        multiAccountsPolicy_value=3    
    print('assign account',choosedAccounts_value)
    if choosedAccounts_value=='' or choosedAccounts_value is None:
        logger.info('please choose which platform and account you want to upload ')
        showinfomsg(message="please choose which platform and account you want to upload ",parent=frame)    
        return                 
    else:
        try:
            choosedAccounts_value=eval(choosedAccounts_value)
            print('convert str to dict',choosedAccounts_value)

        except:
            logger.info(f'please check {choosedAccounts_value} format')
            showinfomsg(message=f'please check {choosedAccounts_value} format',parent=frame)    
            return 

    print('load video meta')
    logger.info('start to load video meta')

    if videometafilepath !='' and videometafilepath is not None:
        filename = os.path.splitext(videometafilepath)[0]
        folder=os.path.dirname(videometafilepath)    
        ext = os.path.splitext(videometafilepath)[1].replace('.','')
        
        if load_meta_file(videometafilepath):
            logger.info('video meta file is ok')

            tmpdict=load_meta_file(videometafilepath)

            tmp['tasks']={}

            # Check the data dictionary for allowed fields and empty values in each entry
            videocounts=len(tmpdict)
            # multiAccountsPolicy_value  根据它来分配视频，
            for platform,accounts in choosedAccounts_value.items():
                if accounts=='':
                    accounts=[]
                else:
                    accounts=accounts.split(',')
                # 直接检测某平台下的账号数量，=1，默认情况 >1,看看策略
                tmpaccounts=[]  
                # ('单平台单账号', '单平台主副账号','单平台多账号随机发布','单平台多账号平均发布')
                # 如果存在主副账号，这个逻辑没想好，主副的区别是啥 副号的作用是啥 意味着两个账号发一模一样的视频，当然可以只是缩略图不同，随机进行测试
                #那也就是说，针对平台下每一个账号进行检测，发现副号则自动新建一个视频任务
                
                # 多账号的意味着视频分摊到每个账号进行发布，发布的视频各不一样
                #多账号下的账号意味着不管它存不存在副号，提交的账号独立对待。           
                
                # accounts={'y1','y2','y3'} 
                # 相当于5个账号
                # {'y1','y11'} {'y2'} {'y3','y31'}
            
                print(f"start to process platform {platform}, accounts are:{accounts},{multiAccountsPolicy_value}")
                
                if len(accounts)==0:
                    logger.info(f'you dont choose any account for this platform:{platform}')
                else:
                    if  multiAccountsPolicy_value==0:
                        if len(accounts)==0:
                            logger.info(f'you dont choose any account for this platform:{platform}')
                        tmpaccounts=  extends_accounts(accounts,videocounts)     
                        print('==单账号=',tmpaccounts)
                        for key, entry in tmpdict.items():
                            print('key',key)
                            print('entry',entry)
                            key=key+'_'+platform
                            tmp['tasks'][key]=entry
                            tmp['tasks'][key]['timeout']=200
                            tmp['tasks'][key]['is_open_browser']=is_open_browser_value
                            tmp['tasks'][key]['is_debug']=is_debug_value
                            tmp['tasks'][key]['platform']=platform
                            tmp['tasks'][key]['wait_policy']=wait_policy_value
                            tmp['tasks'][key]['is_record_video']=is_record_video_value
                            tmp['tasks'][key]['browser_type']=browserType_value

                            


                            data=(AccountModel.filter_accounts(username=accounts[0]))[0]
                            # print('data====',data[0],data[0].username)
                            tmp['tasks'][key]['username']=data.username
                            logger.info(f'get credentials for this account {accounts[0]}')

                            tmp['tasks'][key]['password']=data.password
                            tmp['tasks'][key]['proxy_option']=data.proxy
                            tmp['tasks'][key]['channel_cookie_path']=data.cookies
                        
                        
                                
                    elif multiAccountsPolicy_value==1:
                        print('遍历账号检查是否有副号，计算任务数量，分配视频')
                        # video={'1.mp4'}
                        # accounts={'y1'} {'y1','y11'}
                        taskno=0
                        for username in accounts:
                            r=AccountRelationship.get_AccountRelationship_by_username(username=username)
                            if r is not None:
                                r.backup_account.id
                                # tmpaccounts.append([r.backup_account.id  for x in range(0,videocounts)]   )
                                # print('===',tmpaccounts)
                                for key, entry in tmpdict.items():
                                    print('key',key)
                                    print('entry',entry)
                                    print('taskno',taskno)

                                    key=key+'_'+platform+'-'+str(taskno)
                                    tmp['tasks'][key]=entry
                                    tmp['tasks'][key]['timeout']=200
                                    tmp['tasks'][key]['is_open_browser']=is_open_browser_value
                                    tmp['tasks'][key]['is_debug']=is_debug_value
                                    tmp['tasks'][key]['platform']=platform
                                    tmp['tasks'][key]['wait_policy']=wait_policy_value
                                    tmp['tasks'][key]['is_record_video']=is_record_video_value
                                    tmp['tasks'][key]['browser_type']=browserType_value

                                    

                                    # account=r.backup_account.id
                                    # data=(AccountModel.filter_accounts(username=r.backup_account.username))[0]
                                    # print('data====',data[0],data[0].username)
                                    tmp['tasks'][key]['account_id']=CustomID(custom_id=r.backup_account.id).to_hex()


                                    tmp['tasks'][key]['username']=r.backup_account.username
                                    logger.info(f'get credentials for this account {r.backup_account.username}')

                                    tmp['tasks'][key]['password']=r.backup_account.password
                                    tmp['tasks'][key]['proxy_option']=r.backup_account.proxy
                                    tmp['tasks'][key]['channel_cookie_path']=r.backup_account.cookies
                                    taskno=+1                                
                            
                            for key, entry in tmpdict.items():
                                print('key',key)
                                print('entry',entry)
                                print('taskno',taskno)
                                
                                key=key+'_'+platform+'-'+str(taskno)
                                tmp['tasks'][key]=entry
                                tmp['tasks'][key]['timeout']=200
                                tmp['tasks'][key]['is_open_browser']=is_open_browser_value
                                tmp['tasks'][key]['is_debug']=is_debug_value
                                tmp['tasks'][key]['platform']=platform
                                tmp['tasks'][key]['wait_policy']=wait_policy_value
                                tmp['tasks'][key]['is_record_video']=is_record_video_value
                                tmp['tasks'][key]['browser_type']=browserType_value

                                

                                data=(AccountModel.filter_accounts(username=username))[0]
                                # print('data====',data[0],data[0].username)
                                tmp['tasks'][key]['username']=data.username
                                logger.info(f'get credentials for this account {data.username}')

                                tmp['tasks'][key]['password']=data.password
                                tmp['tasks'][key]['proxy_option']=data.proxy
                                tmp['tasks'][key]['channel_cookie_path']=data.cookies
                                taskno=+1    
                            
                    elif multiAccountsPolicy_value==2:
                        print('遍历账号，生成视频数量对应大小的账号数组，随机分配')
                        if videocounts <len(accounts):
                            tmpaccounts=[random.choice(accounts)]
                        else:
                            tmpaccounts=  extends_accounts(accounts,videocounts,mode='random')  
                        taskno=0
                        for key, entry in tmpdict.items():
                            print('key',key)
                            print('entry',entry)
                            key=key+'_'+platform+'-'+str(taskno)
                            tmp['tasks'][key]=entry
                            tmp['tasks'][key]['timeout']=200
                            tmp['tasks'][key]['is_open_browser']=is_open_browser_value
                            tmp['tasks'][key]['is_debug']=is_debug_value
                            tmp['tasks'][key]['platform']=platform
                            tmp['tasks'][key]['wait_policy']=wait_policy_value
                            tmp['tasks'][key]['is_record_video']=is_record_video_value
                            tmp['tasks'][key]['browser_type']=browserType_value

                            

                            account=tmpaccounts[taskno]
                            data=(AccountModel.filter_accounts(username=account.username))[0]
                            # print('data====',data[0],data[0].username)
                            tmp['tasks'][key]['username']=data.username
                            logger.info(f'get credentials for this account {account}')

                            tmp['tasks'][key]['password']=data.password
                            tmp['tasks'][key]['proxy_option']=data.proxy
                            tmp['tasks'][key]['channel_cookie_path']=data.cookies
                            taskno=+1    
                                                
                    elif multiAccountsPolicy_value==3:
                        print('遍历账号，生成视频数量对应大小的账号数组，平均分配')
                        if videocounts <len(accounts):
                            tmpaccounts=[random.choice(accounts)]
                        else:
                            tmpaccounts=  extends_accounts(accounts,videocounts,mode='equal')      
                        taskno=0
                        for key, entry in tmpdict.items():
                            print('key',key)
                            print('entry',entry)
                            key=key+'_'+platform+'-'+str(taskno)
                            tmp['tasks'][key]=entry
                            tmp['tasks'][key]['timeout']=200
                            tmp['tasks'][key]['is_open_browser']=is_open_browser_value
                            tmp['tasks'][key]['is_debug']=is_debug_value
                            tmp['tasks'][key]['platform']=platform
                            tmp['tasks'][key]['wait_policy']=wait_policy_value
                            tmp['tasks'][key]['is_record_video']=is_record_video_value
                            tmp['tasks'][key]['browser_type']=browserType_value

                            

                            account=tmpaccounts[taskno]
                            data=(AccountModel.filter_accounts(username=account.username))[0]
                            # print('data====',data[0],data[0].username)
                            tmp['tasks'][key]['username']=data.username
                            logger.info(f'get credentials for this account {account}')

                            tmp['tasks'][key]['password']=data.password
                            tmp['tasks'][key]['proxy_option']=data.proxy
                            tmp['tasks'][key]['channel_cookie_path']=data.cookies
                            taskno=+1                                                  
                    else:
                        print('coming soon ')

                

            
            logger.info(f'start to save task meta success')
            print(f"task json:{tmp['tasks']}")

            dumpTaskMetafiles(ext,folder)

            showinfomsg(message=f'save task meta success',parent=frame)    
        else:
            showinfomsg(message=f'load video meta failed',parent=frame)    
def validateTaskMetafile(engine,ttkframe,metafile):
    logger.info('load task metas to database ')
    print('load task meta')


    if metafile !='' and metafile is not None:
        
        logger.info(f'you select task metafile is {metafile}')
        filename = os.path.splitext(metafile)[0]
        folder=os.path.dirname(metafile)    
        ext = os.path.splitext(metafile)[1].replace('.','')
        logger.info('start to load  and parse meta file')

        if load_meta_file(metafile):
            data=load_meta_file(metafile)    
            print('raw tasks',type(data),data) 
            # data=eval(data)
               
            try:
                videos=data
                logger.info(f'we found {len(videos)} videos to be load in db')
                
                for idx,video in videos.items():
                    logger.info(f'video json is ,{type(video)},{video}')
                    logger.info(f'start to process uploadsetting related filed\n:{video} ')
                    settingid=None

                    for key in ['proxy_option','channel_cookie_path']:
                        if video.get(key)==None:
                            logger.error(f" this field {key} is required in given video json data")
                            # raise ValueError(f"this field {key} is required  in given data")
                            
                    for key in ['timeout','timeout','is_debug','wait_policy','is_record_video','username','password']:
                        if video.get(key)==None:
                            logger.info(f"no {key} filed provide in given video json data,we can use default value")
                    logger.info(f"start to validate browser_type:{video.get('browser_type')}")

                    if video.get('browser_type')==None:
                        video['browser_type']='firefox'        
                        video['browser_type']=1
                        logger.info('we use browser_type =firefox')
                    elif type(video.get('browser_type'))==str:
                        video['browser_type']=getattr(BROWSER_TYPE,video.get('browser_type').upper())
                        print('*****',video['browser_type'])
                        if video['browser_type']==None:
                            logger.error('browser_type should be one of "chromium", "firefox", "webkit"')
                    elif type(video.get('browser_type'))==int:
                        if video.get('browser_type') in range(0,len(BROWSER_TYPE.BROWSER_TYPE_TEXT)):
                            pass
                        else:
                            logger.error(f"browser_type should be one of {range(0,len(BROWSER_TYPE.BROWSER_TYPE_TEXT))}")
                    else:
                        logger.error('browser_type should be one of"chromium", "firefox", "webkit"')

                    
                    logger.info(f"start to validate platform:{video.get('platform')}")
                    supported_platform=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
                    supported_platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in supported_platform]
                    supported_platform_types=[x.type for x in supported_platform]
                    if len(supported_platform)==0:
                        logger.error('please initialize supported_platform first')
                    if video.get('platform')==None:
                        video['platform']='youtube'     
                        video['platform']=0   
                        logger.info('you dont specify platform field,we use default youtube')
                    elif   type(video.get('platform'))==str:     
                        platform_rows=PlatformModel.filter_platforms(name=video.get('platform'), ptype=None, server=None)
                        if len(platform_rows)>0:
                            video['platform']=platform_rows[0].type
                        else:
                            logger.error(f'platform should be one of {supported_platform_names} or {supported_platform_types} ')

                    elif   type(video.get('platform'))==int:     
                        platform_rows=PlatformModel.filter_platforms(name=None, ptype=video.get('platform'), server=None)
                        video['platform']=platform_rows[0].type
                        if len(platform_rows)>0:
                            video['platform']=platform_rows[0].type
                        else:
                            logger.error('platform should be one of {platform_names} or {platform_types} ')

                    else:
                            logger.error('platform should be one of {platform_names} or {platform_types} ')
                    logger.info('start to validate timeout')

                    if video.get('timeout')==None:
                        video['timeout']=200000
                        logger.info("you dont specify timeout field,we use default 200*1000")
                    else:
                        if type(video.get('timeout'))!=int:
                            logger.error('timeout should be integer,such as 20*1000=20000, 20 seconds')
                    logger.info('start to validate is_open_browser')

                    if video.get('is_open_browser')==None:
                        video['is_open_browser']=True
                        logger.info("you dont specify is_open_browser field,we use default True")
                        
                    else:
                        
                        if type(video.get('is_open_browser'))==bool:
                            pass
                        elif type(video.get('is_open_browser'))==str and video.get('is_open_browser').lower() not in ['true','false']:

                            logger.error(f'is_open_browser is {video.get("is_open_browser")} of {type(video.get("is_open_browser"))},it should be bool, true or false')
                    logger.info(f"start to validate debug:{video.get('is_debug')}")

                    if video.get('is_debug')==None:
                        video['is_debug']=True
                        logger.info("you dont specify debug field,we use default True")
                        
                    else:
                        
                        if type(video.get('is_debug'))==bool:
                            video['is_debug']=video.get('is_debug')
                        elif type(video.get('is_debug'))==str and video.get('is_debug').lower() not in ['true','false']:

                            logger.error(f"debug is {video.get('is_debug')} of {type(video.get('is_debug'))},it should be bool, true or false")
                            video['is_debug']=video.get('is_debug')
            


                    if video.get('is_record_video')==None:
                        video['is_record_video']=True        
                        logger.info("you dont specify is_record_video field,we use default True")
                        
                    else:
                        
                        if type(video.get('is_record_video'))==bool:
                            pass
                        elif type(video.get('is_record_video'))==str and video.get('is_record_video').lower() not in ['true','false']:

                            logger.error(f'is_record_video is {video.get("is_record_video")} of {type(video.get("is_record_video"))},it should be bool, true or false')
                    if video.get('wait_policy')==None:
                        video['wait_policy']=2        
                        logger.info("you dont specify wait_policy field,we use default 2")
                    else:
                        if type(video.get('wait_policy'))!=int:
                            logger.error('wait_policy should be one of 0,1,2,3,4')
                            video['wait_policy']=WAIT_POLICY_TYPE.WAIT_POLICY_TYPE_TEXT[video.get('wait_policy')][1] 

                        else:
                            if not video.get('wait_policy') in [0,1,2,3,4]:
                                logger.error('wait_policy should be one of 0,1,2,3,4')
                    task_account=None
                    if video.get('account_id') is None:
                        user_data=           {
                            'platform': video['platform'],
                            'username': video.get('username'),
                            'password': video.get('password'),
                            'cookies': video.get('cookies'),
                            'proxy': video.get('proxy'),
                            'wait_policy':video.get('wait_policy')
                        }                       
                        
                        task_account=AccountModel.add_account(account_data=user_data)
                    else:
                        
                        account_id=CustomID(custom_id=video.get('account_id')).to_bin()

                        task_account=AccountModel.get_account_by_id(account_id)
                        if task_account==None:
                            task_account=AccountModel.filter_accounts(
                                                                    username= video.get('username'),
                                                                    platform=video.get('platform')
                                                                    )
                            task_account=task_account[0]
                            if task_account==None:
                                user_data= {
                                        'platform': video['platform'],
                                        'username': video.get('username'),
                                        'password': video.get('password'),
                                        'cookies': video.get('cookies'),
                                        'proxy': video.get('proxy'),
                                        'wait_policy':video.get('wait_policy')
                                    }                       
                        
                                task_account=AccountModel.add_account(account_data=user_data)
                                video['account_id']=task_account.id

                    settingdata={
                            "timeout":video.get('timeout'),
                            "is_open_browser":video.get('is_open_browser'),
                            "is_debug":video.get('is_debug'),
                            "platform":video['platform'],
                            "browser_type":video.get('browser_type'),
                            "is_record_video":video.get('is_record_video'),
                            'wait_policy':video.get('wait_policy'),

                        }                
                    logger.info(f'start to process uploadsetting data {settingdata}')
                    tasksetting=None
                    if video.get('uploadsettingid')==None:
                        logger.info(f" this field uploadsettingid is optional in given video json data")

                        print('add to upload setting and return id for reuse')

                        tasksetting=UploadSettingModel.add_uploadsetting(settingdata,task_account)


                    else:
                        logger.info(f" if uploadsettingid is given,we can auto fill if  the other field is null ")
                        setting_id=CustomID(custom_id=video.get('uploadsettingid')).to_bin()

                        tasksetting=UploadSettingModel.get_uploadsetting_by_id(id=setting_id)
                        print('query id to pull setting, if not exist,create a new one')
                        if tasksetting==None:
                            tasksetting=UploadSettingModel.add_uploadsetting(settingdata,task_account)
                            
                    logger.info(f'end to process uploadsetting data')
                            
                            
                    logger.info(f'start to process video related fields\n:{video} ')


                    for key in ['video_local_path','video_title','video_description','thumbnail_local_path','publish_policy','tags']:
                        if video.get(key)==None:
                            logger.error(f"these {key} field is required,No target{key} in given video json data")
                            raise ValueError(f"these {key} field is required,No target{key} in given video json data")
                        if key in['video_local_path']:
                            if os.path.exists(video.get(key))==False:
                                logger.error(f"these {key} field is required,and check whether local file exists")
                                raise ValueError(f"these {key} field is required,and check whether local file exists")
                        if key in['thumbnail_local_path']:
                            if type(video.get(key)) ==list and len(video.get(key))>0:
                                
                                if os.path.exists(video.get(key)[0])==False:
                                    logger.error(f"these {key} field is required,and check whether local file exists")
                                    raise ValueError(f"these {key} field is required,and check whether local file exists")

                            elif type(video.get(key)) ==str and len(video.get(key))>0:
                                
                                if os.path.exists(eval(video.get(key))[0])==False:
                                    logger.error(f"these {key} field is required,and check whether local file exists")
                                    raise ValueError(f"these {key} field is required,and check whether local file exists")
                            else:
                                logger.error(f"these {key} field is required,and check whether filed value is ok :{video.get(key)}")

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
                            if video.get(key) not in ['true','false',True,False]:
                                logger.error(f'{key} should be bool, true or false') 


                    for key in ['is_age_restriction','is_paid_promotion']:
                        if video.get(key)==None:
                            video[key]=False 

                            logger.info(f"This field {key} is optional in given video json data,we can use default false")
                        else:
                            if video.get(key) not in  ['true','false',True,False]:
                                logger.error(f'{key} should be bool, true or false') 

                    if video.get('categories')==None or video.get('categories')=='':
                        video['categories']=None      
                        logger.info('we use categories =none')
                    else:
                        if type(video.get('categories'))!=int:
                            logger.error('categories should be one of 0,1,....,14')
                        else:
                            if not video.get('categories') in range(0,15):
                                logger.error('categories should be one of 0,1,2,3..........,14')

                    if video.get('license_type')==None or video.get('license_type')=='':
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
                    if video.get('video_language')==None or video.get('video_language')=='':
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
                                        elif video.get('release_date_hour') not in settings[locale]['availableScheduleTimes']:
                                            logger.error(f"we use choose one from {settings[locale]['availableScheduleTimes']}") 
                    if video.get('prorioty')==None:
                        video['prorioty']=False      
                        logger.info(f'we use prorioty ==False')  
                    else:                    
                        if type(video.get('prorioty'))==bool:
                            pass
                        elif type(video.get('prorioty'))==str and video.get('prorioty').lower() not in ['true','false']:

                            logger.error(f'prorioty is {video.get("prorioty")} of {type(video.get("prorioty"))},it should be bool, true or false')
                    
                    if video.get('release_date')==None:
                        nowdate=datetime.now() 
                        video['release_date']=nowdate      
                        logger.info(f'we use release_date =={nowdate }')  
                    else:
                        if video.get('release_date_hour')==None:    
                            video['release_date_hour']="10:15"   
                            logger.info('we use default release_date_hour 10:15')    
                        elif video.get('release_date_hour') not in settings[locale]['availableScheduleTimes']:
                            logger.error(f"we use choose one from {settings[locale]['availableScheduleTimes']}")    
                    if video.get('release_date_hour')==None:     
                        video['release_date_hour']="10:15"   
                        logger.info('we use default release_date_hour 10:15')    
                    elif video.get('release_date_hour') not in settings[locale]['availableScheduleTimes']:
                        logger.error(f"we use choose one from {settings[locale]['availableScheduleTimes']}")  
                    if video.get('tags')==None:
                        video['tags']=None      
                        logger.info('we use tags =[]')
                    else:
                        if type(video.get('tags'))==str and "," in video.get('tags'):
                            logger.info(f'tags is ok:{video.get("tags")}')                                

                        else:
                            logger.error('tags should be a list of keywords such as "one,two" ')
                    taskvideo=None
                    logger.info(f'start to process video data')
                    print(f"this is need to use which video model:{video.get('platform')}")
                    if video.get('platform')=='youtube' or video.get('platform')==0:

                        videodata=    {
                                "video_local_path": str(PurePath(video['video_local_path'])),
                                "video_title": video['video_title'],
                                "video_description": video['video_description'],
                                "thumbnail_local_path":video['thumbnail_local_path'],
                                "publish_policy": video['publish_policy'],
                                "tags": 
                                    video['tags'],
                                
                                }
                        logger.info(f'start to save ytb video data {settingdata} to db')

                        taskvideo=YoutubeVideoModel.add_video(videodata)
                    else:
                        print(f"we dont support yet to save video for: {video.get('platform')}")
                        videodata=    {
                                "video_local_path": video['video_local_path'],
                                "video_title": video['video_title'],
                                "video_description": video['video_description'],
                                "thumbnail_local_path":video['thumbnail_local_path'],
                                "publish_policy": video['publish_policy'],
                                "tags": 
                                    video['tags'],
                                
                                }
                        logger.info(f'start to save ytb video data {settingdata} to db')

                        taskvideo=YoutubeVideoModel.add_video(videodata)                        
                    logger.info(f'end to process video data')

                    taskdata={
                        "type":video['platform'],
                        "status":0,
                        "prorioty":video['prorioty']
                    }
                    logger.info(f'end to process video data')
                    logger.info(f'start to process task data')

                    taskid=TaskModel.add_task(taskdata,taskvideo,tasksetting)
                    if taskid==None:
                        print(f'add task failure:{idx},{video}')

                    else:
                        print(f'add task success:{idx},{video}')
                    logger.info(f'end to process task data')

                                                
            except Exception as e:
                logger.error(f'there is no videos in  your task meta file.check  docs for reference:{e}')                
            


        else:
            showinfomsg(message="please choose a valid task file")
            logger.error("you choosed task meta  file is missing or broken.")

    else:
        showinfomsg(message="please choose a valid task file")
        logger.error("you choosed task meta  file is missing or broken.")       

def uploadView(frame,ttkframe,lang):
    queryframe=tk.Frame(ttkframe)
    queryframe.grid(row = 0, column = 0,sticky='w')
    queryframe.grid_rowconfigure((0,1), weight=1)
    
    queryframe.grid_columnconfigure(0, weight=1)
    
    
    
    global vid
    
    taskstatus = tk.StringVar()
    lbl15 = tk.Label(queryframe, text='Enter status.')
    lbl15.grid(row = 0, column = 3,sticky='w')
    txt15 = tk.Entry(queryframe, textvariable=taskstatus)
    txt15.insert(0,'input status')
    txt15.grid(row = 1, column = 3,sticky='w',columnspan=2)

    # Create a label for the platform dropdown
    platform_label = ttk.Label(queryframe, text="Select Platform:")
    platform_label.grid(row=0, column=6, padx=10, pady=10, sticky=tk.W)
    # Create a Combobox for the platform selection
    platform_var = tk.StringVar()
    platform_var.set("choose one:")    

    def db_values():
        platform_rows=PlatformModel.filter_platforms(name=None, ptype=None, server=None)
        platform_names = [PLATFORM_TYPE.PLATFORM_TYPE_TEXT[x.type][1] for x in platform_rows]

        platform_combo['values'] = platform_names

    def db_refresh(event):
        platform_combo['values'] = db_values()
    platform_combo = ttk.Combobox(queryframe, textvariable=platform_var)
    platform_combo.grid(row=1, column=6, padx=10, pady=10, sticky=tk.W)
    platform_combo.bind('<FocusIn>', lambda event: db_refresh(event))
    platform_combo['values'] = db_values()
    
    # platform_combo['values'] = db_values()
    vid = tk.StringVar()
    lbl15 = tk.Label(queryframe, text='Enter video id.')
    lbl15.grid(row = 0, column = 9,sticky='w')
    txt15 = tk.Entry(queryframe, textvariable=vid)
    txt15.insert(0,'input task id')
    txt15.grid(row = 1, column = 9,sticky='w',columnspan=2)

    vtitle = tk.StringVar()
    lbl15 = tk.Label(queryframe, text='Enter video title.')
    lbl15.grid(row = 2, column = 3,sticky='w')
    txt15 = tk.Entry(queryframe, textvariable=vtitle)
    txt15.insert(0,'input task title')
    txt15.grid(row = 3, column = 3,sticky='w',columnspan=2)

    channelname = tk.StringVar()
    lbl16 = tk.Label(queryframe, text='Enter channelname.')
    lbl16.grid(row = 2, column = 6,sticky='w')
    txt16 = tk.Entry(queryframe,textvariable=channelname)
    txt16.insert(0,'input channelname')
    txt16.grid(row = 3, column = 6,sticky='w',columnspan=2)

    releasedate = tk.StringVar()
    lbl17 = tk.Label(queryframe, text='Enter releasedate.')
    lbl17.grid(row = 2, column = 9,sticky='w')
    txt17 = tk.Entry(queryframe, textvariable=releasedate)
    txt17.insert(0,'input releasedate')
    txt17.grid(row = 3, column = 9,sticky='w',columnspan=2)




    btn5= tk.Button(queryframe, text="Get Info", command = lambda:queryTasks(status=taskstatus.get(),platform=platform_var.get(),username=channelname.get(),vid=vid.get(),vtitle=vtitle.get(),releasedate=releasedate.get()) )
    btn5.grid(row = 3, column = 12,  padx=14, pady=15)
    
    
    btn5= tk.Button(queryframe, text="Reset", padx = 0, pady = 0,command = lambda:(taskstatus.set(""),releasedate.set(""),platform_var.set(""),channelname.set(""),vid.set(''),vtitle.set('')))
    btn5.grid(row=3,column=15, sticky=tk.W)        
    # Create a frame for the canvas and scrollbar(s).
    chooseAccountsWindow=queryframe
    frame2 = tk.Frame(chooseAccountsWindow, bg='Red', bd=1, relief=tk.FLAT)
    frame2.grid(row=4, column=0, rowspan=5,columnspan=15,sticky=tk.NW)

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=1)
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame2, bg='Yellow')
    canvas.grid(row=0, column=0)

        
    def refreshcanvas(headers,datas):

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)
        ROWS_DISP = len(datas)+1 # Number of rows to display.
        COLS_DISP = len(headers)+1  # Number of columns to display.
        COLS=len(headers)+1
        
        ROWS=len(datas)+1



        # Add the buttons to the frame.
        add_buttons = [tk.Button() for j in range(ROWS+1)] 
        del_buttons = [tk.Button() for j in range(ROWS+1)] 
        
        # set table header


        for j,h in enumerate(headers):
            label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text=h)
            label.grid(row=0, column=j, sticky='news')                    
            if h=='operation':
                button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                button.grid(row=0, column=j, sticky='news')

                delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                delete_button.grid(row=0, column=j, sticky='news')

        for i,row in enumerate(datas):
            i=i+1
            for j in range(0,len(headers)):
                
                if headers[j]!='operation':
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=row[headers[j]])
                    label.grid(row=i ,column=j, sticky='news')         


              
            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row(rowid=datas[x]['id']))
            add_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row(rowid=datas[x]['id']))
            del_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')
                    
        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        print('=before==',COLS,COLS_DISP,ROWS,ROWS_DISP)

        for i in range(5,COLS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

            if dw>int( canvas.winfo_width()*0.2):
                COLS=i-1
        for i in range(5,ROWS_DISP):
            dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)                
            if dh>int( canvas.winfo_height()*0.2):
                ROWS=i-1

        print('=after==',COLS,COLS_DISP,ROWS,ROWS_DISP)
        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)

        if dw>int( root.winfo_width()/3):
            dw=int( root.winfo_width()/3)
        if dh>int( root.winfo_height()/3):
            dh=int( root.winfo_height()/3)
            print('use parent frame widht')
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        print('========',w,h,dw,dh,bbox)
    tab_headers=['id', 'platform', 'username', 'proxy', 'video title', 'uploaded_at', 'inserted_at']
    tab_headers.append('operation')
    tab_headers.append('operation')

    refreshcanvas(tab_headers,[])

    print('show tab headers')


    def queryTasks(username=None,platform=None,status=None,vtitle=None,releasedate=None,vid=None):

        if username==''or 'input' in username:
            username=None
        if releasedate==''or 'input' in releasedate:
            releasedate=None           
        if vid==''or 'input' in vid:
            vid=None           
        if vtitle==''or 'input' in vtitle:
            vtitle=None            
        if platform=='' or 'choose' in platform:
            platform=None        
        else:
            print('======',platform)
            print(f'query tasks for {platform} {getattr(PLATFORM_TYPE, platform.upper())} ')

            platform=getattr(PLATFORM_TYPE, platform.upper())

        if status=='' or 'input' in status:
            status=None        
        else:
            status=getattr(TASK_STATUS, status.upper())
            print(f'query tasks for {status} {getattr(TASK_STATUS, status.upper())} ')

        task_rows=TaskModel.filter_tasks(status=status,type=platform,video_title=vtitle,video_id=vid,username=username) 
        if task_rows is None or len(task_rows)==0:
            showinfomsg(message=f"try to add accounts for {platform} first",parent=chooseAccountsWindow)    

        else:                
            logger.info(f'we found {len(task_rows)} record matching ')
            showinfomsg(message='we found {} record matching'.format(len(task_rows)))
            i=0
            task_data=[]
            for row in task_rows:

                task={
                    "id":CustomID(custom_id=row.id).to_hex(),
                    "platform":                    PLATFORM_TYPE.PLATFORM_TYPE_TEXT[row.setting.platform][1]
,
                    "username":row.username,

                    "proxy":row.proxy,
                    "video title":row.video.video_title,
                    "uploaded_at":datetime.fromtimestamp(row.uploaded_at).strftime("%Y-%m-%d %H:%M:%S") if row.uploaded_at else None, 

                    "inserted_at":datetime.fromtimestamp(row.inserted_at).strftime("%Y-%m-%d %H:%M:%S")  
                }
                # print(task.keys())

                task_data.append(task)
            refreshcanvas(tab_headers,task_data)
            print('show header and rows based on query')
        
                
            logger.info(f'Account search and display finished')
                    


    # Bind the platform selection event to the on_platform_selected function



    
    def remove_selected_row(rowid):



        print('you want to remove these selected account',rowid)
        if rowid==0:

            showinfomsg(message='you have not selected  account at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:


            if rowid :
                rowid=CustomID(custom_id=rowid).to_bin()
                result=TaskModel.update_task(id=rowid,is_deleted=True)

                if result:
                    logger.info(f'this account {rowid} removed success')
                    showinfomsg(message=f'this account {rowid} removed success',parent=chooseAccountsWindow)    
                else:
                    logger.info(f'you cannot remove this account {rowid}, not added before')
                    showinfomsg(message=f'this account {rowid} not added before',parent=chooseAccountsWindow)    
            logger.info(f'end to remove,reset account {rowid}')


    def update_selected_row(rowid):
        # showinfomsg(message='not supported yet',parent=chooseAccountsWindow)    
        editsWindow = tk.Toplevel(frame)
        editsWindow.geometry(window_size)
        editsWindow.title('Edit and update task and related setting,video info ')
        rowid=CustomID(custom_id=rowid).to_bin()

        taskresult=TaskModel.get(id=rowid)
        taskresult = model_to_dict(taskresult)



        def renderelements(i=1,column=0,result={},disableelements=['id','inserted_at','unique_hash','platform'],title=None):
            rowkeys={}
            newresult={}
            label= tk.Label(editsWindow, padx=7, pady=7,bg="lightyellow", relief=tk.RIDGE,
                                activebackground= 'orange', text=title)
            label.grid(row=i ,column=column, sticky='news')    
            i=i+1
            for key,value in result.items():
                if i >23:
                    i=1
                    column=i%20+column+2
                # print('current key',key,value)
                if key=='id':
                    value=CustomID(custom_id=value).to_hex()
                if key=='platform':
                    value=  PLATFORM_TYPE.PLATFORM_TYPE_TEXT[value][1]
                if value==None:
                    value=''                        
                if key=='inserted_at':
                    value=datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")    
                if key=='video_local_path':
                    print('value===',value)
                    value=PurePath(value)
                    print('value===',value)
                    value=str(value)
                    print('value===',value)
                if key=='thumbnail_local_path':
                    print('value===',value)
                    value=PurePath(value)
                    print('value===',value)
                    value=str(value)
                    print('value===',value)                    
                if not  key  in disableelements:
                
                    label= tk.Label(editsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=key)
                    label.grid(row=i ,column=column, sticky='news')         
                    entry = tk.Entry(editsWindow)
            
                    entry.insert(0, value)
                    entry.grid(row=i ,column=column+1, sticky='news')   
                    rowkeys[i]=key
                    def callback(event):

                        x = event.widget.grid_info()['row']
                        print(f'current input changes for {rowkeys[x]}',event.widget.get())   

                        newresult[rowkeys[x]]=event.widget.get()
                        if rowkeys[x]=='is_deleted':
                            print('is deleted',type(event.widget.get()))
                            value='0'
                            if event.widget.get()=='0':
                                value=False
                            elif event.widget.get()=='1':
                                value=True                        
                            newresult[rowkeys[x]]=value

                        print('============update row',newresult)

                    # variable.trace('w', lambda:setEnty())    
                    entry.bind("<KeyRelease>", callback)

                else:

                    label = tk.Label(editsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=key)
                    label.grid(row=i ,column=column, sticky='news')         
                    variable=tk.StringVar()
                    variable.set(value)
                    entry = tk.Entry(editsWindow,textvariable=variable)
                    entry.grid(row=i ,column=column+1, sticky='news') 
                    entry.config(state='disabled')
                i=i+1
            return newresult,i,column+2

        tmptask=taskresult
        # tmptask.pop('video')
        # tmptask.pop('setting')
        print('taskresult\n',taskresult)
        print('video\n',taskresult.get('video'))
        print('setting\n',taskresult.get('setting'))
        newtaskresult,serialno,cols=renderelements(i=1,result=tmptask,column=0,disableelements=['id','inserted_at','type','uploaded_at','video','setting'],title='task data')
        newvideoresult={}
        newsettingresult={}
        newaccountresult={}
        print('======================',serialno,cols)

        if taskresult.get('video'):
            print('video is associated to task',serialno,cols)

            newvideoresult,serialno,cols=renderelements(i=1,result=taskresult.get('video'),column=cols,disableelements=['id','inserted_at','unique_hash','platform'],title='video data')
        if taskresult.get('setting'):
            print('setting is associated to task',serialno,cols)

            newsettingresult,serialno,cols=renderelements(i=1,result=taskresult.get('setting'),column=cols,disableelements=['id','inserted_at','account','platform'],title='setting data')
            if taskresult.get('setting').get('account') :
                print('account is associated to setting',serialno,cols)

                newaccountresult,serialno,cols=renderelements(i=serialno,result=taskresult.get('setting').get('account'),column=cols-2,disableelements=['id','inserted_at','unique_hash','platform'],title='account data')

        btn5= tk.Button(editsWindow, text="save", padx = 0, pady = 0,command = lambda:TaskModel.update_task(id=rowid,taskdata=newtaskresult,videodata=newvideoresult,settingdata=newsettingresult,accountdata=newaccountresult))
        btn5.grid(row=i+1,column=cols+1, sticky=tk.W)    


    
    
        



        
    
    b_create_task_metas = tk.Button(frame, text=settings[lang]['b_createTaskMetas'],
                                         command=lambda: threading.Thread(target=createTaskMetas(frame,ttkframe)).start())
    b_create_task_metas.grid(row = 0, column = 0, columnspan=2,padx=14, pady=15,sticky='w')
    Tooltip(b_create_task_metas, text=settings[lang]['t_createTaskMetas'], wraplength=200)


    b_down_video_metas_temp = tk.Button(frame, text=settings[lang]['b_editTaskMetas'], command=
                                #  lambda: webbrowser.open_new("https://jsoncrack.com/editor")
                                 lambda: threading.Thread(target=webbrowser.open_new("https://jsoncrack.com/editor")).start())
    b_down_video_metas_temp.grid(row = 0, column = 1, padx=14, pady=15,sticky='w')
    


    l_import_task_metas = tk.Label(frame, text=settings[lang]['l_importTaskMetas'])
    l_import_task_metas.grid(row = 2, column = 0, padx=14, pady=15,sticky='w')
    Tooltip(l_import_task_metas, text=settings[lang]['t_importTaskMetas'] , wraplength=200)

    b_imported_video_metas_file=tk.Button(frame,text="Select",command=lambda:SelectMetafile('taskmetafilepath',imported_task_metas_file))
    b_imported_video_metas_file.grid(row = 2, column = 2, padx=14, pady=15)


    imported_task_metas_file = tk.StringVar()        
    # l_imported_video_metas_file = tk.Label(ttkframe, text='thumbnail template file')
    # if tmp.has_key('taskmetafilepath'):
    #     imported_task_metas_file.set(tmp['taskmetafilepath'])
    # else:
    #     imported_task_metas_file.set('')
    # l_imported_video_metas_file.place(x=10, y=200)
    e_imported_video_metas_file = tk.Entry(frame, width=int(width*0.02), textvariable=imported_task_metas_file)
    e_imported_video_metas_file.grid(row = 2, column = 1, padx=14, pady=15)

  
    b_validate_video_metas = tk.Button(frame, text=settings[locale]['validateVideoMetas']
                                       , command=lambda: threading.Thread(target=validateTaskMetafile(test_engine,ttkframe,imported_task_metas_file.get())).start())
    b_validate_video_metas.grid(row = 4, column = 0, padx=14, pady=15)
    b_createuploadsession = tk.Button(frame, text=settings[locale]['createuploadsession']
                                      , command=lambda: threading.Thread(target=validateTaskMetafile(prod_engine,ttkframe,imported_task_metas_file.get())).start())
    b_createuploadsession.grid(row = 5, column = 0, padx=14, pady=15)

    # test upload  跳转到一个单独页面，录入一个视频的上传信息，点击上传进行测试。
    b_upload = tk.Button(frame, text=settings[locale]['testupload']
                         , command=lambda: threading.Thread(target=testupload(DBM('test'),ttkframe)).start())
    b_upload.grid(row = 4, column = 1, padx=14, pady=15)

    b_upload = tk.Button(frame, text=settings[locale]['upload']
                         , command=lambda: threading.Thread(target=runTask).start())
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

    checkvideocounts=0
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
    

    


def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# 信息消息框
def showinfomsg(message,title='hints',DURATION = 2000,parent=None):
    # msg1 = messagebox.showinfo(title="消息提示", message=message)
    # messagebox.after(2000,msg1.destroy)
    # parent.focus_force()
    top = Toplevel(parent)
    top.title(title)
    center_window(top)    
    # Update the Toplevel window's width to adapt to the message width

    message_widget=Message(top, text=message, padx=120, pady=120)
    message_widget.pack()
    message_widget.update_idletasks()
    window_width = message_widget.winfo_reqwidth() + 40  # Add padding      
    top.geometry(f"{window_width}x200")  # You can adjust the height as needed      
    top.after(DURATION, top.destroy)


# 疑问消息框

# def askquestionmsg(message):
#     msg4 = messagebox.askquestion(title="询问确认", message=message)
#     print(msg4)


# def askokcancelmsg(message):
#     msg5 = messagebox.askokcancel(title="确定或取消", message=message)
#     print(msg5)


# def askretrycancelmsg(message):
#     msg6 = messagebox.askretrycancel(title="重试或取消", message=message)
#     print(msg6)


# def askyesonmsg(message):
#     msg7 = messagebox.askyesno(title="是或否", message="是否开启团战")
#     print(msg7)


# def askyesnocancelmsg(message):
#     msg8 = messagebox.askyesnocancel(title="是或否或取消", message="是否打大龙", default=messagebox.CANCEL)
#     print(msg8)

def  queryProxies(logger,city=None,state=None,country=None,tags=None,network_type=None,status=None,frame=None,tree=None,langlist=None):
    city=city.lower()
    country=country.lower()
    tags=tags.lower()
    if status=='valid':
        status=1
    elif status=='invalid':
        status=0
    else:
        status=2        
    if city=='':
        city=None
    if country=='':
        country=None  
    if tags=='':
        tags=None      
    if state=='':
        state=None
    if network_type=='':
        network_type=None 
    db_rows=  ProxyModel.filter_proxies(city=city,country=country,tags=tags,status=status,state=state,network_type=network_type)
    hints=None


 
    if db_rows is not None:
        if tree != None:
            records = tree.get_children()
            for element in records:
                tree.delete(element) 
            for row in db_rows:

                proxy_id = row.id
                proxy_id=CustomID(custom_id=row.id).to_hex()
                tree.tag_configure('checkbox', background='lightblue')  # Customize background for checkboxes
                tree.tag_configure('delete', background='lightcoral')   # Customize background for delete buttons

                tree.insert(
                        "", 0, text=proxy_id,
                        values=(row.proxy_host, row.proxy_port, row.status, row.city, row.country, row.tags, row.proxy_validate_network_type, row.inserted_at)# Add a tag to the item
                    )
        if langlist !=None:
            langlist.delete(0,tk.END)
            logger.info(f'we found {len(db_rows)} record matching ')
            i=0
            for row in db_rows:
                proxy_id = str(row.id)
                host=str(row.proxy_host)
                port=str(row.proxy_port)
                protcol=row.proxy_protocol
                print(f"add this {proxy_id+':'+host+'-'+port} to list")
                langlist.insert(tk.END, host+'-'+port+'-'+protcol+':'+proxy_id)
                langlist.itemconfig(int(i), bg = "lime")


        hints=f'there is {len(db_rows)} matching records found for query'
        logger.info(f'search and display finished:\n')
    else:
        logger.info(f'there is no matching records for query:\n')
        hints=f'there is {len(db_rows)} matching records found for query'
        
    showinfomsg(hints)
    # lbl15 = tk.Label(frame,bg="lightyellow", text=hints)
    # lbl15.grid(row=5,column=1, sticky=tk.W)
    # lbl15.after(2000,lbl15.destroy)


def split_proxy(proxy_string):
    # Remove the protocol (e.g., "socks5://")
    if proxy_string.startswith('socks5://') or proxy_string.startswith('http://') or proxy_string.startswith('https://'):
        # proxy_string=proxy_string.replace('socks5://','').replace('http://','').replace('https://','')
        # Split the components using ":"
        components = proxy_string.split(':')

        # Extract the components
        proxy_protocol_type = components[0]
        host = components[1].replace('//','')
        port = components[2]
        user = components[3] if len(components) > 3 else None
        password = components[4] if len(components) > 4 and user is not None else None

        return proxy_protocol_type, host, port, user, password

    else:
        return None

def saveproxies(engine,proxies_list_raw,logger):
    proxies_list=[]
    if 'proxy list should be one proxy oneline,and each proxy in such format' in proxies_list_raw:
        proxies_list_raw=proxies_list_raw.replace('proxy list should be one proxy oneline,and each proxy in such format:','')
    if proxies_list_raw  :
        proxies_list=proxies_list_raw.split('\n')
        proxies_list=list(set(proxies_list))
        proxies_list=list(filter(None, proxies_list))
        logger.info(f'detected {len(proxies_list) } records to be added')
        
        
        tags=None
        servers=[]
        for idx,ele in enumerate(proxies_list):
            logger.info(f'start to pre-process {str(idx)} record: {type(ele)}')
            logger.info(f'start to detect whether tag exist:{ele}')

            if ";" in ele:
                logger.info(f'there is tags in this record:{ele}')

                url=ele.split(";")[0]
                tags=ele.split(";")[-1]
            else:
                logger.info(f'there is no tags in this record:{ele}')

                url=ele
            logger.info(f'end to detect whether tag exist:{ele}')
                
            if url:    
                logger.info(f'split into url:\n{ele.split(";")[0]}\ntags:\n{ele.split(";")[-1]}')
                                
                proxy_protocol_type, host, port, user, password=split_proxy(url)

                proxy_data = {
                    'proxy_protocol': proxy_protocol_type,
                    'proxy_provider_type': 0,
                    'proxy_host': host,
                    'proxy_port': port,
                    'proxy_username': user,
                    'proxy_password': password,
                    'ip_address': '127.0.0.1',
                    'country': 'US',
                    'tags': tags,
                    'status': 2,
                    'proxy_validate_network_type': None,
                    'proxy_validate_server': None,
                    'proxy_validate_results': None,
                }
                result=ProxyModel.add_proxy(proxy_data)
                print(f'save proxy {ele} :{result}')
                if result==False:
                    logger.error(f'add proxy failure :{ele}')   
                    showinfomsg(f'we can not add the same proxy twice :{ele}') 
                else:

                    showinfomsg(f'add proxy ok :{ele}') 

            else:
                logger.error(f'there is no valid proxy in this record :{ele}')         
                showinfomsg(f'there is no valid proxy in this record :{ele}')       
            logger.info(f'end to validate {str(idx)} record: {type(url)}')

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
    
    b_check_proxy=tk.Button(frame,text="bulk check proxy",command=lambda: threading.Thread(target=updateproxies(prod_engine,proxy_textfield.get("1.0", tk.END),logger)).start() )
    b_check_proxy.grid(row=5,column=1, sticky=tk.W)    
    

    b_clear_texts=tk.Button(frame,text="clear all texts",command=lambda: threading.Thread(target=proxy_textfield.delete(1.0,tk.END)).start() )
    b_clear_texts.grid(row=4,column=1, sticky=tk.W)
    
    b_choose_proxy=tk.Button(frame,text="load  from file",command=lambda: threading.Thread(target=select_file).start() )
    b_choose_proxy.grid(row=4,column=0, sticky=tk.W)



        
    global city,country,proxyTags,proxyStatus
    city = tk.StringVar()
    state = tk.StringVar()
    network_type = tk.StringVar()
    country = tk.StringVar()
    proxyTags = tk.StringVar()

    lbl15 = tk.Label(ttkframe, text='by city.')
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0,column=0, sticky=tk.W)

    txt15 = tk.Entry(ttkframe,textvariable=city)
    txt15.insert(0,'Los')
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1,column=0, sticky=tk.W)


    l_state= tk.Label(ttkframe, text='by state.')
    l_state.grid(row=0,column=1, sticky=tk.W)
    e_state = tk.Entry(ttkframe,textvariable=state)
    e_state.insert(0,'LA')
    e_state.grid(row=1,column=1, sticky=tk.W)


    lbl16 = tk.Label(ttkframe, text='by country.')
    lbl16.grid(row=0,column=2, sticky=tk.W)
    txt16 = tk.Entry(ttkframe,textvariable=country)
    txt16.insert(0,'USA')
    txt16.grid(row=1,column=2, sticky=tk.W)
    
    lb17 = tk.Label(ttkframe, text='by tags.')
    lb17.grid(row=0,column=3, sticky=tk.W)
    txt17 = tk.Entry(ttkframe,textvariable=proxyTags)
    txt17.insert(0,'youtube')
    txt17.grid(row=1,column=3, sticky=tk.W)

    l_networktype = tk.Label(ttkframe, text='by networktype.')
    l_networktype.grid(row=2,column=0, sticky=tk.W)
    e_networktype = tk.Entry(ttkframe,textvariable=network_type)
    e_networktype.insert(0,'resident')
    e_networktype.grid(row=3,column=0, sticky=tk.W)

    lb18 = tk.Label(ttkframe, text='by status.')
    lb18.grid(row=2,column=1, sticky=tk.W)


    proxyStatus = tk.StringVar()


    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set("Select From Status")
    proxyStatus.trace('w', proxyStatusCallBack)


    proxyStatusbox = ttk.Combobox(ttkframe, textvariable=proxyStatus)
    proxyStatusbox.config(values = ('valid', 'invalid','unchecked'))
    proxyStatusbox.grid(row = 3, column = 1, padx=14, pady=15)    





    btn5= tk.Button(ttkframe, text="Get proxy list", padx = 0, pady = 0,command = lambda: queryProxy(city.get(),state.get(),country.get(),proxyTags.get(),network_type.get(),
                            proxyStatus.get()))

    btn5.grid(row=4,column=0, sticky=tk.W)    
    
    btn5= tk.Button(ttkframe, text="Reset", padx = 0, pady = 0,command = lambda:(proxyStatus.set(""),country.set(""),state.set(""),city.set(""),proxyTags.set(""),proxyStatus.set("Select From Status"),network_type.set("")))
    btn5.grid(row=4,column=1, sticky=tk.W)    


    # Create a frame for the canvas and scrollbar(s).
    chooseAccountsWindow=ttkframe
    frame2 = tk.Frame(chooseAccountsWindow, bg='Red', bd=1, relief=tk.FLAT)
    frame2.grid(row=5, column=0, rowspan=5,columnspan=5,sticky=tk.NW)

    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    frame2.grid_columnconfigure(1, weight=1)
    # Add a canvas in that frame.
    canvas = tk.Canvas(frame2, bg='Yellow')
    canvas.grid(row=0, column=0)

        
    def refreshcanvas(headers,datas):

        # Create a vertical scrollbar linked to the canvas.
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to the canvas.
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas.configure(xscrollcommand=hsbar.set)

        # Create a frame on the canvas to contain the grid of buttons.
        buttons_frame = tk.Frame(canvas)
            

        COLS=len(headers)+1
        
        ROWS=len(datas)+1
        if COLS>9:
            COLS_DISP=9
        else:
            COLS_DISP=COLS
        if ROWS>20:
            ROWS_DISP=20
        else:
            ROWS_DISP=ROWS        
        # Add the buttons to the frame.
        add_buttons = [tk.Button() for j in range(ROWS+1)] 
        del_buttons = [tk.Button() for j in range(ROWS+1)] 
        
        # set table header


        for j,h in enumerate(headers):
            label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text=h)
            label.grid(row=0, column=j, sticky='news')                    
            if h=='operation':
                button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text='operation')
                button.grid(row=0, column=j, sticky='news')

                # delete_button = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                #                     activebackground= 'orange', text='operation')
                # delete_button.grid(row=0, column=j-1, sticky='news')

        for i,row in enumerate(datas):
            i=i+1
            for j in range(0,len(headers)):
                
                if headers[j]!='operation':
                    label = tk.Label(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                        activebackground= 'orange', text=row[headers[j]])
                    label.grid(row=i ,column=j, sticky='news')         

              
            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='check',command=lambda x=i-1  :check_selected_row(rowid=datas[x]['id']))
            add_buttons[i].grid(row=i, column=len(headers)-3, sticky='news')
              
            add_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='edit',command=lambda x=i-1  :update_selected_row(rowid=datas[x]['id']))
            add_buttons[i].grid(row=i, column=len(headers)-2, sticky='news')

            del_buttons[i] = tk.Button(buttons_frame, padx=7, pady=7, relief=tk.RIDGE,
                                activebackground= 'orange', text='delete',command=lambda x=i-1 :remove_selected_row(rowid=datas[x]['id']))
            del_buttons[i].grid(row=i, column=len(headers)-1, sticky='news')
                    
        # Create canvas window to hold the buttons_frame.
        canvas.create_window((0,0), window=buttons_frame, anchor=tk.NW)

        buttons_frame.update_idletasks()  # Needed to make bbox info available.
        bbox = canvas.bbox(tk.ALL)  # Get bounding box of canvas with Buttons.

        # Define the scrollable region as entire canvas with only the desired
        # number of rows and columns displayed.
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]


        dw, dh = int((w/COLS) * COLS_DISP), int((h/ROWS) * ROWS_DISP)
        if dw>int(width/2):
            dw,dh=int(width/2),int(height/2)
        canvas.configure(scrollregion=bbox, width=dw, height=dh)
        print('========',w,h,dw,dh,bbox)
    tab_headers=['id', 'provider', 'protocol', 'host', 'port', 'username', 'pass', 'country', 'state', 'city', 'tags', 'status', 'validate_results', 'is_deleted', 'inserted_at']
    tab_headers.append('operation')
    tab_headers.append('operation')
    tab_headers.append('operation')
    
    refreshcanvas(tab_headers,[])

    def check_selected_row(rowid):
        
        print('check proxy whether valid and its city country')
        result=ProxyModel.get_proxy_by_id(id=rowid)
        # if len(results)>0:
        #     showinfomsg(f'there are {len(results)} proxy to be validated')
        #     for proxy in results:
        #         proxy_string=(
        #                     f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
        #                     if proxy.proxy_username
        #                     else f"{proxy.proxy_host}:{proxy.proxy_port}"
        #                 )
        #         http_proxy=f"socks5://{proxy_string}"
        #         https_proxy=f"socks5://{proxy_string}"

        #         check=CheckIP(http_proxy=http_proxy,https_proxy=https_proxy)
        #         ip=check.check_api64ipify()
        #         print('check_api64ipify',ip)
        #         asp=check.check_asn_type()
        #         print('asp',asp)
        #         dnscountry=check.check_dns_country(ip)
        #         print('dnscountry',dnscountry)

        #         ipcountry=check.check_ip_coutry(ip)
        #         print('ipcountry',ipcountry)


    def queryProxy(city,state,country,tags,network_type,status):
        city=city.lower()
        country=country.lower()
        tags=tags.lower()
        if status=='valid':
            status=1
        elif status=='invalid':
            status=0
        else:
            status=2        
        if city=='':
            city=None
        if country=='':
            country=None  
        if tags=='':
            tags=None      
        if state=='':
            state=None
        if network_type=='':
            network_type=None 
        db_rows=  ProxyModel.filter_proxies(city=city,country=country,tags=tags,status=status,state=state,network_type=network_type)
        # Extract account names and set them as options in the account dropdown
        if db_rows is None or len(db_rows)==0:
            # langlist.delete(0,tk.END)
            showinfomsg(message=f"try to add proxy first",parent=chooseAccountsWindow)    

        else:                
            logger.info(f'we found {len(db_rows)} record matching ')

            # langlist.delete(0,tk.END)
            i=0
            account_data=[]
            for row in db_rows:
                account={
                    "id":CustomID(custom_id=row.id).to_hex(),
                    "provider": PROXY_PROVIDER_TYPE.PROXY_PROVIDER_TYPE_TEXT[row.proxy_provider_type][1],
                    "protocol":row.proxy_protocol,
                    "host":row.proxy_host,
                    "port":row.proxy_port,                    
                    "username":row.proxy_username,
                    "pass":row.proxy_password,
                    "country":row.country,
                    "state":row.state,
                    "city":row.city,                    
                    "tags":row.tags,                    
                    "status":row.status,                    
                    "validate_results":row.proxy_validate_results,
                    "is_deleted":row.is_deleted   ,
                    "inserted_at":datetime.fromtimestamp(row.inserted_at).strftime("%Y-%m-%d %H:%M:%S")
                }
                account_data.append(account)
                print(account.keys())
            refreshcanvas(tab_headers,account_data)
        
        
                
            logger.info(f'Account search and display finished')
                    


    # Bind the platform selection event to the on_platform_selected function



    
    def remove_selected_row(rowid):



        print('you want to remove these selected account',rowid)
        if rowid==0:

            showinfomsg(message='you have not selected  account at all.choose one or more',parent=chooseAccountsWindow)      
        
        else:


            if rowid :
                rowid=CustomID(custom_id=rowid).to_bin()
                result=ProxyModel.delete_by_id(id=rowid,is_deleted=True)

                if result:
                    logger.info(f'this account {rowid} removed success')
                    showinfomsg(message=f'this account {rowid} removed success',parent=chooseAccountsWindow)    
                else:
                    logger.info(f'you cannot remove this account {rowid}, not added before')
                    showinfomsg(message=f'this account {rowid} not added before',parent=chooseAccountsWindow)    
            logger.info(f'end to remove,reset account {rowid}')


    def update_selected_row(rowid):
        # showinfomsg(message='not supported yet',parent=chooseAccountsWindow)    
        chooseAccountsWindow = tk.Toplevel(frame)
        chooseAccountsWindow.geometry(window_size)
        chooseAccountsWindow.title('Edit and update account info ')
        rowid=CustomID(custom_id=rowid).to_bin()

        result=ProxyModel.get_proxy_by_id(id=rowid)
        from playhouse.shortcuts import model_to_dict
        result = model_to_dict(result)
        print('----------',result)

        i=1
        newresult=result
        rowkeys={}
        for key,value in result.items():
            if key=='id':
                print('convert id to hex',value)
                value=CustomID(custom_id=value).to_hex()
                print('convert id to hex',value)
                
            if key=='platform':
                value=  PLATFORM_TYPE.PLATFORM_TYPE_TEXT[value][1]
            if key=='provider':
                value=  PROXY_PROVIDER_TYPE.PROXY_PROVIDER_TYPE_TEXT[value][1]
                
            if key=='status':
                value =PROXY_STATUS.PROXY_STATUS_TEXT[value][1]
            if value==None:
                value=''
            if key=='inserted_at':
                value=datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")          
            print('current key',key,value)
            if not  key  in ['id','inserted_at','unique_hash','platform']:
            
                label= tk.Label(chooseAccountsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text=key)
                label.grid(row=i ,column=0, sticky='news')         
                entry = tk.Entry(chooseAccountsWindow)

                entry.insert(0, value)
                entry.grid(row=i ,column=1, sticky='news')   
                rowkeys[i]=key
                def callback(event):

                    x = event.widget.grid_info()['row']
                    print(f'current input changes for {rowkeys[x]}',event.widget.get())   

                    newresult[rowkeys[x]]=event.widget.get()
                    if rowkeys[x]=='is_deleted':
                        print('is deleted',type(event.widget.get()))
                        value='0'
                        if event.widget.get()=='0':
                            value=False
                        elif event.widget.get()=='1':
                            value=True                        
                        newresult[rowkeys[x]]=value

                    print('============update row',newresult)

                # variable.trace('w', lambda:setEnty())    
                entry.bind("<KeyRelease>", callback)

            else:

                label = tk.Label(chooseAccountsWindow, padx=7, pady=7, relief=tk.RIDGE,
                                    activebackground= 'orange', text=key)
                label.grid(row=i ,column=0, sticky='news')         
                variable=tk.StringVar()
                variable.set(value)
                entry = tk.Entry(chooseAccountsWindow,textvariable=variable)
                entry.grid(row=i ,column=1, sticky='news') 
                entry.config(state='disabled')
            i=i+1

        btn5= tk.Button(chooseAccountsWindow, text="save", padx = 0, pady = 0,command = lambda:ProxyModel.update_proxy(id=rowid,proxy_data=newresult))
        btn5.grid(row=i+1,column=2, sticky=tk.W)    


def metaView(left,right,lang):
    global metaView_video_folder
    metaView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=settings[locale]['videoFolder'])
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    


    e_video_folder = tk.Entry(left,textvariable=metaView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    if metaView_video_folder.get()!='':
        if tmp['lastfolder'] is None or tmp['lastfolder']=='':
            pass
        else:            
            if tmp['metaView_video_folder'] is None:
                metaView_video_folder.set(tmp['lastfolder'])        
            metaView_video_folder.set(tmp['metaView_video_folder'])   
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(metaView_video_folder,'metaView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    if metaView_video_folder.get()!='':

        tmp['metaView_video_folder']=metaView_video_folder.get()

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(metaView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    l_meta_format = tk.Label(left, text=settings[locale]['l_metafileformat']
                             )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row = 1, column = 0, sticky='w', padx=14, pady=15)    
    global metafileformat
    

    metafileformat = tk.StringVar()


    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
        analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True)        
    metafileformat.set("Select From format")
    metafileformat.trace('w', metafileformatCallBack)


    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values = ( 'json','xlsx', 'csv'))
    metafileformatbox.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)      
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)  



    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(metaView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True,isDesView=True,isTagsView=True,isScheduleView=True)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    


def tagsView(left,right,lang):
    tagView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=settings[locale]['videoFolder'])
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=tagView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(tagView_video_folder,'tagView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)  
    if tagView_video_folder.get()!='':
        if tmp['lastfolder'] is None or tmp['lastfolder']=='':
            pass
        else:            
            if tmp['tagView_video_folder'] is None:
                tagView_video_folder.set(tmp['lastfolder'])        
            tagView_video_folder.set(tmp['tagView_video_folder'])    
    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(tagView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=settings[locale]['l_metafileformat']
                             )
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


    l_video_folder = tk.Label(left, text=settings[locale]['videoFolder'])
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=desView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(desView_video_folder,'desView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)    
    if desView_video_folder.get()!='':
        if tmp['lastfolder'] is None or tmp['lastfolder']=='':
            pass
        else:            
            if tmp['desView_video_folder'] is None:
                desView_video_folder.set(tmp['lastfolder'])        
            desView_video_folder.set(tmp['desView_video_folder'])   
    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(desView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)

    l_meta_format = tk.Label(left, text=settings[locale]['l_metafileformat'])
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
        analyse_video_meta_pair(desView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=False,isDesView=True,isTagsView=False,isScheduleView=False)
    print(f'right now metafileformatbox.get():{metafileformatbox.get()}')
    metafileformat.trace('w', metafileformatCallBack)

    b_download_meta_templates=tk.Button(left,text="check video meta files",command=lambda: threading.Thread(target=openLocal(desView_video_folder.get())).start() )
    b_download_meta_templates.grid(row = 1, column = 3, sticky='w', padx=14, pady=15)  
    Tooltip(b_download_meta_templates, text='run the check video assets will auto gen templates under folder if they dont' , wraplength=200)

    b_video_folder_check=tk.Button(left,text="Step1:check video assets",command=lambda: threading.Thread(target=analyse_video_meta_pair(desView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=False,isDesView=True,isTagsView=False,isScheduleView=False)).start() )
    b_video_folder_check.grid(row = 2, column = 0,sticky='w', padx=14, pady=15)    
    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)

    Tooltip(b_video_folder_check, text='calculate video counts,thumb file count and others' , wraplength=200)
    b_delete_folder_cache=tk.Button(left,text="remove cache data to re-gen",command=lambda: threading.Thread(target=ultra[thumbView_video_folder].unlink()).start() )
    b_delete_folder_cache.grid(row = 2, column = 1,sticky='w', padx=14, pady=15)  

def scheduleView(left,right,lang):
    scheduleView_video_folder = tk.StringVar()


    l_video_folder = tk.Label(left, text=settings[locale]['videoFolder'])
    l_video_folder.grid(row = 0, column = 0, sticky='w', padx=14, pady=15)    
    Tooltip(l_video_folder, text='Start from where your video lives' , wraplength=200)


    e_video_folder = tk.Entry(left,textvariable=scheduleView_video_folder)
    e_video_folder.grid(row = 0, column = 1, sticky='w', padx=14, pady=15)     
    print('===',type(scheduleView_video_folder.get()),scheduleView_video_folder.get())
    if scheduleView_video_folder.get()=='':
        print('herte===')
        if tmp.has_key('lastfolder') and  tmp['lastfolder']=='':
            if tmp['scheduleView_video_folder'] is None:
                scheduleView_video_folder.set(tmp['lastfolder'])    
        else:
            if tmp.has_key('scheduleView_video_folder') and  tmp['scheduleView_video_folder']=='':
                scheduleView_video_folder.set(tmp['scheduleView_video_folder'])  
    
    b_video_folder=tk.Button(left,text="Select",command=lambda: threading.Thread(target=select_tabview_video_folder(scheduleView_video_folder,'scheduleView_video_folder')).start() )
    b_video_folder.grid(row = 0, column = 2, sticky='w', padx=14, pady=15)       

    b_open_video_folder=tk.Button(left,text="open local",command=lambda: threading.Thread(target=openLocal(scheduleView_video_folder.get())).start() )
    b_open_video_folder.grid(row = 0, column = 3, sticky='w', padx=14, pady=15)    
    Tooltip(b_open_video_folder, text='open video folder to find out files change' , wraplength=200)
    print('save folder to tmp',tmp)
    l_meta_format = tk.Label(left, text=settings[locale]['l_metafileformat'])
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



def logView(log_tab_frame,root,lang):

    
    debugLevel = tk.StringVar()

    debugLevel.set("Debug Level:")
    def debugLevelCallBack(*args):
        print(debugLevel.get())
        print(debugLevelbox.current())
        st =ConsoleUi(log_tab_frame,root,row=1,column=0)

    def log_filterCallBack(*args):
        print(log_filter.get())
        st =ConsoleUi(log_tab_frame,root,row=1,column=0)

    debugLevel.trace('w', debugLevelCallBack)

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

def render(root,window,lang):
    global doc_frame,install_frame,thumb_frame,video_frame,proxy_frame,account_frame,upload_frame,meta_frame,tab_control

    tab_control = ttk.Notebook(window)
    tab_control.bind("<<NotebookTabChanged>>", on_tab_change)
    tab_control.grid_columnconfigure(0, weight=1)
    tab_control.grid_columnconfigure(1, weight=1)

    def refresh_video_folder(event):
        if tab_control.index(tab_control.select()) == 4:
            if thumbView_video_folder.get()!='':
                if tmp['lastfolder'] is None or tmp['lastfolder']=='':
                    pass
                else:            
                    if tmp['thumbView_video_folder'] is None:
                        thumbView_video_folder.set(tmp['lastfolder'])        
                    thumbView_video_folder.set(tmp['thumbView_video_folder'])  
            
        elif tab_control.index(tab_control.select()) == 5:
            # scheduleView_video_folder.set('')  # Reset the value to an empty string
            pass
    tab_control.bind("<<NotebookTabChanged>>", refresh_video_folder)
    

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
    logView(log_tab_frame,root,lang)

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
    Cascade_button.menu.add_cascade(label= settings[locale]['chooseLang']
                                    ,
                                    
                                     menu=Cascade_button.menu.choices)    
    
    Cascade_button.menu.loglevel = tk.Menu(Cascade_button.menu)
 
 
     # definition of the menu one level up...
    Cascade_button.menu.loglevel.add_command(label='DEBUG',command=lambda:changeLoglevel('DEBUG',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='INFO',command=lambda:changeLoglevel('INFO',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='WARNING',command=lambda:changeLoglevel('WARNING',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='ERROR',command=lambda:changeLoglevel('ERROR',window,log_frame))
    Cascade_button.menu.loglevel.add_command(label='CRITICAL',command=lambda:changeLoglevel('CRITICAL',window,log_frame))

    
    Cascade_button.menu.add_cascade(label=settings[locale]['loglevel']
                                    ,
                                    
                                     menu=Cascade_button.menu.loglevel)    

    menubar = tk.Menu(window)

    menubar.add_cascade(label=settings[locale]['settings']
                        , menu=Cascade_button.menu)    



    root.config(menu=menubar)
    # return langchoosen.get()

def start(lang,root=None):



    global paned_window,log_frame,mainwindow,text_handler

    root.geometry(window_size)
    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title(settings[lang]['title'])        


    # Create the frame for the notebook
    mainwindow = ttk.Frame(root)
    mainwindow.grid(row=0, column=0, sticky="nsew")

    mainwindow.grid_rowconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(0, weight=1)
    mainwindow.grid_columnconfigure(1, weight=1)


    


    # paned_window.add(log_frame)
    # log_frame.grid(row=1, column=0, sticky="nsew")

    # log_frame.grid_rowconfigure(0, weight=1)
    # log_frame.grid_columnconfigure(0, weight=1)
    # log_frame.columnconfigure(0, weight=1)
    # log_frame.rowconfigure(0, weight=1)


    # st =ConsoleUi(log_frame,root)

    logger.debug(f'Installation path is:{ROOT_DIR}')

    logger.info('TiktokaStudio GUI started')
    render(root,mainwindow,lang)
    root.update_idletasks()

# # Set the initial size of the notebook frame (4/5 of total height)
    # mainwindow_initial_percentage = 5 / 6  

    # Calculate the initial height of mainwindow based on the percentage
    # initial_height = int(float(root.winfo_height()) * mainwindow_initial_percentage)
    # mainwindow.config(height=initial_height)
def all_children (window) :
    _list = window.winfo_children()

    for item in _list :
        if item.winfo_children() :
            _list.extend(item.winfo_children())

    return _list
def changeDisplayLang(lang):
  
    mainwindow.destroy()

    
           
    
    # root.quit()    
    settings['lastuselang']=lang
    start(lang,root)
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

def start_fastapi_server(loop):
    import uvicorn
    config = uvicorn.Config(app, loop=loop, host='0.0.0.0', port=8000)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())
    
def start_fastapi_server_cmd():
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

# Mount the static files directory containing your HTML file
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

async def asynctk():
    start_tkinter_app()
def  start_tkinter_app():
    global root,settings,db
    tmp['accountlinkaccount']={}    

    root = tk.Tk()
    load_setting()
    # print('---',settings)
    locale=settings['lastuselang']
    start(locale,root)

    settings['folders']=tmp
    # root.protocol('WM_DELETE_WINDOW', withdraw_window)


    root.mainloop()
    
    dumpSetting(settingfilename)

@app.get("/")
def read_root():
    return FileResponse("static/proxy.html")  # Replace with the actual path to your HTML file

if __name__ == '__main__':


    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    # Start FastAPI server in a separate thread
    # fastapi_thread = threading.Thread(target=start_fastapi_server).start()

    # loop.create_task(asynctk())
    # start_fastapi_server(loop)

    start_tkinter_app()
