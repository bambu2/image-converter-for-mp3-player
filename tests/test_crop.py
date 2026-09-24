import pytest

from image_converter_for_mp3_player.config import CropSettings
from image_converter_for_mp3_player.core.crop import _get_crop_relative_size


@pytest.fixture
def crop_settings():
    return CropSettings(
        screen_aspect_ratio=1.5,
        crop_relative_size=0.5,
        long_img_max_crop_size=True,
        long_img_threshold=2.0,
    )


def test_get_crop_relative_size(crop_settings):
    assert _get_crop_relative_size(3.0, crop_settings) == 1.0
    assert _get_crop_relative_size(2.0, crop_settings) == 0.5
    assert _get_crop_relative_size(1.0, crop_settings) == 0.5
    assert _get_crop_relative_size(0.5, crop_settings) == 1.0
