import logging
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import (
    BlurSettings,
    EquidistantCropSettings,
    WideImageCropSettings,
)
from image_converter_for_mp3_player.core import (
    apply_pipeline,
    background_blur,
    equidistant_crop,
    router,
)
from image_converter_for_mp3_player.utils.path_utils import get_image_paths

logger = logging.getLogger(__name__)

logger.info("程序启动")

pad_settings = BlurSettings()
equidistant_crop_settings = EquidistantCropSettings()
wide_image_crop_settings = WideImageCropSettings()


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
    input_dir: InputDir = pad_settings.input_dir,
    output_dir: OutputDir = pad_settings.output_dir,
    screen_resolution_str: ScreenResolutionStr = pad_settings.screen_resolution_str,
    threshold: Threshold = pad_settings.threshold,
    recursive: Recursive = pad_settings.recursive,
    dry_run: DryRun = pad_settings.dry_run,
    rotatable_screen: RotatableScreen = pad_settings.rotatable_screen,
    radius: Radius = pad_settings.radius,
):
    settings = pad_settings.model_copy(
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
    input_dir: InputDir = equidistant_crop_settings.input_dir,
    output_dir: OutputDir = equidistant_crop_settings.output_dir,
    screen_resolution_str: ScreenResolutionStr = equidistant_crop_settings.screen_resolution_str,
    threshold: Threshold = pad_settings.threshold,
    recursive: Recursive = equidistant_crop_settings.recursive,
    dry_run: DryRun = equidistant_crop_settings.dry_run,
    rotatable_screen: RotatableScreen = equidistant_crop_settings.rotatable_screen,
    scale_factor: ScaleFactor = equidistant_crop_settings.scale_factor,
):
    settings = equidistant_crop_settings.model_copy(
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
    input_dir: InputDir = wide_image_crop_settings.input_dir,
    output_dir: OutputDir = wide_image_crop_settings.output_dir,
    screen_resolution_str: ScreenResolutionStr = wide_image_crop_settings.screen_resolution_str,
    threshold: Threshold = pad_settings.threshold,
    recursive: Recursive = wide_image_crop_settings.recursive,
    dry_run: DryRun = wide_image_crop_settings.dry_run,
    rotatable_screen: RotatableScreen = wide_image_crop_settings.rotatable_screen,
    scale_factor: ScaleFactor = wide_image_crop_settings.scale_factor,
):
    settings = wide_image_crop_settings.model_copy(
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
    router.route(pad_settings, equidistant_crop_settings, wide_image_crop_settings)


if __name__ == "__main__":
    app()
