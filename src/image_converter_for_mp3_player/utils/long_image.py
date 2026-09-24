from image_converter_for_mp3_player.config import CropSettings
from image_converter_for_mp3_player.utils.orientation import (
    Orientation,
    get_orientation,
)


def is_long_image(img_size: tuple[int, int], settings: CropSettings) -> bool:
    ori = get_orientation(img_size, settings)
    image_aspect_ratio = img_size[0] / img_size[1]

    if settings.rotatable_aspect_ratio:
        if ori == Orientation.LANDSCAPE:
            return (
                image_aspect_ratio
                > settings.screen_aspect_ratio * settings.long_img_threshold
                or image_aspect_ratio
                < settings.rotated_screen_aspect_ratio * settings.long_img_threshold
            )
        else:
            return (
                image_aspect_ratio
                > settings.rotated_screen_aspect_ratio * settings.long_img_threshold
                or image_aspect_ratio
                < settings.screen_aspect_ratio * settings.long_img_threshold
            )
    else:
        return (
            image_aspect_ratio
            > settings.screen_aspect_ratio * settings.long_img_threshold
            or image_aspect_ratio
            < settings.rotated_screen_aspect_ratio * settings.long_img_threshold
        )
