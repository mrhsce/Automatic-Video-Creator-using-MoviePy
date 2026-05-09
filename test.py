import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from moviepy.editor import ColorClip
from moviepy.editor import CompositeVideoClip
from moviepy.editor import ImageClip


def annotate(clip, txt, txt_color="red", fontsize=50, font="fonts/b_n_b.ttf"):
    """Write a text label near the bottom of the clip."""
    font_obj = ImageFont.truetype(font, fontsize)
    probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    probe_draw = ImageDraw.Draw(probe)
    bbox = probe_draw.textbbox((0, 0), txt, font=font_obj)
    text_width = bbox[2] - bbox[0] + 20
    text_height = bbox[3] - bbox[1] + 20

    text_img = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    draw.text((10, 10 - bbox[1]), txt, font=font_obj, fill=txt_color)

    txtclip = ImageClip(np.array(text_img))
    cvc = CompositeVideoClip([clip, txtclip.set_pos(("center", "bottom"))])
    return cvc.set_duration(clip.duration)


def main():
    clip = ColorClip(size=(640, 360), color=(0, 0, 0), duration=2)
    annotated_clip = annotate(clip, "Salam")
    annotated_clip.write_videofile("hi.mp4", fps=24)


if __name__ == "__main__":
    main()
