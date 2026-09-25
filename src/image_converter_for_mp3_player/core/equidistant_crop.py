from collections.abc import Iterable

from PIL import Image

from image_converter_for_mp3_player.config import EquidistantCropSettings
from image_converter_for_mp3_player.utils import Orientation


def equidistant_crop(
    img: Image.Image, ori: Orientation, settings: EquidistantCropSettings
) -> Iterable[Image.Image]: ...
