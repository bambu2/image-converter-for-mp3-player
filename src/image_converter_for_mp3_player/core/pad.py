from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

from image_converter_for_mp3_player.config import PadSettings, Settings


def apply_blurred_background(image: Image.Image) -> Image.Image:
    w, h = image.size

    target_size = (
        Settings.landscape_resolution
        if w / h > Settings.screen_aspect_ratio
        else Settings.portrait_resolution
    )

    bg = ImageOps.fit(image, target_size, method=Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=PadSettings.blur_radius))

    fg = image.copy()
    fg.thumbnail(target_size, Image.Resampling.LANCZOS)

    offset_x = (bg.width - fg.width) // 2
    offset_y = (bg.height - fg.height) // 2
    bg.paste(fg, (offset_x, offset_y))
    return bg
