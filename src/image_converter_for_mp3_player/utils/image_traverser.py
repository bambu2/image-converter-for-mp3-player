from pathlib import Path

from image_converter_for_mp3_player.config import Settings


def traverse_folder(folder: Path, recursive: bool) -> list[Path]:
    if recursive:
        return [p for p in folder.rglob("*") if p.suffix.lower() in Settings.img_exts]
    else:
        return [p for p in folder.glob("*") if p.suffix.lower() in Settings.img_exts]
