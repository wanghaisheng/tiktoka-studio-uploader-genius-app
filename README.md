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

source code:

https://github.com/wanghaisheng/ytb-up
