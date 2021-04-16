---
layout: post
title: FFmpeg - Convert Video to MP3
tags:
  - ffmpeg
  - video
  - mp3
  - extract
---

FFmpeg can easily be used to extract the audio tracks from virtually all video files and save them to new audio files:

### Copy audio track from video file:

This example assumes that the video's audio track is already an MP3 so can be simply copied over without re-encoding.

`ffmpeg - i video.mkv -acodec copy audio.mp3`

### Convert audio track to MP3 (CBR):

This example assumes that the video's audio track is something other than MP3 (or whatever target format you want). FFmpeg will re-encode the audio track so you can also specify some additional quality options.

`ffmpeg -i video.mkv -b:a 192K -vn audio.mp3`

In this command we specify the that the bit rate of the new audio file will be a constant 192kb/s (CBR).

### Convert audio track to variable bit rate MP3 (VBR)

This command creates a variable bit rate (VBR) MP3 instead of the CBR file as in the above example. This will reduce the size of the new MP3, but may sacrifice some quality.

`ffmpeg -i video.mkv -q:a 0 -map a audio.mp3`