from collections.abc import Iterable

from PIL import Image

from image_converter_for_mp3_player.config import CropSettings
from image_converter_for_mp3_player.utils import (
    Orientation,
    get_orientation,
    is_long_image,
)


def grid_crop(img: Image.Image, settings: CropSettings) -> Iterable[Image.Image]:
    img_size = img.size

    ori = get_orientation(img.size, settings)
    crop_relative_size = _get_crop_relative_size(img_size, settings)
    crop_size = _get_crop_size(img_size, ori, crop_relative_size, settings)
    crop_boxes = _get_crop_boxes(img_size, crop_size)
    for box in crop_boxes:
        yield img.crop(box)


def _get_crop_relative_size(img_size: tuple[int, int], settings: CropSettings) -> float:
    crop_relative_size = settings.crop_scale_factor

    if settings.long_img_max_crop and is_long_image(img_size, settings):
        crop_relative_size = settings.long_img_crop_relative_size

    if crop_relative_size < 0:
        raise ValueError("crop_relative_size must be greater than 0")

    return crop_relative_size


def _get_crop_size(
    img_size: tuple[int, int],
    ori: Orientation,
    crop_relative_size: float,
    settings: CropSettings,
) -> tuple[int, int]:
    img_width, img_height = img_size
    if settings.rotatable_aspect_ratio:
        if ori == Orientation.LANDSCAPE:
            crop_height = int(img_height * crop_relative_size)
            crop_width = int(crop_height * settings.screen_aspect_ratio)
        else:
            crop_width = int(img_width * crop_relative_size)
            crop_height = int(crop_width / settings.rotated_screen_aspect_ratio)
    else:
        if ori == Orientation.LANDSCAPE:
            crop_height = int(img_height * crop_relative_size)
            crop_width = int(crop_height * settings.screen_aspect_ratio)
        else:
            crop_width = int(img_width * crop_relative_size)
            crop_height = int(crop_width / settings.screen_aspect_ratio)

    if crop_width < 1:
        raise ValueError("crop_width must be greater than 0")
    if crop_height < 1:
        raise ValueError("crop_height must be greater than 0")

    return (crop_width, crop_height)


def _axis_starts(img_size: int, crop_size: int, devision: int) -> list[int]:
    if crop_size <= 0 or devision <= 0:
        raise ValueError(f"crop_size={crop_size}, devision={devision} 必须为正")
    if devision == 1 or crop_size >= img_size:
        return [0]
    step = (img_size - crop_size) // (devision - 1)
    return [min(i * step, img_size - crop_size) for i in range(devision)]


def _get_crop_boxes(
    img_size: tuple[int, int], crop_size: tuple[int, int]
) -> list[tuple[int, int, int, int]]:
    img_width, img_height = img_size
    crop_width, crop_height = crop_size

    if img_width <= 0 or img_height <= 0:
        raise ValueError(f"图像尺寸必须为正: {img_width}x{img_height}")
    if crop_width <= 0 or crop_height <= 0:
        raise ValueError(f"裁剪尺寸必须为正: {crop_width}x{crop_height}")

    col = -(-img_width // crop_width)
    row = -(-img_height // crop_height)

    xs = _axis_starts(img_width, crop_width, col)
    ys = _axis_starts(img_height, crop_height, row)

    return [(x, y, x + crop_width, y + crop_height) for x in xs for y in ys]
