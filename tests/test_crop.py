import pytest

from image_converter_for_mp3_player.core.config import EquidistantCropSettings


@pytest.fixture
def crop_settings():
    return EquidistantCropSettings(
        screen_resolution_str="300x200",
        scale_factor=0.5,
        rotatable_screen=True,
    )
