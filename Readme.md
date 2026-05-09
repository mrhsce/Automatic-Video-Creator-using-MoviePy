# Automatic Video Creator using MoviePy

This repository contains a small set of **MoviePy-based Python scripts** for generating short videos from existing audio/video sources and Arabic/Persian text.

The scripts were written as practical utilities for a specific workflow: take a lecture, sermon, or talk, split it into multiple segments, and render each segment as its own video with:

- a title or segment number overlaid on the video,
- right-to-left Arabic/Persian text rendering,
- optional logo or static background image support,
- audio cropped from a source file,
- output written into per-project folders such as `project_5/`, `project_6/`, and `project_7/`.

This is not a polished end-user application yet; it is a set of script templates and examples that you edit manually.

## What is in this repository?

### Main scripts

- `creator.py`  
  Builds a video from a **static background image** plus a title rendered as text, then attaches a cropped audio segment.

- `creator 2.py`  
  Repeats a **base video clip** until it matches the requested duration, overlays a number/title, and adds the matching audio segment.

- `creator 3.py`  
  Cuts **subclips from a longer source video**, adds a short title card at the beginning, overlays a logo, and exports the result.

- `test.py`  
  A small MoviePy/Pillow smoke test that renders text on a generated clip.

### Shared helpers

- `video_tools.py`  
  Shared utilities used by the scripts for time conversion, right-to-left text shaping, and the reusable `Video` container.

### Dependency manifest

- `requirements.txt`  
  Lists the Python packages needed to run the scripts.

### Sample project inputs

The `project_1/` to `project_7/` folders each contain a `code.txt` file with example `videoArray.append(...)` lines. These are meant to be copied into the appropriate script while preparing a batch of clips.

### Fonts

The `fonts/` directory contains the Arabic/Persian fonts used by the scripts:

- `fonts/b_n.ttf`
- `fonts/b_n_b.ttf`

## Repository layout

```text
AutomaticVideoCreator-master/
├── creator.py
├── creator 2.py
├── creator 3.py
├── requirements.txt
├── test.py
├── video_tools.py
├── Readme.md
├── fonts/
│   ├── b_n.ttf
│   └── b_n_b.ttf
├── project_1/
│   └── code.txt
├── project_2/
│   └── code.txt
├── project_3/
│   └── code.txt
├── project_4/
│   └── code.txt
├── project_5/
│   └── code.txt
├── project_6/
│   └── code.txt
└── project_7/
    └── code.txt
```

## How the scripts work

All of the scripts use the same general idea:

1. Define a `videoArray` with one entry per output clip.
2. Each entry stores:
   - title text,
   - optional clip number,
   - start time,
   - end time,
   - and, in some scripts, font size or input file name.
3. Convert the Arabic/Persian title using:
   - `arabic_reshaper` for shaping,
   - `bidi.algorithm.get_display()` for right-to-left display.
4. Build the final video using MoviePy.
5. Write each finished clip as an `.mp4` file into the selected project folder.

## Requirements

### Python packages

Install these Python dependencies:

- `moviepy<2` (the scripts use the classic `moviepy.editor` API)
- `Pillow`
- `arabic-reshaper`
- `python-bidi`

### System dependencies

MoviePy text rendering relies on **ImageMagick** in several places, especially in `creator 2.py` and `creator 3.py` because they use `TextClip`.

On Linux, you will usually also want:

- `ffmpeg`
- `imagemagick`

## Setup

### 1) Create and activate a virtual environment

```bash
cd /home/mrhs/workspace/github/AutomaticVideoCreator-master
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Install system packages

On Debian/Ubuntu-based Linux distributions:

```bash
sudo apt update
sudo apt install ffmpeg imagemagick
```

If your distribution uses a different package manager, install the equivalent `ffmpeg` and ImageMagick packages there.

### 4) Make sure the required assets exist

The checked-in code references several files that are **not included in this snapshot** of the repository, so you may need to provide them yourself:

- `background.png` for `creator.py`
- `project_*/input.m4a` or other audio files for `creator.py`
- `project_6/veisi.mp4` and `project_6/shora.wma` for `creator 2.py`
- `archive/logo.png` for `creator 3.py`
- `manaviat/manaviat.mp4` for `creator 3.py`

If you want the scripts to run successfully, create those files or update the paths in the scripts to match your actual media locations.

## Usage

### `creator.py`

This script:

- opens `background.png`,
- renders an Arabic/Persian title centered on the image,
- crops audio from `input.m4a` (or another file you specify),
- combines the image and audio into an MP4 video.

Typical workflow:

1. Open `creator.py`.
2. Replace the `videoArray.append(...)` lines with your own title and timestamps.
3. Set `outputFolder` and `inputName` to the right folder/file.
4. Ensure `background.png` exists.
5. Run:

```bash
python3 creator.py
```

> Note: the repository currently contains a placeholder `videoArray.append(Video("", , , , ))` line in `creator.py`. Replace it with a real `Video(...)` entry before running.

### `creator 2.py`

This script:

- loops a base video until it reaches the required duration,
- overlays the segment number as a text label,
- adds cropped audio,
- exports each result into the selected project folder.

Typical workflow:

1. Put the source video and audio files in the folder referenced by `outputFolder`.
2. Edit the `videoArray.append(...)` lines.
3. Run:

```bash
python3 "creator 2.py"
```

### `creator 3.py`

This script:

- cuts a subclip from a longer source video,
- creates a short 3-second title card,
- overlays a logo in the top-left corner,
- writes a finished segment to `project_7/`.

Typical workflow:

1. Place the source video at `manaviat/manaviat.mp4` or update the path.
2. Place the logo at `archive/logo.png` or update the path.
3. Fill in the `videoArray` lines.
4. Run:

```bash
python3 "creator 3.py"
```

### `test.py`

`test.py` is a quick MoviePy experiment for adding text to a clip. It is useful as a sanity check when you are testing fonts, ImageMagick, or MoviePy text rendering.

## How to use the `project_* / code.txt` files

The `code.txt` files are example input blocks. They typically contain only the `videoArray.append(...)` lines and, in some cases, supporting variable assignments like:

- `outputFolder = "project_6/"`
- `videoClipFileName = outputFolder + "veisi.mp4"`
- `audioClipfFileName = outputFolder + "shora.wma"`

You can copy those lines into the matching script, then adjust the file names and timestamps as needed.

## Notes about Arabic/Persian text

These scripts rely on `arabic_reshaper` and `python-bidi` because Arabic-script languages need shaping and right-to-left display handling.

If the text appears reversed, broken, or incorrectly spaced, check:

- the font file being used,
- whether the font supports the required characters,
- whether `arabic_reshaper.reshape(...)` and `get_display(...)` are both being applied,
- whether ImageMagick is installed and accessible.

## Troubleshooting

### TextClip fails or ImageMagick is not found

If you see errors related to `TextClip`, `convert`, or ImageMagick:

- make sure `imagemagick` is installed,
- verify the executable is on your system path,
- on Windows, you may need to set `IMAGEMAGICK_BINARY` manually in MoviePy.

### Font errors

If MoviePy or PIL cannot find the font:

- confirm `fonts/b_n_b.ttf` exists,
- update the font path in the script,
- make sure the font supports the characters you want to render.

### Missing media files

If a script fails because it cannot open a video, audio, or image file, check the paths hardcoded in the script and make sure the referenced files exist.

## Current project status

This repository looks like an **in-progress utility project** rather than a fully generalized application. The scripts are useful, but they still depend on manual editing and local media assets.

The original TODO ideas in the old README included:

- standardizing input/output and packaging to Windows EXE,
- reading timestamps and names from a text file,
- lowering audio before and after clips to reduce unwanted noise,
- automatically choosing a safe font size so text does not overflow.

## Suggested next steps

If you want to continue improving this project, good next steps would be:

1. Move the hardcoded `videoArray` setup into a text/CSV/JSON input file.
2. Add a single command-line interface for choosing the project and script mode.
3. Add automatic font sizing and text wrapping.
4. Add fades or audio normalization at the start/end of each clip.
5. Add a `requirements.txt` and a reproducible project setup.

## License / attribution

The source files are marked `# By MrHs`. If you plan to publish or redistribute the project, add an explicit license file so usage rights are clear.
