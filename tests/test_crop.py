import pytest

from image_converter_for_mp3_player.config import CropSettings
from image_converter_for_mp3_player.core.crop import (
    _get_crop_relative_size,
    _get_crop_size,
)
from image_converter_for_mp3_player.utils import Orientation, get_orientation


@pytest.fixture
def crop_settings():
    return CropSettings(
        screen_resolution="500x200",
        default_crop_relative_size=0.5,
        long_img_max_crop=True,
        long_img_threshold=3.0,
        rotatable_aspect_ratio=True,
    )


def test_get_crop_relative_size(crop_settings):
    img_size = (640, 320)
    assert _get_crop_relative_size(img_size, crop_settings) == 0.5


def test_get_crop_size(crop_settings): ...
