import logging
from collections.abc import Iterable
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)


def post_process(
    img_iter: Iterable[Image.Image],
    size: tuple[int, int],
    output_dir: Path,
    stem: str,
) -> None:
    """Save thumbnails of `img_iter` as `<stem>_<i>.jpg` in `output_dir`.

    Note: each input image is consumed (may be closed) and should not be
    reused after being passed to this function.
    """
    for i, result_img in enumerate(img_iter):
        thumb = _thumbnail_to_screen(result_img, size)
        _save_as_jpg(thumb, output_dir / f"{stem}_{i}.jpg")


def _thumbnail_to_screen(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    thumb = img.copy()
    thumb.thumbnail(size, Image.Resampling.LANCZOS)
    return thumb


def _save_as_jpg(img: Image.Image, path: Path) -> None:
    try:
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(path, "JPEG", quality=90, subsumpling=0)
    finally:
        img.close()
