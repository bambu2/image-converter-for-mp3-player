from collections.abc import Callable, Iterable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.core import Settings
from image_converter_for_mp3_player.services.background_blur import background_blur
from image_converter_for_mp3_player.services.equidistant_crop import equidistant_crop
from image_converter_for_mp3_player.services.pipeline import apply_pipeline
from image_converter_for_mp3_player.utils import (
    Orientation,
    get_image_paths,
    get_orientation,
)


def dispatch(
    image_paths: list[Path] | None,
    func: Callable[[Image.Image, Orientation, Settings, float], Iterable[Image.Image]],
    settings: Settings,
) -> None:
    if image_paths is not None:
        for path in image_paths:
            with Image.open(path) as img:
                image_paths = []
                orientation = get_orientation(
                    img.size,
                    (settings.landscape_width, settings.landscape_height),
                    settings.threshold,
                )
                if orientation in (
                    Orientation.WIDER_THAN_SCREEN,
                    Orientation.SIMILAR_ASPECT_RATIO,
                    Orientation.NARROWER_THAN_SCREEN,
                ):
                    apply_pipeline(
                        partial(background_blur, radius=radius),
                        updated_settings,
                        output_dir,
                    )
                    equidistant_crop()
                else:
                    equidistant_crop()


def blur_filter(orientation: Orientation) -> bool:
    return


def equidistant_crop_filter(orientation: Orientation) -> bool:
    return orientation in (
        Orientation.WIDER_THAN_SCREEN,
        Orientation.SIMILAR_ASPECT_RATIO,
        Orientation.NARROWER_THAN_SCREEN,
    )


def wide_image_crop_filter(orientation: Orientation) -> bool:
    return orientation in (
        Orientation.WIDER_THAN_THRESHOLD,
        Orientation.NARROWER_THAN_THRESHOLD,
    )


def auto(settings: Settings) -> None:
    image_paths = get_image_paths(settings)

    dispatch()
