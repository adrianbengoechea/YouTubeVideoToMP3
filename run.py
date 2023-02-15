# IMPORT LIBRARIES
import urllib.request
import music_tag
import os
import numpy as np
import tkinter as tk
import random
import threading
import time

from pytube import YouTube
from moviepy.editor import *
from PIL import Image

# +++++++++++++++++++++++++++
# DEFAULT VALUES

rid = str(random.randrange(0, 999999999, 8))
download_thread = '';


videoMetaData = {
  'title': '',
  'artist': '',
  'genre': '',
  'album': '',
}

defaultPath = {
  'video': './resources/videos/',
  'thumbnail': './resources/thumbnails/',
  'audio': './downloaded/',
}

defaultName = {
  'video': 'hqvideo_' + rid +'.mp4', 
  'audio': 'song_' + rid +'.mp3',
  'thumbnail': 'hqthumbnail_' + rid +'.jpg'
}





def GetYTvideoInBackground(video):
  download_thread = threading.Thread(target=YoutubeDownloadVideo, args=[video])
  download_thread.start()

  title = input('Title: ')
  artist = input('Artist: ')
  genre = input('Genre: ')
  album = input('Album: ')

  videoMetaData['title'] = title
  videoMetaData['artist'] = artist
  videoMetaData['genre'] = genre
  videoMetaData['album'] = album

  count = 2
  while(download_thread.is_alive()):
    count += 1
    time.sleep(1)
    print('Downloading' + (count * '.'))
    continue
  
  print('Download Completed!')
  YoutubeVideoToMP3()
  

# FUNCTIONS
def YoutubeDownloadVideo(videoURL):
  video = YouTube(videoURL)

  # DOWNLOAD YOUTUBE VIDEO FILE
  try:
    youtubeVideo = video.streams[2]
    youtubeVideo.download(defaultPath['video'], defaultName['video'])
    # print('> Video Downloaded!')
  except:
    print("> Youtube Video Process Error.")
  


  # DOWNLOAD YOUTUBE THUMBNAIL FILE

  try:
    YouTubeThumbnailURL = video.thumbnail_url 
    urllib.request.urlretrieve(YouTubeThumbnailURL, defaultPath['thumbnail'] + defaultName['thumbnail'])

    image = Image.open(r"" + defaultPath['thumbnail'] + defaultName['thumbnail'])
    art_dimensions = (300, 300)
    image.thumbnail(art_dimensions)
    image.save(defaultPath['thumbnail'] + defaultName['thumbnail'])


   

    # print('> Thumbnail Downloaded!')
  except:
    print('> Thumbnail Process Error.')





def MP4toMP3():
  # TRANSFORM MP4 TO MP3
  print('> Transforming from MP4 to MP3 ...')
  try:
    mp4VideoClip = VideoFileClip(defaultPath['video'] + defaultName['video'])
    mp4AudioClip = mp4VideoClip.audio

    mp4AudioClip.write_audiofile(defaultPath['audio'] + defaultName['audio'])

    mp4AudioClip.close()
    mp4VideoClip.close()
    print('> MP3 File Created!')
  except:
    print('> MP4 Transformation Process Error.')


def MP3UpdateMetadata(f_path):

  # GET MP3 VALUES
  
  print('====================')


  f = music_tag.load_file(f_path)
  new_filename_mp3 = videoMetaData['title'] + " - " + videoMetaData['artist'] + ".mp3"

  # print(f)
  # print(defaultPath['audio'] + filename_mp3)

  # UPDATE MP3 METADATA

  print("> Updating Title")
  f['title'] = videoMetaData['title']
  print("> Updating Artist")
  f['artist'] = videoMetaData['artist']
  print("> Updating Genre")
  f['genre'] = videoMetaData['genre']
  print("> Updating Album")
  f['album'] = videoMetaData['album']


  with open(defaultPath['thumbnail'] + defaultName['thumbnail'], 'rb') as img_in:
    f['artwork'] = img_in.read() 
  


  f.save()

  os.rename(defaultPath['audio'] + defaultName['audio'], defaultPath['audio'] + new_filename_mp3)

  print("====================")
  print("> MP3 INFO")
  print("Filename: " + new_filename_mp3)
  print("Title: " + videoMetaData['title'])
  print("Artist: " + videoMetaData['artist'])
  print("Genre: " + videoMetaData['genre'])
  print("Album: " + videoMetaData['album'])


def YoutubeVideoToMP3():
    try:
      MP4toMP3()
      MP3UpdateMetadata(defaultPath['audio'] + defaultName['audio'])
      print('********************************')
      print('* MP3 Downloaded Successfully! *')
      print('********************************')
    except:
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
      print(' Something went wrong, please try again. ')
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')





# EXECUTE
YouTubeVideoURL = input('Youtube Video URL: ')
GetYTvideoInBackground(YouTubeVideoURL)





