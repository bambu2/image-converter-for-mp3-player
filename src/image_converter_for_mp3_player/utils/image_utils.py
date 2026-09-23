import logging
from collections.abc import Callable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings

logger = logging.getLogger(__name__)


def traverse_folder(folder: Path) -> list[Path]:
    if Settings.recursive:
        return [p for p in folder.rglob("*") if p.suffix.lower() in Settings.img_exts]
    else:
        return [p for p in folder.glob("*") if p.suffix.lower() in Settings.img_exts]


def load_image_rgb(image_path: Path) -> Image.Image:
    with Image.open(image_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img


def process(fn: Callable, img: Image.Image) -> Image.Image:
    return fn(img)


def thumbnail_to_screen(img: Image.Image) -> None:
    with img:
        img.copy()
        img.thumbnail((Settings.screen_width, Settings.screen_height))


def save_as_jpg(img: Image.Image, output_path: Path) -> bool:
    try:
        with img:
            img.save(output_path, "JPEG", quality=100)
        return True
    except OSError as e:
        logger.error(f"Error processing: {e}")
        return False


def apply_pipeline(input_path: Path, output_path: Path, fn: Callable):
    image_paths = traverse_folder(input_path)
    for image_path in image_paths:
        with load_image_rgb(image_path) as img:
            img = process(fn, img)
            thumbnail_to_screen(img)
            save_as_jpg(img, output_path)
