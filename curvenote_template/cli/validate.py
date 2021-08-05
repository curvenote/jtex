import os
import typer
import logging
from pathlib import Path
from ..TemplateOptions import TemplateOptions
from ..TemplateLoader import TemplateLoader


def validate(
    template_path: Path = typer.Argument(
        ...,
        help=("Local folder containing the Curvenote compatible template to validate"),
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    )
):
    try:
        TemplateLoader.validate(str(template_path))
    except ValueError as err:
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)
