# By MrHs
"""
This script makes a video file by adding a title to a static image and using it
as the background of the video whose sound is extracted by cropping an audio file.
"""

import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from moviepy.editor import AudioFileClip
from moviepy.editor import ImageClip

from video_tools import Video
from video_tools import min2sce
from video_tools import prepare_rtl_text


W, H = (1776, 1332)


def main():
    videoArray = []
    outputFolder = "project_/"
    backgroundFile = "background.png"
    tempImageFile = "tmp_img.png"

    # Add your clips here.
    # Example:
    # videoArray.append(Video("", 0, 0, 0, 10, font=95, inputName="input.m4a"))

    os.makedirs(outputFolder, exist_ok=True)

    try:
        for video in videoArray:
            reshaped_text = prepare_rtl_text(video.title)
            font = ImageFont.truetype("fonts/b_n_b.ttf", video.font)
            img = Image.open(backgroundFile)
            draw = ImageDraw.Draw(img)
            draw.text_alignment = "right"
            draw.text_antialias = True
            draw.text_encoding = "utf-8"
            w, h = draw.textsize(reshaped_text, font=font)
            draw.text_kerning = 0.0
            draw.text(((W - w) / 2, (H - h) / 2), reshaped_text, (0, 0, 0), font=font)
            img.save(tempImageFile)

            startTime = min2sce(video.startTime_sec, video.startTime_min)
            endTime = min2sce(video.endTime_sec, video.endTime_min) + 1
            audio = AudioFileClip(os.path.join(outputFolder, video.inputClip)).subclip(startTime, endTime)
            clip = ImageClip(img=tempImageFile, duration=(endTime - startTime)).set_audio(audio)
            clip.write_videofile(os.path.join(outputFolder, video.title + ".mp4"), fps=4)
    finally:
        if os.path.exists(tempImageFile):
            os.remove(tempImageFile)


if __name__ == "__main__":
    main()
