import math
from enum import Enum
from pathlib import Path

from PIL import Image

from image_converter_for_mp3_player.config import Settings, CropSettings
from image_converter_for_mp3_player.utils import get_orientation, Orientation


def crop(image_path: Path):
    screen_width, screen_height = Settings.screen_resolution


"""
from utils import Orientation, pad_to_size
from utils import resize_like_thumbnail


class SlidingDirection(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


    def process(self, image_path: Path, **kwargs) -> list[Image.Image]:
        window_scale = kwargs.get("window_scale", 0.5)
        auto_max_threshold = kwargs.get("auto_max_threshold", 2.0)  # 0 表示不启用

        image = self.load_image(image_path)

        direction = self._determine_sliding_direction(image)

        iw = image.width
        ih = image.height

        image_aspect = iw / ih

        cw = Config.screen_width
        ch = Config.screen_height

        screen_aspect = Config.screen_aspect

        # 自动调整 window_scale（如果启用）
        if auto_max_threshold > 0:
            if (
                image_aspect > screen_aspect * auto_max_threshold
                or image_aspect < screen_aspect / auto_max_threshold
            ):
                window_scale = 1.0

        if direction == SlidingDirection.HORIZONTAL:
            win_h = int(iw * window_scale)
            win_w = int(win_h * screen_aspect)
        else:
            win_w = int(iw * window_scale)
            win_h = int(win_w / screen_aspect)

        # 确保窗口不超界
        win_w = min(win_w, iw)
        win_h = min(win_h, ih)

        selected_windows = self._grid_windows(
            img_w=iw,
            img_h=ih,
            win_w=win_w,
            win_h=win_h,
            screen_aspect=screen_aspect,
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

    def _determine_sliding_direction(self, image: Image.Image) -> SlidingDirection:
        orientation = self.classify_orientation(image)
        return (
            SlidingDirection.VERTICAL
            if orientation == Orientation.PORTRAIT
            else SlidingDirection.HORIZONTAL
        )

    def _grid_windows(
        self,
        img_w: int,
        img_h: int,
        win_w: int,
        win_h: int,
        screen_aspect: float,
        direction: SlidingDirection,
    ) -> list[tuple[int, int, int, int]]:
        if direction == SlidingDirection.VERTICAL:
            cols = math.ceil(img_w / win_w)
            win_w = math.ceil(img_w / cols)
            win_h = math.ceil(win_w / screen_aspect)
            rows = math.ceil(img_h / win_h)
        else:
            rows = math.ceil(img_h / win_h)
            win_h = math.ceil(img_h / rows)
            win_w = math.ceil(win_h * screen_aspect)
            cols = math.ceil(img_w / win_w)

        y_starts = np.linspace(0, img_h - win_h, num=rows, dtype=int)
        x_starts = np.linspace(0, img_w - win_w, num=cols, dtype=int)

        windows = []
        for y in y_starts:
            for x in x_starts:
                windows.append((int(x), int(y), win_w, win_h))

        return windows
    """
