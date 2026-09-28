from pathlib import Path

from pydantic import DirectoryPath, Field, PositiveFloat, PositiveInt, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

toml_file = "config.toml"


class BlurSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="toml_file", toml_table_header=("blur",), extra="ignore"
    )
    output_dir: Path

    radius: float


class EquidistantCropSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="toml_file", toml_table_header=("equidistant-crop",), extra="ignore"
    )
    output_dir: Path

    scale_factor: PositiveFloat


class WideImageCropSettings(BaseSettings):
    model_config = SettingsConfigDict(
        toml_file="toml_file", toml_table_header=("wide-image-crop",), extra="ignore"
    )
    output_dir: Path

    scale_factor: PositiveFloat


class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file="toml_file")

    blur = BlurSettings()  # type:ignore[call-arg]
    equidistant_crop = EquidistantCropSettings()  # type:ignore[call-arg]
    wide_image_crop = WideImageCropSettings()  # type:ignore[call-arg]

    input_dir: DirectoryPath
    output_dir: Path

    landscape_resolution_str: str

    landscape_width: PositiveInt
    landscape_height: PositiveInt
    landscape_resolution: tuple[PositiveInt, PositiveInt]

    portrait_width: PositiveInt
    portrait_height: PositiveInt
    portrait_resolution: tuple[PositiveInt, PositiveInt]

    threshold: float = Field(gt=1.0)

    recursive: bool
    dry_run: bool

    rotatable_screen: bool

    img_exts: frozenset[str]

    @model_validator(mode="after")
    def _derive_screen_fields(self):
        self.landscape_width = int(self.landscape_resolution_str.split("x")[0])
        self.landscape_height = int(self.landscape_resolution_str.split("x")[1])
        self.landscape_resolution = (self.landscape_width, self.landscape_height)

        self.portrait_width = self.landscape_height
        self.portrait_height = self.landscape_width
        self.portrait_resolution = (self.portrait_width, self.portrait_height)
        return self


settings = Settings()  # type: ignore[call-arg]
