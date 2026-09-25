import logging
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import (
    BlurSettings,
    EquidistantCropSettings,
    OverlapGridCropSettings,
)
from image_converter_for_mp3_player.core import (
    background_blur,
    equidistant_crop,
    overlap_grid_crop,
    process,
)

logger = logging.getLogger(__name__)

logger.info("程序启动")

pad_settings = BlurSettings()
overlap_grid_crop_settings = OverlapGridCropSettings()
equidistant_crop_settings = EquidistantCropSettings()


app = typer.Typer()


type InputDir = Annotated[
    Path, typer.Option("--input-dir", "-i", help="input directory")
]
type OutputDir = Annotated[
    Path, typer.Option("--output-dir", "-o", help="output directory")
]
type ScreenResolution = Annotated[str, typer.Option(help="screen resolution")]

type Recursive = Annotated[
    bool, typer.Option("--recursive", "-r", help="whether to process subdirectories")
]
type DryRun = Annotated[
    bool, typer.Option(help="whether to actually write the output files")
]
type RotatableScreen = Annotated[bool, typer.Option(help="allow to rotate the screen")]


@app.command()
def blur(
    input_dir: InputDir = pad_settings.input_dir,
    output_dir: OutputDir = pad_settings.output_dir,
    screen_resolution: ScreenResolution = pad_settings.screen_resolution_str,
    recursive: Recursive = pad_settings.recursive,
    dry_run: DryRun = pad_settings.dry_run,
    rotatable_screen: RotatableScreen = pad_settings.rotatable_screen,
):
    settings = pad_settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_screen": rotatable_screen,
        }
    )
    process(background_blur, settings)


@app.command()
def ogcrop(
    input_dir: InputDir = overlap_grid_crop_settings.input_dir,
    output_dir: OutputDir = overlap_grid_crop_settings.output_dir,
    screen_resolution: ScreenResolution = overlap_grid_crop_settings.screen_resolution_str,
    recursive: Recursive = overlap_grid_crop_settings.recursive,
    dry_run: DryRun = overlap_grid_crop_settings.dry_run,
    rotatable_screen: RotatableScreen = overlap_grid_crop_settings.rotatable_screen,
):
    settings = overlap_grid_crop_settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_screen": rotatable_screen,
        }
    )
    process(overlap_grid_crop, settings)


@app.command()
def ecrop(
    input_dir: InputDir = equidistant_crop_settings.input_dir,
    output_dir: OutputDir = equidistant_crop_settings.output_dir,
    screen_resolution: ScreenResolution = equidistant_crop_settings.screen_resolution_str,
    recursive: Recursive = equidistant_crop_settings.recursive,
    dry_run: DryRun = equidistant_crop_settings.dry_run,
    rotatable_screen: RotatableScreen = equidistant_crop_settings.rotatable_screen,
):
    settings = equidistant_crop_settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_screen": rotatable_screen,
        }
    )
    process(equidistant_crop, settings)


if __name__ == "__main__":
    app()
