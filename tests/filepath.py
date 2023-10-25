import binascii,base64,os
from pathlib import Path,PureWindowsPath,PurePath
path=r'D:\Download\audio-visual\saas\tiktoka\tiktoka-studio-uploader-genius\tests\videos\vertical\1.mp4'
video_local_path2="D:\/Download\/audio-visual\/saas\/tiktoka\/tiktoka-studio-uploader-genius\/tests\/videos\/vertical\\1.mp4"
video_local_path1="\/Users\/wenke\/github\/tiktoka-studio-uploader-app\/tests\/videos\/horizon\/OP.mp4"

print('======',PurePath(path)==PurePath(video_local_path2))
print('',os.path.exists(PurePath(path)),os.path.exists(PurePath(video_local_path2)))
parts=PurePath(path)
print(parts.parts)
PurePath
print(list(parts.parts))