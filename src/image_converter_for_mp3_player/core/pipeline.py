import logging
from collections.abc import Callable, Iterable
from pathlib import Path

import typer
from PIL import Image
from rich.progress import track

from image_converter_for_mp3_player.config import (
    BlurSettings,
    CropSettings,
)
from image_converter_for_mp3_player.utils import Orientation, apply_image_pipeline

logger = logging.getLogger(__name__)


def apply_pipeline[S: BlurSettings | CropSettings](
    func: Callable[[Image.Image, Orientation, S], Iterable[Image.Image]],
    image_paths: list[Path],
    settings: S,
) -> None:
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    for image_path in track(image_paths, description="Processing images"):
        try:
            apply_image_pipeline(
                image_path, func, settings.output_dir, image_path.stem, settings
            )
        except (IsADirectoryError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Error processing: {e}")
            raise typer.Exit(1)
