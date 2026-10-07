# Image Converter for MP3 Player

## Features
- Support 4 different modes: `blur`, `equidistant-crop`, `extreme-crop`, `auto`
- Convert images to suitable size and format(.jpg) for MP3 player
- Avoid image stretching issues on MP3 player
- Support auto orientation and auto processing

## Usage

### Install
```bash
uv install -e .
```

### Run
```bash
uv run python -m image_converter_for_mp3_player.main auto
```

## Main Directory Structure

```
image-converter-for-mp3-player
├─ .python-version
├─ LICENSE
├─ README.md
├─ pyproject.toml
├─ src
│  └─ image_converter_for_mp3_player
│     ├─ __init__.py
│     ├─ core
│     │  ├─ __init__.py
│     │  ├─ config.py
│     │  └─ logging.py
│     ├─ main.py
│     ├─ services
│     │  ├─ __init__.py
│     │  ├─ background_blur.py
│     │  ├─ dispatcher.py
│     │  └─ equidistant_crop.py
│     └─ utils
│        ├─ __init__.py
│        ├─ image_utils.py
│        ├─ orientation.py
│        └─ path_utils.py
└─ uv.lock

```

## License
MIT