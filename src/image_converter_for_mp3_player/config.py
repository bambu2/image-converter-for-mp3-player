from pathlib import Path
from typing import Annotated

from pydantic import DirectoryPath, Field, PositiveFloat, PositiveInt, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_dir: DirectoryPath = Path("input")
    output_dir: Path = Path("output")

    screen_resolution_str: str = "320x240"

    screen_width: PositiveInt = 1
    screen_height: PositiveInt = 1

    landscape_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)
    portrait_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)

    recursive: bool = True
    dry_run: bool = False
    rotatable_aspect_ratio: bool = True

    img_exts: frozenset = frozenset({".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"})

    @model_validator(mode="after")
    def _derive_screen_fields(self):
        self.screen_width = int(self.screen_resolution_str.split("x")[0])
        self.screen_height = int(self.screen_resolution_str.split("x")[1])

        self.landscape_resolution = (self.screen_width, self.screen_height)
        self.portrait_resolution = (self.screen_height, self.screen_width)
        return self


class BlurSettings(Settings):
    output_dir: Path = Path("output") / "blur"

    radius: Annotated[float, Field(ge=0.0)] = 10.0


class CropSettings(Settings):
    output_dir: Path = Path("output") / "crop"

    crop_scale_factor: PositiveFloat = 0.5


class EquidistantCropSettings(Settings):
    output_dir: Path = Path("output") / "crop"

    threshold: PositiveFloat = 2.0
    scale_factor: PositiveFloat = 1.0
