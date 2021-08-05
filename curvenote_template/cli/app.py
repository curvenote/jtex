import sys
import typer
import logging
from .validate import validate
from .build_lite import build_lite
from .build import build

from ..version import __version__

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
        "Build a LaTeX document based on a free-form template, accompanying docmodel"
        "data structure and content. This can be used for general tempate rendering independent of"
        "Curvenote's prescriptive template structure."
        "To build based on (and to develop/test) Curvenote templates use `build`."
    )
)(build_lite)
app.command(
    help=(
        "Build a LaTeX document based on a Curvenote LaTeX Template, accompanying docmodel"
        "data structure and content."
        "Can be used to develop/test Curvenote templates."
    )
)(build)


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
