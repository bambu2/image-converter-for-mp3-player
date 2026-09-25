import logging
from collections.abc import Callable, Iterable
from pathlib import Path

import typer
from PIL import Image
from rich.progress import track

from image_converter_for_mp3_player.config import (
    BlurSettings,
    EquidistantCropSettings,
    OverlapGridCropSettings,
)
from image_converter_for_mp3_player.utils import (
    Orientation,
    apply_image_pipeline,
    get_image_paths,
)

logger = logging.getLogger(__name__)


def process[S: BlurSettings | OverlapGridCropSettings | EquidistantCropSettings](
    fn: Callable[[Image.Image, Orientation, S], Iterable[Image.Image]],
    settings: S,
) -> None:
    try:
        image_paths = get_image_paths(settings.input_dir, settings)
    except (NotADirectoryError, FileNotFoundError, PermissionError) as e:
        logger.error(f"Error processing: {e}")
        raise typer.Exit(1)

    if settings.dry_run:
        print(f"[DRY RUN] input_dir: {settings.input_dir}")
        for image_path in image_paths:
            print(f"[DRY RUN] image_path: {image_path}")
        print(f"[DRY RUN] output_dir: {settings.output_dir}")
    else:
        settings.output_dir.mkdir(parents=True, exist_ok=True)
        apply_pipeline(fn, image_paths, settings)


def apply_pipeline[S: BlurSettings | OverlapGridCropSettings | EquidistantCropSettings](
    func: Callable[[Image.Image, Orientation, S], Iterable[Image.Image]],
    image_paths: list[Path],
    settings: S,
) -> None:
    for image_path in track(image_paths, description="Processing images"):
        try:
            apply_image_pipeline(
                image_path, func, settings.output_dir, image_path.stem, settings
            )
        except (IsADirectoryError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Error processing: {e}")
            raise typer.Exit(1)
