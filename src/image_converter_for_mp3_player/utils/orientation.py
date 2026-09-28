from enum import Enum, auto


class Orientation(Enum):
    WIDER_THAN_THRESHOLD = auto()
    WIDER_THAN_SCREEN = auto()
    SIMILAR_ASPECT_RATIO = auto()
    NARROWER_THAN_SCREEN = auto()
    NARROWER_THAN_THRESHOLD = auto()


def get_orientation(
    img_size: tuple[int, int], screen_size: tuple[int, int], threshold: float
) -> Orientation:
    if threshold <= 1.0:
        raise ValueError("threshold must be > 1.0")
    if img_size[1] == 0 or screen_size[1] == 0:
        raise ValueError("Image and screen heights must be non-zero")

    img_ar = img_size[0] / img_size[1]
    screen_ar = screen_size[0] / screen_size[1]
    ratio = img_ar / screen_ar  # >1 means image is wider than screen

    if ratio > threshold:
        return Orientation.WIDER_THAN_THRESHOLD
    if ratio > 1.0:
        return Orientation.WIDER_THAN_SCREEN
    if ratio < 1.0 / threshold:
        return Orientation.NARROWER_THAN_THRESHOLD
    if ratio < 1.0:
        return Orientation.NARROWER_THAN_SCREEN
    return Orientation.SIMILAR_ASPECT_RATIO
