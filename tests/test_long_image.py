import pytest

from image_converter_for_mp3_player.config import OverlapGridCropSettings
from image_converter_for_mp3_player.utils.long_image import is_long_image


@pytest.fixture
def crop_settings():
    return OverlapGridCropSettings(
        screen_resolution_str="300x200",
        scale_factor=0.5,
        long_img_max_crop=True,
        long_img_threshold=2.0,
        rotatable_screen=True,
    )


def test_long_image(crop_settings):
    img_size = (500, 400)
    assert not is_long_image(img_size, crop_settings)
