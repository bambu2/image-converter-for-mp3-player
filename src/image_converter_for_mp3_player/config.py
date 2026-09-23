from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    input_path: Path = Path("input")
    output_path: Path = Path("output")

    screen_resolution: str = "320x240"
    screen_width, screen_height = map(int, screen_resolution.split("x"))
    screen_aspect_ratio: float = screen_width / screen_height

    landscape_resolution: tuple[PositiveInt, PositiveInt] = (
        screen_width,
        screen_height,
    )
    portrait_resolution: tuple[PositiveInt, PositiveInt] = (screen_height, screen_width)

    recursive: bool = True
    dry_run: bool = False

    img_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


class PadSettings(BaseModel):
    pad_path: Path = Settings.output_path / "pad"
    pipeline = []
    rotatable_aspect_ratio: bool = True
    blur_radius: Annotated[float, Field(ge=0.0)] = 10.0


class CropSettings(BaseSettings):
    crop_path: Path = Settings.output_path / "crop"

    rotatable_aspect_ratio: bool = True

    crop_relative_size: Annotated[float, Field(gt=0.0, le=1.0)] = 0.5
    long_img_max_crop_size: bool = True
    long_img_threshold: PositiveFloat = 2.0
