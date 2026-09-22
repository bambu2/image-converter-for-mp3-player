import logging
from pathlib import Path
from typing import Annotated

import typer
from rich import print
from rich.progress import track

from image_converter_for_mp3_player.log import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

logger.info("程序启动")

app = typer.Typer()


@app.command()
def pad(
    input_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            writable=True,
            resolve_path=True,
        ),
    ],
    screen_resolution: Annotated[tuple[int, int], typer.Argument()],
    rotatable_aspect_ratio: Annotated[bool, typer.Option()],
):

    print("Hello World")


@app.command()
def crop(
    input_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            writable=True,
            resolve_path=True,
        ),
    ],
    screen_resolution: Annotated[tuple[int, int], typer.Argument()],
    rotatable_aspect_ratio: Annotated[bool, typer.Option()],
):
    pass


if __name__ == "__main__":
    app()
