import logging
from pathlib import Path

from image_converter_for_mp3_player.core.config import Settings

logger = logging.getLogger(__name__)


def get_image_paths(settings: Settings) -> list[Path]:
    try:
        return _filter_image(settings.input_dir, settings.recursive, settings.img_exts)
    except OSError as e:
        logger.error(f"Error processing: {e}")
        raise OSError(f"Error processing: {e}")


def _filter_image(dir: Path, recursive: bool, img_exts: frozenset[str]) -> list[Path]:
    if recursive:
        return [p for p in dir.rglob("*") if p.suffix.lower() in img_exts]
    else:
        return [p for p in dir.glob("*") if p.suffix.lower() in img_exts]
