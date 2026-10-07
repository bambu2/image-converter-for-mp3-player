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
SubDir = Annotated[Path, typer.Option("--subdir", "-s", help="subdirectory for output")]
LandscapeResStr = Annotated[str, typer.Option(help="screen resolution")]
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
    landscape_res_str: LandscapeResStr = settings.landscape_res_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    sub_dir: SubDir = settings.blur.sub_dir,
    radius: Radius = settings.blur.radius,
):
    new_blur = settings.blur.model_copy(update={"sub_dir": sub_dir, "radius": radius})

    settings_update = get_settings_update(
        input_dir,
        output_dir,
        landscape_res_str,
        threshold,
        recursive,
        dry_run,
        rotatable_screen,
    )

    update = settings_update | {"blur": new_blur}

    process(update, output_dir / sub_dir, Mode.BLUR)


@app.command()
def equidistant_crop(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.output_dir,
    landscape_res_str: LandscapeResStr = settings.landscape_res_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    sub_dir: SubDir = settings.equidistant_crop.sub_dir,
    scale_factor: ScaleFactor = settings.equidistant_crop.scale_factor,
):

    new_equidistant_crop = settings.equidistant_crop.model_copy(
        update={"sub_dir": sub_dir, "scale_factor": scale_factor}
    )

    settings_update = get_settings_update(
        input_dir,
        output_dir,
        landscape_res_str,
        threshold,
        recursive,
        dry_run,
        rotatable_screen,
    )

    update = settings_update | {"equidistant_crop": new_equidistant_crop}

    process(update, output_dir / sub_dir, Mode.EQUIDISTANT_CROP)


@app.command()
def extreme_crop(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.output_dir,
    landscape_res_str: LandscapeResStr = settings.landscape_res_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    sub_dir: SubDir = settings.extreme_crop.sub_dir,
    scale_factor: ScaleFactor = settings.extreme_crop.scale_factor,
):

    new_extreme_crop = settings.extreme_crop.model_copy(
        update={"sub_dir": sub_dir, "scale_factor": scale_factor}
    )

    settings_update = get_settings_update(
        input_dir,
        output_dir,
        landscape_res_str,
        threshold,
        recursive,
        dry_run,
        rotatable_screen,
    )

    update = settings_update | {"extreme_crop": new_extreme_crop}

    process(update, output_dir / sub_dir, Mode.EXTREME_CROP)


@app.command()
def auto(
    input_dir: InputDir = settings.input_dir,
    output_dir: OutputDir = settings.output_dir,
    sub_dir: SubDir = settings.auto.sub_dir,
    landscape_res_str: LandscapeResStr = settings.landscape_res_str,
    threshold: Threshold = settings.threshold,
    recursive: Recursive = settings.recursive,
    dry_run: DryRun = settings.dry_run,
    rotatable_screen: RotatableScreen = settings.rotatable_screen,
    blur_sub_dir: SubDir = settings.blur.sub_dir,
    equidistant_sub_dir: SubDir = settings.equidistant_crop.sub_dir,
    extreme_sub_dir: SubDir = settings.extreme_crop.sub_dir,
    radius: Radius = settings.blur.radius,
    equidistant_scale_factor: ScaleFactor = settings.equidistant_crop.scale_factor,
    extreme_scale_factor: ScaleFactor = settings.extreme_crop.scale_factor,
):
    # Create updated settings for each mode
    new_blur = settings.blur.model_copy(
        update={"sub_dir": sub_dir / blur_sub_dir, "radius": radius}
    )
    new_equidistant_crop = settings.equidistant_crop.model_copy(
        update={
            "sub_dir": sub_dir / equidistant_sub_dir,
            "scale_factor": equidistant_scale_factor,
        }
    )
    new_extreme_crop = settings.extreme_crop.model_copy(
        update={
            "sub_dir": sub_dir / extreme_sub_dir,
            "scale_factor": extreme_scale_factor,
        }
    )
    new_auto = settings.auto.model_copy(update={"sub_dir": sub_dir})

    settings_update = get_settings_update(
        input_dir,
        output_dir,
        landscape_res_str,
        threshold,
        recursive,
        dry_run,
        rotatable_screen,
    )

    update = (
        settings_update
        | {"blur": new_blur}
        | {"equidistant_crop": new_equidistant_crop}
        | {"extreme_crop": new_extreme_crop}
        | {"auto": new_auto}
    )

    process(update, output_dir / sub_dir, Mode.AUTO)


def get_settings_update(
    input_dir: InputDir,
    output_dir: OutputDir,
    landscape_res_str: LandscapeResStr,
    threshold: Threshold,
    recursive: Recursive,
    dry_run: DryRun,
    rotatable_screen: RotatableScreen,
) -> dict[str, Any]:
    return {
        "input_dir": input_dir,
        "output_dir": output_dir,
        "landscape_res_str": landscape_res_str,
        "threshold": threshold,
        "recursive": recursive,
        "dry_run": dry_run,
        "rotatable_screen": rotatable_screen,
    }


def process(update: dict[str, Any], output_dir: Path, mode: Mode) -> None:
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
                )

            except OSError as e:
                logger.error(f"Error processing: {e}")
                raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
