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
    input_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            writable=True,
            resolve_path=True,
        ),
    ],
    rotatable_aspect_ratio: Annotated[bool, typer.Option()] = True,
):
    """_summary_

    Args:
        input_dir (Annotated[ Path, typer.Argument, optional): _description_. Defaults to True, readable=True, resolve_path=True, ), ].
        output_dir (Annotated[ Path, typer.Argument, optional): _description_. Defaults to True, writable=True, resolve_path=True, ), ].
        rotatable_aspect_ratio (Annotated[bool, typer.Option, optional): _description_. Defaults to True.
    """
    print("Hello World")


def crop(
    input_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Argument(
            exists=True,
            writable=True,
            resolve_path=True,
        ),
    ],
    rotatable_aspect_ratio: Annotated[bool, typer.Option()] = True,
):
    pass


if __name__ == "__main__":
    app()
