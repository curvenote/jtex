import glob
import logging
import os
from pathlib import Path, PurePath
from shutil import copyfile

import typer
import yaml

from .. import DocModel, LatexBuilder, TemplateLoader


def build(
    target_folder: Path = typer.Argument(
        ...,
        help=(
            "Local folder in which to construct the Latex assets. If TARGET exists it"
            "and all files will be removed and a new empty folder structure created"
        ),
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    content_path: Path = typer.Argument(
        ...,
        help=(
            "Path to a folder with containing content to render. Folder shoud contain the following files:\n"
            "  - main.tex\n"
            "  - main.bib\n"
            "  - data.yaml\n"
            "Along with any additional graphics assets"
        ),
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
    template_path: Path = typer.Argument(
        None,
        help=(
            "Path to a Curvenote compatible LaTeX template folder."
            "This is intended for use with local Curvenote templates or in template development."
            "Omitting this option will use the built in template."
        ),
        exists=True,
        dir_okay=True,
        file_okay=False,
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
    typer.echo(f"Target folder: {target_folder}")

    typer.echo(f"Content path: {content_path}")
    content_file = Path(content_path, "main.tex")
    if content_file.exists() and content_file.is_file():
        typer.echo("Found main.tex")
    else:
        typer.echo("main.tex not found")
        raise typer.Exit(code=1)
    data_file = Path(content_path, "data.yml")
    if data_file.exists() and data_file.is_file():
        typer.echo("Found data.yml")
    else:
        typer.echo("data.yml not found")
        raise typer.Exit(code=1)

    bib_file = Path(content_path, "main.bib")
    if bib_file.exists():
        typer.echo("Found main.bib")

    if template_path:
        typer.echo(f"Using template at: {template_path}")
    else:
        typer.echo("Using built in template")

    if lipsum:
        typer.echo(f"Adding lipsum package to final document")

    content = ""
    try:
        with open(content_file) as cfile:
            content = cfile.read()
        typer.echo("Loaded content")
    except:
        typer.echo("Could not read content")
        raise typer.Exit(code=1)

    docmodel = {}
    try:
        with open(data_file) as dfile:
            docmodel = yaml.load(dfile.read(), Loader=yaml.FullLoader)
        typer.echo("Loaded data")
    except:
        typer.echo("Could not load data (DocModel)")
        raise typer.Exit(code=1)

    if lipsum:
        docmodel["lipsum"] = True

    loader = TemplateLoader(str(target_folder))
    if template_path:
        template_options, renderer = loader.initialise_from_path(str(template_path))
    else:
        template_options, renderer = loader.initialise_with_builtin_template()
    typer.echo("Template loaded")

    builder = LatexBuilder(template_options, renderer, str(target_folder))
    builder.build(DocModel(docmodel), [content], bibtex=None)

    if bib_file.exists():
        copyfile(bib_file, os.path.join(str(target_folder), "main.bib"))

    typer.echo("Checking content_path for image assets")
    image_types = ["*.png", "*.jpg", "*.jpeg", "*.eps", "*.gif", "*.bmp"]
    image_files = []
    for im_type in image_types:
        image_files.extend(glob.glob(f"{content_path}/{im_type}"))
    if len(image_files) > 0:
        typer.echo(f"Found {len(image_files)} image assets")
        assets_folder = os.path.join(target_folder, "assets")
        os.makedirs(assets_folder, exist_ok=True)
        for im_file_path in image_files:
            _, filename = os.path.split(im_file_path)
            dest = os.path.join(assets_folder, filename)
            copyfile(im_file_path, dest)
            typer.echo(f"Copied {filename} to {dest}")
    else:
        typer.echo("No image assets found")

    typer.echo("Done!")
