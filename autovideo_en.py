#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import threading

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.editor import concatenate_videoclips, concatenate_audioclips, TextClip, CompositeVideoClip
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
# here put the import lib
import json
import tkinter as tk
from tkinter import OptionMenu, filedialog
import os
import base64
import subprocess
import sys
import random
import os
import time
from datetime import timedelta, date, datetime
# import multiprocessing.dummy as mp
import concurrent
from glob import glob
from src.dbmanipulation import *
from src.UploadSession import *
from PIL import Image
import multiprocessing as mp
import calendar
from src.upload1 import *
from src.ai_detector import AiThumbnailGenerator
from datetime import datetime, date, timedelta
import asyncio
import requests
import re


# dbname = "reddit_popular"
# Open the database and make sure there is a table with appopriate indices

def url_ok(url, proxy_option=''):

    try:
        if not proxy_option == '':

            proxies = {
                'http': proxy_option,
                'https': proxy_option,
            }
            print('use proxy', proxy_option)
            response = requests.head(url, proxies=proxies)
        else:
            response = requests.head(url)

    except Exception as e:
        # print(f"NOT OK: {str(e)}")
        return False
    else:
        print('status code', response.status_code)
        if response.status_code == 200:
            # print("OK")
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
    """Edited from https://stackoverflow.com/questions/44231509/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black"""
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
            print('loading latest Used setting file')

            fp = open(settingfile, 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
        except:
            print('load default setting template')
            fp = open("./assets/config/demo.json", 'r', encoding='utf-8')
            setting_json = fp.read()
            fp.close()
    else:
        print('load default setting template')
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


# 加载剧本
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


settingid = 0
# 保存配置


def save_setting():
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
        video_folder_path = video_folder.get()
    except NameError:
        print('no new  video_folder_path,using existing setting',
              setting['video_folder'])
    if video_folder_path:
        if os.path.exists(video_folder_path):
            setting['video_folder'] = video_folder_path
        else:
            print('we can not find this video foler', video_folder_path)
    try:
        channel_cookie_path = channel_cookie.get()
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
                print('we cannot find cookie file', channel_cookie_path)
    try:
        music_folder_path = music_folder.get()
    except NameError:
        # print('no new  music_folder,using existing setting',
        #   setting['music_folder'])
        music_folder = setting['music_folder']
        # print(music_folder)
    else:
        if music_folder_path:
            setting['music_folder'] = music_folder_path

    setting['ratio'] = ratio.get()

    setting['dailycount'] = dailycount.get()
    setting['channelname'] = channelname.get()
    setting['start_publish_date'] = start_publish_date.get()

    setting['preferdesprefix'] = preferdesprefix.get()
    setting['preferdessuffix'] = preferdessuffix.get()
    setting['proxy_option'] = proxy_option_value
    setting['prefertags'] = prefertags.get()
    setting['publishpolicy'] = publishpolicy.get()
    if setting['publishpolicy'] == '':
        setting['publishpolicy'] = 1
    if setting['start_publish_date'] == '':
        setting['start_publish_date'] = '1'
    if setting['channelname'] is None or setting['channelname'] == '':
        print('before save setting,you need input channelname')
    else:
        if setting['video_folder'] is None or setting['video_folder'] == '':
            print('before save setting,you need input video_folder')
        else:
            if os.path.exists(channel_cookie_path):

                abspath = os.path.abspath('.')
                newsetting = setting
                # json.dumps(setting, indent=4, separators=(',', ': '))
                # print('setting after edited ',setting)
                if os.path.exists('./assets/config/'+setting['channelname']+".json"):
                    with open('./assets/config/'+setting['channelname']+".json", 'r') as fr:
                        exitingsetting = json.loads(fr.read())
                        # print('old same setting file ',exitingsetting)
                        # print('changes ',type(newsetting),type(exitingsetting))
                        if ordered(newsetting) == ordered(exitingsetting):
                            print('no change at all')
                            settingid = Add_New_UploadSetting_In_Db(newsetting)

                            print("setting saved ok", settingid)

                        else:
                            print('new change will be saved')
                        with open('./assets/config/'+setting['channelname']+".json", 'w') as f:
                            f.write(json.dumps(setting, indent=4,
                                    separators=(',', ': ')))
                        settingid = Add_New_UploadSetting_In_Db(setting)
                        print("setting saved ok", settingid)
                        with open('latest-used-setting.txt','w+') as fw:
                            fw.write('./assets/config/'+setting['channelname']+".json")                        
                else:
                    with open(abspath+os.sep+'/assets/config/'+setting['channelname']+".json", 'w') as f:

                        f.write(json.dumps(setting, indent=4,
                                separators=(',', ': ')))
                # print('当前使用的配置为：', setting)

                    settingid = Add_New_UploadSetting_In_Db(setting)
                    print("setting saved ok", settingid)
                    with open('latest-used-setting.txt','w+') as fw:
                        fw.write('./assets/config/'+setting['channelname']+".json")                    
            else:
                print('pls check cookie is there, or is it broken file',
                      channel_cookie_path)


def select_profile_folder():
    global firefox_profile_folder_path
    firefox_profile_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
    if os.path.exists(firefox_profile_folder_path):
        firefox_profile_folder_path = str(firefox_profile_folder_path)
        print("You chose %s" % firefox_profile_folder_path)
        firefox_profile_folder.set(firefox_profile_folder_path)
        # setting['firefox_profile_folder'] = firefox_profile_folder


def select_videos_folder():
    global video_folder_path
    video_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
    if len(video_folder_path) > 0:
        print("You chose %s" % video_folder_path)
        video_folder.set(video_folder_path)
        setting['video_folder'] = video_folder_path


def select_musics_folder():
    global music_folder_path
    music_folder_path = filedialog.askdirectory(
        parent=root, initialdir="/", title='Please select a directory')
    if len(music_folder_path) > 0:
        print("You chose %s" % music_folder_path)
        music_folder.set(music_folder_path)
        setting['music_folder'] = music_folder_path


docsopen = False


def docs():
    global docsopen

    if docsopen == False:
        docsopen = True
        print('show help doc')
        helptext_setting = "==============\n1.install Firefox by yourself,create new profile,\nsee https://support.mozilla.org/en-US/kb/using-multiple-profiles\n2.install firefox extension:Cookie-Editor,login into youtube manually,export cookie.json\n3.find more free music at \nhttps://icons8.com/music/\n=====================\n1.before started,you need a upload setting file,you can import a template to edit as you wish,\nwe got 3 template for you,private、public和schedule,\nsee at assets/config/setting-template.json,Caution:after edit any field you should save it\n======\nvideo folder path:open Menu to choose or manually edit in the UI\n==========\nPreferTags:usually each channel got some prefined tags,\neven bunch of videos got prefined tags,you can defined here.\nother specific tag we recommend you leave them in video filename\n=======\nvideo prefer des prefix:usually each channel got a des template,such as Part A+Part B+PartC\n=========\nvideo des suffix:you can put copyright statements here\n==========\npublish policy:0==private draft，1==publish instantly 2==schedule some time,with daily publish count and days offset(starting publish date,1 means start to set uploaded video public from tomorrow,7 means a week later etc ),\nyou can manage the publish date of each video+1\n==========\nchannel name:we use this field to save uploadsetting files\n=======\ncookie json:please use extension to export one\n==========\n2.if you got videos and thumbnail already,you should load uploadsetting file,\nsave uploadsetting file,create uploadsession,finally start upload.for those you only got videos,we can use a dumb AI to extract clip from videos as thumbnail automatically\n===========\nsometimes you may need batch replace the audio with free music,you can set free music folder and control audio volumn setting to find a better result \n3.leave message at tiktokaofficial@gmail.com "

        newWindow = tk.Toplevel(root)
        label_helptext_setting = tk.Label(
            newWindow, text=helptext_setting, anchor='e', justify='left')
        label_helptext_setting.pack()

    else:
        docsopen = False


def install():
    # subprocess.check_call([sys.executable, "-m", "playwright ", "install"])
    subprocess.check_call(["playwright ", "install"])


def testinstall():
    print('playwright install')
    install()


def testsettingok():
    print('upload default demo video')


headless = True


def watchuploadsteps():
    global headless

    if headless == False:
        headless = True
    else:
        headless = False


def select_setting_file():

    global setting_file
    setting_file = filedialog.askopenfilenames(title="choose setting file", filetypes=[
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
    music_folder_path = setting['music_folder']
    publishpolicy.set(setting['publishpolicy'])
    music_folder.set(music_folder_path)
    ratio.set(setting['ratio'])


def select_cookie_file():

    global channel_cookie_path
    channel_cookie_path = filedialog.askopenfilenames(title="choose cookie file for this channel", filetypes=[
        ("Json", "*.json"), ("All Files", "*")])[0]

    channel_cookie.set(channel_cookie_path)
    setting['channelcookiepath'] = channel_cookie_path


# 清理残留文件

def threadusing_free_musichelper(numbers):

    using_free_music(numbers[0], numbers[1])


def using_free_music(setting, inputmp4):

    if os.path.exists(inputmp4):

        print('video exists', inputmp4)
    else:
        print('video not found')
    try:
        music_folder = setting['music_folder']
    except:
        music_folder = 'assets/freemusic'

    else:
        print('setting==', setting)

        music_folder = setting['music_folder']

    freemusic = []

    for ext in ('*.mp3', '*.wav', '*.wma', '*.ogg', '*.aac', '*.mp4'):
        freemusic.extend(glob(os.path.join(music_folder, ext)))

    if len(freemusic) > 0:

        soundeffect = random.choice(freemusic)
        print('randomly choose a background music', soundeffect)
        ext = os.path.splitext(soundeffect)[1]
        videoext = os.path.splitext(inputmp4)[1]
        videofilename = os.path.splitext(inputmp4)[0]

        print('videoext', videoext)
        print('videofilename', videofilename)
        oldvideofiles = []
        if not ext in ['.mp4', '.wma', '.aac', '.ogg', '.wav', '.mp3']:

            print('we have not found wav,mp3 background music in this folder', freemusic)
        else:
            audioclip = AudioFileClip(soundeffect)

            os.rename(inputmp4, videofilename+'-old'+videoext)
            videoclip = VideoFileClip(videofilename+'-old'+videoext)
            if audioclip.duration > videoclip.duration:
                audioclip = audioclip.subclip(0, videoclip.duration)
            else:
                audioclip = vfx.loop(audioclip, duration=videoclip.duration)
            if setting['ratio']:
                pass
            else:
                setting['ratio'] = 1
            audioclip = audioclip.fx(afx.volumex, float(setting['ratio']))
            # audioclip = volumex(audioclip,setting['ratio'])
            videoclip = videoclip.set_audio(audioclip)

            videoclip.write_videofile(
                videofilename+'.mp4', threads=0, audio=False)


def init_worker(mps, fps, cut):
    global memorizedPaths, filepaths, cutoff
    global DG

    print("process initializing", mp.current_process())
    memorizedPaths, filepaths, cutoff = mps, fps, cut
    DG = 1  # nx.read_gml("KeggComplete.gml", relabel = True)


def batchchangebgmusic():
    folder = setting['video_folder']
    # oldvideofiles=[]
    videofiles = []
    if os.path.exists(folder):
        m = mp.Manager()
        memorizedPaths = m.dict()
        filepaths = m.dict()
        cutoff = 1
        # use all available CPUs
        p = mp.Pool(initializer=init_worker, initargs=(memorizedPaths,
                                                       filepaths,
                                                       cutoff))

        if os.path.isdir(folder):
            print('this is a directory', folder)

            for ext in ('*.flv', '*.mp4', '*.avi'):
                videofiles.extend(glob(os.path.join(folder, ext)))
            print('detecting videos in folder', folder, videofiles)
            if len(videofiles) > 0:
                arguments = []
                for i, f in enumerate(videofiles):
                    videofilename = os.path.splitext(f)[0]
                    videoext = os.path.splitext(f)[1]
                    if not videofilename.endswith('-old'):
                        arguments.append((setting, f))
                    else:
                        oldvideofiles.append(f)
                print('awaiting convert files', videofiles)
                # degreelist = range(100000) ##
                for _ in p.imap_unordered(threadusing_free_musichelper, arguments, chunksize=500):
                    pass
        p.close()
        p.join()

        print('start cleaning old video files')
        oldvideofiles = []

        if os.path.isdir(folder):

            for ext in ('*.flv', '*.mp4', '*.avi'):
                oldvideofiles.extend(glob(os.path.join(folder, ext)))
            # print('this is a directory',folder)

        for f in oldvideofiles:
            videofilename = os.path.splitext(f)[0]

            if videofilename.endswith('-old'):
                print('start cleaning old video file', f)
                os.remove(f)
        print('finish cleaning old video files')
    else:
        print('pls choose a video folder first')


def changebgmusic():
    folder = setting['video_folder']
    if os.path.isdir(folder):
        print('this is a directory', folder)

        videofiles = []
        for ext in ('*.flv', '*.mp4', '*.avi'):
            videofiles.extend(glob(os.path.join(folder, ext)))
        print('detecting videos in folder', folder, videofiles)
        if len(videofiles) > 0:
            # for i,f in enumerate(videofiles):

            #     videofiles.append(f)
            print('awaiting convert files', videofiles)
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

    # save_setting()
    # 文件夹下是否有视频文件

    # 视频文件是否有同名的图片

    try:
        video_folder_path = setting['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            print("sure, it was defined dir.")

            check_video_thumb_pair(video_folder_path, False)
        else:
            print("pls choose file or folder")


def createuploadsession():
    # save_setting()
    # 文件夹下是否有视频文件

    # 视频文件是否有同名的图片

    try:
        video_folder_path = setting['video_folder']

    except NameError:
        print('not found fastlane folder  file')
    else:
        if video_folder_path:
            if os.path.exists(video_folder_path):
                check_video_thumb_pair(video_folder_path, True)
            else:
                print("there is no defined video dir.")
        else:
            print("pls choose file or folder")


def check_video_thumb_pair(folder, session):
    # print('detecting----------',folder)

    for r, d, f in os.walk(folder):
        with os.scandir(r) as i:
            print('detecting----------', r)
            videopair=0

            for entry in i:
                if entry.is_file():
                    filename = os.path.splitext(entry.name)[0]
                    ext = os.path.splitext(entry.name)[1]
                    print(filename,' with extension ',ext)

                    start_index = 1
                    if ext in ('.flv', '.mp4', '.avi','.mkv','.mov'):
                        videopath = os.path.join(r, entry.name)
                        count = 0
                        exist_image_ext = ''
                        for image_ext in ['.jpeg', '.png', '.jpg']:
                            thumbpath = os.path.join(r, filename+image_ext)

                            if not os.path.exists(thumbpath):
                                count += 1
                            else:
                                exist_image_ext = image_ext
                        if count == len(['.jpeg', '.png', '.jpg']):
                            no = random.choice(['001', '002', '003'])
                            if not os.path.exists(os.path.join(r, filename+'-'+no+'.jpg')):
                                generator = AiThumbnailGenerator(videopath)

                                thumbpath = os.path.join(
                                    r, filename+'-'+no+'.jpg')
                                print('generated thumbnail is', thumbpath)
                        else:
                            thubmpath = os.path.join(
                                r, filename+exist_image_ext)
                            print(
                                'thumbnail is there.if you need create,pls delete the old one')
                        if session:
                            print(videopath, thumbpath, filename,
                                  start_index, setting['channelname'], settingid)

                            prepareuploadsession(
                                videopath, thumbpath, filename, start_index, setting['channelname'], settingid)
                        start_index = start_index+1
                        videopair+=1
            if videopair==0:
                print('we could not find any video,prefer format mp4,mkv,flv,mov')

def prepareuploadsession(videopath, thumbpath, filename, start_index, channelname, settingid):
    global uploadsessionid
    isadded, isuploaded = Query_video_status_in_channel(
        videopath, channelname, settingid)

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
        filename = filename.split(os.sep)[-1]
        des = filename
        if preferdesprefix:

            des = preferdesprefix+'========\n'+des
        if preferdessuffix:
            des = des+'=========\n'+preferdessuffix
        des = des[:4900]
        title = isfilenamevalid(filename)
        if len(filename) > 100:
            title = filename[:90]
        nowtime = time.time()
        videoid = b64e(filename)

        olddata = UploadSession()
        olddata.uploadSettingid = settingid
        olddata.videoid = videoid
        olddata.channelname = setting['channelname']
        publishpolicy = setting['publishpolicy']
        start_publish_date = setting['start_publish_date']
        olddata.publishpolicy = publishpolicy
        today = date.today()
        publish_date = datetime(today.year, today.month, today.day, 20, 15)

        if publishpolicy == 0:
            print('video got be private')
            olddata.publish_date = publish_date
        elif publishpolicy == 1:
            olddata.publish_date = publish_date
            print('video got be instant public')

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

            print('video got be schedule to public at ',publish_date)

            olddata.publish_date = publish_date
        olddata.thumbpath = thumbpath
        olddata.title = title
        olddata.des = des
        olddata.videopath = videopath
        olddata.tags = tags
        olddata.status = False
        uploadsessionid = Add_New_UploadSession_In_Db(olddata)
        print('add 1 new videos ', filename,
              'for upload session', uploadsessionid)


def upload():
    print('we got setting proxy ,', setting['proxy_option'])
    try:
        uploadsessionid
        if uploadsessionid is None:
            print('weir error', uploadsessionid)
            createuploadsession()
    except:

        createuploadsession()
        print('before upload,you need create upload session first')

    videos = Query_undone_videos_in_channel()
    print('there is ', len(videos), ' video need to uploading for task ')

    if len(videos) > 0:
        publicvideos = []
        privatevideos = []
        othervideos = []
        if url_ok('http://www.google.com'):
            print('network is fine,there is no need for proxy ')
            setting['proxy_option'] = ""
            print('start browser in headless mode', headless)

        else:
            print('google can not be access ')

            print('we need for proxy ', setting['proxy_option'])
            print('start browser in headless mode',
                  headless, setting['proxy_option'])
        upload = YoutubeUpload(
            # use r"" for paths, this will not give formatting errors e.g. "\n"
            root_profile_directory=setting['firefox_profile_folder'],

            proxy_option=setting['proxy_option'],
            watcheveryuploadstep=headless,
            # if you want to silent background running, set watcheveryuploadstep false
            CHANNEL_COOKIES=setting['channelcookiepath'],
            username='username',
            password='password',
            recordvideo=headless
            # for test purpose we need to check the video step by step ,
        )

        for video in videos:

            if int(video.publishpolicy) == 1:
                print('add public uploading task video', video.videopath)

                publicvideos.append(video)
            elif int(video.publishpolicy) == 0:
                print('add private uploading task video', video.videopath)

                privatevideos.append(video)
            else:
                print('add schedule uploading task video', video.videopath)
                print('intended to public at ',video.publish_date,type(video.publish_date))
                othervideos.append(video)
        if len(publicvideos) > 0:
            print('start public uploading task')
            asyncio.run(bulk_instantpublish(
                videos=publicvideos, upload=upload))
        if len(privatevideos) > 0:
            print('start private uploading task')

            asyncio.run(bulk_privatedraft(videos=privatevideos, upload=upload))
        if len(othervideos) > 0:
            print('start schedule uploading task')

            asyncio.run(bulk_scheduletopublish_specific_date(
                videos=othervideos, upload=upload))


if __name__ == '__main__':

    gui_flag = 1

    # log_file = "log.txt"

    load_setting()

    if gui_flag:

        root = tk.Tk()
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

        l_music_folder = tk.Label(root, text="free music folder")
        l_music_folder.place(x=10, y=130)
        el_music_folder = tk.Entry(root, width=55, textvariable=music_folder)
        el_music_folder.place(x=150, y=130)

        l_prefertags = tk.Label(root, text="preferred tags")
        l_prefertags.place(x=10, y=50)
        el_prefertags = tk.Entry(root, width=55, textvariable=prefertags)
        el_prefertags.place(x=150, y=50)

        l_preferdesprefix = tk.Label(root, text="preferred des prefix")
        l_preferdesprefix.place(x=10, y=70)
        e_preferdesprefix = tk.Entry(
            root, width=55, textvariable=preferdesprefix)
        e_preferdesprefix.place(x=150, y=70)

        l_preferdessuffix = tk.Label(root, text="preferred des suffix")
        l_preferdessuffix.place(x=10, y=100)
        e_preferdessuffix = tk.Entry(
            root, width=55, textvariable=preferdessuffix)
        e_preferdessuffix.place(x=150, y=100)
        lratio = tk.Label(root, text="music volumn")
        lratio.place(x=10, y=150)
        elratio = tk.Entry(root, width=55, textvariable=ratio)
        elratio.place(x=150, y=150)

        l52 = tk.Label(root, text="publish policy")
        l52.place(x=10, y=170)
        e52 = tk.Entry(root, width=55, textvariable=publishpolicy)
        e52.place(x=150, y=170)

        l5 = tk.Label(root, text="daily publish count")
        l5.place(x=10, y=200)
        e5 = tk.Entry(root, width=55, textvariable=dailycount)
        e5.place(x=150, y=200)

        l5_start_publish_date = tk.Label(root, text="days offset")
        l5_start_publish_date.place(x=10, y=230)
        e5start_publish_date = tk.Entry(
            root, width=55, textvariable=start_publish_date)
        e5start_publish_date.place(x=150, y=230)

        l64 = tk.Label(root, text="channel name")
        l64.place(x=10, y=250)
        e64 = tk.Entry(root, width=55, textvariable=channelname)
        e64.place(x=150, y=250)

        l65 = tk.Label(root, text="video folder")
        l65.place(x=10, y=270)
        e65 = tk.Entry(root, width=55, textvariable=video_folder)
        e65.place(x=150, y=270)

        l66 = tk.Label(root, text="profile folder")
        # 暂时屏蔽
        # l66.place(x=10, y=300)
        # e66 = tk.Entry(root, width=55, textvariable=firefox_profile_folder)
        # e66.place(x=150, y=300)

        l67 = tk.Label(root, text="proxy")
        l67.place(x=10, y=330)
        e67 = tk.Entry(root, width=55, textvariable=proxy_option)
        e67.place(x=150, y=330)

        l68 = tk.Label(root, text="cookie json")
        l68.place(x=10, y=360)
        e68 = tk.Entry(root, width=55, textvariable=channel_cookie)
        e68.place(x=150, y=360)

        readbefore = tk.StringVar()
        readbefore.set('')
        lbreadbefore = tk.Label(root, text=readbefore)

        b5 = tk.Button(root, text="Read First", command=docs)
        b5.place(x=10, y=10)

        bselect_setting_file = tk.Button(
            root, text="load setting", command=select_setting_file)
        bselect_setting_file.place(x=10, y=400)

        btestinstall = tk.Button(
            root, text="test install", command=testinstall)
        btestinstall.place(x=100, y=10)

        btestsettingok = tk.Button(
            root, text="test config", command=testsettingok)
        btestsettingok.place(x=200, y=10)

        bsave_setting = tk.Button(
            root, text="save config", command=save_setting)
        bsave_setting.place(x=100, y=400)

        b61 = tk.Button(root, text="headless", command=watchuploadsteps)
        b61.place(x=280, y=10)

        b62 = tk.Button(root, text="batch replace audio",
                        command=threading.Thread(target=batchchangebgmusic).start)
        b62.place(x=350, y=10)
        b7 = tk.Button(root, text="start upload", command=threading.Thread(target=upload).start)
        b7.place(x=450, y=400)

        b8 = tk.Button(root, text="auto thumbnail", command=threading.Thread(target=autothumb).start)
        b8.place(x=200, y=400)

        b11 = tk.Button(root, text="create uploadsession",
                        command=createuploadsession)
        b11.place(x=300, y=400)

        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="browser setting", menu=filemenu)
        # filemenu.add_command(label="选择geckodriver文件",
        #  command=select_driver_file)
        filemenu.add_command(label="choose profile folder",
                             command=select_profile_folder)
        filemenu.add_command(label="choose cookie json",
                             command=select_cookie_file)

        filemenu2 = tk.Menu(menubar, tearoff=False)

        menubar.add_cascade(label="videos", menu=filemenu2)
        filemenu2.add_command(label="choose video folder",
                              command=select_videos_folder)
        filemenu2.add_command(label="choose music folder",
                              command=select_musics_folder)

        root.config(menu=menubar)
        # root.geometry('1280x720')
        root.geometry('530x440')
        root.title("youtube video auto upload GUI")
        root.resizable(width=False, height=False)
        root.iconbitmap("assets/icon.ico")
        root.mainloop()
