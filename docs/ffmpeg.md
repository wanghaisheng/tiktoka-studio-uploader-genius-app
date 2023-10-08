Video Harmonization Tool

https://github.com/ozeliurs/harmopy



compress

https://github.com/kbdevs/kbclip



https://github.com/trek-view/gopro2gsv


https://github.com/NangInShell/VSET



# metadata remove

https://github.com/Anish-M-code/Metadata-Remover/blob/master/Source%20Code/Python%20Source%20Code/MRT/mat2.py


## multi lang audio track 

https://github.com/etherealxx/audiomerger-volumetweak


## extract metadata as json 

ffprobe -v quiet -show_format -show_streams -print_format json input.mp4


ffprobe -v quiet -show_format -print_format json input.mp4
https://github.com/hclivess/nameer/blob/main/nameer.py


##  embed metadata 




https://gist.github.com/sk22/d97a15638256a785fa3ca4cde29024e2


# ffmpeg command cheat sheet

<!--
################################################################################
-->

## ts + vtt subtitles + jpeg thumbnail

* mkv tags: https://www.matroska.org/technical/tagging.html

```bash
ffmpeg -i *.ts -i *.vtt -attach *.jpeg \
  -c copy \
  -metadata title="insert title here" \
  -metadata description="insert description here" \
  -metadata date_released=2020 \
  -metadata:s:t:0 mimetype=image/jpeg -metadata:s:t:0 filename=cover_land.jpg \
  -metadata:s:a:0 language=ger -metadata:s:s:0 language=ger \
  output.mkv
```
```bash
  -c:v libx265 # re-encode as hevc
```

## attach cover.jpg to mkv

* source: https://www.reddit.com/r/ffmpeg/comments/fw4jnh/how_to_make_ffmpeg_keep_attached_images_in_mkv_as/
* cover art specifications: https://www.matroska.org/technical/attachments.html

```bash
ffmpeg -i video.mkv -attach cover.jpg -attach small_cover.jpg -map 0 -c copy \
  -metadata:s:t mimetype=image/jpg \
  -metadata:s:t:0 filename=cover.jpg \
  -metadata:s:t:1 filename=small_cover.jpg \
  out.mkv
```

## scale (e.g.) cover image

* source: https://trac.ffmpeg.org/wiki/Scaling
* cover art specifications: https://www.matroska.org/technical/attachments.html

```bash
ffmpeg -i vert-cover-original.jpg -vf scale=600:-1 cover.jpg
ffmpeg -i vert-cover-original.jpg -vf scale=120:-1 small_cover.jpg
ffmpeg -i land-cover-original.jpg -vf scale=-1:600 cover_land.jpg
ffmpeg -i land-cover-original.jpg -vf scale=-1:120 small_cover_land.jpg
```

## extract cover image

```bash
ffmpeg -i movie.mkv -map 0:v -map -0:V -c copy cover.jpg
```

mapping: include video streams, exclude all normal video streams

## convert to hevc, keep all metadata and other streams, re-add cover image

```bash
ffmpeg -i input-x264.mkv -attach cover.jpg -c copy -c:v libx265 \
  -map 0 -map -0:v:m:filename \
  -metadata:s:t:0 mimetype=image/jpeg -metadata:s:t:0 filename=cover.jpg \
  output-x265.mkv
```

* doesn't properly copy input's cover images, apparently?
  hence re-adding manually
* codecs: copy all, use `libx265` for video streams
* mapping:
  1. include all streams from input 0
  2. exclude the video stream with metadata `filename`
     (which only the cover art video stream has)

## subtitles offset (in seconds; `hh:mm:ss.mmm`)

```bash
ffmpeg -itsoffset 22 -i f.mkv -c copy subtitles.vtt
```

## concat videos

https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg

```
file '/path/to/file1'
file '/path/to/file2'
file '/path/to/file3'
```

> to quickly generate a list of all (matching) files, use this bash script line:
> 
> ```bash
> find -type f -name '*.mp4' | sed "s/.*/file \'&\'/" | tee files.txt
> ```

```bash
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4
```

## trim video

* starting at 0:30, ending 10 seconds later (0:40)

```bash
ffmpeg -ss 00:00:30.0 -i input.mp4 -c copy -t 00:00:10.0 output.mp4
# or:
ffmpeg -ss 00:00:30.0 -i input.mp4 -c copy -to 00:00:40.0 output.mp4
```

> “Note that -t is an output option and always needs to be specified after -i.”
> – https://superuser.com/questions/138331/using-ffmpeg-to-cut-up-video

### make a gif

https://superuser.com/questions/556029/how-do-i-convert-a-video-to-gif-using-ffmpeg-with-reasonable-quality

```bash
ffmpeg -ss 30 -t 3 -i input.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif
```

### re-encode, add cover, add metadata for episodes

* http://ffmpeg.org/pipermail/ffmpeg-user/2018-December/042231.html
* https://wiki.multimedia.cx/index.php/FFmpeg_Metadata
* itunes metadata list in ffmpeg source code http://git.videolan.org/?p=ffmpeg.git;f=libavformat/movenc.c;h=6dab519;hb=HEAD#l3508
  * as linked in http://ffmpeg.org/pipermail/ffmpeg-user/2018-December/042234.html

```bash
ffmpeg -i Angekommen*.mp4 \
  -filter:v "crop=in_w:in_h-64:0:32" \
  -c:v libx265 \
  -attach cover.jpg -attach small_cover.jpg \
  -metadata language="deu" \
  -metadata description="Juana, a 17-year-old wheelchair user, aims to explore her sexuality but is ashamed of her body. Trying to find her place in a new high school, she will go through failure, friendship, fear and politics until she builds her own pride." \
  -metadata:s:v:0 language="deu" \
  -metadata:s:a:0 language="spa" \
  -metadata:s:t mimetype=image/jpg \
  -metadata:s:t:0 filename=cover.jpg \
  -metadata:s:t:1 filename=small_cover.jpg \
  -metadata show="1 Meter 20" \
  -metadata release_date=2021 \
  -metadata season_number=1 \
  -metadata title="Angekommen" \
  -metadata episode_sort=1 \
  "1 Meter 20 - S01E01 - Angekommen.mkv"
```

## mkvpropedit

https://mkvtoolnix.download/doc/mkvpropedit.html

```bash
mkvinfo movie.mkv
```

### set title

```bash
mkvpropedit movie.mkv --set title="The Movie"
```

### get attachments

```bash
mkvextract movie.mkv attachments 1:cover.jpg
```

### set attachment

```bash
mkvpropedit movie.mkv --add-attachment movie-cover.jpg \
  --attachment-name cover.jpg --attachment-mime-type "image/jpeg"
```

### add subtitles

https://superuser.com/questions/609113/how-to-add-and-remove-subtitles-in-an-mkv-file

```bash
mkvmerge -o output.mkv --language 0:ger \
  input.mkv subs.srt
```

### list languages

```bash
mkvmerge --list-languages | grep German
```

## random snippets

```js
let convTime = (h, m, s, ms) => ms + s * 1000 + m * 1000 * 60 + h * 1000 * 60 * 60
let convText = text => convTime(...Array.from(text.split(/:|\./)).map(t => Number(t)))

['00:55:08.54', ..., '00:03:10.44'].forEach(t => console.log(convText))
// => [3341000, ..., 3308054]

// array of chapter lengths
[3341000, ..., 3308054].reduce((pre, cur) => { console.log(pre, pre + cur - 1); return pre + cur }, 0)

let toTime = m => `${Math.floor(m % (1000 * 60 * 60 * 60) / 1000 / 60 / 60)}:${Math.floor(m % (1000 * 60 * 60) / 1000 / 60)}:${Math.floor(m % (1000 * 60) / 1000)}.${m % 1000}`
```

```bash
# get current titles from mkv files and write them to titles.txt
for f in **/*.mkv; do echo $f >> titles.txt; mkvinfo $f | grep Title >> titles.txt; done
# then i used visual studio code to change titles and format the lines to form this command:
mkvpropedit "videofile1.mkv" -s title="video title 1"
```

### concat seperate audio/video segment and merge them

```
find -name 'seg-*-f1-a*' | sort -V | while read f; do cat $f >> audio.ts; done
find -name 'seg-*-f9-v*' | sort -V | while read f; do cat $f >> video.ts; done
ffmpeg -i video.ts -i audio.ts -map 0:v -map 1:a -c copy output.mp4
```

## to be continued.



FFmpeg 安装
如果您没有 FFmpeg，那么 FFBox 只能为您输出命令行，不能进行转码工作。您需要在 FFmpeg 下载页面 下载 FFmpeg 后，放到程序文件夹中，或者将其放到一个位置并添加环境变量，FFBox 即可进行转码工作。

Windows
从 此处 下载 FFmpeg。Version 可以选择最新，但如果使用硬件加速时遇到需要更新显卡驱动的问题，则需要使用旧一点的版本。Linking 请选择 static。 添加到环境变量的操作请查阅 这里 。

Linux
从 此处 下载 FFmpeg。请选择 static 的包。

macOS
从 此处 下载 FFmpeg。



silence

https://github.com/bradsec/desilence/blob/main/desilence.sh


https://github.com/shadax1/yt_concat

https://github.com/HeminWon/mediarchiver、


https://github.com/cdgriffith/FastFlix


https://github.com/wanghaisheng/reddit-video-creator




https://github.com/freemocap/skelly_synchronize

This package synchronizes a set of videos of the same event by cross-correlating their audio files. The videos will be synchronized so that they all start at the earliest shared time, and end at the latest shared time.

