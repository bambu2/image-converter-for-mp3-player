from enum import Enum, auto
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.core.config import Settings
from image_converter_for_mp3_player.services.background_blur import background_blur
from image_converter_for_mp3_player.services.equidistant_crop import equidistant_crop
from image_converter_for_mp3_player.utils import (
    Orientation,
    get_orientation,
    post_process,
    target_dir,
)


class Mode(Enum):
    BLUR = auto()
    EQUIDISTANT_CROP = auto()
    EXTREME_CROP = auto()
    AUTO = auto()


def dispatch(path: Path, settings: Settings, mode: Mode) -> None:
    with Image.open(path) as img:
        orientation = get_orientation(
            img.size,
            (settings.landscape_width, settings.landscape_height),
            settings.threshold,
        )
        match mode:
            case Mode.BLUR:
                blur_process(img, path, settings, orientation)

            case Mode.EQUIDISTANT_CROP:
                equidistant_crop_process(img, path, settings, orientation)

            case Mode.EXTREME_CROP:
                extreme_crop_process(img, path, settings, orientation)

            case Mode.AUTO:
                if orientation in (
                    Orientation.WIDER_THAN_SCREEN,
                    Orientation.SIMILAR_ASPECT_RATIO,
                    Orientation.NARROWER_THAN_SCREEN,
                ):
                    blur_process(img, path, settings, orientation)
                    equidistant_crop_process(img, path, settings, orientation)
                else:
                    extreme_crop_process(img, path, settings, orientation)


def blur_process(
    img: Image.Image,
    path: Path,
    settings: Settings,
    orientation: Orientation,
) -> None:
    output_dir = target_dir(
        input_dir=settings.input_dir,
        output_dir=settings.output_dir / settings.blur.sub_dir,
        path=path,
    )
    img_iter = background_blur(img, orientation, settings, settings.blur.radius)

    post_process(
        img_iter=img_iter,
        size=settings.landscape_resolution,
        output_dir=output_dir,
        img_name=path.stem,
        suffix=str(settings.blur.sub_dir),
    )


def equidistant_crop_process(
    img: Image.Image,
    path: Path,
    settings: Settings,
    orientation: Orientation,
) -> None:
    output_dir = target_dir(
        input_dir=settings.input_dir,
        output_dir=settings.output_dir / settings.equidistant_crop.sub_dir,
        path=path,
    )
    img_iter = equidistant_crop(
        img, orientation, settings, settings.equidistant_crop.scale_factor
    )

    post_process(
        img_iter=img_iter,
        size=settings.landscape_resolution,
        output_dir=output_dir,
        img_name=path.stem,
        suffix=str(settings.equidistant_crop.sub_dir),
    )


def extreme_crop_process(
    img: Image.Image,
    path: Path,
    settings: Settings,
    orientation: Orientation,
) -> None:
    output_dir = target_dir(
        input_dir=settings.input_dir,
        output_dir=settings.output_dir / settings.extreme_crop.sub_dir,
        path=path,
    )
    img_iter = equidistant_crop(
        img, orientation, settings, settings.extreme_crop.scale_factor
    )

    post_process(
        img_iter=img_iter,
        size=settings.landscape_resolution,
        output_dir=output_dir,
        img_name=path.stem,
        suffix=str(settings.extreme_crop.sub_dir),
    )
