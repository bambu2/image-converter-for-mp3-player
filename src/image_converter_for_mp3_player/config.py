from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    input_path: Path = Path("input")
    output_path: Path = Path("output")

    screen_resolution: str = "240x320"
    width, height = map(int, screen_resolution.split("x"))
    screen_aspect_ratio: float = width / height

    landscape_resolution: tuple[PositiveInt, PositiveInt] = (width, height)
    portrait_resolution: tuple[PositiveInt, PositiveInt] = (height, width)

    rotatable_aspect_ratio: bool = True
    recursive: bool = True
    dry_run: bool = False

    img_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


class PadSettings(BaseModel):
    pad_path: Path = Settings.output_path / "pad"

    blur_radius: Annotated[float, Field(ge=0.0)] = 10.0


class CropSettings(BaseSettings):
    crop_path: Path = Settings.output_path / "crop"
    crop_relative_size: Annotated[float, Field(gt=0.0, le=1.0)] = 1.0
