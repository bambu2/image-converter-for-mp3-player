import logging
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings

logger = logging.getLogger(__name__)


def traverse_folder(folder: Path, recursive: bool) -> list[Path]:
    if recursive:
        return [p for p in folder.rglob("*") if p.suffix.lower() in Settings.img_exts]
    else:
        return [p for p in folder.glob("*") if p.suffix.lower() in Settings.img_exts]


def load_image_rgb(image_path: Path) -> Image.Image:
    with Image.open(image_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img


def save_as_jpg(
    image: Image.Image,
    output_path: Path,
    quality: int = 100,
    optimize: bool = True,
) -> bool:
    try:
        image.save(output_path, "JPEG", quality=100)
        return True
    except OSError as e:
        logger.error(f"Error processing: {e}")
        return False
