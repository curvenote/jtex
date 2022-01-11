import os
from pathlib import Path
from shutil import copyfile

import typer

from .. import DocModel, TemplateRenderer, utils


def freeform(
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
    content_tex: Path = typer.Argument(
        ...,
        help=("Path to a file containing the content to render and jtex front matter."),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    output_tex: Path = typer.Option(
        None,
        help=(
            "Optional name of a local file to write the rendered content to."
            "This will override the data specified in the front matter in content."
        ),
        resolve_path=True,
        file_okay=True,
        dir_okay=False,
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
):
    typer.echo(f"Output file: {output_tex}")
    typer.echo(f"Content file: {content_tex}")
    typer.echo(f"Template file: {template_tex}")
    if bib:
        typer.echo(f"Bib file: {bib}")

    fm_and_content = ""
    if content_tex:
        try:
            with open(content_tex) as cfile:
                fm_and_content = cfile.read()
        except:
            typer.echo("Could not read content")
            raise typer.Exit(code=1)

    # Load configuration from front matter
    fm, content = utils.parse_front_matter(fm_and_content)
    if fm is None:
        typer.echo("Could not read front matter in content")
        raise typer.Exit(code=1)

    # will validate and throw on invalid front matter
    docmodel = DocModel(fm, ensure_defaults=False)

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

    rendered = renderer.render_from_string(template, docmodel.to_dict(), content)
    typer.echo("Rendered")

    try:
        os.makedirs(os.path.dirname(output_tex), exist_ok=True)
        with open(output_tex, "w") as outfile:
            outfile.write(utils.stringify_front_matter(docmodel.to_dict()))
            outfile.write(rendered)
    except:
        typer.echo("Could not write output file")
        typer.Exit(1)

    if bib:
        copyfile(bib, os.path.join(str(output_tex), "main.bib"))

    typer.echo("Done!")
