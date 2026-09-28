import logging
from collections.abc import Callable, Iterable

import typer
from PIL import Image
from rich.progress import track

from image_converter_for_mp3_player.core.config import Settings
from image_converter_for_mp3_player.utils import (
    Orientation,
    post_process,
    get_image_paths,
    get_orientation,
)

logger = logging.getLogger(__name__)


def apply_pipeline(
    func: Callable[[Image.Image, Orientation, Settings, float], Iterable[Image.Image]],
    settings: Settings,
) -> None:
    settings.output_dir.mkdir(parents=True, exist_ok=True)

    image_paths = get_image_paths(settings)
    if not image_paths:
        logger.info("No images found.")
        raise typer.Exit()
    else:
        for path in track(image_paths, description="Processing images"):
            try:
                with Image.open(path) as img:
                    orientation = get_orientation(
                        img.size,
                        (settings.landscape_width, settings.landscape_height),
                        settings.threshold,
                    )
                    post_process(img_iter=, output_dir=output_dir, stem=path.stem, settings=settings)
            except OSError as e:
                logger.error(f"Error processing: {e}")
                raise typer.Exit(code=1)
