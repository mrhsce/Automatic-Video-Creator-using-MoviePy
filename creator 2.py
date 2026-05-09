# By MrHs
"""
This script makes a video file by repeating a base video until it reaches the
requested length, then cropping an audio file and adding a static title number.
"""

import os

from moviepy.editor import AudioFileClip
from moviepy.editor import CompositeVideoClip
from moviepy.editor import TextClip
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

from video_tools import Video
from video_tools import min2sce
from video_tools import prepare_rtl_text


def main():
    videoArray = []
    outputFolder = "project_6/"
    videoClipFileName = outputFolder + "veisi.mp4"
    audioClipfFileName = outputFolder + "shora.wma"

    videoArray.append(Video("شورا", "9", 1, 55, 10, 13))
    videoArray.append(Video("شورا", "10", 10, 13, 14, 45))
    videoArray.append(Video("شورا", "11", 14, 47, 22, 16))
    videoArray.append(Video("شورا", "12", 27, 27, 32, 43))
    videoArray.append(Video("شورا", "13", 43, 37, 44, 32))

    os.makedirs(outputFolder, exist_ok=True)

    baseVideoClip = VideoFileClip(videoClipFileName)
    baseLength = baseVideoClip.duration

    try:
        for video in videoArray:
            startTime = min2sce(video.startTime_sec, video.startTime_min)
            endTime = min2sce(video.endTime_sec, video.endTime_min) + 1
            length = endTime - startTime

            if length <= 0:
                continue

            repeat = int(length // baseLength)
            remaining = length - (baseLength * repeat)
            movieList = [baseVideoClip] * repeat
            if remaining != 0:
                movieList.append(baseVideoClip.subclip(0, remaining))
            videoClip = concatenate_videoclips(movieList)

            artext = prepare_rtl_text("(" + video.number + ")")
            txtclip = TextClip(artext, fontsize=150, font="fonts/b_n_b.ttf", color="black")
            videoClip = CompositeVideoClip([videoClip, txtclip.set_pos(lambda t: ("center", 600))]).set_duration(videoClip.duration)

            audio = AudioFileClip(audioClipfFileName).subclip(startTime, endTime)
            videoClip = videoClip.set_audio(audio)
            videoClip = videoClip.resize(0.5)
            videoClip.write_videofile(outputFolder + video.title + "_" + video.number + ".mp4", fps=10)
    finally:
        baseVideoClip.close()


if __name__ == "__main__":
    main()
