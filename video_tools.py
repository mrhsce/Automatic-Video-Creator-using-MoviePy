"""Shared helpers for the video generation scripts."""

import arabic_reshaper
from bidi.algorithm import get_display


def min2sce(sec, minute=0):
    """Convert minutes + seconds to total seconds."""
    return sec + minute * 60


def prepare_rtl_text(text):
    """Shape Arabic/Persian text for right-to-left display."""
    return get_display(arabic_reshaper.reshape(text))


class Video:
    """Container for clip metadata.

    Supports both call styles used in the existing scripts:

    - Video(title, start_min, start_sec, end_min, end_sec, font=..., inputName=...)
    - Video(title, number, start_min, start_sec, end_min, end_sec)
    """

    def __init__(self, title, *args, **kwargs):
        self.title = title
        self.font = kwargs.pop("font", 95)
        self.inputClip = kwargs.pop("inputName", kwargs.pop("inputClip", "input.m4a"))
        self.number = kwargs.pop("number", "")

        if args:
            if len(args) == 4:
                self.startTime_min, self.startTime_sec, self.endTime_min, self.endTime_sec = args
            elif len(args) == 5:
                self.number, self.startTime_min, self.startTime_sec, self.endTime_min, self.endTime_sec = args
            else:
                raise TypeError(
                    "Video() expects either 4 positional time arguments or a number plus 4 time arguments"
                )
        else:
            required = ["startTime_min", "startTime_sec", "endTime_min", "endTime_sec"]
            missing = [name for name in required if name not in kwargs]
            if missing:
                raise TypeError(f"Video() missing required keyword arguments: {', '.join(missing)}")
            self.startTime_min = kwargs.pop("startTime_min")
            self.startTime_sec = kwargs.pop("startTime_sec")
            self.endTime_min = kwargs.pop("endTime_min")
            self.endTime_sec = kwargs.pop("endTime_sec")

        if kwargs:
            unexpected = ", ".join(sorted(kwargs))
            raise TypeError(f"Video() got unexpected keyword arguments: {unexpected}")

