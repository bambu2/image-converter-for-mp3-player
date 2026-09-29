from collections.abc import Iterable

from PIL import Image

from image_converter_for_mp3_player.core import Settings
from image_converter_for_mp3_player.utils import Orientation


def equidistant_crop(
    img: Image.Image, ori: Orientation, settings: Settings, scale_factor: float
) -> Iterable[Image.Image]:
    img_size = img.size

    crop_size = _get_crop_size(img_size, ori, settings, scale_factor)
    crop_boxes = _get_crop_boxes(img_size, crop_size)
    for box in crop_boxes:
        yield img.crop(box)


def _get_crop_size(
    img_size: tuple[int, int], ori: Orientation, settings: Settings, scale_factor: float
) -> tuple[int, int]:
    img_width, img_height = img_size

    if ori == Orientation.WIDER_THAN_SCREEN or ori == Orientation.WIDER_THAN_THRESHOLD:
        crop_width = img_width * scale_factor

        crop_height = crop_width / settings.landscape_width * settings.landscape_height
    else:
        crop_height = img_height * scale_factor
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


def _axis_starts(img_size: int, crop_size: int, devision: int) -> list[int]:
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

    x_starts = _axis_starts(img_width, crop_width, col)
    y_starts = _axis_starts(img_height, crop_height, row)

    return [(x, y, x + crop_width, y + crop_height) for x in x_starts for y in y_starts]
