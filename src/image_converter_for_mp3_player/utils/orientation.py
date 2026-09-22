from enum import Enum, auto

from PIL import Image

from image_converter_for_mp3_player.config import Settings


class Orientation(Enum):
    """图像方向（相对于目标宽高比）。

    通过比较图像宽高比与目标比例得到：
    - LANDSCAPE: 图像宽高比 > 目标比例（相对更宽）
    - SAME_ASPECT_RATIO: 图像宽高比 = 目标比例
    - PORTRAIT: 图像宽高比 < 目标比例（相对更高）
    """

    LANDSCAPE = auto()
    SAME_ASPECT_RATIO = auto()
    PORTRAIT = auto()


def get_orientation(image: Image.Image) -> Orientation:
    aspect_ratio = image.width / image.height
    return (
        Orientation.LANDSCAPE
        if aspect_ratio > Settings.screen_aspect_ratio
        else Orientation.PORTRAIT
    )
