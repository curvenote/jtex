import logging
import sys

import typer

from ..version import __version__
from .freeform import freeform
from .render import render
from .validate import validate

logger = logging.getLogger()

logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


app = typer.Typer()

app.command(help=("Validate a Curvenote LaTeX Template"))(validate)
app.command(
    help=(
        "Build a LaTeX document based on a free-form template, accompanying data structure and optional 'body' content. "
        "This can be used for general template rendering independently from Curvenote's prescriptive template structure. "
        "To build based on (and to develop/test) Curvenote templates use `build`."
    )
)(freeform)
app.command(
    help=(
        "Build a LaTeX document based on a Curvenote LaTeX Template, accompanying docmodel "
        "data structure and content. "
        "Can be used to develop/test Curvenote templates."
    )
)(render)


def version_callback(value: bool):
    if value:
        typer.echo(
            r"""
                LaTeX Template Generating System by Curvenote
            """
        )
        typer.echo(f"Version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    )
):
    return
