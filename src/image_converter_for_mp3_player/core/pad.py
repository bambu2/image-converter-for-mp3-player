from PIL import Image, ImageFilter, ImageOps

from image_converter_for_mp3_player.config import PadSettings, Settings
from image_converter_for_mp3_player.utils import Orientation


def apply_blurred_background(img: Image.Image, ori: Orientation) -> Image.Image:
    if PadSettings.rotatable_aspect_ratio:
        target_resolution = (
            Settings.landscape_resolution
            if ori == Orientation.LANDSCAPE
            else Settings.portrait_resolution
        )
    else:
        target_resolution = Settings.landscape_resolution

    bg = ImageOps.fit(img, target_resolution, method=Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=PadSettings.blur_radius))

    img.thumbnail(target_resolution, Image.Resampling.LANCZOS)

    offset = ((bg.width - img.width) // 2, (bg.height - img.height) // 2)

    bg.paste(img, offset)
    return bg
