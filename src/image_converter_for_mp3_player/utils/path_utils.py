import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_image_paths(dir: Path, settings) -> list[Path]:
    if settings.recursive:
        return [p for p in dir.rglob("*") if p.suffix.lower() in settings.img_exts]
    else:
        return [p for p in dir.glob("*") if p.suffix.lower() in settings.img_exts]
