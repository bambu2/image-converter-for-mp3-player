import logging
from pathlib import Path

from image_converter_for_mp3_player.config import BlurSettings, CropSettings

logger = logging.getLogger(__name__)


def get_image_paths(settings: BlurSettings | CropSettings) -> list[Path] | None:
    try:
        image_paths = _filter_image(
            settings.input_dir, settings.recursive, settings.img_exts
        )
    except (NotADirectoryError, FileNotFoundError, PermissionError) as e:
        logger.error(f"Error processing: {e}")
        raise

    if settings.dry_run:
        print(f"[DRY RUN] input_dir: {settings.input_dir}")
        print(f"[DRY RUN] image_paths: {image_paths}")
        print(f"[DRY RUN] output_dir: {settings.output_dir}")
        return None
    else:
        return image_paths


def _filter_image(dir: Path, recursive: bool, img_exts: frozenset) -> list[Path]:
    if recursive:
        return [p for p in dir.rglob("*") if p.suffix.lower() in img_exts]
    else:
        return [p for p in dir.glob("*") if p.suffix.lower() in img_exts]
