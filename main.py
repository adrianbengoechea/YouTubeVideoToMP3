# IMPORT LIBRARIES
import urllib.request
import music_tag
import os
import numpy as np

from pytube import YouTube
from moviepy.editor import *
from PIL import Image

# PATHS
mp4_save_path = "F:/YoutubeDownloadedMusic/mp4/"
mp3_save_path = "F:/YoutubeDownloadedMusic/mp3/"

# FILENAMES
filename_mp4 = "hqvideo.mp4"
filename_mp3 = "song.mp3"
filename_jpg = "hqthumbnail.jpg"

# FUNCTIONS
def YoutubeGetVideo(video, custom_thumbnail_url = ""):


  # DOWNLOAD YOUTUBE VIDEO FILE
  try:
    youtubeVideo = video.streams[2]
    youtubeVideo.download(mp4_save_path, filename_mp4)
    print('> Video Downloaded!')
  except:
    print("> Youtube Video Process Error.")
  


  # DOWNLOAD YOUTUBE THUMBNAIL FILE
    print(custom_thumbnail_url)
  try:
    if custom_thumbnail_url.strip() != "":
      YouTubeThumbnailURL = custom_thumbnail_url
    else:
      YouTubeThumbnailURL = video.thumbnail_url
      
    urllib.request.urlretrieve(YouTubeThumbnailURL, mp4_save_path + filename_jpg)

    image = Image.open(r"" + mp4_save_path + filename_jpg)
    art_dimensions = (512, 512)
    image.thumbnail(art_dimensions)
    image.save(mp4_save_path + filename_jpg)


   

    print('> Thumbnail Downloaded!')
  except:
    print('> Thumbnail Process Error.')



  # TRANSFORM MP4 TO MP3
  try:
    mp4VideoClip = VideoFileClip(mp4_save_path + filename_mp4)
    mp4AudioClip = mp4VideoClip.audio

    mp4AudioClip.write_audiofile(mp3_save_path + filename_mp3)

    mp4AudioClip.close()
    mp4VideoClip.close()
    print('> MP3 File Created!')
  except:
    print('> MP4 Transformation Process Error.')


def MP3UpdateMetadata(f_path):

  # # MP3 VALUES
  title = input('MP3 Title: ')
  artists = input('MP3 Artist: ')
  genre = input('MP3 Genre: ')
  album = input('MP3 Album: ')
  print('====================')


  f = music_tag.load_file(f_path)
  new_filename_mp3 = title + " - " + artists + ".mp3"

  # print(f)
  # print(mp3_save_path + filename_mp3)

  print("> Updating Title")
  f['title'] = title
  print("> Updating Artist")
  f['artist'] = artists
  print("> Updating Genre")
  f['genre'] = genre
  print("> Updating Album")
  f['album'] = album


  with open(mp4_save_path + filename_jpg, 'rb') as img_in:
    f['artwork'] = img_in.read() 
  


  f.save()

  os.rename(mp3_save_path + filename_mp3, mp3_save_path + new_filename_mp3)

  print("====================")
  print("> MP3 INFO")
  print("Filename: " + new_filename_mp3)
  print("Title: " + title)
  print("Artist: " + artists)
  print("Genre: " + genre)
  print("Album: " + album)


def YoutubeVideoToMP3( video_url = False ):
  if video_url:
    video = YouTube(video_url)

    

    try:
      YoutubeGetVideo(video)
      MP3UpdateMetadata(mp3_save_path + filename_mp3)
      print('********************************')
      print('* MP3 Downloaded Successfully! *')
      print('********************************')
    except:
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
      print(' Something went wrong, please try again. ')
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# VIDEO GET USER VALUES




# DO PROCESS
youtube_video_url = input('Youtube Video URL: ')
YoutubeVideoToMP3(youtube_video_url)
  
  





