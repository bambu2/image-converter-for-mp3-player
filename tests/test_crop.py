import pytest
from image_converter_for_mp3_player.core.crop import _get_crop_relative_size
from image_converter_for_mp3_player.config import CropSettings
@pytest.fixture
def image_aspect_ratio():
    return 2.0

@ pytest.fixture
def crop_settings():
    return CropSettings()

def test_get_crop_relative_size(image_aspect_ratio, crop_settings):
    assert _get_crop_relative_size(image_aspect_ratio, crop_settings) == 0.5
def test_get_crop_relative_size():
    assert _get_crop_relative_size(image_aspect_ratio=2.0,CropSettings()) == 