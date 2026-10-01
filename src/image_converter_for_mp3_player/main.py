import logging
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.progress import track

from image_converter_for_mp3_player.core.config import settings
from image_converter_for_mp3_player.services import Mode, dispatch
from image_converter_for_mp3_player.utils import get_image_paths

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
    output_dir: OutputDir = settings.blur.output_dir,
    screen_resolution_str: ScreenResolutionStr = settings.landscape_resolution_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    radius: Radius = settings.blur.radius,
):
    update: dict[str, Any] = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "screen_resolution": screen_resolution_str,
        "threshold": threshold,
        "recursive": recursive,
        "dry_run": dry_run,
        "rotatable_screen": rotatable_screen,
    }

    process(update, output_dir, Mode.BLUR)


@app.command()
def equidistant_crop(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.equidistant_crop.output_dir,
    screen_resolution_str: ScreenResolutionStr = settings.landscape_resolution_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    scale_factor: ScaleFactor = settings.equidistant_crop.scale_factor,
):

    update: dict[str, Any] = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "screen_resolution": screen_resolution_str,
        "threshold": threshold,
        "recursive": recursive,
        "dry_run": dry_run,
        "rotatable_screen": rotatable_screen,
        "scale_factor": scale_factor,
    }
    process(update, output_dir, Mode.EQUIDISTANT_CROP)


@app.command()
def extreme_crop(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.extreme_crop.output_dir,
    screen_resolution_str: ScreenResolutionStr = settings.landscape_resolution_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    scale_factor: ScaleFactor = settings.extreme_crop.scale_factor,
):

    update: dict[str, Any] = {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "screen_resolution": screen_resolution_str,
        "threshold": threshold,
        "recursive": recursive,
        "dry_run": dry_run,
        "rotatable_screen": rotatable_screen,
        "scale_factor": scale_factor,
    }

    process(update, output_dir, Mode.EXTREME_CROP)


@app.command()
def auto(): ...


def process(
    update: dict[str, Any], output_dir: Path, mode: Mode, **kwargs: Any
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    updated_settings = settings.model_copy(update=update)
    image_paths = get_image_paths(updated_settings)
    if updated_settings.dry_run:
        print(f"[DRY RUN] input_dir: {settings.input_dir}")
        print(f"[DRY RUN] image_paths: {image_paths}")
        print(f"[DRY RUN] output_dir: {output_dir}")
    else:
        if not image_paths:
            logger.info("No images found.")
            raise typer.Exit()

        for path in track(image_paths, description="Processing images"):
            try:
                dispatch(
                    path=path,
                    mode=mode,
                    settings=updated_settings,
                    output_dir=output_dir,
                )

            except OSError as e:
                logger.error(f"Error processing: {e}")
                raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
