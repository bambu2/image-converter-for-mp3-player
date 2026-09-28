from collections.abc import Callable, Iterable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings
from image_converter_for_mp3_player.core.background_blur import background_blur
from image_converter_for_mp3_player.core.equidistant_crop import equidistant_crop
from image_converter_for_mp3_player.core.pipeline import apply_pipeline
from image_converter_for_mp3_player.utils import (
    Orientation,
    get_image_paths,
    get_orientation,
)


def execute(
    image_paths: list[Path] | None,
    func: Callable[[Image.Image, Orientation, Settings, float], Iterable[Image.Image]],
    filter: Callable,
    settings: Settings,
) -> None:
    if image_paths is not None:
        for path in image_paths:
            with Image.open(path) as img:
                image_paths = []
                ori = get_orientation(
                    img.size,
                    (settings.landscape_width, settings.landscape_height),
                    settings.threshold,
                )
                if filter(ori):
                    image_paths.append(path)
            apply_pipeline(func, image_paths, settings)


def blur_filter(orientation: Orientation) -> bool:
    return (
        orientation == Orientation.LANDSCAPE
        or orientation == Orientation.SIMILAR_ASPECT_RATIO
        or orientation == Orientation.PORTRAIT
    )


def equidistant_crop_filter(orientation: Orientation) -> bool:
    return (
        orientation == Orientation.LANDSCAPE
        or orientation == Orientation.SIMILAR_ASPECT_RATIO
        or orientation == Orientation.PORTRAIT
    )


def wide_image_crop_filter(orientation: Orientation) -> bool:
    return orientation == Orientation.PANORAMA or orientation == Orientation.LONG_IMAGE


def route(settings: Settings) -> None:
    image_paths = get_image_paths(settings)

    execute()
