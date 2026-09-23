from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_dir: Path = Path("input")

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

    recursive: bool = True
    dry_run: bool = False

    img_exts: frozenset = frozenset({".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"})


class PadSettings(BaseModel):
    output_dir: Path = Path("output")
    pad_path: Path | None = None

    rotatable_aspect_ratio: bool = True
    blur_radius: Annotated[float, Field(ge=0.0)] = 10.0

    @model_validator(mode="after")
    def _fill_pad_path(self):
        if self.pad_path is None:
            self.pad_path = self.output_dir / "pad"
        return self

    @property
    def pad(self) -> Path:
        assert self.pad_path is not None
        return self.pad_path


class CropSettings(BaseSettings):
    output_dir: Path = Path("output")
    crop_path: Path | None = None

    rotatable_aspect_ratio: bool = True

    crop_relative_size: Annotated[float, Field(gt=0.0, le=1.0)] = 0.5
    long_img_max_crop_size: bool = True
    long_img_threshold: PositiveFloat = 2.0

    @model_validator(mode="after")
    def _fill_crop_path(self):
        if self.crop_path is None:
            self.crop_path = self.output_dir / "crop"
        return self

    @property
    def crop(self) -> Path:
        assert self.crop_path is not None
        return self.crop_path


settings = Settings()
pad_settings = PadSettings()
crop_settings = CropSettings()
