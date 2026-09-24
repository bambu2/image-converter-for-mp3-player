import logging
from collections.abc import Callable
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def apply_image_pipeline(
    image_path: Path, fn: Callable, output_dir: Path, stem: str, settings
):
    with Image.open(image_path) as img:
        img = _convert_rgb(img)
        for i, result in enumerate(fn(img, settings)):
            _thumbnail_to_screen(result, settings=settings)
            _save_as_jpg(result, output_dir, f"{stem}_{i}")


def _convert_rgb(img: Image.Image) -> Image.Image:
    if img.mode != "RGB":
        img = img.convert("RGB")
    return img


def _thumbnail_to_screen(img: Image.Image, settings) -> None:
    with img:
        img.copy()
        img.thumbnail((settings.screen_width, settings.screen_height))


def _save_as_jpg(img: Image.Image, output_dir: Path, stem: str) -> None:
    try:
        with img:
            img.save(output_dir / f"{stem}.jpg", "JPEG", quality=100)
    except OSError as e:
        logger.error(f"Error processing: {e}")
