import logging
from pathlib import Path

from image_converter_for_mp3_player.config import settings

logger = logging.getLogger(__name__)


def get_image_paths(dir: Path) -> list[Path]:
    if settings.recursive:
        return [p for p in dir.rglob("*") if p.suffix.lower() in settings.img_exts]
    else:
        return [p for p in dir.glob("*") if p.suffix.lower() in settings.img_exts]
