#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import threading


# Assuming filter_accounts is the function defined in api.py
from playhouse.shortcuts import model_to_dict
from pathlib import Path, PureWindowsPath, PurePath
from src.models.addtestdata import TestData
from src.bg_music import batchchangebgmusic
import psutil
# here put the import lib
from jsonschema import validate
from jsonschema import ValidationError
import json
import jsons
import tkinter as tk
import webbrowser
from tkinter import OptionMenu, filedialog, ttk, Message, Toplevel

import pandas as pd
import os, queue
import base64
import subprocess
import sys
import random
import os
import time
from src.models.create_tables import *
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
from src.bg_music import using_free_music
from PIL import Image, ImageTk
import multiprocessing as mp
from src.upload import *
from src.tooltip import Tooltip
from datetime import datetime, date, timedelta
import asyncio
import requests
import re
import calendar
from upgenius.utils.webdriver.setupPL import checkRequirments
import logging
from src.gpt_thumbnail import draw_text_on_image, validateSeting
from src.checkIp import CheckIP
from src.models.create_tables import *

try:
    import tkinter.scrolledtext as ScrolledText
except ImportError:
    import Tkinter as tk  # Python 2.x
    import ScrolledText
import pyperclip as clip
import platform
from pystray import MenuItem as item
import pystray

from UltraDict import UltraDict

from src.log import logger
from src.accountTablecrud import *
from src.taskTablecrud import *
from src.proxyTablecrud import *
task_queue = queue.Queue()
done_tasks = 0
taskcounts=0
if platform.system() == "Windows":
    ultra = UltraDict(shared_lock=True, recurse=True)
    tmp = UltraDict(shared_lock=True, recurse=True)
    citydb = UltraDict(shared_lock=True, recurse=True)

else:
    ultra = UltraDict(recurse=True)
    tmp = UltraDict(recurse=True)
    citydb = UltraDict(recurse=True)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

videoassetsfilename = "videos-assets.json"
citydbfilename = "assets/country-db/qq/en_loclist.json"
settingfilename = "settings.json"
locale = "en"
window_size = "1024x720"

height = 720
width = 1024
supported_video_exts = [".flv", ".mp4", ".avi"]
supported_thumb_exts = [".jpeg", ".png", ".jpg", "webp"]
supported_des_exts = [".des"]
supported_tag_exts = [".tags"]
supported_schedule_exts = [".schedule"]
supported_meta_exts = [".json", ".xls", ".xlsx", ".csv"]



window = None

availableScheduleTimes = []
uvicorn_subprocess=None


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

    def __init__(self, frame, root, row=0, column=0):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText.ScrolledText(frame, state="disabled")

        self.scrolled_text.bind_all("<Control-c>", self.copy)

        # Bind right-click event to show context menu
        # https://stackoverflow.com/questions/30668425/tkinter-right-click-popup-unresponsive-on-osx
        MAC_OS = False
        if sys.platform == "darwin":
            MAC_OS = True
        if MAC_OS:
            self.scrolled_text.bind("<Button-2>", self.show_context_menu)
        else:
            self.scrolled_text.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Clear All Text", command=self.clear_text)

        self.scrolled_text.grid(row=row, column=column, columnspan=2, sticky="nswe")
        self.scrolled_text.configure(font="TkFixedFont")
        self.scrolled_text.tag_config("INFO", foreground="black")
        self.scrolled_text.tag_config("DEBUG", foreground="gray")
        self.scrolled_text.tag_config("WARNING", foreground="orange")
        self.scrolled_text.tag_config("ERROR", foreground="red")
        self.scrolled_text.tag_config("CRITICAL", foreground="red", underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter("%(asctime)s: %(message)s")
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)

        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def clear_text(self):
        self.scrolled_text.configure(state="normal")  # Enable text widget
        self.scrolled_text.delete(1.0, tk.END)  # Delete all text
        self.scrolled_text.configure(state="disabled")  # Disable text widget again

    # Create a right-click context menu
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def copy(self, event):
        try:
            string = event.widget.selection_get()
            clip.copy(string)
        except:
            pass

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state="normal")
        self.scrolled_text.insert(tk.END, msg + "\n", record.levelname)
        self.scrolled_text.configure(state="disabled")
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
                lines.append(msg[: self.max_length])
                msg = msg[self.max_length :]
            lines.append(msg)
            msg = "\n".join(lines)

        def append():
            self.text.configure(state="normal")
            self.text.insert(tk.END, msg + "\n")
            self.text.configure(state="disabled")
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


def url_ok(url, proxy_option=""):
    try:
        if not proxy_option == "":
            # proxies = {
            #    'http': 'http://proxy.example.com:8080',
            #    'https': 'http://secureproxy.example.com:8090',
            # }
            if "http:" in proxy_option:
                proxies = {"http": proxy_option}
            elif "https:" in proxy_option:
                proxies = {
                    "https": proxy_option,
                }
            elif "socks" in proxy_option:
                proxies = {
                    "http": proxy_option,
                    "https": proxy_option,
                }
            else:
                proxy_option = "http://"
                proxies = {
                    "http": proxy_option,
                    "https": proxy_option,
                }
            print("use proxy", proxy_option)
            response = requests.head(url, proxies=proxies)
            print("google access is ok use {proxy_option}")
        else:
            response = requests.head(url)
            print("we cant  access google without proxy")

    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        print("we cant  access google")

        return False
    else:
        print("status code", response.status_code)
        if response.status_code == 200:
            print("we cant  access google")
            return True
        else:
            print(f"NOT OK: HTTP response code {response.status_code}")

            return False


def isfilenamevalid(filename):
    # print(imagename)
    invalid = '…,<>:."/\|?*!$\'"#'

    for char in invalid:
        filename = filename.replace(char, "")
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
        new_background = 0
    if len(mode) == 3:  # RGB
        new_background = (0, 0, 0)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (0, 0, 0, 0)
    new_im = Image.new(mode, (w, h), new_background)
    new_im.paste(im, ((w - x) // 2, (h - y) // 2))
    img = new_im.resize((canvas_width, canvas_height))
    if mode == "RGBA":
        img = img.convert("RGB")
    img.save(new_image_path)


def load_locales():
    folder_path = ROOT_DIR + os.sep + "locales" + os.sep

    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)

    # Filter the list to include only JSON files
    json_files = [f for f in file_list if f.endswith(".json")]

    # Loop through the JSON files and read their contents
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        with open(file_path, "r") as file:
            data = json.load(file)


def load_citydb():
    global citydb

    dbfile = PurePath(ROOT_DIR, citydbfilename)
    print(f"start to load country data {dbfile}")
    # print('===',open(dbfile,encoding='utf-8').read())
    failed = False
    if os.path.exists(dbfile):
        try:
            datas = json.loads(open(dbfile, encoding="utf-8").read())
            # print('json data',datas)
            citydb = datas
            # for key,value in enumerate(datas):
            #     print(f'load country db {key} {value}')
            #     citydb[key]=value
        except:
            failed = True
            print("load country db file failure")

    else:
        failed = True
        print("country db file not exist")


def load_setting():
    global settings
    settingfile = os.path.join(ROOT_DIR, settingfilename)
    failed = False
    if os.path.exists(settingfile):
        try:
            fp = open(settingfile, "r", encoding="utf-8")
            setting_json = fp.read()
            fp.close()
            settings = json.loads(setting_json)

        except:
            failed = True

    else:
        failed = True
    if failed == True:
        logger.debug("start initialize settings with default")
        print("start initialize settings with default")

        try:
            settings
        except:
            if platform.system() != "Windows":
                settings = UltraDict(recurse=True)
            else:
                settings = UltraDict(shared_lock=True, recurse=True)

        settings["lastuselang"] = "en"
        settings["zh"] = json.loads(
            open(
                os.path.join(ROOT_DIR + os.sep + "locales", "zh.json"),
                "r",
                encoding="utf-8",
            ).read()
        )
        settings["en"] = json.loads(
            open(
                os.path.join(ROOT_DIR + os.sep + "locales", "en.json"),
                "r",
                encoding="utf-8",
            ).read()
        )
        logger.debug("end to initialize settings with default")
    # print(settings)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


# 加载剧本

settingid = 0
# 保存配置


def select_tabview_video_folder(folder_variable, cache_var):
    global thumbView_video_folder_path
    try:
        thumbView_video_folder_path = filedialog.askdirectory(
            parent=root, initialdir="/", title="Please select a directory"
        )
        if os.path.exists(thumbView_video_folder_path):
            folder_variable.set(thumbView_video_folder_path)
            ultra[cache_var] = thumbView_video_folder_path
            print(f"You chose {folder_variable.get()} for {cache_var}")
            tmp[cache_var] = folder_variable.get()
            otherfolders = [
                "thumbView_video_folder",
                "tagView_video_folder",
                "scheduleView_video_folder",
                "desView_video_folder",
                "metaView_video_folder",
            ]
            for i in otherfolders.remove(folder_variable):
                if i == "" or i is None:
                    tmp[i] = folder_variable.get()
            tmp["lastfolder"] = folder_variable.get()
            print("==", tmp)
        else:
            print("please choose a valid video folder")
            showinfomsg(message="please choose a valid video folder")

    except:
        print("please choose a valid video folder")
        showinfomsg(message="please choose a valid video folder")


def openLocal(folder):
    try:
        webbrowser.open("file:///" + folder)
    except:
        logger.error(f"please choose a valid video folder:\n{folder}")
        showinfomsg(message="please choose a valid video folder")


def select_videosView_video_folder():
    global videosView_video_folder_path
    try:
        videosView_video_folder_path = filedialog.askdirectory(
            parent=root, initialdir="/", title="Please select a directory"
        )
        if os.path.exists(videosView_video_folder_path):
            print("You chose %s" % videosView_video_folder_path)
            videosView_video_folder.set(videosView_video_folder_path)
            print("You chose %s" % videosView_video_folder.get())

        else:
            print("please choose a valid video folder")

    except:
        print("please choose a valid video folder")


def select_videos_folder():
    global video_folder_path
    try:
        video_folder_path = filedialog.askdirectory(
            parent=root, initialdir="/", title="Please select a directory"
        )
        if os.path.exists(video_folder_path):
            print("You chose %s" % video_folder_path)
        else:
            print("please choose a valid video folder")

    except:
        print("please choose a valid video folder")


def select_folder(dict, value):
    global music_folder_path
    try:
        music_folder_path = filedialog.askdirectory(
            parent=root, initialdir="/", title="Please select a directory"
        )

        if os.path.exists(music_folder_path):
            print("You chose %s" % music_folder_path)
            dict = music_folder_path
            value.set(music_folder_path)
        else:
            print("please choose a valid music folder")
    except:
        print("please choose a valid music folder")


docsopen = False


def docs(frame, lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    print("open docmentations")
    label_helptext_setting = tk.Label(
        newWindow,
        text=settings[locale]["docs_str"].replace("\\n", "\n"),
        justify="left",
        wraplength=450,
    )
    label_helptext_setting.pack()


def version(frame, lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)

    label_helptext_setting = tk.Label(
        newWindow,
        text=settings[locale]["version_str"].replace("\\n", "\n"),
        #   text = "First line\n and this is the second",
        justify="left",
    )
    label_helptext_setting.pack()


def contact(frame, lang):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # due to \n in json string should in \\n, so read it from json  need to convert to original
    label_helptext_setting = tk.Label(
        newWindow,
        text=settings[locale]["contact_str"].replace("\\n", "\n"),
        anchor="e",
        justify="left",
        wraplength=450,
    )
    label_helptext_setting.pack()

    group = tk.Label(
        newWindow,
        text=settings[locale]["contact_str_group"],
        anchor="e",
        justify="left",
    )
    group.pack()
    path_group = "./assets/feishu-chatgroup.jpg"
    img_group = Image.open(path_group)
    photo_group = ImageTk.PhotoImage(img_group)

    label_group = tk.Label(newWindow, image=photo_group, height=400, width=256)
    label_group.pack()

    personal = tk.Label(
        newWindow,
        text=settings[locale]["contact_str_personal"].replace("\\n", "\n"),
        anchor="e",
        justify="left",
    )
    personal.pack()
    path_personal = "./assets/wechat.jpg"
    img_personal = Image.open(path_personal)
    photo_personal = ImageTk.PhotoImage(img_personal)  # 在root实例化创建，否则会报错

    label_personal = tk.Label(newWindow, image=photo_personal, height=400, width=256)
    label_personal.pack()

    newWindow.mainloop()


def install():
    # subprocess.check_call([sys.executable, "-m", "playwright ", "install"])
    subprocess.check_call(["playwright ", "install"])


def testInstallRequirements():
    print("check install requirments")
    checkRequirments()


def testNetwork():
    print("start to test network and proxy setting")

    fnull = open(os.devnull, "w")
    return1 = subprocess.call(
        "ping www.whoer.net", shell=True, stdout=fnull, stderr=fnull
    )
    if return1:
        print("network not ready")
        # change_proxy()
        testNetwork()

    else:
        fnull.close()
        return True
    print("netwrork and proxy test is done")


def ValidateSetting():
    print("start to validate your upload settings")
    time.sleep(4)
    print("end to validate your upload settings")


async def bulk_pull_cookie_file():
    ytupload = YoutubeUpload(browserType="firefox", logger=logger)
    # query account in db
    username = None
    password = None
    login = await ytupload.youtube_login(username, password)
    if login:
        logger.debug("we need save cookie to future usage")
        cookiepath = username + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".json"
        await ytupload.page.context.storage_state(path=cookiepath)


def auto_gen_cookie_file(username, password, platform, proxy=None, cookiepath=None):
    print("call upgenius gen cookie api")
    if proxy is None or proxy == "":
        proxyserver = None
    else:
        print(f"get proxy:{proxy}")
        id = CustomID(custom_id=proxy).to_bin()
        proxydata = ProxyModel.get_proxy_by_id(id=id)
        certification = None
        print(f"proxy username:{proxydata.proxy_username}")
        if proxydata.proxy_username is not None:
            certification = f"@{proxydata.proxy_username}:{proxydata.proxy_password}"
        server = None
        if proxydata.proxy_host is not None:
            server = f"{proxydata.proxy_host}:{proxydata.proxy_port}"
        protocol = None
        if proxydata.proxy_protocol is not None:
            protocol = proxydata.proxy_protocol.lower()
        if certification is None:
            proxyserver = f"{protocol}://{server}"
        else:
            proxyserver = f"{protocol}://{server}{certification}"

    browserType = "firefox"
    url = None
    sites = settings[locale]["supportedsites"]
    platformname = None
    if type(platform) == int:
        try:
            platformname = getattr(PLATFORM_TYPE.PLATFORM_TYPE_TEXT, platform)
        except:
            logger.error("please add platform in database")
    else:
        platformname = platform
    try:
        url = sites[platformname]
    except:
        logger.error("please add url in json file")

    print(f"url{url}")
    if browserType in ["firefox", "webkit", "chromium"]:
        if proxyserver:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                # + ' --device "iPad Pro 11 landscape" '
                + " --proxy-server "
                + proxyserver
                + " --lang 'en-GB' --save-storage="
                + username
                + "-cookie.json "
                + url
            )
        else:
            command = (
                "playwright codegen -b "
                + browserType
                # + ' --device "iPhone 12" '
                + " --lang 'en-GB' --save-storage="
                + username
                + "-cookie.json "
                + url
            )
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        print(result)
        if result.returncode:
            print(f"failed to save cookie file:{result.stderr}")
            logger.error(f"failed to save cookie file:{result.stderr}")
            showinfomsg(message=f"failed to save cookie file:{result.stderr}")

        else:
            print(f"just check your cookie file:{username}-cookie.json")
            logger.debug(f"just check your cookie file:{username}-cookie.json")

            cookiepath.set(PurePath(ROOT_DIR, username + "-cookie.json "))


def select_file(title, variable, cached=None, limited="all", parent=None):
    file_path = ""
    try:
        if limited == "json":
            file_path = filedialog.askopenfilenames(
                title=title,
                filetypes=[("Json", "*.json"), ("All Files", "*")],
                parent=parent,
            )[0]
        elif limited == "images":
            file_path = filedialog.askopenfilenames(
                title=title,
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("JPG", "*.jpg"),
                    ("WebP", "*.webp"),
                    ("All Files", "*"),
                ],
                parent=parent,
            )[0]
        else:
            file_path = filedialog.askopenfilenames(
                title=title, filetypes=[("All Files", "*")], parent=parent
            )[0]
        variable.set(file_path)
        if cached is not None:
            cached = file_path
    except:
        print("please select a valid  file")


# 清理残留文件


def threadusing_free_musichelper(numbers):
    using_free_music(numbers[0], numbers[1])


def init_worker(mps, fps, cut):
    global memorizedPaths, filepaths, cutoff
    global DG

    print("process initializing", mp.current_process())
    memorizedPaths, filepaths, cutoff = mps, fps, cut
    DG = 1  ##nx.read_gml("KeggComplete.gml", relabel = True)


def hiddenwatermark():
    print("add hiddenwatermark to each video for  copyright theft")


def b64e(s):
    return base64.b64encode(s.encode()).decode()


def autothumb():
    # 文件夹下是否有视频文件

    # 视频文件是否有同名的图片

    try:
        video_folder_path = tmp["video_folder"]

    except NameError:
        print("not found fastlane folder  file")
    else:
        if video_folder_path:
            print("sure, it was defined dir.", video_folder_path)

            # check_video_thumb_pair(video_folder_path,False)
        else:
            print("pls choose file or folder")


def editVideoMetas():
    print("go to web json editor to edit prepared video metas in json format")


def SelectMetafile(cachename, var):
    logger.debug("start to import prepared video metas in json format")
    try:
        filepath = filedialog.askopenfilenames(
            title="choose  meta  file",
            filetypes=[
                ("Json", "*.json"),
                ("excel", "*.xls"),
                ("csv", "*.csv"),
                ("Excel", "*.xlsx"),
                ("All Files", "*"),
            ],
        )[0]
        tmp[cachename] = filepath
        var.set(filepath)
    except:
        logger.error("you should choose a valid path")
    # setting['channelcookiepath'] = channel_cookie_path
    logger.debug("finished to import prepared video metas in json format")


def chooseAccountsView(newWindow, parentchooseaccounts):
    chooseAccountsWindow = tk.Toplevel(newWindow)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title("Choose associated account")

    def refreshAccount(*args):
        parentchooseaccounts.set(account_var.get())

    account_var = tk.StringVar()
    lbl16 = tk.Label(chooseAccountsWindow, text="binded accounts")
    lbl16.grid(row=5, column=0, sticky=tk.W)
    txt16 = tk.Entry(
        chooseAccountsWindow,
        textvariable=account_var,
        width=int(int(window_size.split("x")[-1]) / 5),
    )
    txt16.grid(row=6, column=0, sticky=tk.W)
    account_var.trace("w", refreshAccount)

    accountView(chooseAccountsWindow, mode="bind", linkAccounts=account_var)


def isFilePairedMetas(r, videofilename, meta_exts_list, dict, meta_name):
    logger.debug(f"start to check {meta_name} for video: {videofilename}")
    print(f"before check:\n{jsons.dump(dict[meta_name])}")

    for ext in meta_exts_list:
        logger.debug(f"start to {ext}--{meta_name}")
        print(f"start to {ext}")

        metapath = os.path.join(r, videofilename + ext)
        if os.path.exists(metapath):
            logger.debug(
                f"meta filed  {meta_name} for {videofilename} is  exist:\n {metapath}"
            )
            if dict[meta_name] is not None and metapath not in dict[meta_name]:
                if dict[meta_name].has_key(videofilename) == False:
                    dict[meta_name][videofilename] = []
                    logger.debug(f"intial {meta_name} for {videofilename}:\n")
                if not metapath in dict[meta_name][videofilename]:
                    dict[meta_name][videofilename].append(metapath)
                print(f"append result:\n{dict[meta_name][videofilename]}")
                if meta_name == "thumbFilePaths":
                    logger.debug(
                        f"found thumbfiles,start to set video metas {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}"
                    )

                    if (
                        dict["videos"][videofilename]["thumbnail_local_path"] is None
                        or dict["videos"][videofilename]["thumbnail_local_path"] == ""
                    ):
                        print("video meta thumbnail is None")
                        print(f"try to add {metapath}")
                        print(dict["videos"][videofilename])
                        emptyfiles = []
                        emptyfiles.append(metapath)
                        print("empty", emptyfiles)
                        dict["videos"][videofilename]["thumbnail_local_path"] = str(
                            emptyfiles
                        )
                        print(dict["videos"][videofilename])

                        print(
                            "update video meta thumbnail",
                            dict["videos"][videofilename]["thumbnail_local_path"],
                        )
                        print(
                            f"found thumbfiles,end to set video metas is None== {ext}== {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}"
                        )

                    else:
                        if (
                            type(dict["videos"][videofilename]["thumbnail_local_path"])
                            == str
                        ):
                            dict["videos"][videofilename][
                                "thumbnail_local_path"
                            ] = eval(
                                dict["videos"][videofilename]["thumbnail_local_path"]
                            ).append(
                                metapath
                            )

                        else:
                            if (
                                not metapath
                                in dict["videos"][videofilename]["thumbnail_local_path"]
                            ):
                                dict["videos"][videofilename][
                                    "thumbnail_local_path"
                                ].append(metapath)
                        print(
                            f"found thumbfiles,end to set video metas {ext}== {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}"
                        )

                    logger.debug(
                        f"found thumbfiles,end to set video metas {type(dict['videos'][videofilename]['thumbnail_local_path'])},{dict['videos'][videofilename]['thumbnail_local_path']}"
                    )

                elif meta_name == "desFilePaths":
                    logger.debug(
                        f"found des files,start to set video metas {type(dict['videos'][videofilename]['video_description'])},{dict['videos'][videofilename]['video_description']}"
                    )
                    # 判断后缀是否包含国家编码

                    #如果发现多个后缀为.des的文件，自动根据suffix判断，en为默认，其他的全部丢到 otherdes 这个字段中，列表形式存储
                    with open(metapath, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                        contents = "\r".join(lines)
                        contents = contents.replace("\n", "")
                        dict["videos"][videofilename]["video_description"] = contents
                    logger.debug(
                        f"found des files,end to set video metas {type(dict['videos'][videofilename]['video_description'])},{dict['videos'][videofilename]['video_description']}"
                    )

                elif meta_name == "tagFilePaths":
                    logger.debug(
                        f"found tag files,start to set video metas {type(dict['videos'][videofilename]['tags'])},{dict['videos'][videofilename]['tags']}"
                    )

                    with open(metapath, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                        contents = "\r".join(lines)
                        contents = contents.replace("\n", "")
                        dict["videos"][videofilename]["tags"] = contents
                    logger.debug(
                        f"found tag files,end to set video metas {type(dict['videos'][videofilename]['tags'])},{dict['videos'][videofilename]['tags']}"
                    )

    print(
        f"after check:\n {jsons.dump(dict[meta_name])}:\n,{dict['videos'][videofilename]['thumbnail_local_path']}"
    )

    logger.debug(
        f"after check:\n {jsons.dump(dict[meta_name])}:\n,{dict['videos'][videofilename]['thumbnail_local_path']}"
    )

    tmpjson = os.path.join(r, videofilename + ".json")
    if os.path.exists(tmpjson):
        logger.debug(f"update to {videofilename} meta json")
        with open(tmpjson, "w") as f:
            f.write(jsons.dumps(dict["videos"][videofilename]))
    else:
        logger.debug(f"create a fresh {videofilename} meta json")
        with open(tmpjson, "a") as f:
            f.write(jsons.dumps(dict["videos"][videofilename]))


def syncVideometa2assetsjson(selectedMetafileformat, folder):
    changed_df_metas = None
    if os.path.exists(
        os.path.join(folder, "videos-meta." + selectedMetafileformat)
    ) and ultra.has_key(folder):
        if selectedMetafileformat == "xlsx":
            changed_df_metas = pd.read_excel(
                os.path.join(folder, "videos-meta.xlsx"), index_col=[0]
            )
            changed_df_metas.replace("nan", "")
            changed_df_metas = json.loads(changed_df_metas.to_json(orient="index"))
        elif selectedMetafileformat == "json":
            changed_df_metas = pd.read_json(os.path.join(folder, "videos-meta.json"))
            changed_df_metas.replace("nan", "")
            changed_df_metas = json.loads(changed_df_metas.to_json())

        elif selectedMetafileformat == "csv":
            changed_df_metas = pd.read_csv(
                os.path.join(folder, "videos-meta.csv"), index_col=[0]
            )
            changed_df_metas.replace("nan", "")
            changed_df_metas = json.loads(changed_df_metas.to_json(orient="index"))
        # ultra[folder]['videos']=changed_df_metas
        # oldvideos=dict(ultra[folder]['videos'])
        tmpvideos = dict({})
        # oldvideos=json.loads(jsons.dumps(ultra[folder] ['videos']))
        newfilenameslist = []
        logger.debug("start to check video file existence in the new metafile ")
        for filename, video in changed_df_metas.items():
            print("video", video, type(video))
            if os.path.exists(video["video_local_path"]):
                logger.debug("video file is ok")
                newfilenameslist.append(filename)
                tmpvideos[filename] = video

            else:
                logger.debug(
                    f"{video['video_local_path']} video file is broken or not found according to video metafile"
                )
                # newfilenameslist.remove(filename)
                # changed_df_metas.remove(filename)
        if ultra[folder].has_key("videos"):
            logger.debug(
                f"=111==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}"
            )

            # ultra[folder]['videos']= {}
            # 当某个key值为空 {} 如果你要赋值一个嵌套的对象 比如json样子的数组 是没有办法直接赋值的
            ultra[folder]['videos']= changed_df_metas
            # if dict(ultra[folder]["videos"]) == dict({}):
            #     logger.debug(
            #         f"=333==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}"
            #     )

            #     for filename, video in tmpvideos.items():
            #         ultra[folder]["videos"][filename] = video
            #     logger.debug(
            #         f"=444==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}"
            #     )
            # else:
            #     logger.debug(
            #         f"=555==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}"
            #     )
            #     try:
            #         ultra[folder]["videos"] = tmpvideos
            #     except Exception as e:
            #         logger.error(e)
            #     logger.debug(
            #         f"=5551==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}"
            #     )
            #     new = dict({})

            #     for filename, video in tmpvideos.items():
            #         logger.info(f"filename:{filename}\n new video data\n:{video}\n olddata:\n{ultra[folder]['videos'][filename]}")
            #         ultra[folder]["videos"][filename] = dict({})
            #         new[filename] = video
            #     ultra[folder]['videos']=new
        else:
            logger.debug(
                f"=666==\r {type(ultra[folder]['videos'])}{ultra[folder]['videos']}"
            )

            new = dict({})
            for filename, video in tmpvideos.items():
                new[filename] = video
            ultra[folder]["videos"] = new
        ultra[folder]["filenames"] = newfilenameslist
        if len(ultra[folder]["filenames"]) == 0:
            logger.debug(
                f"we could not find any video, video counts is {ultra[folder] ['videoCounts']},supported ext includes:\n{'.'.join(supported_video_exts)}"
            )
        # 遍历每个视频文件，核对视频文件、缩略图等文件是否存在，核对元数据中对应字段是否存在
        ultra[folder]["videoCounts"] = len(ultra[folder]["filenames"])
        print(
            f"during sync ,detected video counts {len(ultra[folder] ['filenames'])  }"
        )

        ultra[folder]["updatedAt"] = pd.Timestamp.now().value
        logger.debug("end to check video file existence in the new metafile ")


def creatNewfoldercache(folder):
    if ultra.has_key(folder) == False:
        ultra[folder] = {
            "videoCounts": 0,
            "thumbFileCounts": 0,
            "thumbMetaCounts": 0,
            "desFileCounts": 0,
            "desMetaCounts": 0,
            "tagFileCounts": 0,
            "tagMetaCounts": 0,
            "scheduleFileCounts": 0,
            "scheduleMetaCounts": 0,
            "metaFileCounts": 0,
            "updatedAt": pd.Timestamp.now().value,
            "filenames": [],
            "videoFilePaths": [],
            "thumbFilePaths": {},
            "desFilePaths": {},
            "scheduleFilePaths": {},
            "tagFilePaths": {},
            "metaFilePaths": {},
            "thumb_gen_setting": {
                "mode": 3,
                "render_style": "cord",
                "result_image_width": "",
                "result_image_height": "",
                # "bg_image": "",
                "template_path": "",
                "bg_folder": "",
                "bg_folder_images": [],
                "template": {},
            },
            "des_gen_setting": {
                "prefix": "",
                "suffix": "",
                "mode": "manually from .des file or append prefix suffix with des file or auto summary from subtitle or auto summary from tts",
            },
            "schedule_gen_setting": {"daily_limit": 4, "offset": 1},
            "tag_gen_setting": {
                "preferred": "",
                "mode": "manually from .tag file or manually +preferred or just preferred or api or auto",
            },
            "videos": {},
        }
    else:
        logger.debug(f"there is cache for {folder} already")


def scanVideofiles(folder):
    thumbFileCounts = 0
    thumbMetaCounts = 0

    desFileCounts = 0
    desMetaCounts = 0

    tagFileCounts = 0
    tagMetaCounts = 0
    metaMetaCounts = 0
    scheduleFileCounts = 0
    scheduleMetaCounts = 0
    metaFileCounts = 0
    logger.debug(f"start to scan video file existence in the {folder} ")

    for r, d, f in os.walk(folder):
        videos = []
        with os.scandir(r) as i:
            # how to deal sub-folder and fodler
            # if folder has no video but got 1 subfolder has 1 video, where to put metafiles
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]

                    ext = os.path.splitext(entry.name)[1]
                    if ext in supported_video_exts:
                        if (
                            ultra[folder]["filenames"] != []
                            and filename in ultra[folder]["filenames"]
                        ):
                            logger.debug(
                                f"you have prepared video metas for:{filename}"
                            )
                        else:
                            ultra[folder]["filenames"].append(filename)

                            videopath = os.path.join(r, entry.name)
                            ultra[folder]["videoFilePaths"].append(videopath)
                            print("this video is detected before", filename)
                            #   //0 -private 1-publish 2-schedule 3-Unlisted 4-public&premiere

                            # default single video meta json
                            video = {
                                "video_local_path": "",
                                "video_filename": "",
                                "video_title": "",
                                "heading": "",
                                "subheading": "",
                                "extraheading": "",
                                "video_description": "",
                                "thumbnail_bg_image_path": "",
                                "publish_policy": 2,
                                "thumbnail_local_path": "[]",
                                "release_date": "",
                                "release_date_hour": "10:15",
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
                                "categories": "",
                                "comments_ratings_policy": 1,
                                "tags": "",
                            }
                            ultra[folder]["videos"][filename] = video

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
                            ultra[folder]["videos"][filename]["video_local_path"] = str(
                                PurePath(videopath)
                            )
                            ultra[folder]["videos"][filename]["video_title"] = filename
                            ultra[folder]["videos"][filename][
                                "video_filename"
                            ] = filename
                            ultra[folder]["videos"][filename][
                                "video_description"
                            ] = filename

                            for ext in supported_thumb_exts:
                                filepath = os.path.join(r, filename + ext)
                                if os.path.exists(filepath):
                                    if (
                                        filepath
                                        in ultra[folder]["videos"][filename][
                                            "thumbnail_local_path"
                                        ]
                                    ):
                                        pass
                                    else:
                                        if (
                                            type(
                                                ultra[folder]["videos"][filename][
                                                    "thumbnail_local_path"
                                                ]
                                            )
                                            == str
                                        ):
                                            ultra[folder]["videos"][filename][
                                                "thumbnail_local_path"
                                            ] = eval(
                                                ultra[folder]["videos"][filename][
                                                    "thumbnail_local_path"
                                                ]
                                            )

                                            ultra[folder]["videos"][filename][
                                                "thumbnail_local_path"
                                            ].append(str(PurePath(filepath)))
                                        elif (
                                            ultra[folder]["videos"][filename][
                                                "thumbnail_local_path"
                                            ]
                                            is None
                                            or ultra[folder]["videos"][filename][
                                                "thumbnail_local_path"
                                            ]
                                            in ["", "[]"]
                                            or len(
                                                ultra[folder]["videos"][filename][
                                                    "thumbnail_local_path"
                                                ]
                                            )
                                            == 0
                                        ):
                                            empt = [].append(str(PurePath(filepath)))
                                            ultra[folder]["videos"][filename][
                                                "thumbnail_local_path"
                                            ] = str(empt)
                                        else:
                                            # filepath=base64.b64encode(filepath.encode('utf-8'))

                                            ultra[folder]["videos"][filename][
                                                "thumbnail_local_path"
                                            ].append(str(PurePath(filepath)))

                            # to-do
                            # supported_des_exts
                            # supported_tag_exts

                        if ultra[folder]["videos"][filename]["thumbnail_local_path"]:
                            if (
                                type(
                                    ultra[folder]["videos"][filename][
                                        "thumbnail_local_path"
                                    ]
                                )
                                == str
                            ):
                                ultra[folder]["videos"][filename][
                                    "thumbnail_local_path"
                                ] = eval(
                                    ultra[folder]["videos"][filename][
                                        "thumbnail_local_path"
                                    ]
                                )

                            files = ultra[folder]["videos"][filename][
                                "thumbnail_local_path"
                            ]
                            if files is not None:
                                if len(files) > 0:
                                    start = False
                                    for i in files:
                                        if os.path.exists(i):
                                            start = True
                                    if start == True:
                                        thumbMetaCounts += 1
                            else:
                                print(
                                    f"detect no thumb files for video {filename}==={files}"
                                )
                        if ultra[folder]["videos"][filename]["tags"] != "":
                            tagMetaCounts += 1

                        if ultra[folder]["videos"][filename]["video_description"] != "":
                            desMetaCounts += 1

                        if ultra[folder]["videos"][filename]["release_date"] != "":
                            scheduleMetaCounts += 1

                        # if ultra[folder]['thumbFilePaths'].has_key(filename)==False:
                        #     ultra[folder]['thumbFilePaths'][filename]=[]
                        isFilePairedMetas(
                            r,
                            filename,
                            supported_thumb_exts,
                            ultra[folder],
                            "thumbFilePaths",
                        )
                        isFilePairedMetas(
                            r,
                            filename,
                            supported_des_exts,
                            ultra[folder],
                            "desFilePaths",
                        )
                        isFilePairedMetas(
                            r,
                            filename,
                            supported_meta_exts,
                            ultra[folder],
                            "metaFilePaths",
                        )
                        isFilePairedMetas(
                            r,
                            filename,
                            supported_tag_exts,
                            ultra[folder],
                            "tagFilePaths",
                        )
                        isFilePairedMetas(
                            r,
                            filename,
                            supported_schedule_exts,
                            ultra[folder],
                            "scheduleFilePaths",
                        )
                else:
                    print("is folder", r, d, i)
    if len(ultra[folder]["filenames"]) == 0:
        logger.debug(
            f"we could not find any video, video counts is {ultra[folder] ['videoCounts']},supported ext includes:\n{'.'.join(supported_video_exts)}"
        )
    # 遍历每个视频文件，核对视频文件、缩略图等文件是否存在，核对元数据中对应字段是否存在
    ultra[folder]["videoCounts"] = len(ultra[folder]["filenames"])
    print(f"detected video counts {len(ultra[folder] ['filenames']) }")
    ultra[folder]["thumbFileCounts"] = len(ultra[folder]["thumbFilePaths"])
    ultra[folder]["thumbMetaCounts"] = thumbMetaCounts

    ultra[folder]["desFileCounts"] = len(ultra[folder]["desFilePaths"])
    ultra[folder]["desMetaCounts"] = desMetaCounts

    ultra[folder]["metaFileCounts"] = len(ultra[folder]["metaFilePaths"])
    ultra[folder]["metaMetaCounts"] = metaMetaCounts

    ultra[folder]["tagFileCounts"] = len(ultra[folder]["tagFilePaths"])

    ultra[folder]["tagMetaCounts"] = tagMetaCounts
    ultra[folder]["scheduleFileCounts"] = len(ultra[folder]["scheduleFilePaths"])
    ultra[folder]["scheduleMetaCounts"] = scheduleMetaCounts
    ultra[folder]["updatedAt"] = pd.Timestamp.now().value
    logger.debug(f"end to scan video file existence in the {folder} ")


def analyse_video_meta_pair(
    folder,
    frame,
    right_frame,
    selectedMetafileformat,
    isThumbView=True,
    isDesView=True,
    isTagsView=True,
    isScheduleView=True,
):
    assetpath = os.path.join(folder, videoassetsfilename)

    if folder == "":
        logger.debug("please choose a folder first")
    else:
        logger.debug(f"start to detecting video metas----------{ultra.has_key(folder)}")

        if ultra.has_key(folder):
            print(pd.Timestamp.now().value - ultra[folder]["updatedAt"])
            duration_seconds = (
                pd.Timestamp.now().value - ultra[folder]["updatedAt"]
            ) / 10**9  # Convert nanoseconds to seconds

            logger.debug(
                f"we cached {duration_seconds} seconds before for  this folder {folder}"
            )

        else:
            logger.debug(f"create cached data for this folder:\n{folder}")
            creatNewfoldercache(folder)
        if os.path.exists(videoassetsfilename):
            logger.debug("load video assets to cache")
            # os.remove(videoassetsfilename)
            assetpath = os.path.join(folder, videoassetsfilename)

            changed_df_metas = pd.read_json(assetpath)
            changed_df_metas.replace("nan", "")
            changed_df_metas = json.loads(changed_df_metas.to_json())

            ultra[folder] = changed_df_metas

        if os.path.exists(
            os.path.join(folder, "videos-meta." + selectedMetafileformat)
        ):
            logger.debug("sync videos-meta")
            print("============sync videos-meta==============")
            # os.remove(os.path.join(folder,'videos-meta.'+selectedMetafileformat))
            syncVideometa2assetsjson(selectedMetafileformat, folder)
            print("============end sync videos-meta==============")
        print("============start scanVideofiles==============")

        scanVideofiles(folder)
        print("============end scanVideofiles==============")
        print("============start dumpMetafiles==============")

        ultra[folder]["metafileformat"] = selectedMetafileformat
        dumpMetafiles(selectedMetafileformat, folder)
        print("============end dumpMetafiles==============")

        render_video_folder_check_results(
            frame,
            right_frame,
            folder,
            isThumbView,
            isDesView,
            isTagsView,
            isScheduleView,
            selectedMetafileformat,
        )


def dumpTaskMetafiles(selectedMetafileformat, folder):
    logger.debug(f"start to dump task metas for {folder} ")
    print(f"task to be dump :{tmp['tasks']}")
    if selectedMetafileformat == "xlsx":
        df_metas = pd.read_json(jsons.dumps(tmp["tasks"]), orient="index")

        metaxls = os.path.join(folder, "task-meta.xlsx")

        df_metas.to_excel(metaxls)
        logger.debug(f"end to dump task metas for {folder} to {metaxls}")

    elif selectedMetafileformat == "csv":
        df_metas = pd.read_json(jsons.dumps(tmp["tasks"]), orient="index")

        metacsv = os.path.join(folder, "task-meta.csv")

        df_metas.to_csv(metacsv)
        logger.debug(f"end to dump task metas for {folder} to {metacsv} ")

    else:
        df_metas = pd.read_json(jsons.dumps(tmp["tasks"]), orient="records")

        # json is the default ,there is always a videometa.json file after folder check
        metajson = os.path.join(folder, "task-meta.json")

        df_metas.to_json(metajson)
        logger.debug(f"end to dump task metas for {folder} to {metajson} ")


def dumpMetafiles(selectedMetafileformat, folder):
    logger.debug(f"start to dump video metas for {folder} ")

    if selectedMetafileformat == "xlsx":
        df_metas = pd.read_json(jsons.dumps(ultra[folder]["videos"]), orient="index")

        metaxls = os.path.join(folder, "videos-meta.xlsx")

        df_metas.to_excel(metaxls)
    elif selectedMetafileformat == "csv":
        df_metas = pd.read_json(jsons.dumps(ultra[folder]["videos"]), orient="index")

        metacsv = os.path.join(folder, "videos-meta.csv")

        df_metas.to_csv(metacsv)
    else:
        df_metas = pd.read_json(jsons.dumps(ultra[folder]["videos"]), orient="records")

        # json is the default ,there is always a videometa.json file after folder check
        metajson = os.path.join(folder, "videos-meta.json")

        df_metas.to_json(metajson)
    logger.debug(f"end to dump video metas for {folder} ")
    logger.debug(f"start to dump video assets for {folder} ")

    tmpjson = os.path.join(folder, videoassetsfilename)

    if os.path.exists(tmpjson):
        with open(tmpjson, "w") as f:
            f.write(jsons.dumps(ultra[folder]))
    else:
        with open(tmpjson, "a") as f:
            f.write(jsons.dumps(ultra[folder]))
    logger.debug(f"end to dump video assets for {folder} ")


def dumpSetting(settingfilename):
    folder = ROOT_DIR
    logger.debug(f"start to dump TiktokaStudio settings")
    logger.info(f"check settings before dump {settings}")

    tmpjson = os.path.join(folder, settingfilename)

    if os.path.exists(tmpjson):
        with open(tmpjson, "w") as f:
            f.write(jsons.dumps(settings))
    else:
        with open(tmpjson, "a") as f:
            f.write(jsons.dumps(settings))
    logger.debug(f"end to dump TiktokaStudio settings")


def exportcsv(dbm):
    videos = dbm.Query_undone_videos_in_channel()


def importundonefromcsv(dbm):
    videos = dbm.Query_undone_videos_in_channel()


def testupload(dbm, ttkframe):
    videos = dbm.Query_undone_videos_in_channel()
    print("there is ", len(videos), " video need to uploading for task ")

    if len(videos) > 0:
        publicvideos = []
        privatevideos = []
        othervideos = []
        is_open_browser = videos[0]["is_open_browser"]
        proxy_option = videos[0]["proxy_option"]

        if url_ok("http://www.google.com"):
            print("network is fine,there is no need for proxy ")
            print("start browser in headless mode", is_open_browser)

        else:
            print("google can not be access ")

            print("we need for proxy ", proxy_option)
            print("start browser in headless mode", is_open_browser, proxy_option)
        upload = YoutubeUpload(
            root_profile_directory="",
            proxy_option=proxy_option,
            is_open_browser=is_open_browser,
            debug=True,
            use_stealth_js=False,
            # if you want to silent background running, set watcheveryuploadstep false
            channel_cookie_path=videos[0]["channelcookiepath"],
            username=videos[0]["username"],
            browser_type="firefox",
            wait_policy="go next after copyright check success",
            password=videos[0]["password"],
            is_record_video=videos[0]["is_record_video"]
            # for test purpose we need to check the video step by step ,
        )

        for video in videos:
            if int(video.publishpolicy) == 1:
                print("add public uploading task video", video.videopath)

                publicvideos.append(video)
            elif int(video.publishpolicy) == 0:
                print("add private uploading task video", video.videopath)

                privatevideos.append(video)
            else:
                print("add schedule uploading task video", video.videopath)

                othervideos.append(video)
        if len(publicvideos) > 0:
            print("start public uploading task")
            asyncio.run(bulk_instantpublish(videos=publicvideos, upload=upload))
        if len(privatevideos) > 0:
            print("start private uploading task")

            asyncio.run(bulk_privatedraft(videos=privatevideos, upload=upload))
        if len(othervideos) > 0:
            print("start schedule uploading task")

            asyncio.run(
                bulk_scheduletopublish_specific_date(videos=othervideos, upload=upload)
            )


def cancel_all_waiting_tasks(frame=None):
    global done_tasks
    print(f" {done_tasks} tasks have been done.")

    if task_queue.qsize() > 0:
        with task_queue.mutex:
            # done_tasks.update(task_queue.queue)  # Add waiting tasks to done_tasks set
            task_queue.queue.clear()
        print(f"All waiting tasks have been canceled.")
    else:
        print("No waiting tasks to cancel.")
    print(f'except ongoing  {done_tasks} task is waiting to be finished, all the waiting {taskcounts-done_tasks} tasks are canceled')
    logger.debug(f'except ongoing  {done_tasks} task is waiting to be finished, all the waiting {taskcounts-done_tasks} tasks are canceled')
    askokcancelmsg(
        title='cancel waiting task',
        message=f'except ongoing  {done_tasks} task is waiting to be finished, all the waiting {taskcounts-done_tasks} tasks are canceled',
        parent=frame,
    )

def do_ups(
    async_loop,
    frame=None,
    username=None,
    platform=None,
    status=None,
    vtitle=None,
    schedule_at=None,
    vid=None,
    pageno=None,
    pagecount=None,
    ids=None,
    sortby="ASC",
):
    threading.Thread(
        target=lambda:
            _asyncio_thread_up(
                async_loop,
                frame,
                username,
                platform,
                status,
                vtitle,
                schedule_at,
                vid,
                pageno,
                pagecount,
                ids,
                "ASC",
            ),
    ).start()




def _asyncio_thread_up(
    async_loop,
    frame=None,
    username=None,
    platform=None,
    status=None,
    vtitle=None,
    schedule_at=None,
    vid=None,
    pageno=None,
    pagecount=None,
    ids=None,
    sortby="ASC",
):
    task=querydbtoqueues(
                async_loop=async_loop,
                frame=frame,
                username=username,
                platform=platform,
                status=status,
                vtitle=vtitle,
                schedule_at=schedule_at,
                vid=vid,
                pageno=pageno,
                pagecount=pagecount,
                ids=ids,
                sortby=sortby,
            )


    asyncio.run(task)
    totalmesg=asyncio.run(process_tasks_in_batch())
    update_tabular(

                async_loop=async_loop,
                frame=frame,
                username=username,
                platform=platform,
                status=status,
                vtitle=vtitle,
                schedule_at=schedule_at,
                vid=vid,
                pageno=pageno,
                pagecount=pagecount,
                ids=ids,
                sortby=sortby,
                totalmsg=totalmesg



        )

async def querydbtoqueues(
    async_loop=None,
    frame=None,
    username=None,
    platform=None,
    status=None,
    vtitle=None,
    schedule_at=None,
    vid=None,
    pageno=None,
    pagecount=None,
    ids=None,
    sortby="ASC",
):
    if sortby is None:
        sortby = "Add Date ASC"
    elif "choose" in sortby:
        sortby = "Add Date ASC"

    else:
        print(f"sort by {sortby}")

    sortby = find_key(SORT_BY_TYPE.SORT_BY_TYPE_TEXT, sortby)
    if pagecount is None:
        pagecount = 50
    if username is not None and "input" in username:
        username = None
    if username == "" or username is None:
        username = None
    if schedule_at is not None and "input" in schedule_at:
        schedule_at = None
    if schedule_at == "" or schedule_at is None:
        schedule_at = None
    if vid is not None and "input" in vid:
        vid = None
    if vid == "" or vid is None:
        vid = None
    if vtitle is not None and "input" in vtitle:
        vtitle = None
    if vtitle == "" or vtitle is None:
        vtitle = None

    if type(platform) == str and (
        platform == ""
        or platform in list(dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT).values()) == False
    ):
        platform = None
    else:
        try:
            print(
                f"query tasks for {platform} {getattr(PLATFORM_TYPE, platform.upper())} "
            )

            platform = getattr(PLATFORM_TYPE, platform.upper())
        except:
            platform = None
    if status == "":
        status = None
    elif (
        status is not None
        and status in list(dict(TASK_STATUS.TASK_STATUS_TEXT).values()) == False
    ):
        status = None
    else:
        try:
            print(f"query tasks for {status} {getattr(TASK_STATUS, status.upper())} ")

            status = getattr(TASK_STATUS, status.upper())
        except:
            status = None

    task_rows, counts = TaskModel.filter_tasks(
        status=status,
        schedule_at=schedule_at,
        platform=platform,
        video_title=vtitle,
        video_id=vid,
        username=username,
        pagecount=pagecount,
        pageno=pageno,
        ids=ids,
        sortby=sortby,
    )
    skipcount=0

    if task_rows is None or len(task_rows) == 0:
        showinfomsg(message=f"try to add tasks  first", parent=frame, DURATION=500)

    else:
        logger.debug(f"According to search conditions,we found {counts} record matching to upload")
        # showinfomsg(
        #     message=f"According to search conditions,we found {counts} record matching to upload",
        #     DURATION=500,
        # )
        i = 0
        tasks = []
        taskids = []

        no_concurrent = settings[locale]["no_concurrent"]
        uptasks = set()
        logger.debug(f"there are {len(task_rows)}  video attempt to upload")
        cancel=askokcancelmsg(
            title='verify before upload',
            message=f"{len(task_rows)} tasks add to queue now,upload will start automatically",
            parent=frame,
            DURATION=000,
        )

        if cancel==True:
            totalmsg = ""

            for row in task_rows:
                taskids.append(CustomID(custom_id=row.id).to_hex())
                uploadsetting = model_to_dict(row.setting)
                uploadsetting.pop("id")
                uploadsetting.pop("inserted_at")
                uploadsetting.pop("account")
                uploadsetting.pop("is_deleted")
                uploadsetting.pop("platform")
                uploadsetting["logger"] = logger


                proxyid = row.setting.account.proxy
                if proxyid:
                    proxyid=CustomID(custom_id=proxyid).to_bin()
                    proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                    proxy_string=None
                    if proxy:

                        proxy_string=(
                                    f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
                                    if proxy.proxy_username
                                    else f"{proxy.proxy_host}:{proxy.proxy_port}"
                                )
                        protocol=proxy.proxy_protocol
                        http_proxy=f"{protocol}://{proxy_string}"
                        https_proxy=f"{protocol}://{proxy_string}"

                        uploadsetting["proxy_option"] = https_proxy
                    else:
                        uploadsetting["proxy_option"] = None

                profile_directory = row.setting.account.profile_local_path
                uploadsetting['profile_directory']=profile_directory

                channel_cookie_path = row.setting.account.cookie_local_path
                uploadsetting['channel_cookie_path']=channel_cookie_path

                username=row.setting.account.username
                uploadsetting['username']=username

                password=row.setting.account.password
                uploadsetting['password']=password


                video = model_to_dict(row.video)


                video.pop("id")
                video.pop("unique_hash")
                video.pop("inserted_at")
                video.pop("is_deleted")
                if row.status==TASK_STATUS.SUCCESS:
                    print('task is already upload,skip it')
                    skipcount+=1
                else:
                    uptask = uploadTask(
                        taskid=row.id,
                        video=video,
                        uploadsetting=uploadsetting,
                        account=row.setting.account,
                    )

                    task_queue.put(uptask)

            print('query task from databbase and add it to queues')
    global taskcounts
    taskcounts=counts-skipcount
async def upload_task(uptask):
    global done_tasks

    try:
        done_tasks+=1  # Mark the task as done

        videoid, taskid = await uptask
        logger.debug(f'get videoid after upload: {videoid} for task {taskid}')
        return videoid,taskid

    except asyncio.CancelledError:
        # No problem, we want to stop anyway.
        logger.debug(f'task cancelled')
        return None,taskid

    except Exception as e:
        print(f'{uptask}: resulted in exception')
        logger.exception(e)
        return None,taskid

async def process_tasks_in_batch( ):
    tasks = []
    uptasks = set()
    no_concurrent = settings[locale]["no_concurrent"]
    stop_after_this_kick = False
    totalmsg = []
    global done_tasks

    while not task_queue.empty():
        if stop_after_this_kick:
            break

        uptasks.clear()

        for _ in range(min(no_concurrent - len(uptasks), task_queue.qsize())):
            uptask = task_queue.get()
            uptasks.add(uptask)

        if not uptasks:
            logger.debug('no more scheduled tasks, stopping after this kick.')
            stop_after_this_kick = True
            break

        # Execute tasks in batches using asyncio.gather
        done, pending = await asyncio.wait(
            [upload_task(uptask) for uptask in uptasks],
            return_when=asyncio.ALL_COMPLETED
        )

        all_tasks = done.union(pending)

        if not all_tasks:
            logger.debug('no more scheduled tasks, stopping after this kick.')
            stop_after_this_kick = True
            break

        elif all(task.done() for task in all_tasks):
            logger.debug(f'all {len(all_tasks)} tasks are done, fetching results and stopping after this kick.')

            for task_idx, task in enumerate(all_tasks):
                if not task.done():
                    continue

                try:
                    await task  # Wait for the task to complete
                except Exception as e:
                    print(f'{task}: resulted in exception')
                    logger.exception(e)

        logger.debug(f'end of the batch upload for {len(uptasks)} tasks')
        for task in all_tasks:
            videoid, taskid = task.result()

            if videoid is None:
                result = TaskModel.update_task(
                    id=CustomID(custom_id=taskid).to_bin(),
                    status=TASK_STATUS.FAILURE,
                )
                taskid = CustomID(custom_id=taskid).to_hex()
                totalmsg.append(f"this task {taskid} upload failed")
            else:
                result = TaskModel.update_task(
                    id=CustomID(custom_id=taskid).to_bin(),
                    videodata={"video_id": videoid},
                    status=TASK_STATUS.SUCCESS,
                )
                taskid = CustomID(custom_id=taskid).to_hex()
                totalmsg.append(f"this task {taskid} upload success")

        logger.debug(f'start to update status in the tabular for {len(uptasks)}')
    return "\n".join(totalmsg),  done_tasks



def update_tabular(totalmsg=None,
    async_loop=None,
    frame=None,
    username=None,
    platform=None,
    status=None,
    vtitle=None,
    schedule_at=None,
    vid=None,
    pageno=None,
    pagecount=None,
    ids=None,
    sortby="ASC",



                   ):

    # Notify user about the results
    askokcancelmsg(
        title='Upload Results',
        message=totalmsg,
        parent=frame,
    )

    queryTasks(
        async_loop,
        canvas=None,
        frame=frame,
        status=status,
        platform=platform,
        username=username,
        video_id=vid,
        video_title=vtitle,
        schedule_at=schedule_at,
        pageno=pageno,
        pagecount=pagecount,
        sortby=sortby,
    )
    # logger.debug(f"end to refresh tabular {len(tasks)}")


    # print(f"this batch task {len(tasks)} upload endding")
    # logger.info(f"this batch task {len(tasks)} upload endding")


def docView(frame, ttkframe, lang):
    b_view_readme = tk.Button(
        frame,
        text=settings[locale]["docs"],
        command=lambda: threading.Thread(target=docs(frame, lang)).start(),
    )
    b_view_readme.place(x=50, y=100)

    b_view_contact = tk.Button(
        frame,
        text=settings[locale]["contact"],
        command=lambda: threading.Thread(target=contact(frame, lang)).start(),
    )
    b_view_contact.place(x=50, y=200)

    b_view_version = tk.Button(
        frame,
        text=settings[locale]["version"],
        command=lambda: threading.Thread(target=version(frame, lang)).start(),
    )
    b_view_version.place(x=50, y=300)


def setupWizard(frame, td):
    ttkframe = tk.Toplevel(frame)
    ttkframe.geometry(window_size)
    ttkframe.title("Setup for")
    channel_cookie_user = tk.StringVar()
    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()

    l_platform = tk.Label(ttkframe, text=settings[locale]["testdatainstall"])
    # l_platform.place(x=10, y=90)
    l_platform.grid(row=0, column=0, columnspan=3, padx=14, pady=15)

    socialplatform = tk.StringVar()
    socialplatform_box = ttk.Combobox(ttkframe, textvariable=socialplatform)

    socialplatform_box["values"] = [
        settings[locale]["testdatainstall"],
        settings[locale]["startfromfolder"],
    ]

    # test_tasks,test_setting,test_videos,test_users=None

    def socialplatformOptionCallBack(*args):
        print(socialplatform.get())
        print(socialplatform_box.current())
        if socialplatform_box.current() == 0:
            showinfomsg(message="start to prepare fake data for testing purpose")
            logger.info(f'start to prepare fake data for testing purpose')

            test_tasks, test_setting, test_videos, test_users = td.addTestdata()
            if test_tasks:
                showinfomsg(message="test data is prepared")
                logger.info(f'test data is prepared')
        elif socialplatform_box.current() == 1:
            ttkframe.withdraw()
            tab_control.select(8)

    socialplatform.set("Select")
    socialplatform.trace("w", socialplatformOptionCallBack)
    socialplatform_box.bind("<Button-1>", socialplatformOptionCallBack())

    # socialplatform_box.config(values =platform_names)
    socialplatform_box.grid(row=0, column=5, columnspan=3, padx=14, pady=15)


def installView(frame, ttkframe, lang):
    td = TestData()
    b_view_readme = tk.Button(
        frame,
        text=settings[locale]["installview"]["testinstall"],
        command=lambda: threading.Thread(target=testInstallRequirements).start(),
    )
    b_view_readme.grid(row=0, column=1, sticky="w", padx=14, pady=15)

    b_install_testdata = tk.Button(
        frame,
        text=settings[locale]["installview"]["newuserwizard"],
        command=lambda: threading.Thread(target=setupWizard(frame, td)).start(),
    )
    b_install_testdata.grid(row=1, column=1, sticky="w", padx=14, pady=15)

    b_install_testdataRemove = tk.Button(
        frame,
        text=settings[locale]["installview"]["testdataRemove"],
        command=lambda: threading.Thread(target=td.removedata()).start(),
    )
    b_install_testdataRemove.grid(row=2, column=1, sticky="w", padx=14, pady=15)

    b_install_testdata = tk.Button(
        frame,
        text=settings[locale]["installview"]["cleardb"],
        command=lambda: threading.Thread(target=td.cleardata()).start(),
    )
    b_install_testdata.grid(row=3, column=1, sticky="w", padx=14, pady=15)
    # b_view_contact=tk.Button(frame,text=settings[locale]['testnetwork']
    #                          ,command=lambda: threading.Thread(target=testNetwork).start() )
    # b_view_contact.grid(row = 1, column = 1, sticky='w', padx=14, pady=15)

    # b_view_version=tk.Button(frame,text=settings[locale]['testsettingok']
    #                          ,command=lambda: threading.Thread(target=ValidateSetting).start() )
    # b_view_version.grid(row = 2, column = 1, sticky='w', padx=14, pady=15)

    locale_tkstudio = tk.StringVar()

    l_lang = tk.Label(ttkframe, text=settings[locale]["installview"]["L_chooseLang"])
    # l_lang.place(x=10, y=90)
    l_lang.grid(row=3, column=0, padx=14, pady=15)
    try:
        settings["locale"]
        print(f"cache locale exist {settings['locale']}")
        locale_tkstudio.set(settings["locale"])
    except:
        print("keep the default locale placeholder")
        # locale_tkstudio_box.set("Select From Langs")
        locale_tkstudio.set(settings[locale]["installview"]["chooseLanghint"])
        settings["locale"] = "en"

    def display_selected_item_index(event):
        try:
            settings["locale"]
            print(f"cache locale exist {settings['locale']}")
            locale_tkstudio.set(settings["locale"])
        except:
            print("keep the default locale")
            locale_tkstudio.set(settings[locale]["installview"]["chooseLanghint"])

    def locale_tkstudioOptionCallBack(*args):
        print(locale_tkstudio.get())
        print(locale_tkstudio_box.current())
        settings["locale"] = locale_tkstudio.get()
        print(f"save locale to cache { settings['locale']}")
        changeDisplayLang(locale_tkstudio.get())
        settings["locale"] = locale_tkstudio.get()

        locale = locale_tkstudio.get()

    locale_tkstudio.trace("w", locale_tkstudioOptionCallBack)

    locale_tkstudio_box = ttk.Combobox(ttkframe, textvariable=locale_tkstudio)
    locale_tkstudio_box.config(values=("en", "zh"))
    # locale_tkstudio_box.set(locale_tkstudio.get())
    locale_tkstudio_box.grid(row=3, column=1, padx=14, pady=15)
    locale_tkstudio_box.bind("<<ComboboxSelected>>", display_selected_item_index)


def videosView(left, right, lang):
    # global metaView_video_folder
    metaView_video_folder = tk.StringVar()

    l_video_folder = tk.Label(left, text=settings[locale]["metaview"]["videoFolder"])
    l_video_folder.grid(row=0, column=0, sticky="w", padx=14, pady=15)

    e_video_folder = tk.Entry(left, textvariable=metaView_video_folder)
    e_video_folder.grid(row=0, column=1, sticky="w", padx=14, pady=15)
    if metaView_video_folder.get() != "":
        if tmp["lastfolder"] is None or tmp["lastfolder"] == "":
            pass
        else:
            if tmp["metaView_video_folder"] is None:
                metaView_video_folder.set(tmp["lastfolder"])
            metaView_video_folder.set(tmp["metaView_video_folder"])
    b_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_tabview_video_folder(
                metaView_video_folder, "metaView_video_folder"
            )
        ).start(),
    )
    b_video_folder.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    if metaView_video_folder.get() != "":
        tmp["metaView_video_folder"] = metaView_video_folder.get()

    b_open_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["openlocalfolder"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_open_video_folder.grid(row=0, column=3, sticky="w", padx=14, pady=15)
    l_meta_format = tk.Label(
        left, text=settings[locale]["metaview"]["l_metafileformat"]
    )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    global metafileformat

    metafileformat = tk.StringVar()

    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
        # analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=isThumbView,isDesView=isDesView,isTagsView=isTagsView,isScheduleView=isTagsView)

    metafileformat.set(settings[locale]["metaview"]["dropdown_hints"])
    metafileformat.trace("w", metafileformatCallBack)

    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values=("json", "xlsx", "csv"))
    metafileformatbox.grid(row=1, column=1, sticky="w", padx=14, pady=15)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)

    b_download_meta_templates = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_downvideometafile"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_download_meta_templates.grid(row=1, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_download_meta_templates,
        text=settings[locale]["metaview"]["b_downvideometafile_hints"],
        wraplength=200,
    )

    b_video_folder_check = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_checkvideoassets"],
        command=""
        #    lambda: threading.Thread(target=analyse_video_meta_pair(metaView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=isThumbView,isDesView=isDesView,isTagsView=isTagsView,isScheduleView=isScheduleView)).start()
    )
    b_video_folder_check.grid(row=2, column=0, sticky="w", padx=14, pady=15)
    video_assets_toolkits = tk.Label(right, text=settings[locale]['videoView']["video_assets_toolkits"])
    video_assets_toolkits.grid(row=0, column=0, sticky="w", padx=14, pady=15)
    video_gen_toolkits = tk.Label(right, text=settings[locale]['videoView']["video_gen_toolkits"])
    video_gen_toolkits.grid(row=0, column=1, sticky="w", padx=14, pady=15)

    post_process_toolkits = tk.Label(right, text=settings[locale]['videoView']["post_process_toolkits"])
    post_process_toolkits.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    # b_autothumb = tk.Button(
    #     right,
    #     text=settings[locale]['videoView']["autothumb"],
    #     command=lambda: threading.Thread(target=autothumb).start(),
    # )
    # b_autothumb.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    # b_batchchangebgmusic = tk.Button(
    #     right,
    #     text=settings[locale]['videoView']["batchchangebgmusic"],
    #     command=lambda: threading.Thread(target=batchchangebgmusic).start(),
    # )
    # b_batchchangebgmusic.grid(row=2, column=0, sticky="w", padx=14, pady=15)

    # b_hiddenwatermark = tk.Button(
    #     right,
    #     text=settings[locale]['videoView']["hiddenwatermark"],
    #     command=lambda: threading.Thread(target=hiddenwatermark),
    # )
    # b_hiddenwatermark.grid(row=3, column=0, sticky="w", padx=14, pady=15)


def thumbView(left, right, lang):
    global thumbView_video_folder
    thumbView_video_folder = tk.StringVar()

    l_video_folder = tk.Label(left, text=settings[locale]["thumbview"]["videoFolder"])
    l_video_folder.grid(row=0, column=0, sticky="w", padx=14, pady=15)
    Tooltip(
        l_video_folder,
        text=settings[locale]["thumbview"]["videoFolder_hints"],
        wraplength=200,
    )

    e_video_folder = tk.Entry(left, textvariable=thumbView_video_folder)
    e_video_folder.grid(row=0, column=1, sticky="w", padx=14, pady=15)
    if thumbView_video_folder.get() != "":
        if tmp["lastfolder"] is None or tmp["lastfolder"] == "":
            pass
        else:
            if tmp["thumbView_video_folder"] is None:
                thumbView_video_folder.set(tmp["lastfolder"])
            thumbView_video_folder.set(tmp["thumbView_video_folder"])

    def e_video_folderCallBack(*args):
        print(f"we are dealing folder {thumbView_video_folder.get()}")
        tmp["thumbView_video_folder"] = thumbView_video_folder.get()

    thumbView_video_folder.trace("w", e_video_folderCallBack)

    b_video_folder = tk.Button(
        left,
        text=settings[locale]["thumbview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_tabview_video_folder(
                thumbView_video_folder, "thumbView_video_folder"
            )
        ).start(),
    )
    b_video_folder.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    b_open_video_folder = tk.Button(
        left,
        text=settings[locale]["thumbview"]["openlocalfolder"],
        command=lambda: threading.Thread(
            target=openLocal(thumbView_video_folder.get())
        ).start(),
    )
    b_open_video_folder.grid(row=0, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_open_video_folder,
        text=settings[locale]["thumbview"]["openlocalfolder_hints"],
        wraplength=200,
    )

    l_meta_format = tk.Label(
        left, text=settings[locale]["thumbview"]["l_metafileformat"]
    )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    Tooltip(
        l_meta_format,
        text=settings[locale]["thumbview"]["l_metafileformat_hints"],
        wraplength=200,
    )

    metafileformat = tk.StringVar()

    metafileformat.set(settings[locale]["thumbview"]["dropdown_hints"])

    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values=("json", "xlsx", "csv"))
    metafileformatbox.grid(row=1, column=1, sticky="w", padx=14, pady=15)

    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # analyse_video_meta_pair(thumbView_video_folder.get(),left,right,metafileformatbox.get(),isThumbView=True,isDesView=False,isTagsView=False,isScheduleView=False)

    print(f"right now metafileformatbox.get():{metafileformatbox.get()}")
    metafileformat.trace("w", metafileformatCallBack)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)
    b_download_meta_templates = tk.Button(
        left,
        text=settings[locale]["thumbview"]["b_downvideometafile"],
        command=lambda: threading.Thread(
            target=openLocal(thumbView_video_folder.get())
        ).start(),
    )
    b_download_meta_templates.grid(row=1, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_download_meta_templates,
        text=settings[locale]["thumbview"]["b_downvideometafile_hints"],
        wraplength=200,
    )

    b_video_folder_check = tk.Button(
        left,
        text=settings[locale]["thumbview"]["b_checkvideoassets"],
        command=lambda: threading.Thread(
            target=analyse_video_meta_pair(
                thumbView_video_folder.get(),
                left,
                right,
                metafileformatbox.get(),
                isThumbView=True,
                isDesView=False,
                isTagsView=False,
                isScheduleView=False,
            )
        ).start(),
    )
    b_video_folder_check.grid(row=2, column=0, sticky="w", padx=14, pady=15)
    Tooltip(
        b_video_folder_check,
        text=settings[locale]["thumbview"]["b_checkvideoassets_hints"],
        wraplength=200,
    )
    b_delete_folder_cache = tk.Button(
        left,
        text=settings[locale]["thumbview"]["b_regen"],
        command=lambda: threading.Thread(
            target=ultra[thumbView_video_folder].unlink()
        ).start(),
    )
    b_delete_folder_cache.grid(row=2, column=1, sticky="w", padx=14, pady=15)


def openXLSX(xlsxpath):
    if platform.system() == "Linux":
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'")

    elif platform.system() == "macos":
        os.system("open -a 'Microsoft Excel' 'path/file.xlsx'")
    else:
        os.system('start "excel" "C:\\path\\to\\myfile.xlsx"')


def rendersubmeta(
    frame,
    right_frame,
    folder,
    pairlabel,
    missingfilevar,
    missingmetavar,
    func,
    rowno,
    selectedMetafileformat,
):
    lb_video_submeta_pairs_counts = tk.Label(frame, text=pairlabel + " paired")
    lb_video_submeta_pairs_counts.grid(row=rowno, column=0, sticky="w", columnspan=1)
    Tooltip(
        lb_video_submeta_pairs_counts,
        text=f"if there is the same {pairlabel}filename  exist for video,we take it as paired",
        wraplength=200,
    )

    video_submeta_pairs_counts = ultra[folder][missingmetavar]

    lb_video_submeta_pairs_counts_value = tk.Label(
        frame, text=str(video_submeta_pairs_counts)
    )
    lb_video_submeta_pairs_counts_value.grid(row=rowno, column=0, sticky="e", padx=0)

    lb_video_submeta_missing_file_pairs_counts = tk.Label(frame, text="missing file")
    lb_video_submeta_missing_file_pairs_counts.grid(
        row=rowno, column=1, sticky="w", padx=50
    )
    Tooltip(
        lb_video_submeta_missing_file_pairs_counts,
        text=f"we detect whether there is  {pairlabel}  files with the same video filename in this folder",
        wraplength=200,
    )

    missing_video_submeta_file_pairs_counts = (
        ultra[folder]["videoCounts"] - ultra[folder][missingfilevar]
    )

    lb_missing_video_submeta_file_pairs_counts = tk.Label(
        frame, text=str(missing_video_submeta_file_pairs_counts)
    )
    lb_missing_video_submeta_file_pairs_counts.grid(row=rowno, column=1, sticky="e")

    lb_video_submeta_missing_meta_pairs_counts = tk.Label(frame, text="missing meta")
    lb_video_submeta_missing_meta_pairs_counts.grid(
        row=rowno, column=2, sticky="w", padx=50
    )
    Tooltip(
        lb_video_submeta_missing_meta_pairs_counts,
        text=f"we detect whether {pairlabel}  filed is  filled already in the video metafile",
        wraplength=200,
    )

    missing_video_submeta_meta_pairs_counts = (
        ultra[folder]["videoCounts"] - ultra[folder][missingmetavar]
    )

    lb_missing_video_submeta_meta_pairs_counts = tk.Label(
        frame, text=str(missing_video_submeta_meta_pairs_counts)
    )
    lb_missing_video_submeta_meta_pairs_counts.grid(row=rowno, column=2, sticky="e")

    label_str = "Gen"
    if missing_video_submeta_file_pairs_counts > 0:
        label_str = "Update"

    b_gen_submeta = tk.Button(
        frame,
        text=label_str,
        command=lambda: threading.Thread(
            target=func(right_frame, True, folder, selectedMetafileformat)
        ).start(),
    )
    b_gen_submeta.grid(row=rowno, column=3)
    Tooltip(
        b_gen_submeta, text=f"Click  to create {pairlabel} meta files", wraplength=200
    )


def render_video_folder_check_results(
    frame,
    right_frame,
    folder,
    isThumbView=True,
    isDesView=True,
    isTagsView=True,
    isScheduleView=True,
    selectedMetafileformat="json",
):
    lb_video_counts = tk.Label(
        frame, text=settings[locale]["metaview"]["videototalcounts"]
    )

    lb_video_counts.grid(row=3, column=0, sticky="w")

    lb_video_counts_value = tk.Label(frame, text=str(ultra[folder]["videoCounts"]))
    lb_video_counts_value.grid(row=3, column=1)

    if isThumbView == True:
        rendersubmeta(
            frame,
            right_frame,
            folder,
            "thumb",
            "thumbFileCounts",
            "thumbMetaCounts",
            render_thumb_gen,
            4,
            selectedMetafileformat,
        )

    if isDesView == True:
        rendersubmeta(
            frame,
            right_frame,
            folder,
            "des",
            "desFileCounts",
            "desMetaCounts",
            render_des_gen,
            5,
            selectedMetafileformat,
        )

    if isScheduleView == True:
        rendersubmeta(
            frame,
            right_frame,
            folder,
            "schedule",
            "scheduleFileCounts",
            "scheduleMetaCounts",
            render_schedule_gen,
            6,
            selectedMetafileformat,
        )
        tmp["schview_selectedMetafileformat"] = selectedMetafileformat

    if isTagsView:
        rendersubmeta(
            frame,
            right_frame,
            folder,
            "tags",
            "tagFileCounts",
            "tagMetaCounts",
            render_tag_gen,
            7,
            selectedMetafileformat,
        )

    # if isDesView==True and isScheduleView==True and isTagsView==True and isThumbView==True:
    #     rendersubmeta(frame,right_frame,folder,'meta','metaFileCounts','metaMetaCounts',render_update_meta,8,selectedMetafileformat)


def ValidateTagGenMetas(folder, mode_value, preferred_value, frame=None):
    passed = True
    print(f"start to validate tag gen metas,mode is {mode_value},{type(mode_value)}")
    logger.debug(f"start to validate tag gen metas")

    if mode_value and mode_value is not None:
        logger.debug(f"start to process mode : {mode_value},{type(mode_value)}")

        ultra[folder]["tag_gen_setting"]["mode"] = mode_value
        ultra[folder]["tag_gen_setting"]["preferred"] = preferred_value

        if mode_value == 1:
            logger.debug("in default we fill video tags with video filename")
        elif mode_value == 2:
            logger.debug(
                "summarize description from subtitles of video,this extension is not supported yet"
            )

        elif mode_value == 3:
            logger.debug(
                "summarize description from audio of video,this extension is not supported yet"
            )
        elif mode_value == 4:
            logger.debug("read description from .des .txt with same filename of video")
        elif mode_value == 5:
            logger.debug("it seems you want fill description of video by hands")

        else:
            logger.error(f"no valid mode:{mode_value}")
    else:
        logger.debug("mode value is none")
        passed = False
    print(f"passed is {passed}")

    if passed == True:
        logger.debug(f"tag gen validation passed is {passed}")

        lab = tk.Label(frame, text="validation passed, go to gen tag", bg="lightyellow")
        lab.grid(row=10, column=1, padx=14, pady=15, sticky="nw")
        lab.after(5000, lab.destroy)
        print(
            f'sync total video assets with tag gen video meta {ultra[folder]["videos"]}'
        )

        totaljson = os.path.join(folder, videoassetsfilename)

        if os.path.exists(totaljson):
            with open(totaljson, "w") as f:
                f.write(jsons.dumps(ultra[folder]))
        else:
            with open(totaljson, "a") as f:
                f.write(jsons.dumps(ultra[folder]))
    else:
        logger.debug(f"tag gen validation failed")
    return passed


def genTag(folder, mode_value, prefer_tags, frame=None):
    passed = ValidateTagGenMetas(folder, mode_value, prefer_tags, frame=None)

    print("read video meta")

    print("read tag gen settings")

    template_data = ultra[folder]["tag_gen_setting"]
    video_data = ultra[folder]["videos"]

    for video_id, video_info in video_data.items():
        print(f"tag gen -process video-start tag body {video_id}")

        logger.debug(f"tag gen -process video-start tag body {video_id}")

        if mode_value == 1:
            logger.debug(
                f"tag gen -process video-extract from video filename with # {video_id}"
            )

            ultra[folder]["videos"][video_id]["tags"] = ",".join(
                ultra[folder]["videos"][video_id]["video_filename"].split("#").pop(0)
            )
        elif mode_value == 2:
            logger.debug(
                f"tag gen -process video-gen from  rapidtags not supported yet {video_id}"
            )
        elif mode_value == 3:
            logger.debug(
                f"tag gen -process video-auto gen from category and video description, not supported yet {video_id}"
            )

        elif mode_value == 4:
            logger.debug(
                f"tag gen -process video-read from .tag file with  same video filename {video_id}"
            )
            print(
                f"tag gen -process video-read from .tag file with  same video filename {video_id}"
            )

            # ultra[folder]['videos'][video_id]['tags']=''
            for ext in supported_tag_exts:
                tagfilepath = os.path.join(folder, video_id + ext)
                if os.path.exists(tagfilepath):
                    with open(tagfilepath, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                        contents = "\r".join(lines)
                        contents = contents.replace("\n", "")
                        ultra[folder]["videos"][video_id]["tags"] = contents
                    logger.debug(
                        f"tag gen -set file content  to tag field:\r{tagfilepath}"
                    )

                else:
                    logger.debug(f"tag gen file broken {tagfilepath}")
                    print(f"tag gen file broken {tagfilepath}")

                ultra[folder]["videos"][video_id]["tags"]
        logger.debug(f"tag gen -process video-end tag body {video_id}")
        print(f"tag gen -process video-end tag body {video_id}")

        logger.debug(f"tag gen -process video  start with prefer_tags {video_id}")
        if prefer_tags and prefer_tags != "":
            ultra[folder]["videos"][video_id]["tags"] = (
                prefer_tags + "," + ultra[folder]["videos"][video_id]["tags"]
            )
        logger.debug(f"tag gen -process video  end with prefer_tags {video_id}")

    lab = tk.Label(
        frame,
        text="end to gen tagcription,run check video assets again to see what happens",
        bg="lightyellow",
    )
    lab.grid(row=10, column=1, padx=14, pady=15, sticky="nw")
    lab.after(5000, lab.destroy)
    print(f'sync total video assets with tag gen video meta {ultra[folder]["videos"]}')

    logger.debug("end to gen tagcription")
    logger.debug("start to sync tagcription meta to video meta file")

    dumpMetafiles(ultra[folder]["metafileformat"], folder)
    logger.debug("end to sync gen tagcription meta to video meta file")

    logger.debug("start to sync gen tagcription meta to video assets file")

    syncVideometa2assetsjson(ultra[folder]["metafileformat"], folder)
    logger.debug("end to sync gen tagcription meta to video assets file")


def ValidateDesGenMetas(
    folder, descriptionPrefix_value, mode_value, descriptionSuffix_value, frame=None
):
    passed = True
    print(f"start to validate des gen metas,mode is {mode_value},{type(mode_value)}")
    logger.debug(f"start to validate des gen metas")

    if mode_value and mode_value is not None:
        logger.debug(f"start to process mode : {mode_value},{type(mode_value)}")

        ultra[folder]["des_gen_setting"]["mode"] = mode_value
        ultra[folder]["des_gen_setting"]["descriptionPrefix"] = descriptionPrefix_value
        ultra[folder]["des_gen_setting"]["descriptionSuffix"] = descriptionSuffix_value

        if mode_value == 1:
            logger.debug("in default we fill video description with video filename")
        elif mode_value == 2:
            logger.debug(
                "summarize description from subtitles of video,this extension is not supported yet"
            )

        elif mode_value == 3:
            logger.debug(
                "summarize description from audio of video,this extension is not supported yet"
            )
        elif mode_value == 4:
            logger.debug("read description from .des .txt with same filename of video")
        elif mode_value == 5:
            logger.debug("it seems you want fill description of video by hands")

        else:
            logger.error(f"no valid mode:{mode_value}")
    else:
        logger.debug("mode value is none")
        passed = False
    print(f"passed is {passed}")

    if passed == True:
        logger.debug(f"des gen validation passed is {passed}")

        lab = tk.Label(frame, text="validation passed, go to gen des", bg="lightyellow")
        lab.grid(row=10, column=1, padx=14, pady=15, sticky="nw")
        lab.after(5000, lab.destroy)
        print(
            f'sync total video assets with des gen video meta {ultra[folder]["videos"]}'
        )

        totaljson = os.path.join(folder, videoassetsfilename)

        if os.path.exists(totaljson):
            with open(totaljson, "w") as f:
                f.write(jsons.dumps(ultra[folder]))
        else:
            with open(totaljson, "a") as f:
                f.write(jsons.dumps(ultra[folder]))
    else:
        logger.debug(f"des gen validation failed")
    return passed


def genDes(
    folder, descriptionPrefix_value, mode_value, descriptionSuffix_value, frame=None
):
    passed = ValidateDesGenMetas(
        folder, descriptionPrefix_value, mode_value, descriptionSuffix_value, frame=None
    )

    print("read video meta")

    print("read des gen settings")

    template_data = ultra[folder]["des_gen_setting"]
    video_data = ultra[folder]["videos"]

    for video_id, video_info in video_data.items():
        logger.debug(f"des gen -process video-start des body {video_id}")

        if mode_value == 4:
            ultra[folder]["videos"][video_id]["video_description"] = ""
            for ext in supported_des_exts:
                desfilepath = os.path.join(folder, video_id + ext)
                if os.path.exists(desfilepath):
                    with open(desfilepath, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                        contents = "\r".join(lines)
                        contents = contents.replace("\n", "")
                        ultra[folder]["videos"][video_id][
                            "video_description"
                        ] = contents
                    logger.debug(
                        f"des gen -set file content  to video_description field:\r{desfilepath}"
                    )

                else:
                    logger.debug(f"des gen file broken {desfilepath}")

                ultra[folder]["videos"][video_id]["video_description"]
        logger.debug(f"des gen -process video-end des body {video_id}")

        logger.debug(f"des gen -process video  start with suffix and prefix {video_id}")
        ultra[folder]["videos"][video_id]["video_description"] = (
            descriptionPrefix_value
            + ultra[folder]["videos"][video_id]["video_description"]
            + descriptionSuffix_value
        )
        logger.debug(f"des gen -process video  end with suffix and prefix {video_id}")

    lab = tk.Label(
        frame,
        text="end to gen description,run check video assets again to see what happens",
        bg="lightyellow",
    )
    lab.grid(row=10, column=1, padx=14, pady=15, sticky="nw")
    lab.after(5000, lab.destroy)
    print(f'sync total video assets with des gen video meta {ultra[folder]["videos"]}')

    logger.debug("end to gen description")
    logger.debug("start to sync description meta to video meta file")

    dumpMetafiles(ultra[folder]["metafileformat"], folder)
    logger.debug("end to sync gen description meta to video meta file")

    logger.debug("start to sync gen description meta to video assets file")

    syncVideometa2assetsjson(ultra[folder]["metafileformat"], folder)
    logger.debug("end to sync gen description meta to video assets file")


def render_des_gen(frame, isneed, folder, selectedMetafileformat="json"):
    if isneed == True:
        if len(frame.winfo_children()) > 0:
            for widget in frame.winfo_children():
                widget.destroy()

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky="nw")

        thumbmode = tk.IntVar()

        lab = tk.Label(
            new_canvas,
            text=settings[locale]["metaview"]["choosedespolicy"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")

        thumbmode1 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual"],
            variable=thumbmode,
            value=1,
            command=lambda: render_des_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode1.grid(row=1, column=1, padx=14, pady=15, sticky="nw")
        thumbmode2 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto"],
            variable=thumbmode,
            value=2,
            command=lambda: render_des_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode2.grid(row=2, column=1, padx=14, pady=15, sticky="nw")


def render_des_update_view(frame, folder, desmode, previous_frame=None):
    print("desmode", type(desmode.get()), desmode.get())

    if len(frame.winfo_children()) > 0:
        for widget in frame.winfo_children():
            widget.destroy()

    if desmode.get() == 1:
        lbl15 = tk.Label(
            frame, text=settings[locale]["metaview"]["choosetagpolicy_manual"]
        )
        lbl15.grid(row=0, column=0, padx=14, pady=15, sticky="w")

        lbl15 = tk.Label(
            frame, text="1.手动准备视频描述，填充到元数据对应字段即可，元数据格式支持xlsx json csv", wraplength=600
        )
        lbl15.grid(row=1, column=0, sticky="w")

        lbl15 = tk.Label(frame, text="2.\r", wraplength=600)
        lbl15.grid(row=2, column=0, sticky="w")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["editwithlocaleditor"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=5, column=0, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_check_metas_,
            text=settings[locale]["metaview"]["editwithlocaleditor_hints"],
            wraplength=200,
        )

        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=6, column=0, padx=14, pady=15, sticky="nswe")
            Tooltip(
                b_check_metas_,
                text=settings[locale]["metaview"]["editwithonline_hints"],
                wraplength=200,
            )
        b_open_video_folder = tk.Button(
            frame,
            text=settings[locale]["metaview"]["openlocalfolder"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_open_video_folder.grid(row=4, column=0, padx=14, pady=15, sticky="nswe")

        b_check_metas_ = tk.Button(
            frame,
            text="edit videometa",
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=7, column=0, padx=14, pady=15, sticky="nswe")

        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_des_gen(previous_frame, True, folder),
        )
        b_return.grid(row=8, column=0)

    else:
        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_des_gen(previous_frame, True, folder),
        )
        b_return.grid(row=0, column=1)

        mode = tk.IntVar()
        mode.set(1)

        lab = tk.Label(frame, text="Step1:请选择视频描述主体从何而来", bg="lightyellow", width=30)
        lab.grid(row=0, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        mode1 = tk.Radiobutton(frame, text="视频文件名称", variable=mode, value=1, command="")
        Tooltip(mode1, text="视频描述使用视频文件名称", wraplength=200)

        mode1.grid(row=1, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        mode2 = tk.Radiobutton(
            frame, text="视频字幕文件总结", variable=mode, value=2, command=""
        )
        Tooltip(mode2, text="利用字幕文件总结视频描述，字幕文件须与视频文件同名", wraplength=200)

        mode2.grid(row=1, column=1, columnspan=3, padx=14, pady=15, sticky="nw")
        mode3 = tk.Radiobutton(frame, text="视频音频总结", variable=mode, value=3, command="")
        Tooltip(mode2, text="利用视频音频部分总结视频描述", wraplength=200)

        mode3.grid(row=2, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        mode4 = tk.Radiobutton(
            frame, text="从视频描述文件中来", variable=mode, value=4, command=""
        )
        Tooltip(mode4, text="视频描述文件须与视频文件同名，后缀可以是.des", wraplength=200)

        mode4.grid(row=2, column=1, columnspan=3, padx=14, pady=15, sticky="nw")
        mode5 = tk.Radiobutton(frame, text="从元数据中来", variable=mode, value=5, command="")
        mode5.grid(row=3, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        Tooltip(mode5, text="视频描述文可后续在元数据文件中手动编辑", wraplength=200)

        lab_step2 = tk.Label(frame, text="Step2:是否使用统一前缀后缀", bg="lightyellow")
        lab_step2.grid(row=4, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(lab_step2, text="可以通过设置前缀 后缀模板批量标准化频道的视频描述", wraplength=200)

        descriptionPrefix = tk.StringVar()
        descriptionSuffix = tk.StringVar()

        l_preferdesprefix = tk.Label(frame, text=settings[locale]["descriptionPrefix"])
        l_preferdesprefix.grid(row=5, column=0, padx=14, pady=15, sticky="nw")
        e_preferdesprefix = tk.Entry(frame, width=55, textvariable=descriptionPrefix)
        e_preferdesprefix.grid(row=5, column=1, padx=14, pady=15, sticky="nw")
        Tooltip(
            l_preferdesprefix, text="add \r if you want line breaks", wraplength=200
        )

        l_preferdessuffix = tk.Label(frame, text=settings[locale]["descriptionSuffix"])
        l_preferdessuffix.grid(row=6, column=0, padx=14, pady=15, sticky="nw")
        e_preferdessuffix = tk.Entry(frame, width=55, textvariable=descriptionSuffix)
        e_preferdessuffix.grid(row=6, column=1, padx=14, pady=15, sticky="nw")
        Tooltip(
            l_preferdessuffix, text="add \r if you want line breaks", wraplength=200
        )

        lab = tk.Label(frame, text="Step3:请编辑视频元数据", bg="lightyellow", width=30)
        lab.grid(row=7, column=0, padx=14, pady=15, sticky="nw")

        b_check_metas_ = tk.Button(
            frame,
            text="edit videometa",
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=8, column=0, padx=14, pady=15, sticky="nswe")
        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=8, column=1, padx=14, pady=15, sticky="nswe")
            Tooltip(b_edit_thumb_metas,
                text=settings[locale]["metaview"]["editwithlocaleditor_hints"],
                wraplength=200,
            )
        b_open_video_folder = tk.Button(
            frame,
            text=settings[locale]["metaview"]["openlocalfolder"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_open_video_folder.grid(row=8, column=2, padx=14, pady=15, sticky="nswe")
        lab = tk.Label(frame, text="Step4:生成视频描述", bg="lightyellow", width=30)
        lab.grid(row=9, column=0, padx=14, pady=15, sticky="nw")

        b_update_metas_ = tk.Button(
            frame,
            text="validate meta",
            command=lambda: ValidateDesGenMetas(
                folder,
                descriptionPrefix.get(),
                mode.get(),
                descriptionSuffix.get(),
                frame,
            ),
        )
        b_update_metas_.grid(row=10, column=0, padx=14, pady=15, sticky="nswe")

        b_gen_thumb_ = tk.Button(
            frame,
            text="gen descriptions",
            command=lambda: genDes(
                folder,
                descriptionPrefix.get(),
                mode.get(),
                descriptionSuffix.get(),
                frame,
            ),
        )
        b_gen_thumb_.grid(row=11, column=0, padx=14, pady=15, sticky="nswe")

        b_check_metas_ = tk.Button(
            frame,
            text="check metajson",
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_check_metas_.grid(row=12, column=0, padx=14, pady=15, sticky="nswe")


def render_tag_gen(frame, isneed, folder, selectedMetafileformat="json"):
    if isneed == True:
        if len(frame.winfo_children()) > 0:
            for widget in frame.winfo_children():
                widget.destroy()

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky="nw")

        thumbmode = tk.IntVar()

        lab = tk.Label(
            new_canvas,
            text=settings[locale]["metaview"]["choosetagspolicy"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")

        thumbmode1 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual"],
            variable=thumbmode,
            value=1,
            command=lambda: render_tag_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode1.grid(row=1, column=1, padx=14, pady=15, sticky="nw")
        thumbmode2 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto"],
            variable=thumbmode,
            value=2,
            command=lambda: render_tag_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode2.grid(row=2, column=1, padx=14, pady=15, sticky="nw")


def render_tag_update_view(frame, folder, desmode, previous_frame=None):
    print("tagmode", type(desmode.get()), desmode.get())

    if len(frame.winfo_children()) > 0:
        for widget in frame.winfo_children():
            widget.destroy()

    if desmode.get() == 1:
        lbl15 = tk.Label(
            frame, text=settings[locale]["metaview"]["choosetagpolicy_manual"]
        )
        lbl15.grid(row=0, column=0, padx=14, pady=15, sticky="w")

        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_manual_options_1"],
            wraplength=600,
        )
        lbl15.grid(row=1, column=0, sticky="w")

        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_manual_options_2"],
            wraplength=600,
        )
        lbl15.grid(row=2, column=0, sticky="w")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["editwithlocaleditor"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=5, column=0, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_check_metas_,
            text=settings[locale]["metaview"]["editwithlocaleditor_hints"],
            wraplength=200,
        )

        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=6, column=0, padx=14, pady=15, sticky="nswe")
            Tooltip(
                b_check_metas_,
                text=settings[locale]["metaview"]["editwithonline_hints"],
                wraplength=200,
            )
        b_open_video_folder = tk.Button(
            frame,
            text=settings[locale]["metaview"]["openlocalfolder"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_open_video_folder.grid(row=4, column=0, padx=14, pady=15, sticky="nswe")

        # b_check_metas_=tk.Button(frame,text="edit videometa",command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        # b_check_metas_.grid(row = 7, column = 0, padx=14, pady=15,sticky='nswe')

        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_tag_gen(previous_frame, True, folder),
        )
        b_return.grid(row=8, column=0)

    else:
        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_tag_gen(previous_frame, True, folder),
        )
        b_return.grid(row=0, column=1)

        mode = tk.IntVar()
        mode.set(1)

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=0, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        mode1 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_1"],
            variable=mode,
            value=1,
            command="",
        )
        Tooltip(
            mode1,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_1_hints"],
            wraplength=200,
        )

        mode1.grid(row=1, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        mode2 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_2"],
            variable=mode,
            value=2,
            command="",
        )
        Tooltip(
            mode2,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_2_hints"],
            wraplength=200,
        )

        mode2.grid(row=1, column=1, columnspan=3, padx=14, pady=15, sticky="nw")
        mode3 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_3"],
            variable=mode,
            value=3,
            command="",
        )
        Tooltip(
            mode3,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_3_hints"],
            wraplength=200,
        )

        mode3.grid(row=2, column=0, columnspan=3, padx=14, pady=15, sticky="nw")
        mode4 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_4"],
            variable=mode,
            value=4,
            command="",
        )
        Tooltip(
            mode4,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_4_hints"],
            wraplength=200,
        )

        mode4.grid(row=2, column=1, columnspan=3, padx=14, pady=15, sticky="nw")

        lab_step2 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosetagpolicy_auto_options_prefertag"],
            bg="lightyellow",
        )
        lab_step2.grid(row=4, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(
            lab_step2,
            text=settings[locale]["metaview"][
                "choosetagpolicy_auto_options_prefertag_hints"
            ],
            wraplength=200,
        )

        preferTags = tk.StringVar()

        l_preferredTags = tk.Label(
            frame,
            text=settings[locale]["metaview"][
                "choosetagpolicy_auto_options_prefertag_label"
            ],
        )
        l_preferredTags.grid(row=5, column=0, padx=14, pady=15, sticky="nw")
        e_preferredTags = tk.Entry(frame, width=55, textvariable=preferTags)
        e_preferredTags.grid(row=5, column=1, padx=14, pady=15, sticky="nw")
        Tooltip(
            l_preferredTags,
            text=settings[locale]["metaview"][
                "choosetagpolicy_auto_options_prefertag_label_hints"
            ],
            wraplength=200,
        )

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["L_editvideometa"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=7, column=0, padx=14, pady=15, sticky="nw")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["editwithlocaleditor"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=8, column=0, padx=14, pady=15, sticky="nswe")
        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=8, column=1, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_edit_thumb_metas,
            text=settings[locale]["metaview"]["editwithlocaleditor_hints"],
            wraplength=200,
        )
        b_open_video_folder = tk.Button(
            frame,
            text=settings[locale]["metaview"]["openlocalfolder"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_open_video_folder.grid(row=8, column=2, padx=14, pady=15, sticky="nswe")
        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["L_gentags"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=9, column=0, padx=14, pady=15, sticky="nw")

        b_update_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["validateVideoMetas"],
            command=lambda: ValidateTagGenMetas(
                folder, mode.get(), preferTags.get(), frame
            ),
        )
        b_update_metas_.grid(row=10, column=0, padx=14, pady=15, sticky="nswe")

        b_gen_thumb_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["B_gentags"],
            command=lambda: genTag(folder, mode.get(), preferTags.get(), frame),
        )
        b_gen_thumb_.grid(row=11, column=0, padx=14, pady=15, sticky="nswe")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["b_checkvideometafile"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_check_metas_.grid(row=12, column=0, padx=14, pady=15, sticky="nswe")


def render_schedule_gen(frame, isneed, folder, selectedMetafileformat):
    if isneed == True:
        if len(frame.winfo_children()) > 0:
            for widget in frame.winfo_children():
                widget.destroy()

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky="nw")

        thumbmode = tk.IntVar()

        lab = tk.Label(
            new_canvas,
            text=settings[locale]["metaview"]["chooseschedulepolicy"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")

        thumbmode1 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual"],
            variable=thumbmode,
            value=1,
            command=lambda: render_schedule_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode1.grid(row=1, column=1, padx=14, pady=15, sticky="nw")
        thumbmode2 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto"],
            variable=thumbmode,
            value=2,
            command=lambda: render_schedule_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode2.grid(row=2, column=1, padx=14, pady=15, sticky="nw")


def render_schedule_update_view(frame, folder, thumbmode, previous_frame):
    def policyOptionCallBack(*args):
        schframe = ttk.Frame(frame)
        schframe.grid(row=7, column=0, sticky="nsew")

        # if mode.get() in [3,4,5]:

        l_dailycount = tk.Label(
            schframe, text=settings[locale]["metaview"]["dailyVideoLimit"]
        )
        Tooltip(
            l_dailycount,
            text=settings[locale]["metaview"]["dailyVideoLimit_hints"],
            wraplength=200,
        )

        l_releasehour = tk.Label(
            schframe, text=settings[locale]["metaview"]["releasehour"]
        )
        Tooltip(
            l_releasehour,
            text=settings[locale]["metaview"]["releasehour_hints"],
            wraplength=200,
        )

        releasehour.set(settings[locale]["metaview"]["default_release_hour"])

        e_releasehour = tk.Entry(schframe, width=55, textvariable=releasehour)

        Tooltip(
            e_releasehour,
            text=settings[locale]["metaview"]["default_release_hour_hints"],
            wraplength=200,
        )

        start_publish_date.set(1)

        l_start_publish_date = tk.Label(
            schframe, text=settings[locale]["metaview"]["offsetDays"]
        )
        Tooltip(
            l_start_publish_date,
            text=settings[locale]["metaview"]["offsetDays_hints"],
            wraplength=200,
        )

        e_start_publish_date = tk.Entry(
            schframe, width=55, textvariable=start_publish_date
        )

        releasedatehourbox = ttk.Combobox(schframe, textvariable=dailycount)

        def display_selected_item_index(event):
            print("index of this item is: {}\n".format(releasedatehourbox.current()))
            number = dailycount.get()
            if dailycount.get() in range(0, 21) == False:
                number = 1
                randomNreleasehour = settings[locale]["metaview"][
                    "default_release_hour"
                ]
            else:
                randomNreleasehour = ",".join(
                    random.sample(
                        settings[locale]["availableScheduleTimes"], int(number)
                    )
                )
            releasehour.set(randomNreleasehour)

        def OptionCallBack(*args):
            # print(variable.get())
            # print(releasedatehourbox.current())
            number = dailycount.get()
            print("current dailycount ")
            if dailycount.get() in range(0, 21) == False:
                number = 1
            randomNreleasehour = ",".join(
                random.sample(settings[locale]["availableScheduleTimes"], int(number))
            )
            releasehour.set(randomNreleasehour)

        dailycount.set(settings[locale]["metaview"]["dropdown_hints"])
        dailycount.trace("w", OptionCallBack)

        releasedatehourbox.config(values=list(range(1, 21)))
        releasedatehourbox.bind("<<ComboboxSelected>>", display_selected_item_index)

        # print(f'modeis {type(mode.get())} {mode.get()}')
        if mode.get() in [1, 2]:
            try:
                logger.debug(f"grid_remove hidden offset elements")

                l_dailycount.grid_remove()
                l_start_publish_date.grid_remove()
                e_start_publish_date.grid_remove()
                releasedatehourbox.grid_remove()
                l_releasehour.grid_remove()
                e_releasehour.grid_remove()

            except:
                pass

            try:
                logger.debug(f"grid_forget hidden offset elements")

                l_dailycount.grid_forget()
                l_start_publish_date.grid_forget()
                e_start_publish_date.grid_forget()
                releasedatehourbox.grid_forget()
                l_releasehour.grid_forget()
                e_releasehour.grid_forget()
                logger.debug(f"visible {l_dailycount.winfo_ismapped() }")

            except:
                pass

            try:
                logger.debug(f"destroy hidden offset elements")

                l_dailycount.destroy()
                l_start_publish_date.destroy()
                e_start_publish_date.destroy()
                releasedatehourbox.destroy()
                l_releasehour.destroy()
                e_releasehour.destroy()

            except:
                pass
        elif mode.get() in [3, 4, 5]:
            logger.debug(f"show offset elements")

            l_dailycount.grid(row=1, column=0, padx=14, pady=15, sticky="nswe")
            releasedatehourbox.grid(row=1, column=1, padx=10)

            l_releasehour.grid(row=2, column=0, padx=14, pady=15, sticky="nswe")
            e_releasehour.grid(row=2, column=1, padx=14, pady=15, sticky="nswe")

            l_start_publish_date.grid(row=0, column=0, padx=14, pady=15, sticky="nswe")
            e_start_publish_date.grid(row=0, column=1, padx=14, pady=15, sticky="nswe")

    if len(frame.winfo_children()) > 0:
        for widget in frame.winfo_children():
            widget.destroy()

    if thumbmode.get() == 1:
        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_manual_options"],
        )
        lbl15.grid(row=1, column=0, padx=14, pady=15, sticky="w")
        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_schedule_gen(previous_frame, True, folder),
        )
        b_return.grid(row=0, column=1, padx=14, pady=15, sticky="w")

        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_manual_options_1"],
            wraplength=600,
        )
        lbl15.grid(row=2, column=0, sticky="nswe")

        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_manual_options_2"],
            wraplength=600,
        )
        lbl15.grid(row=3, column=0, sticky="nswe")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["editwithlocaleditor"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=5, column=0, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_check_metas_,
            text="fill release date and hour fields in meta files",
            wraplength=200,
        )

        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=6, column=0, padx=14, pady=15, sticky="nswe")
            Tooltip(
                b_check_metas_,
                text=settings[locale]["metaview"]["editwithonline_hints"],
                wraplength=200,
            )

        b_open_video_folder = tk.Button(
            frame,
            text=settings[locale]["metaview"]["openlocalfolder"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_open_video_folder.grid(row=4, column=0, padx=14, pady=15, sticky="nswe")

        b_update_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["validateVideoMetas"],
            command="validate thumbpath is there",
        )
        b_update_metas_.grid(row=7, column=0, padx=14, pady=15, sticky="nswe")

    else:
        mode = tk.IntVar()
        mode.set(1)
        releasehour = tk.StringVar()
        dailycount = tk.StringVar(frame)
        start_publish_date = tk.StringVar()

        mode.trace_add("write", policyOptionCallBack)

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_auto_options"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")
        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_schedule_gen(previous_frame, True, folder),
        )
        b_return.grid(row=1, column=2, padx=14, pady=15, sticky="e")

        mode1 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_auto_options_1"],
            variable=mode,
            value=1,
            command=policyOptionCallBack,
        )
        Tooltip(
            mode1,
            text=settings[locale]["metaview"][
                "chooseschedulepolicy_auto_options_1_hints"
            ],
            wraplength=200,
        )

        mode1.grid(row=2, column=0, padx=14, pady=15, sticky="nw")
        mode2 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_auto_options_2"],
            variable=mode,
            value=2,
            command=policyOptionCallBack,
        )
        # mode2.configure(state = tk.DISABLED)
        Tooltip(
            mode2,
            text=settings[locale]["metaview"][
                "chooseschedulepolicy_auto_options_2_hints"
            ],
            wraplength=200,
        )

        mode2.grid(row=3, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(
            mode2,
            text=settings[locale]["metaview"][
                "chooseschedulepolicy_auto_options_2_hints"
            ],
            wraplength=200,
        )

        mode3 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_auto_options_3"],
            variable=mode,
            value=3,
            command=policyOptionCallBack,
        )
        mode3.grid(row=4, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(
            mode3,
            text=settings[locale]["metaview"][
                "chooseschedulepolicy_auto_options_3_hints"
            ],
            wraplength=200,
        )

        mode4 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_auto_options_4"],
            variable=mode,
            value=4,
            command=policyOptionCallBack,
        )
        mode4.grid(row=5, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(
            mode4,
            text=settings[locale]["metaview"][
                "chooseschedulepolicy_auto_options_4_hints"
            ],
            wraplength=200,
        )

        mode5 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["chooseschedulepolicy_auto_options_5"],
            variable=mode,
            value=5,
            command=policyOptionCallBack,
        )
        mode5.grid(row=6, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(
            mode5,
            text=settings[locale]["metaview"][
                "chooseschedulepolicy_auto_options_5_hints"
            ],
            wraplength=200,
        )

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["L_genschedule"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=9, column=0, padx=14, pady=15, sticky="nw")

        # b_update_metas_=tk.Button(frame,text="validate meta",command=lambda: ValidateThumbnailGenMetas(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_folder.get(),frame))
        # b_update_metas_.grid(row = 10, column = 0,  padx=14, pady=15,sticky='nswe')

        b_gen_thumb_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["B_genschedule"],
            command=lambda: genScheduleSLots(
                folder,
                mode.get(),
                start_publish_date.get(),
                dailycount.get(),
                releasehour.get(),
                frame,
            ),
        )
        b_gen_thumb_.grid(row=11, column=0, padx=14, pady=15, sticky="nswe")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["b_checkvideometafile"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_check_metas_.grid(row=12, column=0, padx=14, pady=15, sticky="nswe")


def genScheduleSLots(
    folder,
    mode_value,
    start_publish_date_value,
    dailycount_value,
    releasehour_value,
    frame,
):
    logger.debug("start to gen slots")
    publish_policy = [1, 2, 3, 4, 5].index(mode_value)
    # //0 -private 1-publish 2-schedule 3-Unlisted 4-public&premiere
    today = date.today()

    date_to_publish = datetime(today.year, today.month, today.day)
    default_hour_to_publish = settings[locale]["metaview"]["default_release_hour"]
    # if you want more delay ,just change 1 to other numbers to start from other days instead of tomorrow
    start_publish_date_value = int(start_publish_date_value)
    if "Select From policy" == dailycount_value:
        dailycount_value = 1
    dailycount_value = int(dailycount_value)
    metafilechanges = False
    if metafilechanges:
        # 检测缓存中的更新时间 和videometafile的修改时间进行比较，发生变化就同步
        selectedMetafileformat = tmp["schview_selectedMetafileformat"]
        syncVideometa2assetsjson(selectedMetafileformat, folder)
    video_data = ultra[folder]["videos"]
    counts = len(video_data)
    offsets = 0
    avalaibleslots = []
    releasehour_value = releasehour_value.strip()

    # text = "这是一个包含半角逗号,和全角逗号，的示例。"

    # 使用正则表达式搜索半角或全角逗号
    comma_pattern = re.compile(r"[,\uFF0C]")
    match = comma_pattern.search(releasehour_value)

    if match:
        print("字符串中包含半角或全角逗号。")
        releasehour_value = re.sub(r"[,\uFF0C]", ",", releasehour_value)
    if "," in releasehour_value:
        avalaibleslots = releasehour_value.split(",")
    else:
        avalaibleslots.append(releasehour_value)
    if dailycount_value == len(avalaibleslots):
        logger.debug("your daily count and time slot matchs")
    elif dailycount_value > len(avalaibleslots) and len(avalaibleslots) == 1:
        logger.debug(
            f"your daily count is{dailycount_value} time slot is {avalaibleslots},it appears you want to publish them at the same time"
        )
        for i in len(dailycount_value) - 1:
            avalaibleslots.append(avalaibleslots[0])
    elif dailycount_value > len(avalaibleslots) and len(avalaibleslots) > 1:
        logger.debug(
            f"your daily count is{dailycount_value} time slot is {avalaibleslots},it appears you want to random choose { dailycount_value -len(avalaibleslots)} slots for the missing"
        )
        randomslots = random.sample(
            settings[locale]["availableScheduleTimes"],
            dailycount_value - len(avalaibleslots),
        )
        avalaibleslots += randomslots
    elif dailycount_value < len(avalaibleslots):
        logger.debug(
            f"your daily count is{dailycount_value} time slot is {avalaibleslots},it appears you want to random choose { dailycount_value} slots from you specify: {avalaibleslots}  "
        )
        randomslots = random.sample(avalaibleslots, dailycount_value)
        avalaibleslots = randomslots
    tmpslots = avalaibleslots
    for video_id, video_info in video_data.items():
        if offsets == dailycount_value:
            offsets = 0
            tmpslots = avalaibleslots
        if video_info["publish_policy"] in [0, 1]:
            logger.debug(
                f"this video {video_id} is set to public or private without need to gen schedule"
            )
        else:
            if video_info["release_date"] == "":
                video_info["release_date"] = date_to_publish + timedelta(
                    days=start_publish_date_value + offsets
                )
                offsets += 1
                date_hour = random.choice(tmpslots)
                video_info["release_date_hour"] = date_hour
                logger.debug(
                    f"start to assign this video {video_id},{video_info['release_date']},{video_info['release_date_hour']} "
                )

                tmpslots.remove(date_hour)
            else:
                logger.debug(
                    f"this video {video_id} is assigned release date{video_info['release_date']},{video_info['release_date_hour']} "
                )

    logger.debug("sync slots to video metas")
    dumpMetafiles(selectedMetafileformat, folder)
    logger.debug("sync slots to video assets")
    logger.debug("sync slots to cache")
    lab = tk.Label(
        frame,
        text="assign schedules finished,you can check videometa",
        bg="lightyellow",
    )
    lab.grid(row=10, column=0, padx=14, pady=15, sticky="nw")
    lab.after(5000, lab.destroy)


def check_folder_thumb_bg(folder):
    supported_thumb_exts = [".jpeg", ".png", ".jpg", "webp"]
    bg_images = []
    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]

                    ext = os.path.splitext(entry.name)[1]
                    if ext in supported_thumb_exts:
                        filepath = os.path.join(r, filename + ext)
                        bg_images.append(filepath)
    if len(bg_images) == 0:
        logger.debug(
            f"please choose another bg folder,there is no image found:\n{folder}"
        )
    return bg_images


def check_fields_and_empty_values(data_dict, allowed_fields):
    for key, entry in data_dict.items():
        missing_fields = [
            field for field in allowed_fields if field not in entry.keys()
        ]

        if missing_fields:
            print(
                f"The following allowed fields are missing in entry {key}: {', '.join(missing_fields)}"
            )
            return False

        empty_fields = any(entry[field] == "" for field in allowed_fields)

        if empty_fields:
            print(
                f"There are empty values in one or more of the allowed fields in entry {key}."
            )
            return False

    return True


def ValidateThumbnailGenMetas(
    folder,
    thumbnail_template_file_path,
    mode_value,
    thummbnail_bg_folder_path,
    frame=None,
):
    passed = True
    bg_images = []
    if mode_value and mode_value is not None:
        ultra[folder]["thumb_gen_setting"]["mode"] = mode_value

        if mode_value == 1:
            logger.debug(
                "extract first frame of video,this extension is not supported yet"
            )
        elif mode_value == 2:
            logger.debug(
                "extract random key frame of video,this extension is not supported yet"
            )
        elif mode_value == 3:
            if (
                thumbnail_template_file_path is None
                or thumbnail_template_file_path == ""
            ):
                logger.error("please choose a thumbtemplate first")

            else:
                logger.debug(
                    f"start to load thumbnail gen setting json from::\r{thumbnail_template_file_path}"
                )

                if os.path.exists(thumbnail_template_file_path):
                    try:
                        # fp = open(thumbnail_template_file_path, 'r', encoding='utf-8')
                        # setting_json = fp.read()
                        setting = json.load(
                            open(thumbnail_template_file_path, "r", encoding="utf-8")
                        )
                        templateschema = {
                            "$schema": "http://json-schema.org/draft-04/schema#",
                            "type": "object",
                            "properties": {
                                "width": {"type": "integer"},
                                "height": {"type": "integer"},
                                "texts": {
                                    "type": "array",
                                    "items": [
                                        {
                                            "type": "object",
                                            "properties": {
                                                "textType": {"type": "string"},
                                                "fontFile": {"type": "string"},
                                                "x": {"type": "integer"},
                                                "y": {"type": "integer"},
                                                "width": {"type": "integer"},
                                                "height": {"type": "integer"},
                                                "topLeft": {"type": "string"},
                                                "topRight": {"type": "string"},
                                                "bottomLeft": {"type": "string"},
                                                "bottomRight": {"type": "string"},
                                                "fontSize": {"type": "integer"},
                                                "fontName": {"type": "string"},
                                                "gridSize": {"type": "integer"},
                                                "isdrawborder": {"type": "boolean"},
                                                "bordersize": {"type": "integer"},
                                                "bordercolor": {"type": "string"},
                                                "nearestGridSerialNumber": {
                                                    "type": "integer"
                                                },
                                                "fontcolor": {"type": "string"},
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
                                                "fontcolor",
                                            ],
                                        }
                                    ],
                                },
                            },
                            "required": ["width", "height", "texts"],
                        }

                        try:
                            logger.debug("start to validate template")
                            print(f"start to validate template:\r{setting}")

                            validate(setting, schema=templateschema)
                            #    validate template format ,contain videoID  contain text type ,hints for user to edit temporary
                            ultra[folder]["thumb_gen_setting"]["template"] = setting[
                                "texts"
                            ]
                            ultra[folder]["thumb_gen_setting"][
                                "result_image_width"
                            ] = setting["width"]
                            ultra[folder]["thumb_gen_setting"][
                                "result_image_height"
                            ] = setting["height"]
                            ultra[folder]["thumb_gen_setting"][
                                "template_path"
                            ] = thumbnail_template_file_path

                            logger.debug(f"validate thumbnail gen template passed")

                            logger.debug(
                                "start to validate metadata for thumbgen setting"
                            )
                            allowedTextTypes = []
                            for item in setting["texts"]:
                                allowedTextTypes.append(item["textType"])
                            df = None
                            if len(allowedTextTypes) == 0:
                                logger.error(
                                    "it seemed textType in the template is empty"
                                )
                                passed = False
                            else:
                                if ultra[folder]["metafileformat"] == "xlsx":
                                    df = pd.read_excel(
                                        os.path.join(folder, "videos-meta.xlsx"),
                                        index_col=[0],
                                    )
                                    df.replace("nan", "")

                                    dfdict = df.iterrows()
                                elif ultra[folder]["metafileformat"] == "json":
                                    df = pd.read_json(
                                        os.path.join(folder, "videos-meta.json")
                                    )
                                    df.replace("nan", "")

                                    dfdict = df.items()
                                elif ultra[folder]["metafileformat"] == "csv":
                                    df = pd.read_csv(
                                        os.path.join(folder, "videos-meta.csv"),
                                        index_col=[0],
                                    )
                                    df.replace("nan", "")

                                    dfdict = df.iterrows()

                                # List of allowed field names
                                print("reading video meta\r", df)

                                logger.debug(
                                    f"start to check {allowedTextTypes} defined in template"
                                )

                                # Check the data dictionary for allowed fields and empty values in each entry
                                for key, entry in dfdict:
                                    missing_fields = [
                                        field
                                        for field in allowedTextTypes
                                        if field not in entry.keys()
                                    ]

                                    if missing_fields:
                                        print(
                                            f"The following allowed fields are missing in entry {key}: {', '.join(missing_fields)}"
                                        )
                                        logger.error(
                                            f"{missing_fields} filed in defined in template,but not found in metafile,add a column named {missing_fields} in metafile"
                                        )

                                        passed = False

                                    else:
                                        for field in allowedTextTypes:
                                            value = entry[field]
                                            if (
                                                not value
                                                or pd.isna(value)
                                                or value == ""
                                            ):
                                                logger.error(
                                                    f"{field} value is empty in entry {key}."
                                                )
                                                passed = False

                                            else:
                                                logger.debug(
                                                    f"{field} value is {value} in entry {key}."
                                                )
                                                # ultra[folder]['videos'][key][field]=value
                            if passed == True:
                                logger.debug(
                                    "validate metadata for thumbgen setting passed"
                                )
                                if df is not None:
                                    logger.debug(
                                        "start to update user submited metafile to video assets"
                                    )
                                    # df.to_json()==str  直接赋值 这个key的值就是str 后面没法拿video的字段值
                                    # print('==1==',type(ultra[folder]['videos']))
                                    # print('==2==',ultra[folder]['videos'])

                                    # print('==3==',type(json.loads(df.to_json())))
                                    # print('==4==',json.loads(df.to_json()))
                                    new = UltraDict()
                                    tmpdict = None

                                    if ultra[folder]["metafileformat"] == "xlsx":
                                        tmpdict = json.loads(df.to_json(orient="index"))

                                    elif ultra[folder]["metafileformat"] == "json":
                                        tmpdict = json.loads(df.to_json())

                                    elif ultra[folder]["metafileformat"] == "csv":
                                        tmpdict = json.loads(df.to_json(orient="index"))

                                    for key in tmpdict.keys():
                                        new[key] = tmpdict[key]

                                    # new=json.loads(df.to_json())
                                    # 如果不先 new一个UltraDict 而是仅仅凭借json.loads(df.to_json() python 内置的dict类型直接赋值，就会出错
                                    # 奇怪的是这种方法不行，得像上面那样遍历每一个key 赋值以后才行
                                    try:
                                        ultra[folder]["videos"] = new
                                    except Exception as e:
                                        print(f"wohhha {e}")
                                    logger.debug(
                                        "update user submited metafile to video assets passed"
                                    )

                            else:
                                logger.error(
                                    "validate metadata for thumbgen setting failed"
                                )

                        except ValidationError as e:
                            logger.error(f"validate thumbnail gen template failed")

                            logger.error(
                                f"this thumb template json dont follow json schema format,check the error msg:\n{e}"
                            )
                            passed = False
                    except Exception as e:
                        logger.error(
                            f"this thumb template json can not be loaded and parsed,check the error msg:\n{e}"
                        )
                        passed = False
                else:
                    logger.error("template json is not found")
                    passed = False

                logger.debug("start to validate bg folder")

                if os.path.exists(thummbnail_bg_folder_path):
                    bg_images = check_folder_thumb_bg(thummbnail_bg_folder_path)
                    logger.debug(f"bg folder image list :{bg_images}")
                    if len(bg_images) > 0:
                        ultra[folder]["thumb_gen_setting"][
                            "bg_folder"
                        ] = thummbnail_bg_folder_path

                        ultra[folder]["thumb_gen_setting"][
                            "bg_folder_images"
                        ] = bg_images

                        for filename in ultra[folder]["filenames"]:
                            bgpath = random.choice(bg_images)
                            if (
                                ultra[folder]["videos"][filename][
                                    "thumbnail_local_path"
                                ]
                                is None
                            ):
                                ultra[folder]["videos"][filename][
                                    "thumbnail_local_path"
                                ] = []

                            if ultra[folder]["videos"][filename][
                                "thumbnail_local_path"
                            ] in [[], "[]"]:
                                ultra[folder]["videos"][filename][
                                    "thumbnail_bg_image_path"
                                ] = bgpath
                                logger.debug(
                                    f"Random assign bg:{bgpath} to  video:{filename}"
                                )

                            else:
                                logger.debug(
                                    f"{ultra[folder]['videos'][filename]} has got thumbnail setup:\r{ultra[folder]['videos'][filename]['thumbnail_local_path']}"
                                )

                        logger.debug("validate bg folder passed")

                    else:
                        logger.error("validate bg folder failed")
                        passed = False

                        logger.debug(
                            f"there is no images under {thummbnail_bg_folder_path}.please choose another folder"
                        )
                else:
                    logger.error("validate bg folder failed")

                    logger.error("please choose a valid thummbnail_bg_folder_path ")
                    passed = False
        else:
            logger.error(f"no valid mode:{mode_value}")

    else:
        logger.debug("mode value is none")
        passed = False
    print(f"passed is {passed}")
    if passed == True:
        lab = tk.Label(
            frame, text="validation passed, go to gen thumbnail", bg="lightyellow"
        )
        lab.grid(row=10, column=1, padx=14, pady=15, sticky="nw")
        lab.after(5000, lab.destroy)
        print(
            f'sync total video assets with thumb gen video meta {ultra[folder]["videos"]}'
        )

        totaljson = os.path.join(folder, videoassetsfilename)

        if os.path.exists(totaljson):
            with open(totaljson, "w") as f:
                f.write(jsons.dumps(ultra[folder]))
        else:
            with open(totaljson, "a") as f:
                f.write(jsons.dumps(ultra[folder]))
    else:
        print("pass failed")
    return passed


def openVideoMetaFile(folder):
    print(f"you choose metafile format is:{ultra[folder]['metafileformat']}")
    if ultra[folder]["metafileformat"]:
        openLocal(
            os.path.join(folder, "videos-meta." + ultra[folder]["metafileformat"])
        )
    else:
        logger.error(
            f"you dont choose a valid meta fileformat:{ultra[folder]['metafileformat']}"
        )


def genThumbnailFromTemplate(
    folder,
    thumbnail_template_file_path,
    mode_value,
    thummbnail_bg_folder_path,
    frame=None,
):
    passed = ValidateThumbnailGenMetas(
        folder,
        thumbnail_template_file_path,
        mode_value,
        thummbnail_bg_folder_path,
        frame,
    )

    print("read video meta")

    print("read thumb gen settings")

    template_data = validateSeting(ultra[folder]["thumb_gen_setting"])
    video_data = ultra[folder]["videos"]
    render_style = template_data.get("render_style")
    result_image_width = int(template_data.get("result_image_width"))
    result_image_height = int(template_data.get("result_image_height"))
    output_folder = folder
    for video_id, video_info in video_data.items():
        print("1", video_info)
        thumb_gen_setting = template_data.get("template", [])

        ext = ".png"
        dict_9_16 = {
            "xhs": "1080*1440px",
            "dy": "1080*1920px",
            "wx": "1080*1260px",
            "youtube": "1920*1080px",
            "tiktok": "1080*1920px",
        }
        dict_16_9 = {
            "xhs": "1440*1080px",
            "dy": "1080*608px",
            "wx": "1080*608px",
            "youtube": "1280*720px",
            "tiktok": "1080*608px",
        }
        # 如果想同时为一个视频生成多个平台的缩略图，需要准备不同尺寸的背景图，那么这些背景图读进来会放在bg_images，就不能用原来的随机分配一张到文件里了，
        # 在渲染的时候从bg_images里读取尺寸要求相同的背景图即可
        filename = video_id + ext
        # filename=video_id+"_"+str(result_image_width)+"x"+str(result_image_height)+ext
        outputpath = draw_text_on_image(
            video_info,
            thumb_gen_setting,
            result_image_width,
            result_image_height,
            render_style,
            output_folder,
            filename,
        )
        logger.debug("start to add new gen thum to video meta")
        print(
            f"before add thumb for video {video_id} is {video_data[video_id]['thumbnail_local_path']}"
        )
        print(
            "test===",
            type(video_data[video_id]["thumbnail_local_path"]),
            video_data[video_id]["thumbnail_local_path"],
        )
        if type(video_data[video_id]["thumbnail_local_path"]) == str:
            video_data[video_id]["thumbnail_local_path"] = eval(
                video_data[video_id]["thumbnail_local_path"]
            )
            video_data[video_id]["thumbnail_local_path"].append(outputpath)
        elif (
            video_data[video_id]["thumbnail_local_path"] is None
            or video_data[video_id]["thumbnail_local_path"] in ["", "[]"]
            or len(video_data[video_id]["thumbnail_local_path"]) == 0
        ):
            empt = [].append(outputpath)
            video_data[video_id]["thumbnail_local_path"] = str(empt)
        else:
            video_data[video_id]["thumbnail_local_path"].append(outputpath)

        print(
            f"after add thumb for video {video_id} is {video_data[video_id]['thumbnail_local_path']}"
        )

        if result_image_width > result_image_height:
            basedir = output_folder + os.sep + "16-9"
            os.makedirs(basedir, exist_ok=True)

            # 16:9 aspect ratio
            for key, value in dict_16_9.items():
                output_folder = basedir + os.sep + key
                os.makedirs(output_folder, exist_ok=True)
                filename = video_id + ext
                value = value.replace("px", "")
                result_image_width = value.split("*")[0]
                result_image_height = value.split("*")[-1]
                filename = video_id + "_" + value.replace("*", "x") + ext
                result_image_width = int(result_image_width)
                result_image_height = int(result_image_height)

                filepath = draw_text_on_image(
                    video_info,
                    thumb_gen_setting,
                    result_image_width,
                    result_image_height,
                    render_style,
                    output_folder,
                    filename,
                )
        else:
            # 9:16 aspect ratio
            basedir = output_folder + os.sep + "9-16"

            os.makedirs(basedir, exist_ok=True)
            for key, value in dict_9_16.items():
                output_folder = basedir + os.sep + key
                os.makedirs(output_folder, exist_ok=True)
                filename = video_id + ext
                value = value.replace("px", "")
                result_image_width = value.split("*")[0]
                result_image_height = value.split("*")[-1]
                filename = video_id + "_" + value.replace("*", "x") + ext
                result_image_width = int(result_image_width)
                result_image_height = int(result_image_height)

                filepath = draw_text_on_image(
                    video_info,
                    thumb_gen_setting,
                    result_image_width,
                    result_image_height,
                    render_style,
                    output_folder,
                    filename,
                )
    logger.debug("end to gen thumbnail")
    logger.debug("start to sync thumbnail meta to video meta file")

    dumpMetafiles(ultra[folder]["metafileformat"], folder)
    logger.debug("end to sync gen thumbnail meta to video meta file")

    logger.debug("start to sync gen thumbnail meta to video assets file")

    syncVideometa2assetsjson(ultra[folder]["metafileformat"], folder)
    logger.debug("end to sync gen thumbnail meta to video assets file")


def render_submeta_gen(frame, isneed, folder, func):
    if isneed == True:
        if len(frame.winfo_children()) > 0:
            for widget in frame.winfo_children():
                widget.destroy()

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky="nw")

        thumbmode = tk.IntVar()

        lab = tk.Label(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")

        thumbmode1 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual"],
            variable=thumbmode,
            value=1,
            command=lambda: func(new_canvas, folder, thumbmode, frame),
        )
        thumbmode1.grid(row=1, column=1, padx=14, pady=15, sticky="nw")
        thumbmode2 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto"],
            variable=thumbmode,
            value=2,
            command=lambda: func(new_canvas, folder, thumbmode, frame),
        )
        thumbmode2.grid(row=2, column=1, padx=14, pady=15, sticky="nw")


def render_thumb_gen(frame, isneed, folder, func):
    if isneed == True:
        if len(frame.winfo_children()) > 0:
            for widget in frame.winfo_children():
                widget.destroy()

        new_canvas = tk.Frame(frame)
        new_canvas.grid(row=2, column=0, pady=(5, 0), sticky="nw")

        thumbmode = tk.IntVar()

        lab = tk.Label(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")

        thumbmode1 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual"],
            variable=thumbmode,
            value=1,
            command=lambda: render_thumb_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode1.grid(row=1, column=1, padx=14, pady=15, sticky="nw")
        thumbmode2 = tk.Radiobutton(
            new_canvas,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto"],
            variable=thumbmode,
            value=2,
            command=lambda: render_thumb_update_view(
                new_canvas, folder, thumbmode, frame
            ),
        )
        thumbmode2.grid(row=2, column=1, padx=14, pady=15, sticky="nw")


def render_thumb_update_view(frame, folder, thumbmode, previous_frame=None):
    print("thumbmode", type(thumbmode.get()), thumbmode.get())
    chooseAccountsWindow = tk.Toplevel(frame)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title("Choose associated proxy")
    chooseAccountsWindow = frame
    if len(frame.winfo_children()) > 0:
        for widget in frame.winfo_children():
            widget.destroy()

    if thumbmode.get() == 1:
        lbl15 = tk.Label(
            frame, text=settings[locale]["metaview"]["choosethumbpolicy_manual_options"]
        )
        lbl15.grid(row=0, column=0, padx=14, pady=15, sticky="w")

        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual_options_1"],
            wraplength=600,
        )
        lbl15.grid(row=1, column=0, sticky="w")

        lbl15 = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosethumbpolicy_manual_options_2"],
            wraplength=600,
        )
        lbl15.grid(row=2, column=0, sticky="w")

        b_edit_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["editwithlocaleditor"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_edit_metas_.grid(row=6, column=0, padx=14, pady=15, sticky="nswe")
        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=5, column=0, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_edit_metas_,
            text=settings[locale]["metaview"]["editwithlocaleditor_hints"],
            wraplength=200,
        )
        b_open_video_folder = tk.Button(
            frame,
            text=settings[locale]["metaview"]["openlocalfolder"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_open_video_folder.grid(row=4, column=0, padx=14, pady=15, sticky="nswe")

        # b_update_metas_=tk.Button(frame,text=settings[locale]['metaview']['validateVideoMetas'],command=lambda: ValidateThumbnailGenMetas(folder,thumbnail_template_file.get(),mode.get(),thummbnail_bg_folder.get(),frame))

        # b_update_metas_.grid(row = 7, column = 0,  padx=14, pady=15,sticky='nswe')

        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_thumb_gen(previous_frame, True, folder),
        )
        b_return.grid(row=8, column=0)

    else:
        mode = tk.IntVar()
        mode.set(3)
        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto_options"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=1, column=0, padx=14, pady=15, sticky="nw")
        b_return = tk.Button(
            frame,
            text=settings[locale]["metaview"]["return"],
            command=lambda: render_thumb_gen(previous_frame, True, folder),
        )
        b_return.grid(row=1, column=1, padx=14, pady=15, sticky="e")
        mode1 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto_options_1"],
            variable=mode,
            value=1,
            command="",
        )
        mode1.configure(state=tk.DISABLED)
        Tooltip(mode1, text="you dont install this extension yet", wraplength=200)

        mode1.grid(row=2, column=0, padx=14, pady=15, sticky="nw")
        mode2 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto_options_2"],
            variable=mode,
            value=2,
            command="",
        )
        mode2.configure(state=tk.DISABLED)
        Tooltip(mode2, text="you dont install this extension yet", wraplength=200)

        mode2.grid(row=2, column=1, padx=14, pady=15, sticky="nw")
        mode3 = tk.Radiobutton(
            frame,
            text=settings[locale]["metaview"]["choosethumbpolicy_auto_options_3"],
            variable=mode,
            value=3,
            command="",
        )
        mode3.grid(row=3, column=0, padx=14, pady=15, sticky="nw")
        Tooltip(mode3, text="please select the bg image folder ", wraplength=200)

        thummbnail_bg_folder = tk.StringVar()
        b_thumbnail_bg_folder = tk.Button(
            frame,
            text="select",
            command=lambda: threading.Thread(
                target=select_folder(
                    ultra[folder]["thumb_gen_setting"]["bg_folder"],
                    thummbnail_bg_folder,
                )
            ).start(),
        )
        b_thumbnail_bg_folder.grid(row=4, column=1, padx=14, pady=15, sticky="nswe")
        e_thumbnail_bg_folder = tk.Entry(frame, textvariable=thummbnail_bg_folder)
        e_thumbnail_bg_folder.grid(row=4, column=0, padx=14, pady=15, sticky="nswe")

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"][
                "choosethumbpolicy_auto_options_template"
            ],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=5, column=0, padx=14, pady=15, sticky="nw")

        b_edit_thumb = tk.Button(
            frame,
            text=settings[locale]["metaview"]["createtemplatewithlocaleditor"],
            command=lambda: webbrowser.open_new(
                "file:///{base_dir}/template.html".format(base_dir=ROOT_DIR)
            ),
        )

        b_edit_thumb.grid(row=6, column=0, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_edit_thumb,
            text="figure out  heading,subheading,extra text position,font,fontclolor use editor.you can update the json manually to set heading,subheading,extra type,adjust font name and font file ,because fontcolor,fontsize is auto detected, it need to be verify.and set a default bg image for all the videos to use",
            wraplength=200,
        )

        thumbnail_template_file = tk.StringVar()

        b_thumbnail_template_file = tk.Button(
            frame,
            text="select",
            command=lambda: threading.Thread(
                target=select_file(
                    "select thumb template json file",
                    thumbnail_template_file,
                    ultra[folder]["thumb_gen_setting"]["template_path"],
                    "json",
                )
            ).start(),
        )
        b_thumbnail_template_file.grid(row=7, column=1, padx=14, pady=15, sticky="nswe")
        e_thumbnail_template_file = tk.Entry(
            frame, textvariable=thumbnail_template_file
        )
        e_thumbnail_template_file.grid(row=7, column=0, padx=14, pady=15, sticky="nswe")

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["L_editvideometa"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=8, column=0, padx=14, pady=15, sticky="nw")

        # b_check_metas_=tk.Button(frame,text=settings[locale]['metaview']['editwithlocaleditor'],command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start() )
        # b_check_metas_.grid(row = 8, column = 1, padx=14, pady=15,sticky='nswe')

        b_edit_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["editwithlocaleditor"],
            command=lambda: threading.Thread(target=openVideoMetaFile(folder)).start(),
        )
        b_edit_metas_.grid(row=9, column=0, padx=14, pady=15, sticky="nswe")
        if ultra[folder]["metafileformat"] == "json":
            b_edit_thumb_metas = tk.Button(
                frame,
                text=settings[locale]["metaview"]["editwithonline"],
                command=lambda: webbrowser.open_new("https://jsoncrack.com/editor"),
            )
            b_edit_thumb_metas.grid(row=9, column=1, padx=14, pady=15, sticky="nswe")
        Tooltip(
            b_edit_metas_,
            text=settings[locale]["metaview"]["editwithlocaleditor_hints"],
            wraplength=200,
        )
        # b_open_video_folder=tk.Button(frame,text=settings[locale]['metaview']['openlocalfolder'] ,command=lambda: threading.Thread(target=openLocal(folder)).start() )
        # b_open_video_folder.grid(row =8, column = 2, padx=14, pady=15,sticky='nswe')

        lab = tk.Label(
            frame,
            text=settings[locale]["metaview"]["L_genthumb"],
            bg="lightyellow",
            width=30,
        )
        lab.grid(row=10, column=0, padx=14, pady=15, sticky="nw")

        b_validate_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["validateVideoMetas"],
            command=lambda: ValidateThumbnailGenMetas(
                folder,
                thumbnail_template_file.get(),
                mode.get(),
                thummbnail_bg_folder.get(),
                frame,
            ),
        )

        b_validate_metas_.grid(row=11, column=0, padx=14, pady=15, sticky="nswe")

        b_gen_thumb_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["B_genthumb"],
            command=lambda: genThumbnailFromTemplate(
                folder,
                thumbnail_template_file.get(),
                mode.get(),
                thummbnail_bg_folder.get(),
                frame,
            ),
        )
        b_gen_thumb_.grid(row=11, column=1, padx=14, pady=15, sticky="nswe")

        b_check_metas_ = tk.Button(
            frame,
            text=settings[locale]["metaview"]["b_checkvideometafile"],
            command=lambda: threading.Thread(target=openLocal(folder)).start(),
        )
        b_check_metas_.grid(row=12, column=0, padx=14, pady=15, sticky="nswe")


def printValues(choices):
    for name, var in choices.items():
        print("%s: %s" % (name, var.get()))


def setEntry(str, var):
    var.set(str)


def chooseProxies(ttkframe, platform=None, accountLinkproxy=None):
    chooseAccountsWindow = tk.Toplevel(ttkframe)
    chooseAccountsWindow.geometry(window_size)
    chooseAccountsWindow.title("Choose associated proxy")

    def refreshproxyoption(*args):
        print("sync link proxy back")
        accountLinkproxy.set(proxy_var.get())

    proxy_var = tk.StringVar()
    lbl16 = tk.Label(chooseAccountsWindow, text="binded proxy")
    lbl16.grid(row=5, column=0, sticky=tk.W)
    txt16 = tk.Entry(
        chooseAccountsWindow,
        textvariable=proxy_var,
        width=int(int(window_size.split("x")[-1]) / 5),
    )
    txt16.grid(row=6, column=0, sticky=tk.W)
    proxy_var.trace("w", refreshproxyoption)

    proxyView(chooseAccountsWindow, mode="bind", linkProxy=proxy_var, platform=None)


def chooseProxies_listbox(ttkframe, username, parentchooseProxies):
    newWindow = tk.Toplevel(ttkframe)
    newWindow.geometry(window_size)

    newWindow.title("proxy selection")

    if username == "":
        username = "this user account"

    # label = tk.Label(newWindow,
    #             text = f"Select the proxies for {username} below : ",
    #             font = ("Times New Roman", 10),
    #             padx = 10, pady = 10)
    # # label.pack()
    # label.grid(row=0,column=0, sticky=tk.W)

    ttkframe = newWindow

    global city_user, country_user, proxyTags_user, proxyStatus_user, proxy_str
    city = tk.StringVar()
    state = tk.StringVar()
    network_type = tk.StringVar()
    country = tk.StringVar()
    proxyTags = tk.StringVar()

    lbl15 = tk.Label(ttkframe, text="by city.")
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0, column=0, sticky=tk.W)

    txt15 = tk.Entry(ttkframe, textvariable=city)
    txt15.insert(0, "Los")
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1, column=0, sticky=tk.W)

    l_state = tk.Label(ttkframe, text="by state.")
    l_state.grid(row=0, column=1, sticky=tk.W)
    e_state = tk.Entry(ttkframe, textvariable=state)
    e_state.insert(0, "LA")
    e_state.grid(row=1, column=1, sticky=tk.W)

    lbl16 = tk.Label(ttkframe, text="by country.")
    lbl16.grid(row=0, column=2, sticky=tk.W)
    txt16 = tk.Entry(ttkframe, textvariable=country)
    txt16.insert(0, "USA")
    txt16.grid(row=1, column=2, sticky=tk.W)

    l_networktype = tk.Label(ttkframe, text="by networktype.")
    l_networktype.grid(row=2, column=0, sticky=tk.W)
    e_networktype = tk.Entry(ttkframe, textvariable=network_type)
    e_networktype.insert(0, "resident")
    e_networktype.grid(row=3, column=0, sticky=tk.W)

    lb18 = tk.Label(ttkframe, text="by status.")
    lb18.grid(row=2, column=1, sticky=tk.W)
    lb17 = tk.Label(ttkframe, text="by tags.")
    lb17.grid(row=2, column=2, sticky=tk.W)
    txt17 = tk.Entry(ttkframe, textvariable=proxyTags)
    txt17.insert(0, "youtube")
    txt17.grid(row=3, column=2, sticky=tk.W)

    proxyStatus = tk.StringVar()
    proxy_str = tk.StringVar()

    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set("Select From Status")
    proxyStatus.trace("w", proxyStatusCallBack)

    proxyStatusbox = ttk.Combobox(ttkframe, textvariable=proxyStatus)
    proxyStatusbox.config(values=("valid", "invalid", "unchecked"))
    proxyStatusbox.grid(row=3, column=1, padx=14, pady=15)

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(newWindow)
    frame_canvas.grid(row=7, column=0, columnspan=20, sticky="nw", padx=14, pady=15)
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # for scrolling vertically
    # for scrolling vertically
    yscrollbar = tk.Scrollbar(frame_canvas)
    yscrollbar.pack(side=tk.RIGHT, fill="both")

    langlist = tk.Listbox(
        frame_canvas, selectmode="multiple", yscrollcommand=yscrollbar.set
    )
    langlist.pack(padx=10, pady=10, expand=tk.YES, fill="both")
    btn5 = tk.Button(
        ttkframe,
        text="Get proxy list",
        padx=0,
        pady=0,
        command=lambda: threading.Thread(
            target=queryProxies(
                logger,
                city.get(),
                state.get(),
                country.get(),
                proxyTags.get(),
                network_type.get(),
                proxyStatus.get(),
                ttkframe,
                tree=None,
                langlist=langlist,
            )
        ).start(),
    )
    btn5.grid(row=4, column=1, sticky=tk.W)

    btn5 = tk.Button(
        ttkframe,
        text="Reset",
        padx=0,
        pady=0,
        command=lambda: (
            proxyStatus.set(""),
            country.set(""),
            state.set(""),
            city.set(""),
            proxyTags.set(""),
            proxyStatus.set("Select From Status"),
            network_type.set(""),
        ),
    )
    btn5.grid(row=4, column=2, sticky=tk.W)

    btn6 = tk.Button(
        newWindow,
        text="remove selected",
        padx=10,
        pady=10,
        command=lambda: threading.Thread(target=remove_selected_row).start(),
    )
    btn6.grid(row=8, column=6, sticky=tk.W)
    lbl16 = tk.Label(newWindow, text="selected proxies")
    lbl16.grid(row=8, column=0, sticky=tk.W)
    txt16 = tk.Entry(
        newWindow,
        textvariable=proxy_str
        #  ,width=int(int(window_size.split('x')[-1])/4)
    )
    txt16.insert(0, "")
    txt16.grid(
        row=8,
        column=1,
        #    width=width,
        columnspan=4,
        #    rowspan=3,
        sticky="nswe",
    )

    tmp["accountaddproxies"] = {}

    def remove_selected_row():
        selected_accounts = tmp["accountaddproxies"]
        show_str = proxy_str.get()

        print("you want to remove these selected proxy", selected_accounts)
        if len(selected_accounts) == 0:
            showinfomsg(
                message="you have not selected  proxy at all.choose one or more"
            )

        else:
            existingaccounts = proxy_str.get().split(",")
            logger.debug(
                f"you want to remove this selected proxy {selected_accounts} from existing: {existingaccounts}"
            )

            for item in selected_accounts:
                if item in existingaccounts:
                    existingaccounts.remove(item)

                    logger.debug(f"this proxy {item} removed success")
                    showinfomsg(message=f"this proxy {item} removed success")
                else:
                    logger.debug(
                        f"you cannot remove this proxy {item}, not added before"
                    )
                    showinfomsg(message=f"this proxy {item} not added before")
            logger.debug(f"end to remove,reset proxystr {existingaccounts}")
            show_str = ",".join(
                item for item in existingaccounts if item is not None and item != ""
            )

        proxy_str.set(show_str)
        parentchooseProxies.set(show_str)

    def add_selected_accounts(event):
        listbox = event.widget
        values = [listbox.get(idx).split(":")[1] for idx in listbox.curselection()]

        tmp["accountaddproxies"] = values
        existingaccounts = proxy_str.get().split(",")
        show_str = proxy_str.get()
        if len(list(values)) == 0:
            logger.debug("you have not selected  proxiess at all.choose one or more")
            showinfomsg(
                message="you have not selected  proxiess at all.choose one or more"
            )

        elif values == existingaccounts:
            logger.debug("you have not selected new proxiess at all")
            showinfomsg(message="you have not selected new proxiess at all")

        else:
            for item in values:
                if item in existingaccounts:
                    logger.debug(f"this proxy {item} added before")
                    showinfomsg(message=f"this proxiess {item} added before")

                else:
                    existingaccounts.append(item)
                    logger.debug(f"this proxy {item} added successS")
                    showinfomsg(message=f"this proxy {item} added successS")

                    if show_str == "":
                        show_str = item
                    else:
                        show_str = show_str + "," + item

        proxy_str.set(show_str)
        parentchooseProxies.set(show_str)

    langlist.bind("<<ListboxSelect>>", add_selected_accounts)


def bulkImportUsers(frame):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # 缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0, 1), weight=1)

    newWindow.title("user bulk import")
    newWindow.grid_rowconfigure(0, weight=1)
    newWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    newWindow.grid_columnconfigure(1, weight=2)

    account_frame_left = tk.Frame(newWindow, height=height)
    account_frame_left.grid(row=0, column=0, sticky="nsew")
    account_frame_right = tk.Frame(newWindow, height=height)
    account_frame_right.grid(row=0, column=1, sticky="nsew")
    # accountView(account_frame_right)
    accountView(account_frame_right, mode="query", linkAccounts=None)

    ttkframe = account_frame_left

    lbl15 = tk.Label(ttkframe, text="input account info with \\n separator")
    lbl15.grid(row=0, column=0, sticky=tk.W)

    from tkinter.scrolledtext import ScrolledText

    textfield = ScrolledText(ttkframe, wrap=tk.WORD)
    textfield.grid(row=1, column=0, columnspan=5, padx=14, pady=15)
    textfield.bind_all("<Control-c>", _copy)
    accountfilepath = tk.StringVar()

    b_choose_proxy = tk.Button(
        ttkframe,
        text="load  from file",
        command=lambda: threading.Thread(
            target=select_file(
                "",
                variable=accountfilepath,
            )
        ).start(),
    )
    b_choose_proxy.grid(row=2, column=0, sticky=tk.W)

    b_save_user = tk.Button(
        ttkframe,
        text="save user",
        command=lambda: threading.Thread(
            target=bulksaveUser(accountfilepath.get())
        ).start(),
    )
    b_save_user.grid(row=10, column=0, columnspan=3, padx=14, pady=15)


def bulksaveUser(accountfilepath):
    print(accountfilepath)


def saveUser(platform, username, password, proxy, cookies, linkaccounts=None,profilepath=None):
    for v in [platform, username, password, proxy, linkaccounts]:
        if v == "" or len(v) == 0:
            v = None
    if platform is None:
        logger.error("please choose a platform")
        showinfomsg(message="please choose a platform first")
    else:
        platform = find_key(dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT), platform)
    if username is None:
        logger.error("please provide  a username")
        showinfomsg(message="please provide  a username")

    else:
        if password is None:
            logger.debug("you dont provide password")
            if cookies is None:
                logger.error("please provide a cookie file without  password")
                showinfomsg(message="please provide a cookie file without  password")

        # Define a list of proxy IDs associated with the account
        proxy_ids = proxy
        # [1, 2, 3]  # Replace with the actual IDs of the proxies

        # Serialize the list of proxy IDs to JSON
        # proxy_ids_json = json.dumps(proxy_ids)
        user_data = {
            "platform": platform,
            "username": username,
            "password": password,
            "cookie_local_path": cookies,
            "profile_local_path":profilepath,
            "proxy": proxy_ids,
        }
        # Create the user and associate the proxy IDs
        logger.debug(f"start to save user:\r{user_data}")
        print(f"start to save user:\r{user_data}")

        userid = AccountModel.add_account(user_data)

        if userid:
            print(f"check link account {type(linkaccounts)} {len(linkaccounts)}")
            if linkaccounts is None or len(linkaccounts) == 0:
                print(f"there is no backup account to be add at all")
                showinfomsg(message="this account added ok")

            else:
                accounts = eval(linkaccounts)
                for key, value in enumerate(accounts):
                    if len(value.split(",")) != 0:
                        for id in value.split(","):
                            r = AccountRelationship.add_AccountRelationship_by_username(
                                main_username=userid, otherusername=id
                            )
                            if r:
                                print(f"bind {id} to {username} as side account")
                                showinfomsg(message="this backup account added ok")
                            else:
                                showinfomsg(message="this backup account added failed")
        else:
            showinfomsg(message="this account added failed")


def find_key(input_dict, value):
    if type(input_dict) == list:
        input_dict = dict(input_dict)
    result = "None"
    for key, val in input_dict.items():
        if val == value:
            result = key
    return result


def newaccountView(frame):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # 缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0, 1), weight=1)

    newWindow.title(settings[locale]["newaccountview"]["title"])
    newWindow.grid_rowconfigure(0, weight=1)
    newWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    newWindow.grid_columnconfigure(1, weight=2)

    account_frame_left = tk.Frame(newWindow, height=height)
    account_frame_left.grid(row=0, column=0, sticky="nsew")
    account_frame_right = tk.Frame(newWindow, height=height)
    account_frame_right.grid(row=0, column=1, sticky="nsew")

    ttkframe = account_frame_left
    global proxy_option_account, channel_cookie_user

    channel_cookie_user = tk.StringVar()
    channel_profile_path=tk.StringVar()
    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()

    l_platform = tk.Label(
        ttkframe, text=settings[locale]["newaccountview"]["l_platform"]
    )
    # l_platform.place(x=10, y=90)
    l_platform.grid(row=0, column=0, columnspan=3, padx=14, pady=15)

    socialplatform = tk.StringVar()
    socialplatform_box = ttk.Combobox(ttkframe, textvariable=socialplatform)

    def socialplatformdb_values():
        platform_rows = PlatformModel.filter_platforms(
            name=None, ptype=None, server=None
        )

        platform_names = [
            dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows
        ]

        socialplatform_box["values"] = platform_names

    def socialplatformdb_refresh(event):
        socialplatform_box["values"] = socialplatformdb_values()

    socialplatform_box["values"] = socialplatformdb_values()

    def socialplatformOptionCallBack(*args):
        print(socialplatform.get())
        print(socialplatform_box.current())

    socialplatform.set(settings[locale]["newaccountview"]["l_platform_hints"])
    socialplatform.trace("w", socialplatformOptionCallBack)
    socialplatform_box.bind("<Button-1>", lambda event: socialplatformdb_refresh(event))

    # socialplatform_box.config(values =platform_names)
    socialplatform_box.grid(row=0, column=5, columnspan=3, padx=14, pady=15)

    l_username = tk.Label(ttkframe, text=settings[locale]["newaccountview"]["username"])
    # l_username.place(x=10, y=150)
    l_username.grid(row=2, column=0, columnspan=3, padx=14, pady=15)

    e_username = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=username)
    # e_username.place(x=10, y=180)
    e_username.grid(row=2, column=5, columnspan=3, padx=14, pady=15, sticky="w")

    l_password = tk.Label(ttkframe, text=settings[locale]["newaccountview"]["password"])
    e_password = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=password)

    l_password.grid(row=3, column=0, columnspan=3, padx=14, pady=15)
    e_password.grid(row=3, column=5, columnspan=3, padx=14, pady=15, sticky="w")

    linkAccounts = tk.StringVar()

    l_linkAccounts = tk.Label(
        ttkframe, text=settings[locale]["newaccountview"]["linkAccounts"]
    )
    e_linkAccounts = tk.Entry(
        ttkframe, width=int(width * 0.01), textvariable=linkAccounts
    )

    l_linkAccounts.grid(row=4, column=0, columnspan=3, padx=14, pady=15)
    e_linkAccounts.grid(row=4, column=5, columnspan=3, padx=14, pady=15, sticky="w")

    Tooltip(
        l_linkAccounts,
        text="if you want to associate any account as the backup accounts,query in the right and bind one",
        wraplength=200,
    )

    accountView(account_frame_right, mode="bind", linkAccounts=linkAccounts)

    # b_choose_account=tk.Button(ttkframe,text="Link",command=lambda: threading.Thread(target=lambda:chooseAccountsView(ttkframe,linkAccounts)).start() )

    # b_choose_account.grid(row = 4, column = 9, columnspan = 2, padx=14, pady=15)
    l_proxy_option = tk.Label(
        ttkframe, text=settings[locale]["newaccountview"]["proxy"]
    )

    l_proxy_option.grid(row=5, column=0, columnspan=3, padx=14, pady=15)

    e_proxy_option = tk.Entry(ttkframe, textvariable=proxy_option_account)
    e_proxy_option.grid(row=5, column=5, columnspan=3, padx=14, pady=15, sticky="w")

    b_choose_proxy = tk.Button(
        ttkframe,
        text=settings[locale]["newaccountview"]["proxylink"],
        command=lambda: threading.Thread(
            target=chooseProxies(
                ttkframe,
                platform=socialplatform.get(),
                accountLinkproxy=proxy_option_account,
            )
        ).start(),
    )

    b_choose_proxy.grid(row=5, column=9, columnspan=2, padx=14, pady=15)
    Tooltip(b_choose_proxy, text="if you want to use any proxy", wraplength=200)

    l_channel_cookie = tk.Label(
        ttkframe,
        text=settings[locale]["newaccountview"]["cookies"]
        # settings[locale]['select_cookie_file']
    )
    # l_channel_cookie.place(x=10, y=330)
    l_channel_cookie.grid(row=6, column=0, columnspan=3, padx=14, pady=15)

    e_channel_cookie = tk.Entry(ttkframe, textvariable=channel_cookie_user)
    # e_channel_cookie.place(x=10, y=360)
    e_channel_cookie.grid(row=6, column=5, columnspan=3, padx=14, pady=15, sticky="w")

    b_channel_cookie = tk.Button(
        ttkframe,
        text="Select",
        command=lambda: threading.Thread(
            target=select_file(
                "select cookie file for account", channel_cookie_user, cached=None,parent=newWindow
            )
        ).start(),
    )
    # b_channel_cookie.place(x=10, y=390)
    b_channel_cookie.grid(row=6, column=9, columnspan=2, padx=14, pady=15)

    b_channel_cookie_gen = tk.Button(
        ttkframe,
        text=settings[locale]["newaccountview"]["pullcookie"],
        command=lambda: threading.Thread(
            target=auto_gen_cookie_file(
                username.get(),
                password.get(),
                socialplatform.get(),
                proxy_option_account.get(),
                channel_cookie_user,
            )
        ).start(),
    )
    # b_channel_cookie_gen.place(x=100, y=390)
    b_channel_cookie_gen.grid(row=6, column=12, columnspan=2, padx=14, pady=15)


    l_channel_profile = tk.Label(
        ttkframe,
        text=settings[locale]["newaccountview"]["profilepath"]
        # settings[locale]['select_cookie_file']
    )
    # l_channel_profile.place(x=10, y=330)
    l_channel_profile.grid(row=7, column=0, columnspan=3, padx=14, pady=15)

    e_channel_profile = tk.Entry(ttkframe, textvariable=channel_profile_path)
    # e_channel_profile.place(x=10, y=360)
    e_channel_profile.grid(row=7, column=5, columnspan=3, padx=14, pady=15, sticky="w")

    b_channel_profile = tk.Button(
        ttkframe,
        text="Select",
        command=lambda: threading.Thread(
            target=select_file(
                "select cookie file for account", channel_profile_path, cached=None
            )
        ).start(),
    )
    # b_channel_profile.place(x=10, y=390)
    b_channel_profile.grid(row=7, column=9, columnspan=2, padx=14, pady=15)



    b_save_user = tk.Button(
        ttkframe,
        text=settings[locale]["newaccountview"]["save"],
        command=lambda: threading.Thread(
            target=saveUser(
                socialplatform.get(),
                username.get(),
                password.get(),
                proxy_option_account.get(),
                channel_cookie_user.get(),
                linkAccounts.get(),
                channel_profile_path.get()
            )
        ).start(),
    )
    b_save_user.grid(row=10, column=0, columnspan=3, padx=14, pady=15)


def accountView(frame, mode="query", linkAccounts=None):
    global q_username_account, latest_user_conditions_user, q_platform_account
    q_username_account = tk.StringVar()
    q_platform_account = tk.StringVar()

    query_frame = tk.Frame(frame, bd=1, relief=tk.FLAT)
    query_frame.grid(row=0, column=0, sticky="nswe")
    latest_user_conditions_user = tk.StringVar()
    lbl15 = tk.Label(query_frame, text=settings[locale]["accountview"]["q_username"])
    # lbl15.place(x=430, y=15, anchor=tk.NE)
    lbl15.grid(row=0, column=0, padx=14, pady=15, sticky="w")
    txt15 = tk.Entry(query_frame, width=11, textvariable=q_platform_account)
    txt15.insert(0, "")
    txt15.grid(row=1, column=0, padx=14, pady=15, sticky="w")

    lb18 = tk.Label(query_frame, text=settings[locale]["accountview"]["q_platform"])
    lb18.grid(row=0, column=1, sticky=tk.W)

    q_platform = tk.StringVar()
    q_platform_accountbox = ttk.Combobox(query_frame, textvariable=q_platform)

    def q_platformb_values():
        platform_rows = PlatformModel.filter_platforms(
            name=None, ptype=None, server=None
        )
        platform_names = [
            dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows
        ]

        q_platform_accountbox["values"] = platform_names

    def q_platformdb_refresh(event):
        q_platform_accountbox["values"] = q_platformb_values()

    q_platform_accountbox["values"] = q_platformb_values()

    def q_platformOptionCallBack(*args):
        print(q_platform.get())
        print(q_platform_accountbox.current())

    q_platform.set(settings[locale]["accountview"]["q_platform_hints"])
    q_platform.trace("w", q_platformOptionCallBack)

    q_platform_accountbox["values"] = q_platformb_values()

    q_platform_accountbox.bind("<Button-1>", lambda event: q_platformdb_refresh(event))
    q_platform_accountbox.grid(row=1, column=1, padx=14, pady=15, sticky="w")

    btn5 = tk.Button(
        query_frame,
        text=settings[locale]["accountview"]["reset"],
        padx=0,
        pady=0,
        command=lambda: (q_platform.set(""), q_platform_account.set("")),
    )
    btn5.grid(row=1, column=5, sticky=tk.W)

    operation_frame = tk.Frame(frame)
    operation_frame.grid(row=1, column=0, sticky="nswe")

    b_new_users = tk.Button(
        operation_frame,
        text=settings[locale]["accountview"]["new"],
        command=lambda: threading.Thread(target=newaccountView(frame)).start(),
    )
    b_new_users.grid(row=0, column=0, padx=14, pady=15)

    b_bulk_import_users = tk.Button(
        operation_frame,
        text=settings[locale]["accountview"]["bulkimport"],
        command=lambda: threading.Thread(target=bulkImportUsers(frame)).start(),
    )
    # b_bulk_import_users.place(x=10, y=450)
    b_bulk_import_users.grid(row=0, column=1, padx=14, pady=15)

    hints = "bulk pull sessionid and cookies"

    b_bulk_pull_cookies = tk.Button(
        operation_frame,
        text=settings[locale]["accountview"]["bulkimport_hints"],
        command=lambda: threading.Thread(target=bulkImportUsers(frame)).start(),
    )
    # b_bulk_import_users.place(x=10, y=450)
    b_bulk_pull_cookies.grid(row=0, column=2, padx=14, pady=15)

    result_frame = tk.Frame(frame, bd=1, relief=tk.FLAT)
    result_frame.grid(row=2, column=0, sticky="nswe")

    tab_headers = [
        "id",
        "platform",
        "username",
        "pass",
        "is_deleted",
        "proxy",
        "inserted_at",
    ]

    refreshAccountcanvas(canvas=None, frame=result_frame, headers=tab_headers, datas=[])

    btn5 = tk.Button(
        query_frame,
        text=settings[locale]["accountview"]["querynow"],
        command=lambda: queryAccounts(
            frame=result_frame,
            canvas=None,
            tab_headers=tab_headers,
            username=q_username_account.get(),
            platform=q_platform.get(),
            linkAccounts=linkAccounts,
            mode=mode,
        ),
    )

    btn5.grid(row=1, column=3, padx=14, pady=15)


def getBool(var):  # get rid of the event argument
    print(var.get())
    value = var.get()


def createTaskMetas(left, right):
    creatTaskWindow = tk.Toplevel(right)
    creatTaskWindow.geometry(window_size)

    username = tk.StringVar()

    # creatTaskWindow.focus_force()
    # creatTaskWindow.grab_set()

    creatTaskWindow.title(settings[locale]["newtaskview"]["title"])

    creatTaskWindow.grid_rowconfigure(0, weight=1)
    creatTaskWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    creatTaskWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    creatTaskWindow.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    creatTaskWindow.grid_columnconfigure(1, weight=2)

    account_frame_left = tk.Frame(creatTaskWindow, height=height)
    account_frame_left.grid(row=0, column=0, sticky="nsew")
    account_frame_right = tk.Frame(creatTaskWindow, height=height)
    account_frame_right.grid(row=0, column=1, sticky="nsew")

    if username == "":
        username = "this user account"

    label = tk.Label(
        account_frame_left,
        text=settings[locale]["newtaskview"]["instruction"],
        font=("Times New Roman", 10),
        padx=10,
        pady=10,
    )
    # label.pack()
    label.grid(row=0, column=0, sticky=tk.W)

    global videometafile, country_user, uploadsettingid, proxyStatus_user, choosedAccounts
    videometafile = tk.StringVar()
    uploadsettingid = tk.StringVar()
    choosedAccounts = tk.StringVar()
    global latest_proxy_conditions_user
    latest_proxy_conditions_user = tk.StringVar()
    lbl15 = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["L_loadvideometa"]
    )
    lbl15.grid(row=1, column=0, padx=14, pady=15, sticky=tk.W)

    txt15 = tk.Entry(account_frame_left, textvariable=videometafile)
    txt15.insert(0, "")
    b_thumbnail_template_file = tk.Button(
        account_frame_left,
        text=settings[locale]["newtaskview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_file(
                "select video meta  file", videometafile, "", "all", creatTaskWindow
            )
        ).start(),
    )
    b_thumbnail_template_file.grid(row=1, column=1, padx=14, pady=15, sticky="nswe")
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=2, column=1, sticky=tk.W)

    button1 = ttk.Button(
        account_frame_left,
        text=settings[locale]["newtaskview"]["B_startfromfolder"],
        command=lambda: (creatTaskWindow.withdraw(), tab_control.select(8)),
    )
    button1.grid(row=0, column=1, sticky=tk.W)

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

    lb17 = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["L_bindaccounts"]
    )
    lb17.grid(row=4, column=0, padx=14, pady=15, sticky=tk.W)
    txt17 = tk.Entry(account_frame_left, textvariable=choosedAccounts)
    txt17.insert(0, "")
    txt17.grid(row=5, column=1, sticky=tk.W)

    button1 = ttk.Button(
        account_frame_left,
        text=settings[locale]["newtaskview"]["B_bindaccounts"],
        command=lambda: chooseAccountsView(account_frame_right, choosedAccounts),
    )
    button1.grid(row=4, column=1, sticky=tk.W)

    multiAccountsPolicy = tk.StringVar()

    def multiAccountsPolicyCallBack(*args):
        print(multiAccountsPolicy.get())
        print(multiAccountsPolicybox.current())

    multiAccountsPolicy.set(settings[locale]["newtaskview"]["dropdown_hints"])
    multiAccountsPolicy.trace("w", multiAccountsPolicyCallBack)

    l_multiAccountsPolicybox = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["policy"]
    )
    l_multiAccountsPolicybox.grid(row=6, column=0, padx=14, pady=15, sticky=tk.W)

    multiAccountsPolicybox = ttk.Combobox(
        account_frame_left, textvariable=multiAccountsPolicy
    )
    policy_optionsvalues=list(dict(settings[locale]["newtaskview"]["policy_options"]).values())
    policy_optionsvalues=[ inner.strip() for inner in policy_optionsvalues]


    multiAccountsPolicybox.config(
        values=policy_optionsvalues)

    multiAccountsPolicybox.grid(row=6, column=1, padx=14, pady=15, sticky="w")

    lb18 = tk.Label(account_frame_left, text=settings[locale]["newtaskview"]["runson"])
    lb18.grid(row=7, column=0, padx=14, pady=15, sticky=tk.W)

    deviceType = tk.StringVar()
    browserType = tk.StringVar()

    def deviceTypeCallBack(*args):
        print(deviceType.get())
        print(deviceTypebox.current())
        if "browser" in deviceType.get():
            browserType.set(settings[locale]["newtaskview"]["dropdown_hints"])

            def browserTypeCallBack(*args):
                print(browserType.get())
                print(browserTypebox.current())

            browserType.trace("w", browserTypeCallBack)

            browserTypebox = ttk.Combobox(account_frame_left, textvariable=browserType)
            browserTypebox.config(
                values=settings[locale]["newtaskview"]["browser_options"].split(",")
            )
            browserTypebox.grid(row=8, column=1, padx=14, pady=15, sticky="w")

        else:
            showinfomsg(message="not supported yet")

    deviceType.set(settings[locale]["newtaskview"]["dropdown_hints"])
    deviceType.trace("w", deviceTypeCallBack)

    deviceTypebox = ttk.Combobox(account_frame_left, textvariable=deviceType)
    deviceTypebox.config(
        values=settings[locale]["newtaskview"]["devicetype_options"].split(",")
    )
    deviceTypebox.grid(row=7, column=1, padx=14, pady=15, sticky="w")

    is_open_browser = tk.BooleanVar()
    is_open_browser.set(True)
    is_open_browser.trace(
        "w", lambda *_: print("The value is_open_browser was changed")
    )
    l_is_open_browser = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["silent_mode"]
    )

    l_is_open_browser.grid(row=9, column=0, padx=14, pady=15, sticky="w")
    checkbutton = tk.Checkbutton(
        account_frame_left,
        text=settings[locale]["newtaskview"]["checkbuttonoption"],
        variable=is_open_browser,
        command=lambda: getBool(is_open_browser),
    )
    checkbutton.grid(row=9, column=1, padx=14, pady=15, sticky="w")

    is_debug = tk.BooleanVar()
    is_debug.set(True)
    l_is_debug = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["is_debug"]
    )
    is_debug.trace("w", lambda *_: print("The value is_debug was changed"))

    l_is_debug.grid(row=10, column=0, padx=14, pady=15, sticky="w")
    checkbutton = tk.Checkbutton(
        account_frame_left,
        text=settings[locale]["newtaskview"]["checkbuttonoption"],
        variable=is_debug,
        command=lambda: getBool(is_debug),
    )
    checkbutton.grid(row=10, column=1, padx=14, pady=15, sticky="w")

    is_record_video = tk.BooleanVar()
    is_record_video.set(True)
    is_record_video.trace(
        "w", lambda *_: print("The value is_record_video was changed")
    )

    l_is_record_video = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["is_record_video"]
    )
    l_is_record_video.grid(row=11, column=0, padx=14, pady=15, sticky="w")

    checkbutton = tk.Checkbutton(
        account_frame_left,
        text=settings[locale]["newtaskview"]["checkbuttonoption"],
        variable=is_record_video,
        command=lambda: getBool(is_record_video),
    )
    checkbutton.grid(row=11, column=1, padx=14, pady=15, sticky="w")

    wait_policy = tk.IntVar()
    wait_policy.set(3)
    l_wait_policy = tk.Label(
        account_frame_left, text=settings[locale]["newtaskview"]["wait_policy"]
    )
    wait_policy.trace("w", lambda *_: print("The value wait_policy was changed"))

    l_wait_policy.grid(row=12, column=0, padx=14, pady=15, sticky="w")
    mode0 = tk.Radiobutton(
        account_frame_left,
        text=settings[locale]["newtaskview"]["wait_policy_option1"],
        variable=wait_policy,
        value=1,
        command=lambda: getBool(wait_policy),
    )
    mode0.grid(row=12, column=1, padx=14, pady=15, sticky="w")
    mode1 = tk.Radiobutton(
        account_frame_left,
        text=settings[locale]["newtaskview"]["wait_policy_option2"],
        variable=wait_policy,
        value=2,
        command=lambda: getBool(wait_policy),
    )
    mode1.grid(row=13, column=1, padx=14, pady=15, sticky="w")
    mode1 = tk.Radiobutton(
        account_frame_left,
        text=settings[locale]["newtaskview"]["wait_policy_option3"],
        variable=wait_policy,
        value=3,
        command=lambda: getBool(wait_policy),
    )
    mode1.grid(row=14, column=1, padx=14, pady=15, sticky="w")
    btn6 = tk.Button(
        account_frame_left,
        text=settings[locale]["newtaskview"]["B_gentaskfile"],
        padx=10,
        pady=10,
        command=lambda: threading.Thread(
            target=genUploadTaskMetas(
                videometafile.get(),
                choosedAccounts.get(),
                multiAccountsPolicy.get(),
                deviceType.get(),
                browserType.get(),
                is_open_browser.get(),
                wait_policy.get(),
                is_debug.get(),
                is_record_video.get(),
                account_frame_left,
            )
        ).start(),
    )
    btn6.grid(row=15, column=1, sticky=tk.W)

    def uploadStrategyCallBack(*args):
        print(uploadStrategy.get())
        # print(uploadStrategybox.current())
        # if uploadStrategybox.current()==0 or uploadStrategy.get()=='单帐号' :
        #     pass

    uploadStrategy.trace("w", uploadStrategyCallBack)


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


def extends_accounts(accounts, videocount, mode="equal"):
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
    if mode == "equal":
        return extended_list2
    elif mode == "random":
        return [random.choice(accounts) for x in range(0, m)]
    else:
        print(f"mode:{mode} not supported yet")


def load_meta_file(filepath):
    videometafilepath = filepath
    if videometafilepath != "" and videometafilepath is not None:
        filename = os.path.splitext(videometafilepath)[0]
        folder = os.path.dirname(videometafilepath)
        ext = os.path.splitext(videometafilepath)[1].replace(".", "")
        logger.debug(f"you select video metafile is {videometafilepath}")
        if os.path.exists(videometafilepath):
            # check_video_thumb_pair(dbm,video_folder_path,True)
            logger.debug("start to load  and parse meta file")

            tmpdict = {}
            if ext == "xlsx":
                df = pd.read_excel(videometafilepath, index_col=[0])
                df.replace("nan", "")
                tmpdict = json.loads(df.to_json(orient="index"))

                dfdict = df.iterrows()
            elif ext == "json":
                df = pd.read_json(videometafilepath)
                df.replace("nan", "")
                tmpdict = json.loads(df.to_json())

                dfdict = df.items()
            elif ext == "csv":
                df = pd.read_csv(videometafilepath, index_col=[0])
                df.replace("nan", "")
                tmpdict = json.loads(df.to_json(orient="index"))

                dfdict = df.iterrows()
            return tmpdict
        else:
            logger.error(f"{filepath}is not not exist or broken")

            return None
    else:
        logger.error(f"{filepath}is not provide")
        return None


def genUploadTaskMetas(
    videometafilepath,
    choosedAccounts_value,
    multiAccountsPolicy_value,
    deviceType_value,
    browserType_value,
    is_open_browser_value,
    wait_policy_value,
    is_debug_value,
    is_record_video_value,
    frame,
):
    try:
        multiAccountsPolicy_value = find_key(
            settings[locale]["newtaskview"]["policy_options"], multiAccountsPolicy_value
        )
    except:
        multiAccountsPolicy_value = '2'
    # if multiAccountsPolicy_value=='单平台单账号':
    # # ('单平台单账号', '同平台主副账号','单平台多独立账号随机发布','单平台多独立账号平均发布'))
    #     multiAccountsPolicy_value=0
    # elif multiAccountsPolicy_value=='同平台主副账号':
    #     multiAccountsPolicy_value=1
    # elif multiAccountsPolicy_value=='单平台多独立账号独立发布':
    #     multiAccountsPolicy_value=2
    # elif multiAccountsPolicy_value=='单平台多独立账号平均发布':
    #     multiAccountsPolicy_value=3
    print("assign account", choosedAccounts_value)
    if choosedAccounts_value == "" or choosedAccounts_value is None:
        logger.debug("please choose which platform and account you want to upload ")
        showinfomsg(
            message="please choose which platform and account you want to upload ",
            parent=frame,
        )
        return
    else:
        try:
            choosedAccounts_value = eval(choosedAccounts_value)
            print("convert str to dict", choosedAccounts_value)

        except:
            logger.debug(f"please check {choosedAccounts_value} format")
            showinfomsg(
                message=f"please check {choosedAccounts_value} format", parent=frame
            )
            return

    print("load video meta")
    logger.debug("start to load video meta")

    if videometafilepath != "" and videometafilepath is not None:
        filename = os.path.splitext(videometafilepath)[0]
        folder = os.path.dirname(videometafilepath)
        ext = os.path.splitext(videometafilepath)[1].replace(".", "")

        if load_meta_file(videometafilepath):
            logger.debug("video meta file is ok")

            tmpdict = load_meta_file(videometafilepath)

            tmp["tasks"] = {}

            # Check the data dictionary for allowed fields and empty values in each entry
            videocounts = len(tmpdict)
            # multiAccountsPolicy_value  根据它来分配视频，
            taskno = 0

            for platform, accounts in choosedAccounts_value.items():
                if accounts == "":
                    accounts = []
                else:
                    if type(accounts) == str:
                        accounts = accounts.split(",")
                    accounts = [CustomID(custom_id=x).to_bin() for x in accounts]
                # 直接检测某平台下的账号数量，=1，默认情况 >1,看看策略
                tmpaccounts = []
                # ('单平台单账号', '单平台主副账号','单平台多账号随机发布','单平台多账号平均发布')
                # 如果存在主副账号，这个逻辑没想好，主副的区别是啥 副号的作用是啥 意味着两个账号发一模一样的视频，当然可以只是缩略图不同，随机进行测试
                # 那也就是说，针对平台下每一个账号进行检测，发现副号则自动新建一个视频任务

                # 多账号的意味着视频分摊到每个账号进行发布，发布的视频各不一样
                # 多账号下的账号意味着不管它存不存在副号，提交的账号独立对待。

                # accounts={'y1','y2','y3'}
                # 相当于5个账号
                # {'y1','y11'} {'y2'} {'y3','y31'}

                print(
                    f"start to process platform {platform}, accounts are:{accounts},{multiAccountsPolicy_value}"
                )

                if len(accounts) == 0:
                    logger.debug(
                        f"you dont choose any account for this platform:{platform}"
                    )
                else:
                    if multiAccountsPolicy_value == '0':
                        if len(accounts) == 0:
                            logger.debug(
                                f"you dont choose any account for this platform:{platform}"
                            )
                        tmpaccounts = extends_accounts(accounts, videocounts)
                        print("==单账号=", tmpaccounts)

                        for key, entry in tmpdict.items():
                            print("key", key)
                            print("entry", entry)
                            key = key + "_" + platform + "-" + str(taskno)
                            tmp["tasks"][key] = entry
                            tmp["tasks"][key]["timeout"] = 200
                            tmp["tasks"][key]["is_open_browser"] = is_open_browser_value
                            tmp["tasks"][key]["is_debug"] = is_debug_value
                            tmp["tasks"][key]["platform"] = platform
                            tmp["tasks"][key]["wait_policy"] = wait_policy_value
                            tmp["tasks"][key]["is_record_video"] = is_record_video_value
                            tmp["tasks"][key]["browser_type"] = browserType_value

                            data = AccountModel.get_account_by_id(id=accounts[0])
                            # print('data====',data[0],data[0].username)

                            tmp["tasks"][key]["account_id"] =CustomID(custom_id= data.id).to_hex()

                            tmp["tasks"][key]["username"] = data.username
                            logger.debug(
                                f"get credentials for this account {accounts[0]}"
                            )

                            tmp["tasks"][key]["password"] = data.password
                            tmp["tasks"][key]["proxy_option_id"] = data.proxy

                            if data.proxy:
                                proxyid=data.proxy
                                proxyid=CustomID(custom_id=proxyid).to_bin()
                                proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                                proxy_string=None
                                if proxy:

                                    proxy_string=(
                                                f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
                                                if proxy.proxy_username
                                                else f"{proxy.proxy_host}:{proxy.proxy_port}"
                                            )

                                    protocol=proxy.proxy_protocol
                                    http_proxy=f"{protocol}://{proxy_string}"
                                    https_proxy=f"{protocol}://{proxy_string}"
                                    tmp["tasks"][key]["proxy_option_string"] = http_proxy


                            tmp["tasks"][key][
                                "channel_cookie_path"
                            ] = data.cookie_local_path
                            taskno = +1

                    elif multiAccountsPolicy_value == '1':
                        print("遍历账号检查是否有副号，计算任务数量，分配视频")
                        # video={'1.mp4'}
                        # accounts={'y1'} {'y1','y11'}
                        for id_ in accounts:
                            r = AccountRelationship.get_AccountRelationship_by_username(
                                id=id_
                            )
                            if r is not None:
                                r.backup_account.id
                                # tmpaccounts.append([r.backup_account.id  for x in range(0,videocounts)]   )
                                # print('===',tmpaccounts)
                                for key, entry in tmpdict.items():
                                    print("key", key)
                                    print("entry", entry)
                                    print("taskno", taskno)

                                    key = key + "_" + platform + "-" + str(taskno)
                                    tmp["tasks"][key] = entry
                                    tmp["tasks"][key]["timeout"] = 200
                                    tmp["tasks"][key][
                                        "is_open_browser"
                                    ] = is_open_browser_value
                                    tmp["tasks"][key]["is_debug"] = is_debug_value
                                    tmp["tasks"][key]["platform"] = platform
                                    tmp["tasks"][key]["wait_policy"] = wait_policy_value
                                    tmp["tasks"][key][
                                        "is_record_video"
                                    ] = is_record_video_value
                                    tmp["tasks"][key][
                                        "browser_type"
                                    ] = browserType_value

                                    # account=r.backup_account.id
                                    # data=(AccountModel.filter_accounts(username=r.backup_account.username))[0]
                                    # print('data====',data[0],data[0].username)
                                    tmp["tasks"][key]["account_id"] = CustomID(
                                        custom_id=r.backup_account.id
                                    ).to_hex()

                                    tmp["tasks"][key][
                                        "username"
                                    ] = r.backup_account.username
                                    logger.debug(
                                        f"get credentials for this account {r.backup_account.username}"
                                    )

                                    tmp["tasks"][key][
                                        "password"
                                    ] = r.backup_account.password
                                    tmp["tasks"][key][
                                        "proxy_option"
                                    ] = r.backup_account.proxy
                                    tmp["tasks"][key][
                                        "channel_cookie_path"
                                    ] = r.backup_account.cookie_local_path
                                    taskno = +1

                            for key, entry in tmpdict.items():
                                print("key", key)
                                print("entry", entry)
                                print("taskno", taskno)

                                key = key + "_" + platform + "-" + str(taskno)
                                tmp["tasks"][key] = entry
                                tmp["tasks"][key]["timeout"] = 200
                                tmp["tasks"][key][
                                    "is_open_browser"
                                ] = is_open_browser_value
                                tmp["tasks"][key]["is_debug"] = is_debug_value
                                tmp["tasks"][key]["platform"] = platform
                                tmp["tasks"][key]["wait_policy"] = wait_policy_value
                                tmp["tasks"][key][
                                    "is_record_video"
                                ] = is_record_video_value
                                tmp["tasks"][key]["browser_type"] = browserType_value

                                data = AccountModel.get_account_by_id(id=id_)
                                # print('data====',data[0],data[0].username)
                                tmp["tasks"][key]["account_id"] =CustomID(custom_id= data.id).to_hex()

                                tmp["tasks"][key]["username"] = data.username
                                logger.debug(
                                    f"get credentials for this account {data.username}"
                                )

                                tmp["tasks"][key]["password"] = data.password
                                tmp["tasks"][key]["proxy_option_id"] = data.proxy

                                if data.proxy:
                                    proxyid=data.proxy
                                    proxyid=CustomID(custom_id=proxyid).to_bin()
                                    proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                                    proxy_string=None
                                    if proxy:

                                        proxy_string=(
                                                    f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
                                                    if proxy.proxy_username
                                                    else f"{proxy.proxy_host}:{proxy.proxy_port}"
                                                )

                                        protocol=proxy.proxy_protocol
                                        http_proxy=f"{protocol}://{proxy_string}"
                                        https_proxy=f"{protocol}://{proxy_string}"
                                        tmp["tasks"][key]["proxy_option_string"] = http_proxy


                                tmp["tasks"][key][
                                    "channel_cookie_path"
                                ] = data.cookie_local_path
                                taskno = +1

                    elif multiAccountsPolicy_value == '2':
                        print(
                            f"遍历账号，生成视频数量{len(tmpdict)}*账号数量{len(accounts)}的对应大小的账号数组"
                        )

                        accountids = accounts
                        videoids = tmpdict.keys()
                        from itertools import product

                        result = product(accountids, videoids)
                        print(list(result))
                        for index, entry in tmpdict.items():
                            print("video index:\n", index)
                            print("video entry:\n", entry)
                            print("taskno:\n", taskno)

                            key = index + "_" + platform + "-" + str(taskno)
                            tmp["tasks"][key] = entry
                            tmp["tasks"][key]["timeout"] = 200
                            tmp["tasks"][key]["is_open_browser"] = is_open_browser_value
                            tmp["tasks"][key]["is_debug"] = is_debug_value
                            tmp["tasks"][key]["platform"] = platform
                            tmp["tasks"][key]["wait_policy"] = wait_policy_value
                            tmp["tasks"][key]["is_record_video"] = is_record_video_value
                            tmp["tasks"][key]["browser_type"] = browserType_value
                            # account=tmpaccounts[taskno]
                            logger.debug(f'grab account data for {taskno},{type(taskno)} {tmpaccounts}')
                            data = AccountModel.get_account_by_id(id=tmpaccounts[taskno])
                            # print('data====',data[0],data[0].username)
                            tmp["tasks"][key]["account_id"] =CustomID(custom_id= data.id).to_hex()

                            tmp["tasks"][key]["username"] = data.username
                            logger.debug(f"get credentials for this account {data}")

                            tmp["tasks"][key]["password"] = data.password
                            tmp["tasks"][key]["proxy_option_id"] = data.proxy

                            if data.proxy:
                                proxyid=data.proxy
                                proxyid=CustomID(custom_id=proxyid).to_bin()
                                proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                                proxy_string=None
                                if proxy:

                                    proxy_string=(
                                                f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
                                                if proxy.proxy_username
                                                else f"{proxy.proxy_host}:{proxy.proxy_port}"
                                            )

                                    protocol=proxy.proxy_protocol
                                    http_proxy=f"{protocol}://{proxy_string}"
                                    https_proxy=f"{protocol}://{proxy_string}"
                                    tmp["tasks"][key]["proxy_option_string"] = http_proxy

                            tmp["tasks"][key][
                                "channel_cookie_path"
                            ] = data.cookie_local_path
                            taskno = +1

                    elif multiAccountsPolicy_value == '3':
                        print("遍历账号，生成视频数量对应大小的账号数组，平均分配")
                        if videocounts < len(accounts):
                            tmpaccounts = random.sample(accounts, videocounts)
                        else:
                            tmpaccounts = extends_accounts(
                                accounts, videocounts, mode="equal"
                            )
                        for key, entry in tmpdict.items():
                            print("key", key)
                            print("entry", entry)
                            key = key + "_" + platform + "-" + str(taskno)
                            tmp["tasks"][key] = entry
                            tmp["tasks"][key]["timeout"] = 200
                            tmp["tasks"][key]["is_open_browser"] = is_open_browser_value
                            tmp["tasks"][key]["is_debug"] = is_debug_value
                            tmp["tasks"][key]["platform"] = platform
                            tmp["tasks"][key]["wait_policy"] = wait_policy_value
                            tmp["tasks"][key]["is_record_video"] = is_record_video_value
                            tmp["tasks"][key]["browser_type"] = browserType_value

                            account = tmpaccounts[taskno]
                            data = AccountModel.get_account_by_id(id=account)
                            # print('data====',data[0],data[0].username)
                            tmp["tasks"][key]["account_id"] =CustomID(custom_id= data.id).to_hex()

                            tmp["tasks"][key]["username"] = data.username
                            logger.debug(f"get credentials for this account {account}")

                            tmp["tasks"][key]["password"] = data.password
                            tmp["tasks"][key]["proxy_option_id"] = data.proxy

                            if data.proxy:
                                proxyid=data.proxy
                                proxyid=CustomID(custom_id=proxyid).to_bin()
                                proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                                proxy_string=None
                                if proxy:

                                    proxy_string=(
                                                f"{proxy.proxy_username}:{proxy.proxy_password}@{proxy.proxy_host}:{proxy.proxy_port}"
                                                if proxy.proxy_username
                                                else f"{proxy.proxy_host}:{proxy.proxy_port}"
                                            )

                                    protocol=proxy.proxy_protocol
                                    http_proxy=f"{protocol}://{proxy_string}"
                                    https_proxy=f"{protocol}://{proxy_string}"
                                    tmp["tasks"][key]["proxy_option_string"] = http_proxy


                            tmp["tasks"][key][
                                "channel_cookie_path"
                            ] = data.cookie_local_path
                            taskno = +1
                    else:
                        print("coming soon ")

            logger.debug(f"start to save task meta success")
            print(f"task json:{tmp['tasks']}")

            dumpTaskMetafiles(ext, folder)

            showinfomsg(message=f"save task meta success", parent=frame)
        else:
            showinfomsg(message=f"load video meta failed", parent=frame)


def validateTaskMetafile(loop, frame, metafile, canvas=None):
    logger.debug("load task metas to database ")
    print("load task meta")

    taskids = []
    if metafile != "" and metafile is not None:
        logger.debug(f"you select task metafile is {metafile}")
        filename = os.path.splitext(metafile)[0]
        folder = os.path.dirname(metafile)
        ext = os.path.splitext(metafile)[1].replace(".", "")
        logger.debug("start to load  and parse meta file")

        if load_meta_file(metafile):
            data = load_meta_file(metafile)
            print("raw tasks", type(data), data)
            # data=eval(data)

            try:
                videos = data
                logger.debug(f"we found {len(videos)} videos to be load in db")
                showinfomsg(
                    message=f"we found {len(videos)} videos to be load in db",
                    DURATION=500,
                )

                for idx, video in videos.items():
                    logger.debug(f"video json is ,{type(video)},{video}")
                    logger.debug(
                        f"start to process uploadsetting related filed\n:{video} "
                    )
                    settingid = None

                    for key in ["proxy_option_id",'proxy_option_string', "channel_cookie_path",'profile_local_path']:
                        if video.get(key) == None:
                            logger.debug(
                                f" this field {key} is optional in given video json data"
                            )
                            # raise ValueError(f"this field {key} is required  in given data")

                    for key in [
                        "timeout",
                        "log_level",
                        "wait_policy",
                        "is_record_video",
                        "username",
                        "password",
                    ]:
                        if video.get(key) == None:
                            logger.debug(
                                f"no {key} filed provide in given video json data,we can use default value"
                            )
                    logger.debug(
                        f"start to validate browser_type:{video.get('browser_type')}"
                    )

                    if video.get("browser_type") == None:
                        video["browser_type"] = "firefox"
                        video["browser_type"] = 1
                        logger.debug("we use browser_type =firefox")

                    elif type(video.get("browser_type")) == int:
                        if video.get("browser_type") in range(
                            0, len(BROWSER_TYPE.BROWSER_TYPE_TEXT)
                        ):
                            pass
                        else:
                            logger.error(
                                f"browser_type should be one of {range(0,len(BROWSER_TYPE.BROWSER_TYPE_TEXT))}"
                            )
                    else:
                        try:
                            video["browser_type"] = getattr(
                                BROWSER_TYPE, video.get("browser_type").upper()
                            )
                        except:
                            if (
                                video["browser_type"]
                                in list(dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT).values())
                                == False
                            ):
                                logger.error(
                                    f"browser_type should be one of {dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT).values()}"
                                )
                            else:
                                video["browser_type"] = "firefox"
                                video["browser_type"] = 1
                                logger.debug("we use browser_type =firefox")

                    logger.debug(f"start to validate platform:{video.get('platform')}")
                    supported_platform = PlatformModel.filter_platforms(
                        name=None, ptype=None, server=None
                    )
                    supported_platform_names = [
                        dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type]
                        for x in supported_platform
                    ]
                    supported_platform_types = [x.type for x in supported_platform]
                    if len(supported_platform) == 0:
                        logger.error("please initialize supported_platform first")
                    if video.get("platform") == None:
                        video["platform"] = "youtube"
                        video["platform"] = 0
                        logger.debug(
                            "you dont specify platform field,we use default youtube"
                        )
                    elif type(video.get("platform")) == str:
                        platform_rows = PlatformModel.filter_platforms(
                            name=video.get("platform"), ptype=None, server=None
                        )
                        if len(platform_rows) > 0:
                            video["platform"] = platform_rows[0].type
                        else:
                            video["platform"] = 100
                            logger.error(
                                f"platform name is unknown,it should be one of {supported_platform_names} or {supported_platform_types} "
                            )

                    elif type(video.get("platform")) == int:
                        platform_rows = PlatformModel.filter_platforms(
                            name=None, ptype=video.get("platform"), server=None
                        )
                        video["platform"] = platform_rows[0].type
                        if len(platform_rows) > 0:
                            video["platform"] = platform_rows[0].type
                        else:
                            logger.error(
                                "platform should be one of {platform_names} or {platform_types} "
                            )

                    else:
                        logger.error(
                            "platform should be one of {platform_names} or {platform_types} "
                        )
                    logger.debug("start to validate timeout")

                    if video.get("timeout") == None:
                        video["timeout"] = 200000
                        logger.debug(
                            "you dont specify timeout field,we use default 200*1000"
                        )
                    else:
                        if type(video.get("timeout")) != int:
                            logger.error(
                                "timeout should be integer,such as 20*1000=20000, 20 seconds"
                            )
                    logger.debug("start to validate is_open_browser")

                    if video.get("is_open_browser") == None:
                        video["is_open_browser"] = True
                        logger.debug(
                            "you dont specify is_open_browser field,we use default True"
                        )

                    else:
                        if type(video.get("is_open_browser")) == bool:
                            pass
                        elif type(video.get("is_open_browser")) == str and video.get(
                            "is_open_browser"
                        ).lower() not in ["true", "false"]:
                            logger.error(
                                f'is_open_browser is {video.get("is_open_browser")} of {type(video.get("is_open_browser"))},it should be bool, true or false'
                            )
                    logger.debug(f"start to validate debug:{video.get('log_level')}")

                    if video.get("log_level") == None:
                        video["log_level"] = 10
                        logger.debug("you dont specify debug field,we use default True")

                    else:
                        if video.get("log_level") in list(dict(LOG_LEVEL.LOG_LEVEL_TEXT).values()):
                            video["log_level"] = video.get("log_level")
                        elif type(video.get("log_level")) == str:

                            video["log_level"] = find_key(dict(LOG_LEVEL.LOG_LEVEL_TEXT),video.get("log_level"))
                        else:
                            video["log_level"] = 10

                    if video.get("is_record_video") == None:
                        video["is_record_video"] = True
                        logger.debug(
                            "you dont specify is_record_video field,we use default True"
                        )

                    else:
                        if type(video.get("is_record_video")) == bool:
                            pass
                        elif type(video.get("is_record_video")) == str and video.get(
                            "is_record_video"
                        ).lower() not in ["true", "false"]:
                            logger.error(
                                f'is_record_video is {video.get("is_record_video")} of {type(video.get("is_record_video"))},it should be bool, true or false'
                            )
                    if video.get("wait_policy") == None:
                        video["wait_policy"] = 2
                        logger.debug(
                            "you dont specify wait_policy field,we use default 2"
                        )
                    else:
                        if type(video.get("wait_policy")) != int:
                            logger.error("wait_policy should be one of 0,1,2,3,4")
                            video["wait_policy"] = dict(
                                WAIT_POLICY_TYPE.WAIT_POLICY_TYPE_TEXT
                            )[video.get("wait_policy")]

                        else:
                            if not video.get("wait_policy") in [0, 1, 2, 3, 4]:
                                logger.error("wait_policy should be one of 0,1,2,3,4")
                    task_account = None
                    logger.debug('start to process account info')
                    if video.get("account_id") is None:
                        proxyid=None
                        logger.debug(f'there is no account_id set and try to save new account')
                        if video.get("proxy_option_id"):
                            proxyid=CustomID(custom_id=video.get("proxy_option_id")).to_bin()
                            proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                            if proxy is None:

                                if video.get("proxy_option_string"):
                                    proxy_string=video.get("proxy_option_string")
                                    logger.debug('validate proxy_option_string in this task')
                                    proxy_protocol_type, host, port, user, password = split_proxy(proxy_string)

                                    proxy_data = {
                                        "proxy_protocol": proxy_protocol_type,
                                        "proxy_provider_type": 0,
                                        "proxy_host": host,
                                        "proxy_port": port,
                                        "proxy_username": user,
                                        "proxy_password": password,
                                        # "ip_address": video.get("proxy_option_string"),
                                        # "country": video.get("proxy_country"),
                                        # "state": video.get("proxy_state"),
                                        # "city": video.get("proxy_city"),

                                        # "tags": video.get("proxy_tags"),
                                        "status": 2,
                                        "proxy_validate_network_type": None,
                                        "proxy_validate_server": None,
                                        "proxy_validate_results": None,
                                    }
                                    result = ProxyModel.add_proxy(proxy_data)
                                    proxyid=result.id
                                    logger.debug(f'save proxy to {result}')
                        user_data = {
                            "platform": video["platform"],
                            "username": video.get("username"),
                            "password": video.get("password"),
                            "cookie_local_path": video.get("channel_cookie_path"),
                            "profile_local_path": video.get("profile_local_path"),

                                "proxy": CustomID(custom_id=proxyid).to_hex()
                        }

                        task_account = AccountModel.add_account(account_data=user_data)
                        logger.debug(f'there is no account_id set and end to save new account:{task_account}')

                    else:
                        account_id = CustomID(
                            custom_id=video.get("account_id")
                        ).to_bin()

                        task_account = AccountModel.get_account_by_id(account_id)
                        logger.debug(f'detect account_id{task_account} whether exist in db ')
                        if task_account == None:
                            logger.debug(f" account_id:{video.get('account_id')} not exist and end to save new account:{task_account}")

                            proxyid=None
                            logger.debug(f'there is no account_id set and try to save new account')
                            if video.get("proxy_option_id"):
                                proxyid=CustomID(custom_id=video.get("proxy_option_id")).to_bin()
                                proxy=ProxyModel.get_proxy_by_id(id=proxyid)
                                if proxy is None:

                                    if video.get("proxy_option_string"):
                                        proxy_string=video.get("proxy_option_string")
                                        logger.debug('validate proxy_option_string in this task')
                                        proxy_protocol_type, host, port, user, password = split_proxy(proxy_string)

                                        proxy_data = {
                                            "proxy_protocol": proxy_protocol_type,
                                            "proxy_provider_type": 0,
                                            "proxy_host": host,
                                            "proxy_port": port,
                                            "proxy_username": user,
                                            "proxy_password": password,
                                            # "ip_address": video.get("proxy_option_string"),
                                            # "country": video.get("proxy_country"),
                                            # "state": video.get("proxy_state"),
                                            # "city": video.get("proxy_city"),

                                            # "tags": video.get("proxy_tags"),
                                            "status": 2,
                                            "proxy_validate_network_type": None,
                                            "proxy_validate_server": None,
                                            "proxy_validate_results": None,
                                        }
                                        logger.debug(f'try to save proxy_data to {proxy_data}')

                                        result = ProxyModel.add_proxy(proxy_data)
                                        proxyid=result.id
                                        logger.debug(f'save proxy to {proxyid}')


                            user_data = {
                                "platform": video["platform"],
                                "username": video.get("username"),
                                "password": video.get("password"),
                                "cookie_local_path": video.get("channel_cookie_path"),
                                "profile_local_path": video.get("profile_local_path"),

                                "proxy": CustomID(custom_id=proxyid).to_hex()
                            }


                            task_account = AccountModel.add_account(
                                account_data=user_data
                            )
                            video["account_id"] = task_account.id
                            logger.debug(f'update account_id to {task_account.id}')

                    logger.debug('end to process account info')

                    settingdata = {
                        "timeout": video.get("timeout"),
                        "is_open_browser": video.get("is_open_browser"),
                        "log_level": LOG_LEVEL.DEBUG,
                        "platform": video["platform"],
                        "browser_type": video.get("browser_type"),
                        "is_record_video": video.get("is_record_video"),
                        "wait_policy": video.get("wait_policy"),
                    }
                    logger.debug(f"start to process uploadsetting data {settingdata}")
                    tasksetting = None
                    if video.get("uploadsettingid") == None:
                        logger.debug(
                            f" save uploadsetting data:{settingdata}"
                        )

                        logger.debug("add to upload setting and return id for reuse")

                        tasksetting = UploadSettingModel.add_uploadsetting(
                            settingdata, video["account_id"]
                        )

                    else:
                        logger.debug(
                            f" if uploadsettingid is given,we can auto fill if  the other field is null "
                        )
                        setting_id = CustomID(
                            custom_id=video.get("uploadsettingid")
                        ).to_bin()

                        tasksetting = UploadSettingModel.get_uploadsetting_by_id(
                            id=setting_id
                        )
                        print("query id to pull setting, if not exist,create a new one")
                        if tasksetting == None:
                            tasksetting = UploadSettingModel.add_uploadsetting(
                                settingdata, task_account
                            )

                    logger.debug(f"end to process uploadsetting data")

                    logger.debug(f"start to process video related fields\n:{video} ")

                    for key in [
                        "video_local_path",
                        "video_title",
                        "video_description",
                        "thumbnail_local_path",
                        "publish_policy",
                        "tags",
                    ]:
                        if video.get(key) == None:
                            logger.error(
                                f"these {key} field is required,No target{key} in given video json data"
                            )
                            # raise ValueError(f"these {key} field is required,No target{key} in given video json data")
                        if key in ["video_local_path"]:
                            if os.path.exists(video.get(key)) == False:
                                logger.error(
                                    f"these {key} field is required,and check whether local file exists"
                                )
                                # raise ValueError(f"these {key} field is required,and check whether local file exists")
                                break
                        if key in ["thumbnail_local_path"]:
                            if type(video.get(key)) == list and len(video.get(key)) > 0:
                                if os.path.exists(video.get(key)[0]) == False:
                                    logger.error(
                                        f"these {key} field is required,and check whether local file exists"
                                    )
                                    # raise ValueError(f"these {key} field is required,and check whether local file exists")
                                    break

                            elif (
                                type(video.get(key)) == str and len(video.get(key)) > 0
                            ):
                                if os.path.exists(eval(video.get(key))[0]) == False:
                                    logger.error(
                                        f"these {key} field is required,and check whether local file exists"
                                    )
                                    # raise ValueError(f"these {key} field is required,and check whether local file exists")
                                    break

                            else:
                                logger.error(
                                    f"these {key} field is required,and check whether filed value is ok :{video.get(key)}"
                                )

                    for key in [
                        "video_film_date",
                        "video_film_location",
                        "first_comment",
                        "subtitles",
                    ]:
                        video[key] = None
                        logger.debug(f"now we have no rules about {key} validation ")

                    for key in [
                        "is_allow_embedding",
                        "is_publish_to_subscriptions_feed_notify",
                        "is_automatic_chapters",
                        "is_featured_place",
                        "is_not_for_kid",
                        "is_show_howmany_likes",
                        "is_monetization_allowed",
                    ]:
                        if video.get(key) == None:
                            video[key] = True
                            logger.debug(
                                f"This field {key} is optional in given video json data,we can use default true"
                            )
                        else:
                            if video.get(key) not in ["true", "false", True, False]:
                                logger.error(f"{key} should be bool, true or false")

                    for key in ["is_age_restriction", "is_paid_promotion"]:
                        if video.get(key) == None:
                            video[key] = False

                            logger.debug(
                                f"This field {key} is optional in given video json data,we can use default false"
                            )
                        else:
                            if video.get(key) not in ["true", "false", True, False]:
                                logger.error(f"{key} should be bool, true or false")

                    if video.get("categories") == None or video.get("categories") == "":
                        video["categories"] = None
                        logger.debug("we use categories =none")
                    else:
                        if type(video.get("categories")) != int:
                            logger.error("categories should be one of 0,1,....,14")
                        else:
                            if not video.get("categories") in range(0, 15):
                                logger.error(
                                    "categories should be one of 0,1,2,3..........,14"
                                )

                    if (
                        video.get("license_type") == None
                        or video.get("license_type") == ""
                    ):
                        video["license_type"] = 0
                        logger.debug("we use license_type =0")
                    else:
                        if type(video.get("license_type")) != int:
                            logger.error("license_type should be one of 0,1")
                        else:
                            if not video.get("license_type") in range(0, 2):
                                logger.error("license_type should be one of 0,1")
                    if video.get("shorts_remixing_type") == None:
                        video["shorts_remixing_type"] = 0
                        logger.debug("we use shorts_remixing_type =0")
                    else:
                        if type(video.get("shorts_remixing_type")) != int:
                            logger.error("shorts_remixing_type should be one of 0,1,2")
                        else:
                            if not video.get("shorts_remixing_type") in range(0, 3):
                                logger.error(
                                    "shorts_remixing_type should be one of 0,1,2"
                                )
                    if video.get("comments_ratings_policy") == None:
                        video["comments_ratings_policy"] = 1
                        logger.debug("we use comments_ratings_policy =1")
                    else:
                        if type(video.get("comments_ratings_policy")) != int:
                            logger.error(
                                "comments_ratings_policy should be one of 0,1,2,3,4,5"
                            )
                        else:
                            if not video.get("comments_ratings_policy") in range(0, 6):
                                logger.error(
                                    "comments_ratings_policy should be one of 0,1,2,3,4,5"
                                )

                    if video.get("captions_certification") == None:
                        video["captions_certification"] = 0
                        logger.debug("we use captions_certification =0")
                    else:
                        if type(video.get("captions_certification")) != int:
                            logger.error(
                                "captions_certification should be one of 0,1,2,3,4,5"
                            )
                        else:
                            if not video.get("captions_certification") in range(0, 6):
                                logger.error(
                                    "captions_certification should be one of 0,1,2,3,4,5"
                                )
                    if (
                        video.get("video_language") == None
                        or video.get("video_language") == ""
                    ):
                        video["video_language"] = None
                        logger.debug("we use video_language =none")
                    else:
                        if type(video.get("video_language")) != int:
                            logger.error(
                                "video_language should be one of 0,1,2,3,4...23"
                            )
                        else:
                            if not video.get("video_language") in range(0, 24):
                                logger.error(
                                    "video_language should be one of 0,1,2,3,4...23"
                                )

                    if video.get("publish_policy") == None:
                        video["publish_policy"] = 0
                        logger.debug("we use publish_policy =0")
                    else:
                        if type(video.get("publish_policy")) != int:
                            logger.error("publish_policy should be one of 0,1,2,3,4")
                        else:
                            if not video.get("publish_policy") in [0, 1, 2, 3, 4]:
                                logger.error(
                                    "publish_policy should be one of 0,1,2,3,4"
                                )
                            else:
                                # check release date and datehour exists
                                if video.get("publish_policy") == 2:
                                    if video.get("release_date") == None:
                                        video["release_date"] = None
                                        logger.debug("we use release_date ==none")
                                    else:
                                        if video.get("release_date_hour") == None:
                                            logger.debug(
                                                "we use default release_date_hour 10:15"
                                            )
                                        elif (
                                            video.get("release_date_hour")
                                            not in settings[locale][
                                                "availableScheduleTimes"
                                            ]
                                        ):
                                            logger.error(
                                                f"we use choose one from {settings[locale]['availableScheduleTimes']}"
                                            )
                    if video.get("prorioty") == None:
                        video["prorioty"] = False
                        logger.debug(f"we use prorioty ==False")
                    else:
                        if type(video.get("prorioty")) == bool:
                            pass
                        elif type(video.get("prorioty")) == str and video.get(
                            "prorioty"
                        ).lower() not in ["true", "false"]:
                            logger.error(
                                f'prorioty is {video.get("prorioty")} of {type(video.get("prorioty"))},it should be bool, true or false'
                            )

                    if video.get("release_date") == None:
                        nowdate = datetime.now()
                        video["release_date"] = nowdate
                        logger.debug(f"we use release_date =={nowdate }")
                    else:
                        if video.get("release_date_hour") == None:
                            video["release_date_hour"] = "10:15"
                            logger.debug("we use default release_date_hour 10:15")
                        elif (
                            video.get("release_date_hour")
                            not in settings[locale]["availableScheduleTimes"]
                        ):
                            logger.error(
                                f"we use choose one from {settings[locale]['availableScheduleTimes']}"
                            )
                    if video.get("release_date_hour") == None:
                        video["release_date_hour"] = "10:15"
                        logger.debug("we use default release_date_hour 10:15")
                    elif (
                        video.get("release_date_hour")
                        not in settings[locale]["availableScheduleTimes"]
                    ):
                        logger.error(
                            f"we use choose one from {settings[locale]['availableScheduleTimes']}"
                        )
                    if video.get("tags") == None:
                        video["tags"] = None
                        logger.debug("we use tags =[]")
                    else:
                        if type(video.get("tags")) == str and "," in video.get("tags"):
                            logger.debug(f'tags is ok:{video.get("tags")}')

                        else:
                            logger.error(
                                'tags should be a list of keywords such as "one,two" '
                            )
                    taskvideo = None
                    logger.debug(f"start to process video data")
                    print(
                        f"this is need to use which video model:{video.get('platform')}"
                    )
                    if video.get("platform") == "youtube" or video.get("platform") == 0:
                        videodata = {
                            "video_local_path": str(
                                PurePath(video["video_local_path"])
                            ),
                            "video_title": video["video_title"],
                            "video_description": video["video_description"],
                            "thumbnail_local_path": video["thumbnail_local_path"],
                            "publish_policy": video["publish_policy"],
                            "tags": video["tags"],
                        }
                        logger.debug(
                            f"start to save ytb video data {settingdata} to db"
                        )

                        taskvideo = YoutubeVideoModel.add_video(videodata)
                    else:
                        print(
                            f"we dont support yet to save video for: {video.get('platform')}"
                        )
                        videodata = {
                            "video_local_path": video["video_local_path"],
                            "video_title": video["video_title"],
                            "video_description": video["video_description"],
                            "thumbnail_local_path": video["thumbnail_local_path"],
                            "publish_policy": video["publish_policy"],
                            "tags": video["tags"],
                        }
                        logger.debug(
                            f"start to save ytb video data {settingdata} to db"
                        )
                        try:
                            taskvideo = YoutubeVideoModel.add_video(videodata)
                        except Exception as e:
                            logger.error(f'save taskvideo failed when validation:{e}')
                    logger.debug(f"end to process video data")

                    taskdata = {
                        "type": video["platform"],
                        "status": TASK_STATUS.PENDING,
                        "prorioty": video["prorioty"],
                    }
                    logger.debug(f"end to process video data")
                    logger.debug(f"start to process task data")

                    task = TaskModel.add_task(taskdata, taskvideo, tasksetting)
                    if task == None:
                        print(f"add task failure:{idx},{video}")

                    else:
                        print(f"add task success:{idx},{video}")
                        taskids.append(task.id)

                logger.debug(f"end to process task data")
                print("show added task in the tabular", taskids)
                try:
                    queryTasks(
                        loop,
                        frame=frame,
                        canvas=canvas,
                        tab_headers=None,
                        username=None,
                        platform=None,
                        status=None,
                        video_title=None,
                        schedule_at=None,
                        video_id=None,
                        pageno=1,
                        pagecount=50,
                        ids=taskids,
                        sortby="ASC",
                    )
                except Exception as e:
                    logger.error(f'queryTasks failed when after save task data:{e}')
                showinfomsg(message=f"end to process task data")

            except Exception as e:
                logger.error(
                    f"there is no videos in  your task meta file.check  docs for reference:{e}"
                )

        else:
            showinfomsg(message="please choose a valid task file")
            logger.error("you choosed task meta  file is missing or broken.")

    else:
        showinfomsg(message="please choose a valid task file")
        logger.error("you choosed task meta  file is missing or broken.")

async def cancerlall():
    try:
        tasks = asyncio.Task.all_tasks()
        pending = [task for task in tasks if not task.done()]
        for task in pending:
            task.cancel()
            try:
                async with asyncio.timeout(-1):
                    await task
            except asyncio.CancelledError:
                if asyncio.current_task().cancelling() == 0:
                    raise
                else:
                    return # this is the only non-exceptional return
            else:
                raise RuntimeError("Cancelled task did not end with an exception")
    except:
        print('there is no waiting task at all')
def uploadView(frame, ttkframe, lang, async_loop):
    queryframe = tk.Frame(ttkframe)
    # queryframe=frame
    queryframe.grid(row=0, column=0, sticky="w")
    queryframe.grid_rowconfigure((0, 1), weight=1)

    queryframe.grid_columnconfigure(0, weight=1)

    global vid, canvas

    taskstatus = tk.StringVar()
    lbl15 = tk.Label(queryframe, text=settings[locale]["uploadview"]["q_status"])
    lbl15.grid(row=0, column=0, sticky="w")

    task_status_var = tk.StringVar()
    task_status_var.set(settings[locale]["uploadview"]["dropdown_hints"])

    def task_status_db_values():
        task_status_names = dict(TASK_STATUS.TASK_STATUS_TEXT).values()

        task_status_combo["values"] = list(task_status_names)

    def task_status_db_refresh(event):
        task_status_combo["values"] = task_status_db_values()

    task_status_combo = ttk.Combobox(queryframe, textvariable=task_status_var)
    task_status_combo.grid(row=1, column=0, sticky=tk.W)
    task_status_combo.bind("<Button-1>", lambda event: task_status_db_refresh(event))
    task_status_combo["values"] = task_status_db_values()

    # Create a label for the platform dropdown
    platform_label = ttk.Label(
        queryframe, text=settings[locale]["uploadview"]["q_platform"]
    )
    platform_label.grid(row=0, column=3, sticky=tk.W)
    # Create a Combobox for the platform selection
    platform_var = tk.StringVar()
    platform_var.set(settings[locale]["uploadview"]["dropdown_hints"])

    def platform_db_values():
        platform_rows = PlatformModel.filter_platforms(
            name=None, ptype=None, server=None
        )
        platform_names = [
            dict(PLATFORM_TYPE.PLATFORM_TYPE_TEXT)[x.type] for x in platform_rows
        ]

        platform_combo["values"] = platform_names

    def platform_db_refresh(event):
        platform_combo["values"] = platform_db_values()

    platform_combo = ttk.Combobox(queryframe, textvariable=platform_var)
    platform_combo.grid(row=1, column=3, padx=10, pady=10, sticky=tk.W)
    platform_combo.bind("<Button-1>", lambda event: platform_db_refresh(event))
    platform_combo["values"] = platform_db_values()

    # platform_combo['values'] = db_values()
    vid = tk.StringVar()
    lbl15 = tk.Label(queryframe, text=settings[locale]["uploadview"]["q_videoid"])
    lbl15.grid(row=0, column=6, sticky="w")
    txt15 = tk.Entry(queryframe, textvariable=vid)
    txt15.insert(0, "input task id")
    txt15.grid(row=1, column=6, sticky="w", columnspan=2)

    vtitle = tk.StringVar()
    lbl15 = tk.Label(queryframe, text=settings[locale]["uploadview"]["q_videotitle"])
    lbl15.grid(row=0, column=9, sticky="w")
    txt15 = tk.Entry(queryframe, textvariable=vtitle)
    txt15.insert(0, "input task title")
    txt15.grid(row=1, column=9, sticky="w", columnspan=2)

    channelname = tk.StringVar()
    lbl16 = tk.Label(queryframe, text=settings[locale]["uploadview"]["q_channelname"])
    lbl16.grid(row=0, column=12, sticky="w")
    txt16 = tk.Entry(queryframe, textvariable=channelname)
    txt16.insert(0, "input channelname")
    txt16.grid(row=1, column=12, sticky="w", columnspan=2)

    schedule_at_var = tk.StringVar()
    lbl17 = tk.Label(queryframe, text=settings[locale]["uploadview"]["q_scheduledate"])
    lbl17.grid(row=0, column=15, sticky="w")
    txt17 = tk.Entry(queryframe, textvariable=schedule_at_var)
    txt17.insert(0, "input schedule date")
    txt17.grid(row=1, column=15, sticky="w", columnspan=2)

    sortby_var = tk.StringVar()
    sortby_var.set(settings[locale]["uploadview"]["dropdown_hints"])

    l_sortby = tk.Label(queryframe, text=settings[locale]["uploadview"]["q_Sortby"])
    l_sortby.grid(row=0, column=18, columnspan=1, sticky="w")

    sortby_combo = ttk.Combobox(queryframe, textvariable=sortby_var)
    sortby_combo.grid(row=1, column=18, columnspan=1, padx=10, pady=10, sticky=tk.W)
    # sortby_combo.bind('<Button-1>', lambda event: platform_db_refresh(event))
    sortby_combo["values"] = list(dict(SORT_BY_TYPE.SORT_BY_TYPE_TEXT).values())

    operationframe = tk.Frame(ttkframe)
    # queryframe=frame
    operationframe.grid(row=1, column=0, sticky="w")

    result_frame = tk.Frame(ttkframe, bd=1, relief=tk.FLAT)
    result_frame.grid(row=3, column=0, rowspan=5, sticky="nswe")

    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)
    result_frame.grid_columnconfigure(1, weight=1)

    b_create_task_metas = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["b_createTaskMetas"],
        command=lambda: threading.Thread(
            target=createTaskMetas(frame, ttkframe)
        ).start(),
    )
    b_create_task_metas.grid(row=0, column=0, padx=14, pady=15, sticky="w")
    Tooltip(
        b_create_task_metas, text=settings[locale]["t_createTaskMetas"], wraplength=200
    )

    b_down_video_metas_temp = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["b_editTaskMetas"],
        command=
        #  lambda: webbrowser.open_new("https://jsoncrack.com/editor")
        lambda: threading.Thread(
            target=webbrowser.open_new("https://jsoncrack.com/editor")
        ).start(),
    )
    b_down_video_metas_temp.grid(row=0, column=1, padx=14, pady=15, sticky="w")

    # l_import_task_metas = tk.Label(operationframe, text=settings[locale]['l_importTaskMetas'])
    # l_import_task_metas.grid(row = 0, column = 2, padx=14, pady=15,sticky='w')

    b_imported_video_metas_file = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["l_importTaskMetas"],
        command=lambda: select_file(title='import task file',cached="taskmetafilepath", variable=imported_task_metas_file,limited='all'),
    )
    b_imported_video_metas_file.grid(row=0, column=2, padx=14, pady=15)
    Tooltip(
        b_imported_video_metas_file,
        text=settings[locale]["uploadview"]["t_importTaskMetas"],
        wraplength=200,
    )

    imported_task_metas_file = tk.StringVar()
    e_imported_video_metas_file = tk.Entry(
        operationframe, width=int(width * 0.02), textvariable=imported_task_metas_file
    )
    e_imported_video_metas_file.grid(row=0, column=3, padx=14, pady=15)

    b_validate_video_metas = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["validateVideoMetas"],
        command=lambda: threading.Thread(
            target=validateTaskMetafile(
                loop, result_frame, imported_task_metas_file.get(), canvas=None
            )
        ).start(),
    )
    b_validate_video_metas.grid(row=0, column=5, padx=14, pady=15)

    # test upload  跳转到一个单独页面，录入一个视频的上传信息，点击上传进行测试。
    b_upload = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["testupload"],
        command=lambda: threading.Thread(
            target=testupload(DBM("test"), ttkframe)
        ).start(),
    )
    b_upload.grid(row=0, column=6, padx=14, pady=15)

    tab_headers = [
        "id",
        "platform",
        "prorioty",
        "username",
        "status",
        "schedule_at",
        "proxy",
        "video title",
        "uploaded_at",
        "inserted_at",
    ]
    tab_headers.append("operation")
    tab_headers.append("operation")
    tab_headers.append("operation")

    refreshTaskcanvas(
        async_loop, canvas=None, frame=result_frame, headers=tab_headers, datas=[]
    )

    print("First time render tab headers")

    btn5 = tk.Button(
        queryframe,
        text=settings[locale]["uploadview"]["querynow"],
        command=lambda: queryTasks(
            loop,
            canvas=None,
            frame=result_frame,
            status=task_status_var.get(),
            platform=platform_var.get(),
            username=channelname.get(),
            video_id=vid.get(),
            video_title=vtitle.get(),
            schedule_at=schedule_at_var.get(),
            pageno=1,
            pagecount=50,
            sortby=sortby_var.get(),
        ),
    )
    btn5.grid(row=1, column=21, padx=14, pady=15)

    btn5 = tk.Button(
        queryframe,
        text=settings[locale]["uploadview"]["reset"],
        padx=0,
        pady=0,
        command=lambda: (
            task_status_var.set(""),
            schedule_at_var.set(""),
            platform_var.set(""),
            channelname.set(""),
            vid.set(""),
            vtitle.set(""),
            sortby_var.set(""),
        ),
    )
    btn5.grid(row=1, column=24, sticky=tk.W)

    b_upload = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["b_uploadAll"],
        command=lambda: threading.Thread(
            target=do_ups(
                async_loop=async_loop,
                frame=result_frame,
                status=task_status_var.get(),
                platform=platform_var.get(),
                username=channelname.get(),
                vid=vid.get(),
                vtitle=vtitle.get(),
                schedule_at=schedule_at_var.get(),
                pageno=None,
                pagecount=50,
                sortby=sortby_var.get(),
            )
        ).start(),
    )
    b_upload.grid(row=0, column=7, padx=14, pady=15)

    # Modify the b_upload_cancelall button to call cancel_all_waiting_tasks
    b_upload_cancelall = tk.Button(
        operationframe,
        text=settings[locale]["uploadview"]["b_cancelAll"],
        command=lambda: threading.Thread(
            target=cancel_all_waiting_tasks(frame=result_frame)  # Pass the result_frame
        ).start(),
    )
    b_upload_cancelall.grid(row=0, column=8, padx=14, pady=15)

    # Bind the platform selection event to the on_platform_selected function


def pluginsView(frame, ttkframe, lang):
    plugins = ["youtube basic upload", ""]


def statsView(frame, ttkframe, lang):
    lb_youtube_counts = tk.Label(frame, text="youtube", font=(" ", 15))
    lb_youtube_counts.grid(row=2, column=0)

    lb_tiktok_counts = tk.Label(frame, text="tiktok", font=(" ", 15))
    lb_tiktok_counts.grid(row=3, column=0)

    lb_total_counts = tk.Label(frame, text="all", font=(" ", 15))
    lb_total_counts.grid(row=4, column=0)

    lb_account_counts = tk.Label(frame, text="account", font=(" ", 15))
    lb_account_counts.grid(row=1, column=1)

    lb_video_counts = tk.Label(frame, text="success", font=(" ", 15))
    lb_video_counts.grid(row=1, column=2)

    lb_video_queuedcounts = tk.Label(frame, text="queued", font=(" ", 15))
    lb_video_queuedcounts.grid(row=1, column=3)

    lb_video_failure_counts = tk.Label(frame, text="failure", font=(" ", 15))
    lb_video_failure_counts.grid(row=1, column=4)

    checkvideocounts = 0
    lb_youtube_success_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_youtube_success_counts_value.grid(row=2, column=1)

    lb_youtube_queued_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_youtube_queued_counts_value.grid(row=2, column=2)

    lb_youtube_failure_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_youtube_failure_counts_value.grid(row=2, column=3)

    lb_tiktok_success_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_tiktok_success_counts_value.grid(row=3, column=1)

    lb_tiktok_queued_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_tiktok_queued_counts_value.grid(row=3, column=2)

    lb_tiktok_failure_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_tiktok_failure_counts_value.grid(row=3, column=3)

    lb_total_success_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_total_success_counts_value.grid(row=4, column=1)

    lb_total_queued_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_total_queued_counts_value.grid(row=4, column=2)

    lb_total_failure_counts_value = tk.Label(
        frame, text=str(checkvideocounts), font=(" ", 18)
    )
    lb_total_failure_counts_value.grid(row=4, column=3)


def split_proxy(proxy_string):
    # Remove the protocol (e.g., "socks5://")
    if (
        proxy_string.startswith("socks5://")
        or proxy_string.startswith("http://")
        or proxy_string.startswith("https://")
    ):
        # proxy_string=proxy_string.replace('socks5://','').replace('http://','').replace('https://','')
        # Split the components using ":"
        components = proxy_string.split(":")

        # Extract the components
        proxy_protocol_type = components[0]
        host = components[1].replace("//", "")
        port = components[2]
        user = components[3] if len(components) > 3 else None
        password = components[4] if len(components) > 4 and user is not None else None

        return proxy_protocol_type, host, port, user, password

    else:
        return None


def saveBulkproxies(proxies_list_raw, logger):
    proxies_list = []
    if (
        "proxy list should be one proxy oneline,and each proxy in such format"
        in proxies_list_raw
    ):
        proxies_list_raw = proxies_list_raw.replace(
            "proxy list should be one proxy oneline,and each proxy in such format:", ""
        )
    if proxies_list_raw:
        proxies_list = proxies_list_raw.split("\n")
        proxies_list = list(set(proxies_list))
        proxies_list = list(filter(None, proxies_list))
        logger.debug(f"detected {len(proxies_list) } records to be added")

        tags = None
        servers = []
        for idx, ele in enumerate(proxies_list):
            logger.debug(f"start to pre-process {str(idx)} record: {type(ele)}")
            logger.debug(f"start to detect whether tag exist:{ele}")

            if ";" in ele:
                logger.debug(f"there is tags in this record:{ele}")

                url = ele.split(";")[0]
                tags = ele.split(";")[-1]
            else:
                logger.debug(f"there is no tags in this record:{ele}")

                url = ele
            logger.debug(f"end to detect whether tag exist:{ele}")

            if url:
                logger.debug(
                    f'split into url:\n{ele.split(";")[0]}\ntags:\n{ele.split(";")[-1]}'
                )

                proxy_protocol_type, host, port, user, password = split_proxy(url)

                proxy_data = {
                    "proxy_protocol": proxy_protocol_type,
                    "proxy_provider_type": 0,
                    "proxy_host": host,
                    "proxy_port": port,
                    "proxy_username": user,
                    "proxy_password": password,
                    "ip_address": None,
                    "country": None,
                    "tags": tags,
                    "status": 2,
                    "proxy_validate_network_type": None,
                    "proxy_validate_server": None,
                    "proxy_validate_results": None,
                }
                result = ProxyModel.add_proxy(proxy_data)
                print(f"save proxy {ele} :{result}")
                if result == None:
                    logger.error(f"add proxy failure :{ele}")
                    showinfomsg(f"we can not add the same proxy twice :{ele}")
                else:
                    showinfomsg(f"add proxy ok {result.id}")

            else:
                logger.error(f"there is no valid proxy in this record :{ele}")
                showinfomsg(f"there is no valid proxy in this record :{ele}")
            logger.debug(f"end to validate {str(idx)} record: {type(url)}")

    else:
        logger.debug("you should input valid proxy list and try again")


def saveProxy(
    proxy_protocol_type=None,
    iptype=None,
    proxy_provider_type=None,
    host=None,
    port=None,
    user=None,
    password=None,
    ip_address=None,
    country=None,
    state=None,
    city=None,
    tags=None,
    status=None,
    network_type=None,
):
    print("proxy_protocol_type", proxy_protocol_type, type(proxy_protocol_type))
    if "Select" in country:
        country = None
    if "Select" in state:
        state = None
    if "Select" in city:
        city = None

    if "Select" in proxy_protocol_type:
        proxy_protocol_type = None
    if "Select" in proxy_provider_type:
        proxy_provider_type = None
    if "Select" in iptype:
        iptype = None
    if "Select" in network_type:
        network_type = None

    if proxy_provider_type == None:
        proxy_provider_type = PROXY_PROVIDER_TYPE.CUSTOM
    if type(proxy_provider_type) == str:
        proxy_provider_type = find_key(
            PROXY_PROVIDER_TYPE.PROXY_PROVIDER_TYPE_TEXT, proxy_provider_type
        )
    if proxy_protocol_type == None:
        proxy_protocol_type = PROXY_PROTOCOL.HTTP
    if type(proxy_protocol_type) == str:
        proxy_protocol_type = find_key(
            PROXY_PROTOCOL.PROXY_PROTOCOL_TEXT, proxy_protocol_type
        )
    if status in ["VALID", "INVALID", "UNCHEKCED"]:
        status = find_key(PROXY_STATUS.PROXY_STATUS_TEXT, status)
    if network_type == None:
        network_type = IP_SOURCE_TYPE.datacenter
    else:
        if type(network_type) == str:
            network_type = find_key(IP_SOURCE_TYPE.IP_SOURCE_TYPE_TEXT, network_type)
    if iptype == None:
        iptype = IP_TYPE.IPv4
    else:
        if type(iptype) == str:
            iptype = find_key(IP_TYPE.IP_TYPE_TEXT, iptype)

    if host == "":
        host = None
    if port == "":
        port = None
    if user == "":
        user = None
    if password == "":
        password = None
    if ip_address == "":
        ip_address = None
    if tags == "":
        tags = None
    if host == None or port == None or proxy_protocol_type == None:
        logger.error(f"there is no valid proxy ")
        showinfomsg(
            f"there is no valid proxy,please fill host and port protocol at least"
        )
    else:
        proxy_data = {
            "proxy_protocol": proxy_protocol_type,
            "proxy_provider_type": proxy_provider_type,
            "proxy_host": host,
            "proxy_port": port,
            "proxy_username": user,
            "proxy_password": password,
            "ip_address": ip_address,
            "country": country,
            "state": state,
            "city": city,
            "ip_type": iptype,
            "tags": tags,
            "status": status,
            "network_type": network_type,
            "proxy_validate_server": None,
            "proxy_validate_results": None,
        }
        result = ProxyModel.add_proxy(proxy_data)
        print(f"save proxy {proxy_data} :{result}")
        if result == None:
            logger.error(f"add proxy failure :{proxy_data}")
            showinfomsg(f"add proxy failure")
        else:
            showinfomsg(f"add proxy ok {CustomID(custom_id=result.id).to_hex()}")


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


def bulkimportproxyView(frame):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # 缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0, 1), weight=1)

    newWindow.title(settings[locale]["bulkimportproxyView"]["title"])
    newWindow.grid_rowconfigure(0, weight=1)
    newWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    newWindow.grid_columnconfigure(1, weight=2)

    account_frame_left = tk.Frame(newWindow, height=height)
    account_frame_left.grid(row=0, column=0, sticky="nsew")
    account_frame_right = tk.Frame(newWindow, height=height)
    account_frame_right.grid(row=0, column=1, sticky="nsew")
    proxyView(account_frame_right)

    frame = account_frame_left

    lbl15 = tk.Label(frame, text=settings[locale]["bulkimportproxyView"]["copyhints"])
    lbl15.grid(row=0, column=0, sticky=tk.W)

    global proxy_textfield_str
    proxy_textfield_str = tk.StringVar()
    global latest_conditions
    latest_conditions = tk.StringVar()

    from tkinter.scrolledtext import ScrolledText

    proxy_textfield = ScrolledText(frame, wrap=tk.WORD)
    proxy_textfield.grid(row=3, column=0, columnspan=2, padx=0, pady=15)
    proxy_textfield.insert(
        tk.END, settings[locale]["bulkimportproxyView"]["placeholder"]
    )
    proxy_textfield.bind("<Return>", returnProxy_textfield)
    proxy_textfield.bind_all("<Control-c>", _copy)

    b_save_proxy = tk.Button(
        frame,
        text=settings[locale]["bulkimportproxyView"]["save"],
        command=lambda: threading.Thread(
            target=saveBulkproxies(proxy_textfield.get("1.0", tk.END), logger)
        ).start(),
    )
    b_save_proxy.grid(row=5, column=0, sticky=tk.W)

    b_check_proxy = tk.Button(
        frame,
        text=settings[locale]["bulkimportproxyView"]["bulkcheck"],
        command=lambda: threading.Thread(
            target=updateproxies(
                prod_engine, proxy_textfield.get("1.0", tk.END), logger
            )
        ).start(),
    )
    b_check_proxy.grid(row=5, column=1, sticky=tk.W)

    b_clear_texts = tk.Button(
        frame,
        text=settings[locale]["bulkimportproxyView"]["clearall"],
        command=lambda: threading.Thread(
            target=proxy_textfield.delete(1.0, tk.END)
        ).start(),
    )
    b_clear_texts.grid(row=4, column=1, sticky=tk.W)

    b_choose_proxy = tk.Button(
        frame,
        text=settings[locale]["bulkimportproxyView"]["loadfile"],
        command=lambda: threading.Thread(target=select_file).start(),
    )
    b_choose_proxy.grid(row=4, column=0, sticky=tk.W)


def newproxyView(frame):
    newWindow = tk.Toplevel(frame)
    newWindow.geometry(window_size)
    # 缺少这两行填充设置，两个frame展示的大小始终是不对的
    newWindow.rowconfigure(0, weight=1)
    newWindow.columnconfigure((0, 1), weight=1)

    newWindow.title(settings[locale]["newproxyview"]["title"])
    newWindow.grid_rowconfigure(0, weight=1)
    newWindow.grid_columnconfigure(0, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(1, weight=1, uniform="group1")
    newWindow.grid_columnconfigure(0, weight=1)
    newWindow.grid_columnconfigure(1, weight=2)

    account_frame_left = tk.Frame(newWindow, height=height)
    account_frame_left.grid(row=0, column=0, sticky="nsew")
    account_frame_right = tk.Frame(newWindow, height=height)
    account_frame_right.grid(row=0, column=1, sticky="nsew")
    proxyView(account_frame_right)

    ttkframe = account_frame_left

    l_provider = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["l_provider"])
    # l_platform.place(x=10, y=90)
    l_provider.grid(row=0, column=0, padx=14, pady=15)

    proxyprovider = tk.StringVar()
    proxyprovider_box = ttk.Combobox(ttkframe, textvariable=proxyprovider)

    def proxyproviderdb_values():
        proxyprovider_names = list(
            dict(PROXY_PROVIDER_TYPE.PROXY_PROVIDER_TYPE_TEXT).values()
        )

        proxyprovider_box["values"] = proxyprovider_names

    def proxyproviderdb_refresh(event):
        proxyprovider_box["values"] = proxyproviderdb_values()

    proxyprovider_box["values"] = proxyproviderdb_values()

    def proxyproviderOptionCallBack(*args):
        print(proxyprovider.get())
        print(proxyprovider_box.current())

    proxyprovider.set(settings[locale]["newproxyview"]["dropdown_hints"])
    proxyprovider.trace("w", proxyproviderOptionCallBack)
    proxyprovider_box.bind("<Button-1>", lambda event: proxyproviderdb_refresh(event))

    # proxyprovider_box.config(values =proxyprovider_names)
    proxyprovider_box.grid(row=0, column=5, padx=14, pady=15)

    proxy_host = tk.StringVar()
    proxy_port = tk.StringVar()
    proxy_ip = tk.StringVar()

    username = tk.StringVar()
    proxy_option_account = tk.StringVar()
    password = tk.StringVar()
    refresh_url = tk.StringVar()
    username = tk.StringVar()
    proxy_tag = tk.StringVar()
    password = tk.StringVar()

    l_host = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["L_proxy_host"])
    l_host.grid(row=7, column=0, padx=14, pady=15)

    e_host = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=proxy_host)
    e_host.grid(row=7, column=5, padx=14, pady=15, sticky="w")

    l_port = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["L_proxy_port"])
    l_port.grid(row=8, column=0, padx=14, pady=15)

    e_port = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=proxy_port)
    e_port.grid(row=8, column=5, padx=14, pady=15, sticky="w")

    l_ip = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["L_proxy_ip"])
    l_ip.grid(row=9, column=0, padx=14, pady=15)

    e_ip = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=proxy_ip)
    e_ip.grid(row=9, column=5, padx=14, pady=15, sticky="w")

    l_username = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["username"])
    l_username.grid(row=10, column=0, padx=14, pady=15)

    e_username = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=username)
    e_username.grid(row=10, column=5, padx=14, pady=15, sticky="w")

    l_password = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["password"])
    e_password = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=password)

    l_password.grid(row=11, column=0, padx=14, pady=15)
    e_password.grid(row=11, column=5, padx=14, pady=15, sticky="w")

    l_refresh_url = tk.Label(
        ttkframe, text=settings[locale]["newproxyview"]["L_refresh_url"]
    )
    l_refresh_url.grid(row=12, column=0, padx=14, pady=15)

    e_refresh_url = tk.Entry(
        ttkframe, width=int(width * 0.01), textvariable=refresh_url
    )
    e_refresh_url.grid(row=12, column=5, padx=14, pady=15, sticky="w")

    l_tag = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["L_proxy_tag"])
    l_tag.grid(row=13, column=0, padx=14, pady=15)

    e_tag = tk.Entry(ttkframe, width=int(width * 0.01), textvariable=proxy_tag)
    e_tag.grid(row=13, column=5, padx=14, pady=15, sticky="w")

    l_iptype = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["l_iptype"])
    l_iptype.grid(row=1, column=0, padx=14, pady=15)

    iptype = tk.StringVar()
    iptype_box = ttk.Combobox(ttkframe, textvariable=iptype)

    def iptypedb_values():
        platform_rows = PlatformModel.filter_platforms(
            name=None, ptype=None, server=None
        )

        platform_names = list(dict(IP_TYPE.IP_TYPE_TEXT).values())

        iptype_box["values"] = platform_names

    def iptypedb_refresh(event):
        iptype_box["values"] = iptypedb_values()

    iptype_box["values"] = iptypedb_values()

    def iptypeOptionCallBack(*args):
        print(iptype.get())
        print(iptype_box.current())

    iptype.set(settings[locale]["newproxyview"]["dropdown_hints"])
    iptype.trace("w", iptypeOptionCallBack)
    iptype_box.bind("<Button-1>", lambda event: iptypedb_refresh(event))
    iptype_names = list(dict(IP_TYPE.IP_TYPE_TEXT).values())

    iptype_box.config(values=iptype_names)
    iptype_box.grid(row=1, column=5, padx=14, pady=15)

    l_ipsource = tk.Label(ttkframe, text=settings[locale]["newproxyview"]["l_ipsource"])
    # l_platform.place(x=10, y=90)
    l_ipsource.grid(row=2, column=0, padx=14, pady=15)

    ipsource = tk.StringVar()
    ipsource_box = ttk.Combobox(ttkframe, textvariable=ipsource)

    def ipsourcedb_values():
        platform_rows = PlatformModel.filter_platforms(
            name=None, ptype=None, server=None
        )

        platform_names = list(dict(IP_SOURCE_TYPE.IP_SOURCE_TYPE_TEXT).values())

        ipsource_box["values"] = platform_names

    def ipsourcedb_refresh(event):
        ipsource_box["values"] = ipsourcedb_values()

    ipsource_box["values"] = ipsourcedb_values()

    def ipsourceOptionCallBack(*args):
        print(ipsource.get())
        print(ipsource_box.current())

    ipsource.set(settings[locale]["newproxyview"]["dropdown_hints"])
    ipsource.trace("w", ipsourceOptionCallBack)
    ipsource_box.bind("<Button-1>", lambda event: ipsourcedb_refresh(event))
    ipsource_names = list(dict(IP_SOURCE_TYPE.IP_SOURCE_TYPE_TEXT).values())

    ipsource_box.config(values=ipsource_names)
    ipsource_box.grid(row=2, column=5, padx=14, pady=15)

    l_proxycountry = tk.Label(ttkframe, text=settings[locale]["l_proxycountry"])
    # l_platform.place(x=10, y=90)
    l_proxycountry.grid(row=3, column=0, padx=14, pady=15)

    proxycountry = tk.StringVar()
    proxycountry_box = ttk.Combobox(ttkframe, textvariable=proxycountry)
    proxycountrycode = tk.StringVar()

    def proxycountrydb_values():
        proxycountry_names = citydb["countries"].values()
        # print('proxycountry_names',proxycountry_names)

        proxycountry_box["values"] = list(proxycountry_names)

    def proxycountrydb_refresh(event):
        proxycountry_box["values"] = proxycountrydb_values()

    proxycountry_box["values"] = proxycountrydb_values()

    def proxycountryOptionCallBack(*args):
        print(proxycountry.get())
        country_code = find_key(citydb["countries"], proxycountry.get())
        proxycountrycode.set(country_code)
        print(proxycountry_box.current())

    proxycountry.set(settings[locale]["newproxyview"]["dropdown_hints"])

    proxycountry.trace("w", proxycountryOptionCallBack)
    proxycountry_box.bind("<Button-1>", lambda event: proxycountrydb_refresh(event))
    # proxycountry_box.bind("<<ComboboxSelected>>",proxycountryOptionCallBack)

    # proxycountry_box.config(values =proxycountry_names)
    proxycountry_box.grid(row=3, column=5, padx=14, pady=15)

    l_proxystate = tk.Label(ttkframe, text=settings[locale]["l_proxystate"])
    # l_platform.place(x=10, y=90)
    l_proxystate.grid(row=4, column=0, padx=14, pady=15)

    proxystate = tk.StringVar()
    proxystate_box = ttk.Combobox(ttkframe, textvariable=proxystate)
    proxystatecode = tk.StringVar()

    def proxystatedb_values():
        proxystate_names = []
        print(f"cache proxycountry_codes : {proxycountrycode.get()}")
        if proxycountry.get() is not None:
            print(proxycountry.get())
            if proxycountrycode.get():
                country_code = find_key(citydb["countries"], proxycountry.get())
                # print(f"country_code:{country_code}")

                proxystate_names = citydb[country_code].keys()
                proxystate_names = list(proxystate_names)
                # print(f"proxystate_names:{proxystate_names}")
                if len(proxystate_names) == 0:
                    proxystate_names = [None]
                proxystate_box["values"] = proxystate_names

    def proxystatedb_refresh(event):
        proxystate_box["values"] = proxystatedb_values()

    proxystate_box["values"] = proxystatedb_values()

    def proxystateOptionCallBack(*args):
        print(proxystate.get())
        print(proxystate_box.current())
        # proxystate_box['values'] = proxystatedb_values()

    proxystate.set(settings[locale]["newproxyview"]["dropdown_hints"])

    # proxystate.trace('w', proxystateOptionCallBack)
    proxystate_box.bind("<Button-1>", lambda event: proxystatedb_refresh(event))

    proxystate_box.bind("<<ComboboxSelected>>", proxystateOptionCallBack)

    proxystate_box.config(values=[])
    proxystate_box.grid(row=4, column=5, padx=14, pady=15)

    l_proxycity = tk.Label(ttkframe, text=settings[locale]["l_proxycity"])
    # l_platform.place(x=10, y=90)
    l_proxycity.grid(row=5, column=0, padx=14, pady=15)

    proxycity = tk.StringVar()
    proxycity_box = ttk.Combobox(ttkframe, textvariable=proxycity)

    def proxycitydb_values():
        print(f"cache proxycountry_codes : {proxycountrycode.get()}")
        country_code = None
        state_code = None
        if proxycountry.get() is not None:
            print(proxycountry.get())
            country_code = proxycountry.get()
            if proxycountrycode.get():
                country_code = find_key(citydb["countries"], proxycountry.get())
                print(f"country_code:{country_code}")

                if proxystate.get():
                    state_code = proxystate.get()
                    print(f"state_code:{state_code}")

                    citynames = citydb[country_code][state_code]
                    citynames = list(citynames)
                else:
                    citynames = [None]

            else:
                citynames = [None]
            print("city names", citynames)
            proxycity_box["values"] = citynames
            # proxycity.set("Select From city")

        else:
            showinfomsg(message="choose a country and state first")

    def proxycitydb_refresh(event):
        proxycity_box["values"] = proxycitydb_values()

    def proxycityOptionCallBack(*args):
        print("choose city", proxycity.get())

    proxycity.set(settings[locale]["newproxyview"]["dropdown_hints"])

    proxycity_box.bind("<Button-1>", lambda event: proxycitydb_refresh(event))

    # proxycity_box.bind('<Button-1>', lambda event: proxycitydb_refresh(event))
    proxycity_box.bind("<<ComboboxSelected>>", proxycityOptionCallBack)
    # proxycity_box.bind("<KeyRelease>",proxycityOptionCallBack)
    # proxycity_box['values'] = proxycitydb_values()

    # proxycity_box.config(values =proxycitydb_values())
    proxycity_box.grid(row=5, column=5, padx=14, pady=15)

    l_proxyprotocol = tk.Label(ttkframe, text=settings[locale]["L_proxyprotocol"])
    # l_platform.place(x=10, y=90)
    l_proxyprotocol.grid(row=14, column=0, padx=14, pady=15)

    proxyprotocol = tk.StringVar()
    proxyprotocol_box = ttk.Combobox(ttkframe, textvariable=proxyprotocol)

    def proxyprotocoldb_values():
        proxyprotocol_box["values"] = list(
            dict(PROXY_PROTOCOL.PROXY_PROTOCOL_TEXT).values()
        )

    def proxyprotocoldb_refresh(event):
        proxyprotocol_box["values"] = proxyprotocoldb_values()

    def proxyprotocolOptionCallBack(*args):
        print("choose PROXY_PROTOCOL", proxyprotocol.get())

    # proxyprotocol.trace('w', proxyprotocolOptionCallBack)
    proxyprotocol.set(settings[locale]["newproxyview"]["dropdown_hints"])

    proxyprotocol_box.bind("<Button-1>", lambda event: proxyprotocoldb_refresh(event))

    # proxyprotocol_box.bind('<Button-1>', lambda event: proxyprotocoldb_refresh(event))
    proxyprotocol_box.bind("<<ComboboxSelected>>", proxyprotocolOptionCallBack)
    # proxyprotocol_box.bind("<KeyRelease>",proxyprotocolOptionCallBack)
    # proxyprotocol_box['values'] = proxyprotocoldb_values()

    # proxyprotocol_box.config(values =proxyprotocoldb_values())
    proxyprotocol_box.grid(row=14, column=5, padx=14, pady=15)

    b_save_proxy = tk.Button(
        ttkframe,
        text=settings[locale]["newproxyview"]["save"],
        command=lambda: threading.Thread(
            target=saveProxy(
                proxy_protocol_type=proxyprotocol.get(),
                proxy_provider_type=proxyprovider.get(),
                host=proxy_host.get(),
                port=proxy_port.get(),
                user=username.get(),
                password=password.get(),
                ip_address=proxy_ip.get(),
                iptype=iptype.get(),
                country=proxycountry.get(),
                state=proxystate.get(),
                city=proxycity.get(),
                tags=proxy_tag.get(),
                status=2,
                network_type=ipsource.get(),
            )
        ).start(),
    )
    b_save_proxy.grid(row=15, column=0, sticky=tk.W)


def proxyView(frame, mode="query", linkProxy=None, platform=None):
    operation_frame = tk.Frame(frame, bd=1, relief=tk.FLAT)
    operation_frame.grid(row=1, column=0, sticky="nswe")
    query_frame = tk.Frame(frame, bd=1, relief=tk.FLAT)
    query_frame.grid(row=0, column=0, sticky="nswe")

    b_new_proxy = tk.Button(
        operation_frame,
        text=settings[locale]["proxyview"]["new"],
        command=lambda: threading.Thread(target=newproxyView(frame)).start(),
    )
    b_new_proxy.grid(row=0, column=0, padx=14, pady=15)

    b_bulk_import_users = tk.Button(
        operation_frame,
        text=settings[locale]["proxyview"]["bulkimport"],
        command=lambda: threading.Thread(target=bulkimportproxyView(frame)).start(),
    )
    # b_bulk_import_users.place(x=10, y=450)
    b_bulk_import_users.grid(row=0, column=1, padx=14, pady=15)

    b_check_proxy = tk.Button(
        operation_frame,
        text=settings[locale]["proxyview"]["bulkcheck"],
        command=lambda: threading.Thread(
            target=updateproxies(
                prod_engine, proxy_textfield.get("1.0", tk.END), logger
            )
        ).start(),
    )
    b_check_proxy.grid(row=0, column=2, sticky=tk.W)

    result_frame = tk.Frame(frame, bd=1, relief=tk.FLAT)
    result_frame.grid(row=3, column=0, sticky="nswe")

    result_frame.grid_rowconfigure(0, weight=1)
    result_frame.grid_columnconfigure(0, weight=1)
    result_frame.grid_columnconfigure(1, weight=1)

    # global city,country,proxyTags,proxyStatus
    city = tk.StringVar()
    state = tk.StringVar()
    network_type = tk.StringVar()
    country = tk.StringVar()
    proxyTags = tk.StringVar()

    lbl15 = tk.Label(query_frame, text=settings[locale]["proxyview"]["q_city"])
    # lbl15.place(x=430, y=30, anchor=tk.NE)
    # lbl15.pack(side='left')

    lbl15.grid(row=0, column=0, sticky=tk.W)

    txt15 = tk.Entry(query_frame, textvariable=city)
    txt15.insert(0, "Los")
    # txt15.place(x=580, y=30, anchor=tk.NE)
    # txt15.pack(side='left')
    txt15.grid(row=1, column=0, sticky=tk.W)

    l_state = tk.Label(query_frame, text=settings[locale]["proxyview"]["q_state"])
    l_state.grid(row=0, column=1, sticky=tk.W)
    e_state = tk.Entry(query_frame, textvariable=state)
    e_state.insert(0, "LA")
    e_state.grid(row=1, column=1, sticky=tk.W)

    lbl16 = tk.Label(query_frame, text=settings[locale]["proxyview"]["q_country"])
    lbl16.grid(row=0, column=2, sticky=tk.W)
    txt16 = tk.Entry(query_frame, textvariable=country)
    txt16.insert(0, "USA")
    txt16.grid(row=1, column=2, sticky=tk.W)

    lb17 = tk.Label(query_frame, text=settings[locale]["proxyview"]["q_tags"])
    lb17.grid(row=0, column=3, sticky=tk.W)
    txt17 = tk.Entry(query_frame, textvariable=proxyTags)
    txt17.insert(0, "youtube")
    txt17.grid(row=1, column=3, sticky=tk.W)

    l_networktype = tk.Label(
        query_frame, text=settings[locale]["proxyview"]["q_networktype"]
    )
    l_networktype.grid(row=2, column=0, sticky=tk.W)
    e_networktype = tk.Entry(query_frame, textvariable=network_type)
    e_networktype.insert(0, "resident")
    e_networktype.grid(row=3, column=0, sticky=tk.W)

    lb18 = tk.Label(query_frame, text=settings[locale]["proxyview"]["q_status"])
    lb18.grid(row=2, column=1, sticky=tk.W)

    proxyStatus = tk.StringVar()

    proxyStatusbox = ttk.Combobox(query_frame, textvariable=proxyStatus)
    # proxyStatusbox.config(values = ('valid', 'invalid','unchecked'))
    proxyStatusbox.grid(row=3, column=1, padx=14, pady=15)

    def proxyStatusbox_refresh(*args):
        proxyStatusbox["values"] = list(dict(PROXY_STATUS.PROXY_STATUS_TEXT).values())

    def proxyStatusCallBack(*args):
        print(proxyStatus.get())
        print(proxyStatusbox.current())

    proxyStatus.set(settings[locale]["proxyview"]["q_status_hints"])
    proxyStatus.trace("w", proxyStatusCallBack)
    proxyStatusbox.bind("<Button-1>", lambda event: proxyStatusbox_refresh(event))

    btn5 = tk.Button(
        query_frame,
        text=settings[locale]["proxyview"]["querynow"],
        padx=0,
        pady=0,
        command=lambda: queryProxy(
            frame=result_frame,
            canvas=None,
            tab_headers=tab_headers,
            city=city.get(),
            state=state.get(),
            country=country.get(),
            tags=proxyTags.get(),
            network_type=network_type.get(),
            status=proxyStatus.get(),
            mode=mode,
            linkProxy=linkProxy,
            platform=platform,
        ),
    )

    btn5.grid(row=4, column=0, sticky=tk.W)

    btn5 = tk.Button(
        query_frame,
        text=settings[locale]["proxyview"]["reset"],
        padx=0,
        pady=0,
        command=lambda: (
            proxyStatus.set(""),
            country.set(""),
            state.set(""),
            city.set(""),
            proxyTags.set(""),
            proxyStatus.set("Select From Status"),
            network_type.set(""),
        ),
    )
    btn5.grid(row=4, column=1, sticky=tk.W)

    tab_headers = [
        "id",
        "provider",
        "protocol",
        "host",
        "port",
        "username",
        "pass",
        "country",
        "state",
        "city",
        "tags",
        "status",
        "validate_results",
        "is_deleted",
        "inserted_at",
    ]

    refreshProxycanvas(canvas=None, frame=result_frame, headers=tab_headers, datas=[])


def metaView(
    left, right, isThumbView=True, isDesView=True, isTagsView=True, isScheduleView=True
):
    # global metaView_video_folder
    metaView_video_folder = tk.StringVar()

    l_video_folder = tk.Label(left, text=settings[locale]["metaview"]["videoFolder"])
    l_video_folder.grid(row=0, column=0, sticky="w", padx=14, pady=15)

    e_video_folder = tk.Entry(left, textvariable=metaView_video_folder)
    e_video_folder.grid(row=0, column=1, sticky="w", padx=14, pady=15)
    if metaView_video_folder.get() != "":
        if tmp["lastfolder"] is None or tmp["lastfolder"] == "":
            pass
        else:
            if tmp["metaView_video_folder"] is None:
                metaView_video_folder.set(tmp["lastfolder"])
            metaView_video_folder.set(tmp["metaView_video_folder"])
    b_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_tabview_video_folder(
                metaView_video_folder, "metaView_video_folder"
            )
        ).start(),
    )
    b_video_folder.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    if metaView_video_folder.get() != "":
        tmp["metaView_video_folder"] = metaView_video_folder.get()

    b_open_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["openlocalfolder"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_open_video_folder.grid(row=0, column=3, sticky="w", padx=14, pady=15)
    l_meta_format = tk.Label(
        left, text=settings[locale]["metaview"]["l_metafileformat"]
    )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    global metafileformat

    metafileformat = tk.StringVar()

    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
        analyse_video_meta_pair(
            metaView_video_folder.get(),
            left,
            right,
            metafileformatbox.get(),
            isThumbView=isThumbView,
            isDesView=isDesView,
            isTagsView=isTagsView,
            isScheduleView=isTagsView,
        )

    metafileformat.set(settings[locale]["metaview"]["dropdown_hints"])
    metafileformat.trace("w", metafileformatCallBack)

    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values=("json", "xlsx", "csv"))
    metafileformatbox.grid(row=1, column=1, sticky="w", padx=14, pady=15)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)

    b_download_meta_templates = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_downvideometafile"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_download_meta_templates.grid(row=1, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_download_meta_templates,
        text=settings[locale]["metaview"]["b_downvideometafile_hints"],
        wraplength=200,
    )

    b_video_folder_check = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_checkvideoassets"],
        command=lambda: threading.Thread(
            target=analyse_video_meta_pair(
                metaView_video_folder.get(),
                left,
                right,
                metafileformatbox.get(),
                isThumbView=isThumbView,
                isDesView=isDesView,
                isTagsView=isTagsView,
                isScheduleView=isScheduleView,
            )
        ).start(),
    )
    b_video_folder_check.grid(row=2, column=0, sticky="w", padx=14, pady=15)


def tagsView(left, right, lang):
    # global metaView_video_folder
    metaView_video_folder = tk.StringVar()

    l_video_folder = tk.Label(left, text=settings[locale]["metaview"]["videoFolder"])
    l_video_folder.grid(row=0, column=0, sticky="w", padx=14, pady=15)

    e_video_folder = tk.Entry(left, textvariable=metaView_video_folder)
    e_video_folder.grid(row=0, column=1, sticky="w", padx=14, pady=15)
    if metaView_video_folder.get() != "":
        if tmp["lastfolder"] is None or tmp["lastfolder"] == "":
            pass
        else:
            if tmp["metaView_video_folder"] is None:
                metaView_video_folder.set(tmp["lastfolder"])
            metaView_video_folder.set(tmp["metaView_video_folder"])
    b_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_tabview_video_folder(
                metaView_video_folder, "metaView_video_folder"
            )
        ).start(),
    )
    b_video_folder.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    if metaView_video_folder.get() != "":
        tmp["metaView_video_folder"] = metaView_video_folder.get()

    b_open_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["openlocalfolder"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_open_video_folder.grid(row=0, column=3, sticky="w", padx=14, pady=15)
    l_meta_format = tk.Label(
        left, text=settings[locale]["metaview"]["l_metafileformat"]
    )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    global metafileformat

    metafileformat = tk.StringVar()

    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
        analyse_video_meta_pair(
            metaView_video_folder.get(),
            left,
            right,
            metafileformatbox.get(),
            isThumbView=False,
            isDesView=False,
            isTagsView=True,
            isScheduleView=False,
        )

    metafileformat.set(settings[locale]["metaview"]["dropdown_hints"])
    metafileformat.trace("w", metafileformatCallBack)

    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values=("json", "xlsx", "csv"))
    metafileformatbox.grid(row=1, column=1, sticky="w", padx=14, pady=15)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)

    b_download_meta_templates = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_downvideometafile"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_download_meta_templates.grid(row=1, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_download_meta_templates,
        text=settings[locale]["metaview"]["b_downvideometafile_hints"],
        wraplength=200,
    )

    b_video_folder_check = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_checkvideoassets"],
        command=lambda: threading.Thread(
            target=analyse_video_meta_pair(
                metaView_video_folder.get(),
                left,
                right,
                metafileformatbox.get(),
                isThumbView=False,
                isDesView=False,
                isTagsView=True,
                isScheduleView=False,
            )
        ).start(),
    )
    b_video_folder_check.grid(row=2, column=0, sticky="w", padx=14, pady=15)


def desView(left, right, lang):
    # global metaView_video_folder
    metaView_video_folder = tk.StringVar()

    l_video_folder = tk.Label(left, text=settings[locale]["metaview"]["videoFolder"])
    l_video_folder.grid(row=0, column=0, sticky="w", padx=14, pady=15)

    e_video_folder = tk.Entry(left, textvariable=metaView_video_folder)
    e_video_folder.grid(row=0, column=1, sticky="w", padx=14, pady=15)
    if metaView_video_folder.get() != "":
        if tmp["lastfolder"] is None or tmp["lastfolder"] == "":
            pass
        else:
            if tmp["metaView_video_folder"] is None:
                metaView_video_folder.set(tmp["lastfolder"])
            metaView_video_folder.set(tmp["metaView_video_folder"])
    b_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_tabview_video_folder(
                metaView_video_folder, "metaView_video_folder"
            )
        ).start(),
    )
    b_video_folder.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    if metaView_video_folder.get() != "":
        tmp["metaView_video_folder"] = metaView_video_folder.get()

    b_open_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["openlocalfolder"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_open_video_folder.grid(row=0, column=3, sticky="w", padx=14, pady=15)
    l_meta_format = tk.Label(
        left, text=settings[locale]["metaview"]["l_metafileformat"]
    )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    global metafileformat

    metafileformat = tk.StringVar()

    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
        analyse_video_meta_pair(
            metaView_video_folder.get(),
            left,
            right,
            metafileformatbox.get(),
            isThumbView=False,
            isDesView=True,
            isTagsView=False,
            isScheduleView=False,
        )

    metafileformat.set(settings[locale]["metaview"]["dropdown_hints"])
    metafileformat.trace("w", metafileformatCallBack)

    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values=("json", "xlsx", "csv"))
    metafileformatbox.grid(row=1, column=1, sticky="w", padx=14, pady=15)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)

    b_download_meta_templates = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_downvideometafile"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_download_meta_templates.grid(row=1, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_download_meta_templates,
        text=settings[locale]["metaview"]["b_downvideometafile_hints"],
        wraplength=200,
    )

    b_video_folder_check = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_checkvideoassets"],
        command=lambda: threading.Thread(
            target=analyse_video_meta_pair(
                metaView_video_folder.get(),
                left,
                right,
                metafileformatbox.get(),
                isThumbView=False,
                isDesView=True,
                isTagsView=False,
                isScheduleView=False,
            )
        ).start(),
    )
    b_video_folder_check.grid(row=2, column=0, sticky="w", padx=14, pady=15)


def scheduleView(left, right, lang):
    scheduleView_video_folder = tk.StringVar()

    # global metaView_video_folder
    metaView_video_folder = tk.StringVar()

    l_video_folder = tk.Label(left, text=settings[locale]["metaview"]["videoFolder"])
    l_video_folder.grid(row=0, column=0, sticky="w", padx=14, pady=15)

    e_video_folder = tk.Entry(left, textvariable=metaView_video_folder)
    e_video_folder.grid(row=0, column=1, sticky="w", padx=14, pady=15)
    if metaView_video_folder.get() != "":
        if tmp["lastfolder"] is None or tmp["lastfolder"] == "":
            pass
        else:
            if tmp["metaView_video_folder"] is None:
                metaView_video_folder.set(tmp["lastfolder"])
            metaView_video_folder.set(tmp["metaView_video_folder"])
    b_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["dropdown_hints"],
        command=lambda: threading.Thread(
            target=select_tabview_video_folder(
                metaView_video_folder, "metaView_video_folder"
            )
        ).start(),
    )
    b_video_folder.grid(row=0, column=2, sticky="w", padx=14, pady=15)

    if metaView_video_folder.get() != "":
        tmp["metaView_video_folder"] = metaView_video_folder.get()

    b_open_video_folder = tk.Button(
        left,
        text=settings[locale]["metaview"]["openlocalfolder"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_open_video_folder.grid(row=0, column=3, sticky="w", padx=14, pady=15)
    l_meta_format = tk.Label(
        left, text=settings[locale]["metaview"]["l_metafileformat"]
    )
    # l_platform.place(x=10, y=90)
    l_meta_format.grid(row=1, column=0, sticky="w", padx=14, pady=15)
    global metafileformat

    metafileformat = tk.StringVar()

    def metafileformatCallBack(*args):
        print(metafileformat.get())
        print(metafileformatbox.current())
        # ultra[metaView_video_folder]['metafileformat']=metafileformat.get()
        analyse_video_meta_pair(
            metaView_video_folder.get(),
            left,
            right,
            metafileformatbox.get(),
            isThumbView=False,
            isDesView=False,
            isTagsView=False,
            isScheduleView=True,
        )

    metafileformat.set(settings[locale]["metaview"]["dropdown_hints"])
    metafileformat.trace("w", metafileformatCallBack)

    metafileformatbox = ttk.Combobox(left, textvariable=metafileformat)
    metafileformatbox.config(values=("json", "xlsx", "csv"))
    metafileformatbox.grid(row=1, column=1, sticky="w", padx=14, pady=15)
    metafileformatbox.bind("<<ComboboxSelected>>", metafileformatCallBack)

    b_download_meta_templates = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_downvideometafile"],
        command=lambda: threading.Thread(
            target=openLocal(metaView_video_folder.get())
        ).start(),
    )
    b_download_meta_templates.grid(row=1, column=3, sticky="w", padx=14, pady=15)
    Tooltip(
        b_download_meta_templates,
        text=settings[locale]["metaview"]["b_downvideometafile_hints"],
        wraplength=200,
    )

    b_video_folder_check = tk.Button(
        left,
        text=settings[locale]["metaview"]["b_checkvideoassets"],
        command=lambda: threading.Thread(
            target=analyse_video_meta_pair(
                metaView_video_folder.get(),
                left,
                right,
                metafileformatbox.get(),
                isThumbView=False,
                isDesView=False,
                isTagsView=False,
                isScheduleView=True,
            )
        ).start(),
    )
    b_video_folder_check.grid(row=2, column=0, sticky="w", padx=14, pady=15)


def logView(log_tab_frame, root, lang):
    debugLevel = tk.StringVar()

    debugLevel.set("Debug Level:")

    def debugLevelCallBack(*args):
        print(debugLevel.get())
        print(debugLevelbox.current())
        logger.setLevel(debugLevel.get())

    def log_filterCallBack(*args):
        print(log_filter.get())
        # for k in log_filter.get().split(','):
        #     addKeywordfilter(k)

    debugLevel.trace("w", debugLevelCallBack)

    debugLevelbox = ttk.Combobox(log_tab_frame, textvariable=debugLevel)
    debugLevelbox.config(values=("DEBUG", "INFO", "ERROR"))
    debugLevelbox.grid(row=0, column=0, padx=14, pady=15, sticky="w")
    log_filter = tk.StringVar()
    e_log_filter = tk.Entry(log_tab_frame, textvariable=log_filter)
    log_filter.set("log filter")
    log_filter.trace("w", log_filterCallBack)

    e_log_filter.grid(row=0, column=1, padx=14, pady=15, sticky="nswe")

    st = ConsoleUi(log_tab_frame, root, row=1, column=0)
    logger.debug(f"Installation path is:{ROOT_DIR}")

    logger.debug("TiktokaStudio GUI started")


def on_tab_change(event):
    selected_tab = tab_control.index(tab_control.select())


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
    return doc_frame, doc_frame_left, doc_frame_right


def render(root, window, lang, async_loop):
    global doc_frame, install_frame, thumb_frame, video_frame, proxy_frame, account_frame, upload_frame, meta_frame, tab_control

    tab_control = ttk.Notebook(window)
    tab_control.bind("<<NotebookTabChanged>>", on_tab_change)
    # tab_control.grid_columnconfigure(0, weight=1)
    # tab_control.grid_columnconfigure(1, weight=1)

    # def refresh_video_folder(event):
    #     if tab_control.index(tab_control.select()) == 4:
    #         if metaView_video_folder.get()!='':
    #             if tmp.has_key('lastfolder') and  tmp['lastfolder'] is not None or tmp['lastfolder']!='':
    #                 if tmp['metaView_video_folder'] is None:
    #                     metaView_video_folder.set(tmp['lastfolder'])
    #                 metaView_video_folder.set(tmp['metaView_video_folder'])

    #     elif tab_control.index(tab_control.select()) == 5:
    #         # scheduleView_video_folder.set('')  # Reset the value to an empty string
    #         pass
    # tab_control.bind("<<NotebookTabChanged>>", refresh_video_folder)

    doc_frame = ttk.Frame(tab_control)
    doc_frame.grid_rowconfigure(0, weight=1)
    doc_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    doc_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    doc_frame.grid_columnconfigure(1, weight=2)
    doc_frame.grid(row=0, column=0, sticky="nsew")

    doc_frame_left = tk.Frame(doc_frame, height=height)
    doc_frame_left.grid(row=0, column=0, sticky="nsew")
    doc_frame_right = tk.Frame(doc_frame, height=height)
    doc_frame_right.grid(row=0, column=1, sticky="nsew")

    install_frame = ttk.Frame(tab_control)
    install_frame.grid_rowconfigure(0, weight=1)
    install_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    install_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    install_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    install_frame.grid_columnconfigure(1, weight=2)
    install_frame.grid(row=0, column=0, sticky="nsew")

    install_frame_left = tk.Frame(install_frame, height=height)
    install_frame_left.grid(row=0, column=0, sticky="nsew")
    install_frame_right = tk.Frame(install_frame, height=height)
    install_frame_right.grid(row=0, column=1, sticky="nsew")

    thumb_frame = ttk.Frame(tab_control)
    thumb_frame.grid_rowconfigure(0, weight=1)
    thumb_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    thumb_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    thumb_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    thumb_frame.grid_columnconfigure(1, weight=2)
    thumb_frame.grid(row=0, column=0, sticky="nsew")
    thumb_frame_left = tk.Frame(thumb_frame)
    thumb_frame_left.grid(row=0, column=0, sticky="nswe")
    thumb_frame_right = tk.Frame(thumb_frame)
    thumb_frame_right.grid(row=0, column=1, sticky="nswe")

    thumb_frame_left = tk.Frame(thumb_frame, height=height)
    thumb_frame_left.grid(row=0, column=0, sticky="nsew")
    thumb_frame_right = tk.Frame(thumb_frame, height=height)
    thumb_frame_right.grid(row=0, column=1, sticky="nsew")

    tags_frame = ttk.Frame(tab_control)
    tags_frame.grid_rowconfigure(0, weight=1)
    tags_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    tags_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    tags_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    tags_frame.grid_columnconfigure(1, weight=2)
    tags_frame.grid(row=0, column=0, sticky="nsew")
    tags_frame_left = tk.Frame(tags_frame)
    tags_frame_left.grid(row=0, column=0, sticky="nswe")
    tags_frame_right = tk.Frame(tags_frame)
    tags_frame_right.grid(row=0, column=1, sticky="nswe")
    tags_frame_left = tk.Frame(tags_frame, height=height)
    tags_frame_left.grid(row=0, column=0, sticky="nsew")
    tags_frame_right = tk.Frame(tags_frame, height=height)
    tags_frame_right.grid(row=0, column=1, sticky="nsew")

    des_frame = ttk.Frame(tab_control)
    des_frame.grid_rowconfigure(0, weight=1)
    des_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    des_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    des_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    des_frame.grid_columnconfigure(1, weight=2)
    des_frame.grid(row=0, column=0, sticky="nsew")
    des_frame_left = tk.Frame(des_frame)
    des_frame_left.grid(row=0, column=0, sticky="nswe")
    des_frame_right = tk.Frame(des_frame)
    des_frame_right.grid(row=0, column=1, sticky="nswe")

    des_frame_left = tk.Frame(des_frame, height=height)
    des_frame_left.grid(row=0, column=0, sticky="nsew")
    des_frame_right = tk.Frame(des_frame, height=height)
    des_frame_right.grid(row=0, column=1, sticky="nsew")

    schedule_frame = ttk.Frame(tab_control)
    schedule_frame.grid_rowconfigure(0, weight=1)
    schedule_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    schedule_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    schedule_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    schedule_frame.grid_columnconfigure(1, weight=2)
    schedule_frame.grid(row=0, column=0, sticky="nsew")
    schedule_frame_left = tk.Frame(schedule_frame)
    schedule_frame_left.grid(row=0, column=0, sticky="nswe")
    schedule_frame_right = tk.Frame(schedule_frame)
    schedule_frame_right.grid(row=0, column=1, sticky="nswe")

    schedule_frame_left = tk.Frame(schedule_frame, height=height)
    schedule_frame_left.grid(row=0, column=0, sticky="nsew")
    schedule_frame_right = tk.Frame(schedule_frame, height=height)
    schedule_frame_right.grid(row=0, column=1, sticky="nsew")

    video_frame = ttk.Frame(tab_control)
    video_frame.grid_rowconfigure(0, weight=1)
    video_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    video_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    video_frame.grid_columnconfigure(0, weight=1, minsize=int(0.5 * width))
    video_frame.grid_columnconfigure(1, weight=2)
    video_frame.grid(row=0, column=0, sticky="nsew")
    video_frame_left = tk.Frame(video_frame)
    video_frame_left.grid(row=0, column=0, sticky="nswe")
    video_frame_right = tk.Frame(video_frame)
    video_frame_right.grid(row=0, column=1, sticky="nswe")

    proxy_frame = ttk.Frame(tab_control)
    # proxy_frame.grid_rowconfigure(0, weight=1)
    # proxy_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    # proxy_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    # proxy_frame.grid_columnconfigure(0, weight=1,
    #                                   minsize=int(0.5*width)

    #                                   )
    # proxy_frame.grid_columnconfigure(1, weight=2)
    proxy_frame.grid(row=0, column=0, sticky="nsew")

    proxy_frame_left = tk.Frame(proxy_frame)
    proxy_frame_left.grid(row=0, column=0, sticky="nsew")
    # proxy_frame_right = tk.Frame(proxy_frame, height = height)
    # proxy_frame_right.grid(row=0,column=1,sticky="nsew")
    # input_canvas.grid(row=0, column=0, pady=(5, 0), sticky='nw')

    account_frame = ttk.Frame(tab_control)
    # account_frame.grid_rowconfigure(0, weight=1)
    # account_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    # account_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    # account_frame.grid_columnconfigure(0, weight=1,
    #                                   minsize=int(0.5*width)

    #                                   )
    # account_frame.grid_columnconfigure(1, weight=2)
    account_frame.grid(row=0, column=0, sticky="nsew")

    account_frame_left = tk.Frame(account_frame)
    account_frame_left.grid(row=0, column=0, sticky="nsew")
    # account_frame_right = tk.Frame(account_frame, height = height)
    # account_frame_right.grid(row=0,column=1,sticky="nsew")

    upload_frame = ttk.Frame(tab_control)
    upload_frame.grid_rowconfigure(0, weight=1)
    # upload_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    # upload_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    # upload_frame.grid_columnconfigure(0, weight=1,
    #                                   minsize=int(0.5*width)

    #                                   )
    # upload_frame.grid_columnconfigure(1, weight=2)
    upload_frame.grid(row=0, column=0, sticky="nsew")
    upload_frame_left = tk.Frame(upload_frame)
    upload_frame_left.grid(row=0, column=0, sticky="nswe")
    upload_frame_right = tk.Frame(upload_frame)
    upload_frame_right.grid(row=0, column=1, sticky="nswe")

    meta_frame = ttk.Frame(tab_control)
    meta_frame.grid_rowconfigure(0, weight=1)
    meta_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    meta_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    meta_frame.grid_columnconfigure(0, weight=1)
    meta_frame.grid_columnconfigure(1, weight=2)
    meta_frame.grid(row=0, column=0, sticky="nsew")
    meta_frame_left = tk.Frame(meta_frame)
    meta_frame_left.grid(row=0, column=0, sticky="nswe")
    meta_frame_right = tk.Frame(meta_frame)
    meta_frame_right.grid(row=0, column=1, sticky="nswe")

    stats_frame = ttk.Frame(tab_control)
    # stats_frame.grid_rowconfigure(0, weight=1)
    # stats_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    # stats_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    # stats_frame.grid_columnconfigure(0, weight=1,
    #                                   minsize=int(0.5*width)

    #                                   )
    # stats_frame.grid_columnconfigure(1, weight=2)
    stats_frame.grid(row=0, column=0, sticky="nsew")

    plugins_frame = ttk.Frame(tab_control)
    # plugins_frame.grid_rowconfigure(0, weight=1)
    # plugins_frame.grid_columnconfigure(0, weight=1, uniform="group1")
    # plugins_frame.grid_columnconfigure(1, weight=1, uniform="group1")
    # plugins_frame.grid_columnconfigure(0, weight=1,
    #                                   minsize=int(0.5*width)

    #                                   )
    # plugins_frame.grid_columnconfigure(1, weight=2)
    plugins_frame.grid(row=0, column=0, sticky="nsew")

    tab_control.add(install_frame, text=settings[locale]["installView"])

    installView(install_frame_left, install_frame_right, lang)

    tab_control.add(account_frame, text=settings[locale]["accountView"])

    accountView(account_frame, mode="query")

    tab_control.add(proxy_frame, text=settings[locale]["proxyView"])

    proxyView(proxy_frame)

    tab_control.add(video_frame, text=settings[locale]["videosView"])
    videosView(video_frame_left, video_frame_right, lang)

    tab_control.add(thumb_frame, text=settings[locale]["thumbView"])

    thumbView(thumb_frame_left, thumb_frame_right, lang)
    # metaView(thumb_frame_left,thumb_frame_right,isThumbView=True,isDesView=False,isTagsView=False,isScheduleView=False)

    tab_control.add(tags_frame, text=settings[locale]["tagsView"])

    tagsView(tags_frame_left, tags_frame_right, lang)
    # metaView(tags_frame_left,tags_frame_right,isThumbView=False,isDesView=False,isTagsView=True,isScheduleView=False)

    tab_control.add(des_frame, text=settings[locale]["desView"])

    desView(des_frame_left, des_frame_right, lang)
    # metaView(des_frame_left,des_frame_right,isThumbView=False,isDesView=True,isTagsView=False,isScheduleView=False)

    tab_control.add(schedule_frame, text=settings[locale]["scheduleView"])

    scheduleView(schedule_frame_left, schedule_frame_right, lang)
    # metaView(schedule_frame_left,schedule_frame_right,isThumbView=False,isDesView=False,isTagsView=False,isScheduleView=True)

    tab_control.add(meta_frame, text=settings[locale]["metaView"])
    metaView(
        meta_frame_left,
        meta_frame_right,
        isThumbView=True,
        isDesView=True,
        isTagsView=True,
        isScheduleView=True,
    )
    # metaView(meta_frame_left,meta_frame_right,lang)
    # metaView(meta_frame_right,meta_frame_left,lang)

    tab_control.add(upload_frame, text=settings[locale]["uploadView"])
    # uploadView(upload_frame_left,upload_frame_right,lang)
    uploadView(upload_frame_left, upload_frame_left, lang, async_loop)

    statsView(stats_frame, root, lang)

    tab_control.add(stats_frame, text=settings[locale]["statsView"], sticky="nswe")

    tab_control.add(doc_frame, text=settings[locale]["docView"])

    docView(doc_frame_left, doc_frame_right, lang)
    # tab_control.pack(expand=1, fill='both')
    tab_control.grid(row=0, column=0, sticky="nswe")

    log_tab_frame = ttk.Frame(tab_control)
    # log_frame.grid_rowconfigure((0,1), weight=1)
    # log_frame.grid_columnconfigure((0,1), weight=1 )
    log_tab_frame.grid_rowconfigure(1, weight=1)

    log_tab_frame.grid_columnconfigure(1, weight=1)
    logView(log_tab_frame, root, lang)

    tab_control.add(log_tab_frame, text=settings[locale]["logView"], sticky="nswe")

    pluginsView(stats_frame, root, lang)

    tab_control.add(plugins_frame, text=settings[locale]["pluginsView"], sticky="nswe")

    Cascade_button = tk.Menubutton(window)
    # Cascade_button.pack(side=tk.LEFT, padx="2m")

    # the primary pulldown
    Cascade_button.menu = tk.Menu(Cascade_button)

    # this is the menu that cascades from the primary pulldown....
    Cascade_button.menu.choices = tk.Menu(Cascade_button.menu)

    # definition of the menu one level up...
    Cascade_button.menu.choices.add_command(
        label="zh", command=lambda: changeDisplayLang("zh")
    )
    Cascade_button.menu.choices.add_command(
        label="en", command=lambda: changeDisplayLang("en")
    )
    Cascade_button.menu.add_cascade(
        label=settings[locale]["chooseLang"], menu=Cascade_button.menu.choices
    )

    Cascade_button.menu.loglevel = tk.Menu(Cascade_button.menu)

    # definition of the menu one level up...
    Cascade_button.menu.loglevel.add_command(
        label="DEBUG", command=lambda: logger.setLevel("DEBUG")
    )
    Cascade_button.menu.loglevel.add_command(
        label="INFO", command=lambda: logger.setLevel("INFO")
    )
    Cascade_button.menu.loglevel.add_command(
        label="WARNING", command=lambda: logger.setLevel("WARNING")
    )
    Cascade_button.menu.loglevel.add_command(
        label="ERROR", command=lambda: logger.setLevel("ERROR")
    )
    Cascade_button.menu.loglevel.add_command(
        label="CRITICAL", command=lambda: logger.setLevel("CRITICAL")
    )

    Cascade_button.menu.add_cascade(
        label=settings[locale]["loglevel"], menu=Cascade_button.menu.loglevel
    )

    menubar = tk.Menu(window)

    menubar.add_cascade(label=settings[locale]["settings"], menu=Cascade_button.menu)

    root.config(menu=menubar)
    # return langchoosen.get()


def start(lang, root=None, async_loop=None):
    global mainwindow, canvas

    root.geometry(window_size)
    # root.resizable(width=True, height=True)
    root.iconbitmap("assets/icon.ico")
    root.title(settings[locale]["title"])

    # Create the frame for the notebook
    mainwindow = ttk.Frame(root)
    mainwindow.grid(row=0, column=0, sticky="nsew")

    # mainwindow.grid_rowconfigure(0, weight=1)
    # mainwindow.grid_columnconfigure(0, weight=1)
    # mainwindow.grid_columnconfigure(1, weight=1)

    logger.debug(f"TiktokaStudio Installation path is:{ROOT_DIR}")

    logger.debug("TiktokaStudio GUI started")
    render(root, mainwindow, lang, async_loop)
    root.update_idletasks()


# # Set the initial size of the notebook frame (4/5 of total height)
# mainwindow_initial_percentage = 5 / 6


# Calculate the initial height of mainwindow based on the percentage
# initial_height = int(float(height) * mainwindow_initial_percentage)
# mainwindow.config(height=initial_height)
def all_children(window):
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    return _list


def changeDisplayLang(lang):
    mainwindow.destroy()

    global locale

    # root.quit()
    settings["lastuselang"] = lang
    locale = lang
    start(lang, root)
    settings["locale"] = lang

    logger.debug(f"switch lang to locale:{lang}")

    root.mainloop()


def quit_window(icon, item):

    print('cancel all waiting tasks')

    # threading.Thread(
    #             target=cancerlall()
    #         ).start()
    asyncio.run(cancerlall())
    print('Shutdown icon')
    icon.stop()

    print('Shutdown server')
    if uvicorn_subprocess is not None:
        uvicorn_subprocess.terminate()
        time.sleep(0.5)
        done=uvicorn_subprocess.poll()
        if done==None:
            print(f'server shutdown error :{done}')

        else:
            print('server shutdown')
    else:
        print('server not started')
    if uvicorn_subprocess.returncode is  None:
        print('check result server is there ')
        parent = psutil.Process(uvicorn_subprocess.pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
    else:
        print('check result server is shutdown already')

    print('Shutdown root')
    # https://github.com/insolor/async-tkinter-loop/issues/10
    root.quit()
    root.destroy()



def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def withdraw_window():
    root.withdraw()
    image = Image.open("assets/icon.ico")
    menu = (item("Quit", quit_window), item("Show", show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run_detached()
    # icon.run()


def start_fastapi_server():
    global uvicorn_subprocess
    uvicorn_command = ["uvicorn", "fastapiserver:app", "--host", "0.0.0.0", "--port", "8000"]
    uvicorn_subprocess = subprocess.Popen(uvicorn_command)
    try:
        outs, errs = uvicorn_subprocess.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        uvicorn_subprocess.kill()
        outs, errs = uvicorn_subprocess.communicate()




def start_tkinter_app(async_loop):
    global root, settings, db, canvas, locale
    tmp["accountlinkaccount"] = {}

    root = tk.Tk()
    # async_executor.submit(run_in_thread, 3).then(print_result)
    load_setting()
    load_citydb()
    # print('---',settings)
    locale = settings["lastuselang"]
    start(locale, root, async_loop)

    settings["folders"] = tmp
    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    settings["locale"] = locale
    dumpSetting(settingfilename)

    root.mainloop()


if __name__ == "__main__":
    global loop, fastapi_thread
    loop = None
    mode='debug'

    if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


    if sys.platform == 'win32':

        asyncio.get_event_loop().close()
        # On Windows, the default event loop is SelectorEventLoop, which does
        # not support subprocesses. ProactorEventLoop should be used instead.
        # Source: https://docs.python.org/3/library/asyncio-subprocess.html
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    # Start FastAPI server in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi_server).start()

    start_tkinter_app(loop)
    # loop.run_forever()
    # loop.close()