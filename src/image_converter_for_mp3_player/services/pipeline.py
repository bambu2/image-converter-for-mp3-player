import logging
from collections.abc import Callable, Iterable
from pathlib import Path

import typer
from PIL import Image
from rich.progress import track

from image_converter_for_mp3_player.core.config import Settings
from image_converter_for_mp3_player.utils import (
    Orientation,
    get_image_paths,
    get_orientation,
    post_process,
)

logger = logging.getLogger(__name__)


def apply_pipeline(
    func: Callable[[Image.Image, Orientation, Settings], Iterable[Image.Image]],
    settings: Settings,
    output_dir: Path,
) -> None:
    image_paths = get_image_paths(settings)
    if not image_paths:
        logger.info("No images found.")
        raise typer.Exit()

    for path in track(image_paths, description="Processing images"):
        try:
            with Image.open(path) as img:
                orientation = get_orientation(
                    img.size,
                    settings.landscape_resolution,
                    settings.threshold,
                )
                img_iter = func(img, orientation, settings)
                post_process(
                    img_iter=img_iter,
                    size=settings.landscape_resolution,
                    output_dir=output_dir,
                    stem=path.stem,
                )
        except OSError as e:
            logger.error(f"Error processing: {e}")
            raise typer.Exit(code=1)
