from pathlib import Path

from pydantic import DirectoryPath, PositiveFloat, PositiveInt, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_dir: DirectoryPath = Path("input")
    output_dir: Path = Path("output")

    screen_resolution_str: str = "320x240"

    landscape_width: PositiveInt = 1
    landscape_height: PositiveInt = 1
    landscape_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)

    portrait_width: PositiveInt = 1
    portrait_height: PositiveInt = 1
    portrait_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)

    threshold: PositiveFloat = 2.0

    recursive: bool = True
    dry_run: bool = False
    rotatable_screen: bool = True

    img_exts: frozenset = frozenset({".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"})

    @model_validator(mode="after")
    def _derive_screen_fields(self):
        self.landscape_width = int(self.screen_resolution_str.split("x")[0])
        self.landscape_height = int(self.screen_resolution_str.split("x")[1])
        self.landscape_resolution = (self.landscape_width, self.landscape_height)

        self.portrait_width = self.landscape_height
        self.portrait_height = self.landscape_width
        self.portrait_resolution = (self.portrait_width, self.landscape_height)
        return self


class BlurSettings(Settings):
    output_dir: Path = Path("output") / "blur"

    radius: PositiveFloat = 2.0


class OverlapGridCropSettings(Settings):
    output_dir: Path = Path("output") / "grid_crop"

    scale_factor: PositiveFloat = 0.5


class EquidistantCropSettings(Settings):
    output_dir: Path = Path("output") / "equidistant_crop"

    scale_factor: PositiveFloat = 1.0
