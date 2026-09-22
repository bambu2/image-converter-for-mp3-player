from pathlib import Path

from pydantic import BaseModel, Field, PositiveInt
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False

    input_path: Path = Path("input")
    output_path: Path = Path("output")

    screen_resolution: tuple[PositiveInt, PositiveInt] = (240, 320)
    screen_aspect_ratio: float = screen_resolution[0] / screen_resolution[1]

    rotatable_aspect_ratio: bool = True
    recursive: bool = True

    img_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}


class PadSettings(BaseModel):
    pad_path: Path = Settings.output_path / "pad"


class CropSettings(BaseSettings):
    crop_path: Path = Settings.output_path / "crop"
