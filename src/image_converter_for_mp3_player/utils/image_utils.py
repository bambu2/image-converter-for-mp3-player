import logging
from collections.abc import Callable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import settings

logger = logging.getLogger(__name__)


def apply_image_pipeline(image_path: Path, fn: Callable, output_dir: Path, stem: str):
    img = _load_image_rgb(image_path)
    with img:
        img = _process(fn, img)
        _thumbnail_to_screen(img)
        _save_as_jpg(img, output_dir, stem)


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
        img.thumbnail((settings.screen_width, settings.screen_height))


def _save_as_jpg(img: Image.Image, output_dir: Path, stem: str) -> None:
    try:
        with img:
            img.save(output_dir / f"{stem}.jpg", "JPEG", quality=100)
    except OSError as e:
        logger.error(f"Error processing: {e}")


# FIXME: img.save for a real file name
