import logging
from collections.abc import Callable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings

logger = logging.getLogger(__name__)


def apply_image_pipeline(image_path: Path, fn: Callable):
    img = _load_image_rgb(image_path)
    with img:
        img = _process(fn, img)
        _thumbnail_to_screen(img)
        _save_as_jpg(img, Settings.output_path)


def _load_image_rgb(image_path: Path) -> Image.Image:
    with Image.open(image_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img


def _process(fn: Callable, img: Image.Image) -> Image.Image:
    return fn(img)


def _thumbnail_to_screen(img: Image.Image) -> None:
    with img:
        img.copy()
        img.thumbnail((Settings.screen_width, Settings.screen_height))


def _save_as_jpg(img: Image.Image, output_dir: Path) -> None:
    try:
        with img:
            img.save(output_dir, "JPEG", quality=100)
    except OSError as e:
        logger.error(f"Error processing: {e}")
