from collections.abc import Callable, Iterable
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import (
    BlurSettings,
    CropSettings,
    EquidistantCropSettings,
    WideImageCropSettings,
)
from image_converter_for_mp3_player.core.background_blur import background_blur
from image_converter_for_mp3_player.core.equidistant_crop import equidistant_crop
from image_converter_for_mp3_player.core.pipeline import apply_pipeline
from image_converter_for_mp3_player.utils import (
    Orientation,
    get_image_paths,
    get_orientation,
)


def execute[S: BlurSettings | CropSettings](
    image_paths: list[Path] | None,
    func: Callable[[Image.Image, Orientation, S], Iterable[Image.Image]],
    filter: Callable,
    settings: S,
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


def blur_filter(ori) -> bool:
    return (
        ori == Orientation.LANDSCAPE
        or ori == Orientation.SIMILAR_ASPECT_RATIO
        or ori == Orientation.PORTRAIT
    )


def equidistant_crop_filter(ori) -> bool:
    return (
        ori == Orientation.LANDSCAPE
        or ori == Orientation.SIMILAR_ASPECT_RATIO
        or ori == Orientation.PORTRAIT
    )


def wide_image_crop_filter(ori) -> bool:
    return ori == Orientation.PANORAMA or ori == Orientation.LONG_IMAGE


def route(
    blur_settings: BlurSettings,
    equidistant_crop_settings: EquidistantCropSettings,
    wide_image_crop_settings: WideImageCropSettings,
):
    blur_image_paths = get_image_paths(blur_settings)
    equidistant_crop_image_paths = get_image_paths(equidistant_crop_settings)
    wide_image_crop_image_paths = get_image_paths(wide_image_crop_settings)

    execute(blur_image_paths, background_blur, blur_filter, blur_settings)
    execute(
        equidistant_crop_image_paths,
        equidistant_crop,
        equidistant_crop_filter,
        equidistant_crop_settings,
    )
    execute(
        wide_image_crop_image_paths,
        equidistant_crop,
        wide_image_crop_filter,
        wide_image_crop_settings,
    )
