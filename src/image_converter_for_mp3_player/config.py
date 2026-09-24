from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, DirectoryPath, Field, PositiveFloat, PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    recursive: bool = True
    dry_run: bool = False

    img_exts: frozenset = frozenset({".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"})


class PadSettings(BaseModel):
    input_dir: DirectoryPath = Path("input")
    output_dir: DirectoryPath = Path("output") / "pad"

    screen_resolution: str = "320x240"

    screen_width: int = Field(
        default_factory=lambda d: int(d["screen_resolution"].split("x")[0])
    )
    screen_height: int = Field(
        default_factory=lambda d: int(d["screen_resolution"].split("x")[1])
    )
    screen_aspect_ratio: float = Field(
        default_factory=lambda d: d["screen_width"] / d["screen_height"]
    )
    landscape_resolution: tuple[PositiveInt, PositiveInt] = Field(
        default_factory=lambda d: (d["screen_width"], d["screen_height"])
    )
    portrait_resolution: tuple[PositiveInt, PositiveInt] = Field(
        default_factory=lambda d: (d["screen_height"], d["screen_width"])
    )

    rotatable_aspect_ratio: bool = True

    blur_radius: Annotated[float, Field(ge=0.0)] = 10.0


class CropSettings(BaseModel):
    input_dir: DirectoryPath = Path("input")
    output_dir: DirectoryPath = Path("output") / "crop"

    screen_resolution: str = "320x240"

    screen_width: int = Field(
        default_factory=lambda d: int(d["screen_resolution"].split("x")[0])
    )
    screen_height: int = Field(
        default_factory=lambda d: int(d["screen_resolution"].split("x")[1])
    )
    screen_aspect_ratio: float = Field(
        default_factory=lambda d: d["screen_width"] / d["screen_height"]
    )
    landscape_resolution: tuple[PositiveInt, PositiveInt] = Field(
        default_factory=lambda d: (d["screen_width"], d["screen_height"])
    )
    portrait_resolution: tuple[PositiveInt, PositiveInt] = Field(
        default_factory=lambda d: (d["screen_height"], d["screen_width"])
    )

    rotatable_aspect_ratio: bool = True

    crop_relative_size: Annotated[float, Field(gt=0.0, le=1.0)] = 0.5
    long_img_max_crop_size: bool = True
    long_img_threshold: PositiveFloat = 2.0


settings = Settings()
pad_settings = PadSettings()
crop_settings = CropSettings()
