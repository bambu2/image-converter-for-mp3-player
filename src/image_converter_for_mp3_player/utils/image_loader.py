from pathlib import Path

from PIL import Image


def load_image_rgb(image_path: Path) -> Image.Image:
    """加载图像并转换为 RGB 模式。"""
    with Image.open(image_path) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        return img
