# By MrHs
"""
This script makes subclips of a video file and adds a title card and logo.
"""

import os

from moviepy.editor import CompositeVideoClip
from moviepy.editor import ImageClip
from moviepy.editor import TextClip
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

from video_tools import Video
from video_tools import min2sce
from video_tools import prepare_rtl_text


def main():
    videoArray = []
    outputFolder = "project_7/"
    logoAddr = "archive/logo.png"
    videoClipFileName = "manaviat/manaviat.mp4"

    # videoArray.append(Video("معنویت", "1", 0, 0, 4, 54))
    # videoArray.append(Video("معنویت", "2", 4, 54, 10, 12))
    # videoArray.append(Video("معنویت", "3", 10, 12, 16, 11))
    # videoArray.append(Video("معنویت", "4", 16, 12, 25, 6))
    # videoArray.append(Video("معنویت", "5", 26, 10, 36, 1))
    # videoArray.append(Video("معنویت", "6", 36, 50, 42, 22))
    # videoArray.append(Video("معنویت", "7", 42, 23, 50, 8))
    # videoArray.append(Video("معنویت", "8", 58, 32, 63, 18))
    # videoArray.append(Video("معنویت", "9", 67, 48, 75, 6))
    # videoArray.append(Video("معنویت", "10", 75, 19, 81, 45))
    # videoArray.append(Video("معنویت", "11", 81, 49, 84, 43))
    # videoArray.append(Video("معنویت", "12", 85, 42, 95, 29))
    # videoArray.append(Video("معنویت", "13", 95, 30, 98, 52))
    # videoArray.append(Video("معنویت", "14", 99, 35, 107, 15))

    os.makedirs(outputFolder, exist_ok=True)

    sourceClip = VideoFileClip(videoClipFileName)

    try:
        for video in videoArray:
            titleText = "\n" + video.title + "\n" + "بخش" + " (" + video.number + ")" + "\n"
            artext = prepare_rtl_text(titleText)
            txtclip = TextClip(artext, fontsize=150, font="fonts/b_n_b.ttf", color="white").set_duration(3)

            startTime = min2sce(video.startTime_sec, video.startTime_min)
            endTime = min2sce(video.endTime_sec, video.endTime_min) + 1
            videoClip = sourceClip.subclip(startTime, endTime)
            logo = (
                ImageClip(logoAddr)
                .set_duration(videoClip.duration)
                .resize(height=100)
                .margin(left=180, top=15, opacity=0)
                .set_pos(("left", "top"))
            )

            videoClip = CompositeVideoClip([videoClip, logo])
            finalClip = concatenate_videoclips([txtclip, videoClip], method="compose")
            finalClip.write_videofile(os.path.join(outputFolder, video.title + "_" + video.number + ".mp4"))
    finally:
        sourceClip.close()


if __name__ == "__main__":
    main()
