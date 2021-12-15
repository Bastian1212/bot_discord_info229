from __future__ import unicode_literals
import youtube_dl
import os 

## BY: Bastián Villanueva 

def descargaMusic(url):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
            pass

    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            
            ydl.download([url])
        except PermissionError:
            return False
    for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

    return True



