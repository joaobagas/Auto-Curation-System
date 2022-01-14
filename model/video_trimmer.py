# This file holds the function which is used to crop frames off a video and save them.
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def trim(video, start, end, title):
    # End and start are displayed in seconds
    path = title[0] + ".mp4"
    ffmpeg_extract_subclip(video, start, end, targetname=path)
