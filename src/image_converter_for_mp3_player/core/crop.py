import math
from enum import Enum
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings, CropSettings
from image_converter_for_mp3_player.utils import get_orientation, Orientation


def crop(img: Image.Image) -> list[Image.Image]:
    screen_width, screen_height = Settings.screen_resolution
    img_width, img_height = img.size
    image_aspect_ratio = img_width / img_height

    if CropSettings.long_img_max_crop_size and (
        image_aspect_ratio
        > Settings.screen_aspect_ratio * CropSettings.long_img_threshold
        or image_aspect_ratio
        < Settings.screen_aspect_ratio / CropSettings.long_img_threshold
    ):
        crop_relative_size = 1.0
    else:
        crop_relative_size = CropSettings.crop_relative_size

    if CropSettings.rotatable_aspect_ratio:
        if get_orientation(img) == Orientation.LANDSCAPE:
            crop_width = int(img_width * crop_relative_size)
            crop_height = int(crop_width / Settings.screen_aspect_ratio)
        else:
            crop_height = int(img_height * crop_relative_size)
            crop_width = int(crop_height / Settings.screen_aspect_ratio)
    else:
        crop_width = int(img_width * crop_relative_size)
        crop_height = int(crop_width / Settings.screen_aspect_ratio)


"""
        selected_windows = self._grid_windows(
            img_w=iw,
            img_h=ih,
            win_w=win_w,
            win_h=win_h,
            Settings.screen_aspect_ratio=Settings.screen_aspect_ratio,
            direction=direction,
        )
        crops = []
        for x, y, w, h in selected_windows:
            cropped = image.crop((x, y, x + w, y + h))
            resized = resize_like_thumbnail(cropped, cw, ch)
            padded = pad_to_size(
                resized, (Config.screen_width, Config.screen_height), color=(0, 0, 0)
            )
            crops.append(padded)
        return crops

    def _grid_windows(
        self,
        img_w: int,
        img_h: int,
        win_w: int,
        win_h: int,
        Settings.screen_aspect_ratio: float,
        direction: SlidingDirection,
    ) -> list[tuple[int, int, int, int]]:
        if direction == SlidingDirection.VERTICAL:
            cols = math.ceil(img_w / win_w)
            win_w = math.ceil(img_w / cols)
            win_h = math.ceil(win_w / Settings.screen_aspect_ratio)
            rows = math.ceil(img_h / win_h)
        else:
            rows = math.ceil(img_h / win_h)
            win_h = math.ceil(img_h / rows)
            win_w = math.ceil(win_h * Settings.screen_aspect_ratio)
            cols = math.ceil(img_w / win_w)

        y_starts = np.linspace(0, img_h - win_h, num=rows, dtype=int)
        x_starts = np.linspace(0, img_w - win_w, num=cols, dtype=int)

        windows = []
        for y in y_starts:
            for x in x_starts:
                windows.append((int(x), int(y), win_w, win_h))

        return windows
    """
