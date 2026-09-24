import logging
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import crop_settings, pad_settings, settings
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
        Path | None,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Argument(
            exists=False,
            writable=True,
            resolve_path=True,
        ),
    ] = None,
    screen_resolution: Annotated[str | None, typer.Argument()] = None,
    rotatable_aspect_ratio: Annotated[
        bool | None, typer.Option(help="allow to rotate the aspect ratio")
    ] = None,
):
    updates = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "screen_resolution": screen_resolution,
        "rotatable_aspect_ratio": rotatable_aspect_ratio,
    }
    for key, value in updates.items():
        if value is not None:
            setattr(settings, key, value)

    pad_settings.output_dir.mkdir(parents=True, exist_ok=True)
    apply_pipeline(
        pad_settings.input_dir, apply_blurred_background, pad_settings.output_dir
    )


@app.command()
def crop(
    input_dir: Annotated[
        Path | None,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ] = None,
    output_dir: Annotated[
        Path | None,
        typer.Argument(
            exists=False,
            writable=True,
            resolve_path=True,
        ),
    ] = None,
    screen_resolution: Annotated[str | None, typer.Argument()] = None,
    rotatable_aspect_ratio: Annotated[
        bool | None, typer.Option(help="allow to rotate the aspect ratio")
    ] = None,
):
    updates = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "screen_resolution": screen_resolution,
        "rotatable_aspect_ratio": rotatable_aspect_ratio,
    }
    for key, value in updates.items():
        if value is not None:
            setattr(settings, key, value)
    crop_settings.output_dir.mkdir(parents=True, exist_ok=True)
    apply_pipeline(crop_settings.input_dir, crop_into_images, crop_settings.output_dir)


if __name__ == "__main__":
    app()
