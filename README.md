# autovideo



>there are some cash cow guys having their own custom software plus robot voice over that does everything for them automatically. the robot sounds human like and they monetize it nicely.

>the bot also scrapes articles automatically daily, spins words, makes unique sentences, auto edits, and also auto posts the videos.

ytb_up GUI demo 

Dirty code but works


## yt-dlp support

```

# yt-dlp "bilisearch100:雷电将军" --config-location config.txt
#config.txt
# -o "./%(extractor_key)s/[%(channel_id)s] %(uploader)s/[%(upload_date)s] %(title)s [%(id)s].%(ext)s"
# -ciw
# --console-title
# --extractor-args "youtube:player_client=android,web;comment_sort=top;max_comments=1000"
# --yes-playlist
# --remux-video flv>mp4
# --merge-output-format mp4
# --no-embed-sub
# --no-clean-infojson
# --write-thumbnail
# --sub-lang all
# --convert-subtitles srt
# --write-description
# --write-info-json
# --convert-thumbnails png
# --no-write-comments
# --embed-metadata
# --parse-metadata "title:(?s)(?P<meta_title>.+)"
# --parse-metadata "uploader:(?s)(?P<meta_artist>.+)"
# --parse-metadata " : (?P<meta_synopsis>.*)"
# --parse-metadata " : (?P<meta_album>.*)"
# --abort-on-unavailable-fragment
# --no-write-playlist-metafiles
```


```
#yt-dlp  --config-location config.txt https://www.youtube.com/results?search_query=%23dentaldigest
yt-dlp "bilisearch500:申鹤mmd" --config-location down.txt 

cd D:\\Download\\audio-visual\\UCBBj-A2EqL5pNApsLhoeM6w\\shenhe
# cd D:\\Download\\audio-visual\\UCBBj-A2EqL5pNApsLhoeM6w\\BiliBili

# remove green from template

#remove space in filename


while [ "$(find ./ -regex '.* .*' | wc -l)" -gt 0 ];
    do filename="$(find ./ -regex '.* .*' | head -n 1)"
    mv "$filename" "$(echo "$filename" | sed 's|'" "'|_|g')"
done


for filename in ./*.flv; do   
    echo $filename
    name=$(echo "$filename" | sed 's/\.[^.]*$//')
    echo $name
    if [ -e "${name}-shenhe.mp4" ]
    then
        echo "compilation video exist-----------"

        rm "${name}-overlay.mp4"   
    else
        duration=$(ffprobe -i $filename -show_entries format=duration -v quiet -of csv="p=0")
        echo $duration
        ffmpeg -n -stream_loop  -1 -i ../overlay.mp4 -t $duration -c copy  $name-overlay.mp4

        ffmpeg -n -i $filename  -i $name-overlay.mp4 -filter_complex "[1:v]colorkey=0x34d454:0.3:0.15[ckout];[0:v][ckout]overlay[despill];[despill] despill=green[colorspace];[colorspace]format=yuv420p[out]" -map "[out]" -map 0:a -c:a copy  $name-shenhe.mp4

        rm "${filename}-overlay.mp4"   

    fi      

done


```
source code:

https://github.com/wanghaisheng/ytb-up
