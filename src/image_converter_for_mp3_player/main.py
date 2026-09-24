import logging
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import CropSettings, PadSettings
from image_converter_for_mp3_player.core import (
    apply_blurred_background,
    crop_into_images,
    process,
)

logger = logging.getLogger(__name__)

logger.info("程序启动")

pad_settings = PadSettings()
crop_settings = CropSettings()


app = typer.Typer()


InputDir = Annotated[Path, typer.Option("--input-dir", "-i", help="input directory")]
OutputDir = Annotated[Path, typer.Option("--output-dir", "-o", help="output directory")]
ScreenResolution = Annotated[str, typer.Option(help="screen resolution")]

Recursive = Annotated[
    bool, typer.Option("--recursive", "-r", help="whether to process subdirectories")
]
DryRun = Annotated[
    bool, typer.Option(help="whether to actually write the output files")
]
RotatableAspectRatio = Annotated[
    bool, typer.Option(help="allow to rotate the aspect ratio")
]


@app.command()
def pad(
    input_dir: InputDir = pad_settings.input_dir,
    output_dir: OutputDir = pad_settings.output_dir,
    screen_resolution: ScreenResolution = pad_settings.screen_resolution,
    recursive: Recursive = pad_settings.recursive,
    dry_run: DryRun = pad_settings.dry_run,
    rotatable_aspect_ratio: RotatableAspectRatio = pad_settings.rotatable_aspect_ratio,
):
    settings = pad_settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_aspect_ratio": rotatable_aspect_ratio,
        }
    )
    process(apply_blurred_background, settings)


@app.command()
def crop(
    input_dir: InputDir = crop_settings.input_dir,
    output_dir: OutputDir = crop_settings.output_dir,
    screen_resolution: ScreenResolution = crop_settings.screen_resolution,
    recursive: Recursive = crop_settings.recursive,
    dry_run: DryRun = crop_settings.dry_run,
    rotatable_aspect_ratio: RotatableAspectRatio = crop_settings.rotatable_aspect_ratio,
):
    settings = crop_settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_aspect_ratio": rotatable_aspect_ratio,
        }
    )
    process(crop_into_images, settings)


if __name__ == "__main__":
    app()
