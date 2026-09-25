from enum import Enum, auto


class Orientation(Enum):
    PANORAMA = auto()
    LANDSCAPE = auto()
    SIMILAR_ASPECT_RATIO = auto()
    PORTRAIT = auto()
    LONG_IMAGE = auto()


def get_orientation(
    img_size: tuple[int, int], screen_size: tuple[int, int], threshold: float
) -> Orientation:
    img_aspect_ratio = img_size[0] / img_size[1]
    screen_aspect_ratio = screen_size[0] / screen_size[1]

    if img_aspect_ratio > screen_aspect_ratio:
        if img_aspect_ratio > screen_aspect_ratio * threshold:
            return Orientation.PANORAMA
        return Orientation.LANDSCAPE
    elif img_aspect_ratio < screen_aspect_ratio:
        if img_aspect_ratio < screen_aspect_ratio / threshold:
            return Orientation.PANORAMA
        return Orientation.PORTRAIT
    else:
        return Orientation.SIMILAR_ASPECT_RATIO
