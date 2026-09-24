from collections.abc import Iterable

from PIL import Image

from image_converter_for_mp3_player.config import CropSettings
from image_converter_for_mp3_player.utils import Orientation, get_orientation


def crop_into_images(img: Image.Image, settings: CropSettings) -> Iterable[Image.Image]:
    img_width, img_height = img.size
    image_aspect_ratio = img_width / img_height

    ori = get_orientation(img, settings)
    crop_relative_size = _get_crop_relative_size(image_aspect_ratio, settings)
    crop_width, crop_height = _get_crop_size(
        img_width, img_height, ori, crop_relative_size, settings
    )
    crop_boxes = _get_crop_boxes(img_width, img_height, crop_width, crop_height, ori)
    for box in crop_boxes:
        yield img.crop(box)


def _get_crop_relative_size(image_aspect_ratio: float, settings: CropSettings) -> float:
    if settings.long_img_max_crop_size and (
        image_aspect_ratio > settings.screen_aspect_ratio * settings.long_img_threshold
        or image_aspect_ratio
        < settings.screen_aspect_ratio / settings.long_img_threshold
    ):
        crop_relative_size = 1.0
    else:
        crop_relative_size = settings.crop_relative_size
    return crop_relative_size


def _get_crop_size(
    img_width: int,
    img_height: int,
    ori: Orientation,
    crop_relative_size: float,
    settings: CropSettings,
) -> tuple[int, int]:
    if settings.rotatable_aspect_ratio:
        if ori == Orientation.LANDSCAPE:
            crop_width = int(img_width * crop_relative_size)
            crop_height = int(crop_width / settings.screen_aspect_ratio)
        else:
            crop_height = int(img_height * crop_relative_size)
            crop_width = int(crop_height / settings.screen_aspect_ratio)
    else:
        crop_width = int(img_width * crop_relative_size)
        crop_height = int(crop_width / settings.screen_aspect_ratio)
    return (crop_width, crop_height)


def _get_crop_boxes(
    img_width, img_height, crop_width, crop_height, ori
) -> list[tuple[int, int, int, int]]:
    col = -(-img_width // crop_width)
    row = -(-img_height // crop_height)
    x_step = (crop_width * col - img_width) // col
    y_step = (crop_height * row - img_height) // row
    return [
        (x, y, x + crop_width, y + crop_height)
        for x in range(0, img_width, x_step)
        for y in range(0, img_height, y_step)
    ]
