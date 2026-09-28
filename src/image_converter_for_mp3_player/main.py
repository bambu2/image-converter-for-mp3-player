import logging
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import settings
from image_converter_for_mp3_player.core import (
    apply_pipeline,
    background_blur,
    equidistant_crop,
    router,
)
from image_converter_for_mp3_player.utils.path_utils import get_image_paths

logger = logging.getLogger(__name__)

logger.info("程序启动")


app = typer.Typer()


InputDir = Annotated[Path, typer.Option("--input-dir", "-i", help="input directory")]
OutputDir = Annotated[Path, typer.Option("--output-dir", "-o", help="output directory")]
ScreenResolutionStr = Annotated[str, typer.Option(help="screen resolution")]
Threshold = Annotated[float, typer.Option(help="threshold")]
Recursive = Annotated[
    bool, typer.Option("--recursive", "-r", help="whether to process subdirectories")
]
DryRun = Annotated[
    bool, typer.Option(help="whether to actually write the output files")
]
RotatableScreen = Annotated[bool, typer.Option(help="allow to rotate the screen")]

Radius = Annotated[float, typer.Option(help="radius of GaussianBlur")]

ScaleFactor = Annotated[float, typer.Option(help="the scale factor of crop size")]


@app.command()
def blur(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.output_dir,
    screen_resolution_str: ScreenResolutionStr = settings.screen_resolution_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    radius: Radius = settings.radius,
):
    settings = settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution_str,
            "threshold": threshold,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_screen": rotatable_screen,
            "radius": radius,
        }
    )
    image_paths = get_image_paths(settings)
    if image_paths is not None:
        apply_pipeline(background_blur, image_paths, settings)


@app.command()
def crop(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.output_dir,
    screen_resolution_str: ScreenResolutionStr = settings.screen_resolution_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    scale_factor: ScaleFactor = settings.scale_factor,
):
    settings = settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution_str,
            "threshold": threshold,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_screen": rotatable_screen,
            "scale_factor": scale_factor,
        }
    )
    image_paths = get_image_paths(settings)
    if image_paths is not None:
        apply_pipeline(equidistant_crop, image_paths, settings)


@app.command()
def widecrop(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.output_dir,
    screen_resolution_str: ScreenResolutionStr = settings.screen_resolution_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    scale_factor: ScaleFactor = settings.scale_factor,
):
    settings = settings.model_copy(
        update={
            "input_dir": input_dir,
            "output_dir": output_dir,
            "screen_resolution": screen_resolution_str,
            "threshold": threshold,
            "recursive": recursive,
            "dry_run": dry_run,
            "rotatable_screen": rotatable_screen,
            "scale_factor": scale_factor,
        }
    )
    image_paths = get_image_paths(settings)
    if image_paths is not None:
        apply_pipeline(equidistant_crop, image_paths, settings)


@app.command()
def route():
    router.route(settings, settings, settings)


if __name__ == "__main__":
    app()
