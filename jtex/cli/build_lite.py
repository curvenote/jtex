import os
from pathlib import Path
from shutil import copyfile

import typer
import yaml

from .. import TemplateRenderer


def build_lite(
    data_yml: Path = typer.Argument(
        ...,
        help=(
            "Path to a YAML file containing the DocModel (a free-form dict) required to render the template."
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    template_tex: Path = typer.Argument(
        ...,
        help=(
            "Path to a file with a compatible LaTeX template e.g. mytemplate.tex. "
            "The template should align with the data structure given by the DocModel"
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    output_tex: Path = typer.Argument(
        ...,
        help=(
            "Name of a local file to write the rendered content to. If OUTPUT exists it will be replaced."
        ),
        resolve_path=True,
        file_okay=True,
        dir_okay=False,
    ),
    content: Path = typer.Option(
        None,
        help=("Path to a file containing the content to render in the [-CONTENT-] variable"),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    bib: Path = typer.Option(
        None,
        help=(
            "Path to an optional bib file. "
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
            "If specified will patch the document with '\\usepackage{lipsum}'. "
            "Useful in testing where `content.tex` or `temaplte.tex` uses the lipsum package."
        ),
    ),
):
    typer.echo(f"Output folder: {output_tex}")
    typer.echo(f"Doc Model file: {data_yml}")
    typer.echo(f"Content file: {content}")
    typer.echo(f"Template file: {template_tex}")
    if bib:
        typer.echo(f"Bib file: {bib}")
    if lipsum:
        typer.echo(f"Adding lipsum package to final document")

    body_content = ""
    if (content):
        try:
            with open(content) as cfile:
                body_content = cfile.read()
        except:
            typer.echo("Could not read content")
            raise typer.Exit(code=1)

    docmodel = {}
    try:
        with open(data_yml) as dfile:
            docmodel = yaml.load(dfile.read(), Loader=yaml.FullLoader)
    except:
        typer.echo("Could not load data (DocModel)")
        raise typer.Exit(code=1)

    template = ""
    try:
        with open(template_tex) as tfile:
            template = tfile.read()
    except:
        typer.echo("Could not template")
        raise typer.Exit(1)

    typer.echo("Rendering...")
    renderer = TemplateRenderer()
    renderer.reset_environment()

    if lipsum:
        docmodel["lipsum"] = True

    rendered = renderer.render_from_string(template, dict(**docmodel, CONTENT=body_content))
    typer.echo("Rendered")

    try:
        with open(output_tex, "w") as outfile:
            outfile.write(rendered)
    except:
        typer.echo("Could not write output file")
        typer.Exit(1)

    if bib:
        copyfile(bib, os.path.join(str(output_tex), "main.bib"))

    typer.echo("Done!")
