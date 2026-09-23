import logging
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import CropSettings, PadSettings, Settings
from image_converter_for_mp3_player.core import (
    apply_blurred_background,
    apply_pipeline,
    crop_into_images,
)

logger = logging.getLogger(__name__)

logger.info("程序启动")

app = typer.Typer()


@app.command()
def pad(
    input_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ] = Settings.input_path,
    output_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            writable=True,
            resolve_path=True,
        ),
    ] = Settings.output_path,
    screen_resolution: Annotated[str, typer.Argument()] = Settings.screen_resolution,
    rotatable_aspect_ratio: Annotated[
        bool, typer.Option(help="allow to rotate the aspect ratio")
    ] = PadSettings.rotatable_aspect_ratio,
):
    apply_pipeline(input_dir, output_dir, apply_blurred_background)


@app.command()
def crop(
    input_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ] = Settings.input_path,
    output_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            writable=True,
            resolve_path=True,
        ),
    ] = Settings.output_path,
    screen_resolution: Annotated[str, typer.Argument()] = Settings.screen_resolution,
    rotatable_aspect_ratio: Annotated[
        bool, typer.Option(help="allow to rotate the aspect ratio")
    ] = CropSettings.rotatable_aspect_ratio,
):
    apply_pipeline(input_path, output_path, crop_into_images)


if __name__ == "__main__":
    app()
