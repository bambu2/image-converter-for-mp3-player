from collections.abc import Iterable

from PIL import Image, ImageFilter, ImageOps

from image_converter_for_mp3_player.config import BlurSettings
from image_converter_for_mp3_player.utils import Orientation, get_orientation


def background_blur(img: Image.Image, settings: BlurSettings) -> Iterable[Image.Image]:
    ori = get_orientation(
        img.size,
    )
    if settings.rotatable_aspect_ratio:
        target_resolution = (
            settings.landscape_resolution
            if ori == Orientation.LANDSCAPE
            else settings.portrait_resolution
        )
    else:
        target_resolution = settings.landscape_resolution

    bg = ImageOps.fit(img, target_resolution, method=Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=settings.radius))

    img.thumbnail(target_resolution, Image.Resampling.LANCZOS)

    offset = ((bg.width - img.width) // 2, (bg.height - img.height) // 2)

    bg.paste(img, offset)
    yield bg
