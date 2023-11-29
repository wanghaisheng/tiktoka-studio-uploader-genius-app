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
from glob import glob

import os,random
def using_free_music(music_folder,inputmp4,ratio):

    if os.path.exists(inputmp4):

        print('video exists', inputmp4)
    else:
        print('video not found')
    try:
        music_folder
    except:
        music_folder='assets/freemusic'


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
        try:
            ratio
        except:
            ratio=1
        audioclip = audioclip.fx( afx.volumex, float(ratio))
        audioclip.write_audiofile(videofilename+'.mp3')

        audioclip = volumex(audioclip,ratio)          
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
def batchchangebgmusic(folder):

    # use all available CPUs
    # p = mp.Pool(initializer=init_worker, initargs=(memorizedPaths,
    #                                                filepaths,
    #                                                cutoff))
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
                    using_free_music(folder,f)
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

