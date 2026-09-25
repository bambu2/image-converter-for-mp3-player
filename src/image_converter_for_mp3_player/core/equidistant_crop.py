from collections.abc import Iterable

from PIL import Image

from image_converter_for_mp3_player.config import CropSettings
from image_converter_for_mp3_player.utils import Orientation, axis_starts


def equidistant_crop(
    img: Image.Image, ori: Orientation, settings: CropSettings
) -> Iterable[Image.Image]:
    img_size = img.size

    crop_size = _get_crop_size(img_size, ori, settings)
    crop_boxes = _get_crop_boxes(img_size, crop_size)
    for box in crop_boxes:
        yield img.crop(box)


def _get_crop_size(
    img_size: tuple[int, int],
    ori: Orientation,
    settings: CropSettings,
) -> tuple[int, int]:
    img_width, img_height = img_size

    if ori == Orientation.LANDSCAPE or ori == Orientation.PANORAMA:
        crop_width = img_width * settings.scale_factor

        crop_height = crop_width / settings.landscape_width * settings.landscape_height
    else:
        crop_height = img_height * settings.scale_factor
        if settings.rotatable_screen:
            crop_width = (
                crop_height / settings.portrait_height * settings.portrait_width
            )
        else:
            crop_width = (
                crop_height / settings.landscape_height * settings.landscape_width
            )

    if crop_width < 1:
        raise ValueError("crop_width must be greater than 0")
    if crop_height < 1:
        raise ValueError("crop_height must be greater than 0")

    return (int(crop_width), int(crop_height))


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

    xs = axis_starts(img_width, crop_width, col)
    ys = axis_starts(img_height, crop_height, row)

    return [(x, y, x + crop_width, y + crop_height) for x in xs for y in ys]
