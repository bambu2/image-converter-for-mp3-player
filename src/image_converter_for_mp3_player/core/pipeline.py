import logging
from collections.abc import Callable
from pathlib import Path

import typer
from rich.progress import track

from image_converter_for_mp3_player.utils import apply_image_pipeline, get_image_paths

logger = logging.getLogger(__name__)


def apply_pipeline(input_dir: Path, output_dir: Path, fn: Callable):
    try:
        image_paths = get_image_paths(input_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for image_path in track(image_paths, description="Processing images"):
            try:
                apply_image_pipeline(image_path, fn)
            except (IsADirectoryError, FileNotFoundError, PermissionError) as e:
                logger.error(f"Error processing: {e}")
                raise typer.Exit(1)

    except (NotADirectoryError, FileNotFoundError, PermissionError) as e:
        logger.error(f"Error processing: {e}")
        raise typer.Exit(1)
