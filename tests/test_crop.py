import pytest

from image_converter_for_mp3_player.config import OverlapGridCropSettings
from image_converter_for_mp3_player.core.overlap_grid_crop import (
    _get_crop_relative_size,
    _get_crop_size,
)


@pytest.fixture
def crop_settings():
    return OverlapGridCropSettings(
        screen_resolution_str="300x200",
        scale_factor=0.5,
        long_img_max_crop=True,
        long_img_threshold=2.0,
        rotatable_screen=True,
    )


def test_get_crop_relative_size(crop_settings):
    img_size = (500, 400)
    assert _get_crop_relative_size(img_size, crop_settings) == 0.5


def test_get_crop_size(crop_settings): ...
