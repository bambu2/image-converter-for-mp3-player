import logging
from collections.abc import Callable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings
from image_converter_for_mp3_player.utils.orientation import get_orientation

logger = logging.getLogger(__name__)


def apply_image_pipeline(
    image_path: Path, func: Callable, output_dir: Path, stem: str, settings: Settings
):
    with Image.open(image_path) as img:
        img = _convert_rgb(img)
        orientation = get_orientation(
            img.size,
            settings.landscape_resolution,
            settings.threshold,
        )
        for i, result in enumerate(func(img, orientation, settings)):
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


def axis_starts(img_size: int, crop_size: int, devision: int) -> list[int]:
    if devision == 1 or crop_size >= img_size:
        return [0]
    step = (img_size - crop_size) // (devision - 1)
    return [min(i * step, img_size - crop_size) for i in range(devision)]
