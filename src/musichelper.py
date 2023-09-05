    def download_song(self, file_name, link):
        ydl_opts = {
            'outtmpl': './'+file_name,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
            'prefer_ffmpeg': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)

        pass

https://github.com/zhangxin6/free_music

https://github.com/GyanMcaptain/yt-audio-library
