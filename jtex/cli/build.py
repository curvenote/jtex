import glob
import logging
import os
from pathlib import Path, PurePath
from shutil import copyfile

import typer
import yaml

from .. import DocModel, LatexBuilder, TemplateLoader, PublicTemplateLoader


def build(
    content_path: Path = typer.Argument(
        ...,
        help=(
            "Path to a folder with containing data and content to render. The folder should contain the following files: "
            "data.yml, main.tex, main.bib - along with any additional graphics assets"
        ),
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
    output_path: Path = typer.Argument(
        ...,
        help=(
            "Path to a folder in which to construct the Latex assets. If OUTPUT_PATH exists it "
            "and all files will be removed and a new empty folder created"
        ),
        resolve_path=True,
        dir_okay=True,
        file_okay=False,
    ),
    template_path: Path = typer.Option(
        None,
        help=(
            "Path to a Curvenote compatible LaTeX template folder. "
            "This is intended for use with local Curvenote templates or in template development. "
            "Omitting this option will use the built in template."
        ),
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
    template_name: str = typer.Option(
        None,
        help=(
            "Name of a Curvenote template available from the public Curvenote API. (e.g. 'default'). "
            "Specifying template-path will override this option if both are provided."
        ),
    ),
    lipsum: bool = typer.Option(
        False,
        help=(
            "If lipsum, will patch the document with '\\usepackage{lipsum}'. "
            "Useful when testing templates, where `content.tex` uses the lipsum package."
        ),
    ),
    strict: bool = typer.Option(
        False,
        help=(
            "If strict, then missing required tagged content or options will halt the process."
        ),
    ),
    copy: bool = typer.Option(
        True,
        help=("Should image assets will be copied into the target folder?"),
    ),
):
    typer.echo(f"Target folder: {output_path}")

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
    elif template_name:
        typer.echo(f"Using template {template_name} from the Curvenote API")
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


    if template_path:
        loader = TemplateLoader(str(output_path))
        template_options, renderer = loader.initialise_from_path(str(template_path))
    elif template_name:
        loader = PublicTemplateLoader(str(output_path))
        template_options, renderer = loader.initialise_from_template_api(template_name)
    else:
        loader = TemplateLoader(str(output_path))
        template_options, renderer = loader.initialise_with_builtin_template()
    typer.echo("Template loaded")

    builder = LatexBuilder(template_options, renderer, str(output_path))
    builder.build(DocModel(docmodel), [content], bibtex=None, raise_if_invalid=strict)

    if bib_file.exists():
        copyfile(bib_file, os.path.join(str(output_path), "main.bib"))

    typer.echo("Checking content_path for image assets")
    typer.echo(f"Content Path: {content_path}")
    typer.echo(f"Target Folder: {output_path}")
    if not copy:
        typer.echo("--no-copy option is set - not copying image assets")
    else:
        image_types = ["*.png", "*.jpg", "*.jpeg", "*.eps", "*.gif", "*.bmp"]
        image_files = []
        for im_type in image_types:
            image_files.extend(
                glob.glob(f"{content_path}/**/{im_type}", recursive=True)
            )
        if len(image_files) > 0:
            typer.echo(f"Found {len(image_files)} image assets")
            for im_file_path in image_files:
                src_path, filename = os.path.split(im_file_path)
                internal_src_path = Path(src_path).relative_to(content_path)
                os.makedirs(output_path / internal_src_path, exist_ok=True)
                dest = output_path / internal_src_path / filename
                copyfile(im_file_path, dest)
                typer.echo(f"Copied {filename} to {dest}")
        else:
            typer.echo("No image assets found")

    typer.echo("Done!")
