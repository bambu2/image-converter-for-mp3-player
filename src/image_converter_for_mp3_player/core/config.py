from pathlib import Path
from typing import Annotated

from pydantic import DirectoryPath, Field, PositiveFloat, PositiveInt, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

toml_file = "config.toml"


class BlurSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="toml_file", toml_table_header=("blur",), extra="ignore"
    )
    output_dir: Path = Path("output") / "blur"

    radius: float = 2.0


class EquidistantCropSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="toml_file", toml_table_header=("equidistant-crop",), extra="ignore"
    )
    output_dir: Path = Path("output") / "equidistant_crop"

    scale_factor: PositiveFloat = 0.5


class WideImageCropSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="toml_file", toml_table_header=("wide-image-crop",), extra="ignore"
    )
    output_dir: Path = Path("output") / "wide_image_crop"

    scale_factor: PositiveFloat = 1.0


class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file="toml_file")

    blur = BlurSettings()  # type:ignore[call-arg]
    equidistant_crop = EquidistantCropSettings()  # type:ignore[call-arg]
    wide_image_crop = WideImageCropSettings()  # type:ignore[call-arg]

    input_dir: DirectoryPath = Path("input")

    landscape_resolution_str: str = "320x240"

    landscape_width: PositiveInt = 1
    landscape_height: PositiveInt = 1
    landscape_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)

    portrait_width: PositiveInt = 1
    portrait_height: PositiveInt = 1
    portrait_resolution: tuple[PositiveInt, PositiveInt] = (1, 1)

    threshold: Annotated[float, Field(gt=1.0)] = 2.0

    recursive: bool = True
    dry_run: bool = False

    rotatable_screen: bool = True

    img_exts: frozenset[str] = frozenset(
        {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    )

    @model_validator(mode="after")
    def _derive_screen_fields(self):
        self.landscape_width = int(self.landscape_resolution_str.split("x")[0])
        self.landscape_height = int(self.landscape_resolution_str.split("x")[1])
        self.landscape_resolution = (self.landscape_width, self.landscape_height)

        self.portrait_width = self.landscape_height
        self.portrait_height = self.landscape_width
        self.portrait_resolution = (self.portrait_width, self.portrait_height)
        return self


settings = Settings()
