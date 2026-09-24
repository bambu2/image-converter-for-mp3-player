from enum import Enum, auto


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


def get_orientation(img_size: tuple[int, int], settings) -> Orientation:
    aspect_ratio = img_size[0] / img_size[1]
    return (
        Orientation.LANDSCAPE
        if aspect_ratio > settings.screen_aspect_ratio
        else Orientation.PORTRAIT
    )
