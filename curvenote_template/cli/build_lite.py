import os
from pathlib import Path
from shutil import copyfile

import typer
import yaml

from .. import TemplateRenderer


def build_lite(
    target: Path = typer.Argument(
        ...,
        help=(
            "Local files to write the rendered content to. If TARGET exists it will be replaced"
        ),
        resolve_path=True,
        file_okay=True,
        dir_okay=False,
    ),
    docmodel_file: Path = typer.Argument(
        ...,
        help=(
            "Path to a YAML file containing the DocModel required to render the template."
            "For free-form rendering the DocModel is a free-dorm dict."
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    content_file: Path = typer.Argument(
        ...,
        help=(
            "Path to a YAML file containing the DocModel required to render the template"
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    template_file: Path = typer.Argument(
        ...,
        help=(
            "Path to a file with a compatible LaTeX template e.g. mytemplate.tex."
            "Intended for simple free-form usage with any template and matching DocModel data"
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    bib_file: Path = typer.Option(
        None,
        help=(
            "Path to an optional bib file."
            "This will be copied as-is into the target folder."
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    lipsum: bool = typer.Option(
        False,
        help=(
            "If specified will patch the document with '\\usepackage{lipsum}'."
            "For use in template testing where `example/content.tex` uses the lipsum package."
        ),
    ),
):
    typer.echo(f"Target folder: {target}")
    typer.echo(f"Doc Model file: {docmodel_file}")
    typer.echo(f"Content file: {content_file}")
    typer.echo(f"Template file: {template_file}")
    if bib_file:
        typer.echo(f"Bib file: {bib_file}")
    if lipsum:
        typer.echo(f"Adding lipsum package to final document")

    content = ""
    try:
        with open(content_file) as cfile:
            content = cfile.read()
    except:
        typer.echo("Could not read content")
        raise typer.Exit(code=1)

    docmodel = {}
    try:
        with open(docmodel_file) as dfile:
            docmodel = yaml.load(dfile.read(), Loader=yaml.FullLoader)
    except:
        typer.echo("Could not load data (DocModel)")
        raise typer.Exit(code=1)

    template = ""
    try:
        with open(template_file) as tfile:
            template = tfile.read()
    except:
        typer.echo("Could not template")
        raise typer.Exit(1)

    typer.echo("Rendering...")
    renderer = TemplateRenderer()
    renderer.reset_environment()

    if lipsum:
        docmodel["lipsum"] = True

    rendered = renderer.render_from_string(template, dict(**docmodel, CONTENT=content))
    typer.echo("Rendered")

    try:
        with open(target, "w") as outfile:
            outfile.write(rendered)
    except:
        typer.echo("Could not write output file")
        typer.Exit(1)

    if bib_file:
        copyfile(bib_file, os.path.join(str(target), "main.bib"))

    typer.echo("Done!")
