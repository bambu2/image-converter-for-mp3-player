import pytest

from image_converter_for_mp3_player.config import OverlapGridCropSettings
from image_converter_for_mp3_player.core.overlap_grid_crop import (
    
)


@pytest.fixture
def crop_settings():
    return OverlapGridCropSettings(
        screen_resolution_str="300x200",
        scale_factor=0.5,
        rotatable_screen=True,
    )

def test