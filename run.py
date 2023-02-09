# IMPORT LIBRARIES
import urllib.request
import music_tag
import os
import numpy as np

from pytube import YouTube
from moviepy.editor import *
from PIL import Image

# +++++++++++++++++++++++++++
# DEFAULT VALUES
defaultPath = {
  'video': './resources/videos/',
  'thumbnail': './resources/thumbnails/',
  'audio': './downloaded/',
}

defaultName = {
  'video': 'hqvideo.mp4', 
  'audio': 'song.mp3',
  'thumbnail': 'hqthumbnail.jpg'
}


# FUNCTIONS
def YoutubeGetVideo(video, custom_thumbnail_url = ""):


  # DOWNLOAD YOUTUBE VIDEO FILE
  try:
    youtubeVideo = video.streams[2]
    youtubeVideo.download(defaultPath['video'], defaultName['video'])
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
      
    urllib.request.urlretrieve(YouTubeThumbnailURL, defaultPath['thumbnail'] + defaultName['thumbnail'])

    image = Image.open(r"" + defaultPath['thumbnail'] + defaultName['thumbnail'])
    art_dimensions = (512, 512)
    image.thumbnail(art_dimensions)
    image.save(defaultPath['thumbnail'] + defaultName['thumbnail'])


   

    print('> Thumbnail Downloaded!')
  except:
    print('> Thumbnail Process Error.')



  # TRANSFORM MP4 TO MP3
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
  title = input('MP3 Title: ')
  artists = input('MP3 Artist: ')
  genre = input('MP3 Genre: ')
  album = input('MP3 Album: ')
  print('====================')


  f = music_tag.load_file(f_path)
  new_filename_mp3 = title + " - " + artists + ".mp3"

  # print(f)
  # print(defaultPath['audio'] + filename_mp3)

  # UPDATE MP3 METADATA

  print("> Updating Title")
  f['title'] = title
  print("> Updating Artist")
  f['artist'] = artists
  print("> Updating Genre")
  f['genre'] = genre
  print("> Updating Album")
  f['album'] = album


  with open(defaultPath['thumbnail'] + defaultName['thumbnail'], 'rb') as img_in:
    f['artwork'] = img_in.read() 
  


  f.save()

  os.rename(defaultPath['audio'] + defaultName['audio'], defaultPath['audio'] + new_filename_mp3)

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
      MP3UpdateMetadata(defaultPath['audio'] + defaultName['audio'])
      print('********************************')
      print('* MP3 Downloaded Successfully! *')
      print('********************************')
    except:
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
      print(' Something went wrong, please try again. ')
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')





# EXECUTE
youtube_video_url = input('Youtube Video URL: ')
YoutubeVideoToMP3(youtube_video_url)
  
  





