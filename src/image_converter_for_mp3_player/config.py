from pathlib import Path
from typing import Annotated

from pydantic import DirectoryPath, Field, PositiveFloat, PositiveInt, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_dir: DirectoryPath = Path("input")
    output_dir: Path = Path("output")

    screen_resolution: str = "320x240"

    screen_width: int = 0
    screen_height: int = 0
    screen_aspect_ratio: float = 0.0
    landscape_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)
    portrait_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)

    recursive: bool = True
    dry_run: bool = False
    rotatable_aspect_ratio: bool = True

    img_exts: frozenset = frozenset({".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"})

    @model_validator(mode="after")
    def _derive_screen_fields(self):
        w_str, h_str = self.screen_resolution.lower().split("x")
        self.screen_width = int(w_str)
        self.screen_height = int(h_str)
        self.screen_aspect_ratio = self.screen_width / self.screen_height
        self.landscape_resolution = (self.screen_width, self.screen_height)
        self.portrait_resolution = (self.screen_height, self.screen_width)
        return self


class PadSettings(Settings):
    output_dir: Path = Path("output") / "pad"

    blur_radius: Annotated[float, Field(ge=0.0)] = 10.0


class CropSettings(Settings):
    output_dir: Path = Path("output") / "crop"

    crop_relative_size: Annotated[float, Field(gt=0.0, le=1.0)] = 0.5
    long_img_max_crop_size: bool = True
    long_img_threshold: PositiveFloat = 2.0


pad_settings = PadSettings()
crop_settings = CropSettings()
