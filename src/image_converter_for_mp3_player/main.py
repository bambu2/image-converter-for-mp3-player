import logging
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from image_converter_for_mp3_player.config import crop_settings, pad_settings
from image_converter_for_mp3_player.core import (
    apply_blurred_background,
    apply_pipeline,
    crop_into_images,
)
from image_converter_for_mp3_player.utils import get_image_paths, update_settings

logger = logging.getLogger(__name__)

logger.info("程序启动")

app = typer.Typer()


@dataclass
class CommonArgs:
    input_dir: Annotated[
        Path | None,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ] = None
    output_dir: Annotated[
        Path | None,
        typer.Argument(
            exists=False,
            writable=True,
            resolve_path=True,
        ),
    ] = None
    screen_resolution: Annotated[str | None, typer.Argument()] = None


@dataclass
class CommonOpts:
    recursive: Annotated[
        bool | None, typer.Option(help="whether to process subdirectories")
    ] = None
    dry_run: Annotated[
        bool | None, typer.Option(help="whether to actually write the output files")
    ] = None


@app.command()
def pad(
    args: CommonArgs,
    opts: CommonOpts,
    rotatable_aspect_ratio: Annotated[
        bool | None, typer.Option(help="allow to rotate the aspect ratio")
    ] = None,
):
    args_updates = {
        "input_dir": args.input_dir,
        "output_dir": args.output_dir,
        "screen_resolution": args.screen_resolution,
    }
    opts_updates = {
        "recursive": opts.recursive,
        "dry_run": opts.dry_run,
    }
    pad_updates = {"rotatable_aspect_ratio": rotatable_aspect_ratio}

    for updates in (args_updates, opts_updates, pad_updates):
        update_settings(updates, pad_settings)

    process(apply_blurred_background, pad_settings)


@app.command()
def crop(
    args: CommonArgs,
    opts: CommonOpts,
    rotatable_aspect_ratio: Annotated[
        bool | None, typer.Option(help="allow to rotate the aspect ratio")
    ] = None,
):
    args_updates = {
        "input_dir": args.input_dir,
        "output_dir": args.output_dir,
        "screen_resolution": args.screen_resolution,
    }
    opts_updates = {
        "recursive": opts.recursive,
        "dry_run": opts.dry_run,
    }
    crop_updates = {"rotatable_aspect_ratio": rotatable_aspect_ratio}

    for updates in (args_updates, opts_updates, crop_updates):
        update_settings(updates, crop_updates)

    process(crop_into_images, crop_settings)


def process(fn: Callable, settings):
    try:
        image_paths = get_image_paths(settings.input_dir, settings)
    except (NotADirectoryError, FileNotFoundError, PermissionError) as e:
        logger.error(f"Error processing: {e}")
        raise typer.Exit(1)

    if settings.dry_run:
        print(f"[DRY RUN] input_dir: {settings.input_dir}")
        for image_path in image_paths:
            print(f"[DRY RUN] image_path: {image_path}")
        print(f"[DRY RUN] output_dir: {settings.output_dir}")
    else:
        settings.output_dir.mkdir(parents=True, exist_ok=True)
        apply_pipeline(fn, image_paths, settings)


if __name__ == "__main__":
    app()
