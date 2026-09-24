from PIL import Image

from image_converter_for_mp3_player.config import crop_settings
from image_converter_for_mp3_player.utils import Orientation, get_orientation


def crop_into_images(img: Image.Image) -> list[Image.Image]:
    img_width, img_height = img.size
    image_aspect_ratio = img_width / img_height

    ori = get_orientation(img, crop_settings)
    crop_relative_size = _get_crop_relative_size(image_aspect_ratio)
    crop_width, crop_height = _get_crop_size(
        img_width, img_height, ori, crop_relative_size
    )
    crop_boxes = _get_crop_boxes(img_width, img_height, crop_width, crop_height, ori)
    return [img.crop(box) for box in crop_boxes]


def _get_crop_relative_size(image_aspect_ratio: float) -> float:
    if crop_settings.long_img_max_crop_size and (
        image_aspect_ratio
        > crop_settings.screen_aspect_ratio * crop_settings.long_img_threshold
        or image_aspect_ratio
        < crop_settings.screen_aspect_ratio / crop_settings.long_img_threshold
    ):
        crop_relative_size = 1.0
    else:
        crop_relative_size = crop_settings.crop_relative_size
    return crop_relative_size


def _get_crop_size(
    img_width: int, img_height: int, ori: Orientation, crop_relative_size: float
) -> tuple[int, int]:
    if crop_settings.rotatable_aspect_ratio:
        if ori == Orientation.LANDSCAPE:
            crop_width = int(img_width * crop_relative_size)
            crop_height = int(crop_width / crop_settings.screen_aspect_ratio)
        else:
            crop_height = int(img_height * crop_relative_size)
            crop_width = int(crop_height / crop_settings.screen_aspect_ratio)
    else:
        crop_width = int(img_width * crop_relative_size)
        crop_height = int(crop_width / crop_settings.screen_aspect_ratio)
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
