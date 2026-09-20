import logging
from pathlib import Path

import typer

from image_converter_for_mp3_player.log import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

logger.info("程序启动")


def main(input_dir: Path, output_dir: Path, rotatable_aspect_ratio: bool = True):
    print("Hello World")


if __name__ == "__main__":
    typer.run(main)
