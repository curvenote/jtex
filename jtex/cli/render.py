import glob
import os
from pathlib import Path
from shutil import copyfile
from typing import Dict

import typer

from .. import DocModel, LatexBuilder, PublicTemplateLoader, TemplateLoader, utils


def validate_document(docmodel: DocModel):
    # TODO
    return True


def render(
    content_file: Path = typer.Argument(
        ...,
        help=(
            "Path to a .tex file with containing jtex front matter content to render."
        ),
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
    ),
    output_path: Path = typer.Option(
        None,
        help=(
            "If supplied with override the jtex.output.path (and default path) specified in front matter"
            "This is useful when dynamically setting a temporary output folder."
            "Will be created if it does not exist."
        ),
        exists=False,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
    template_path: Path = typer.Option(
        None,
        help=(
            "If supplied with override the jtex.template option and use the template found on this path"
        ),
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
    ),
):
    typer.echo(f"Content: {content_file}")
    if content_file.exists() and content_file.is_file():
        typer.echo("Found content")
    else:
        typer.echo("content not found")
        raise typer.Exit(code=1)

    # open content file
    fm_and_content = ""
    try:
        with open(content_file) as cfile:
            fm_and_content = cfile.read()
        typer.echo("Loaded content")
    except:
        typer.echo("Could not read content")
        raise typer.Exit(code=1)

    # Load configuration from front matter
    fm, content = utils.parse_front_matter(fm_and_content)
    if fm is None:
        typer.echo("Could not read front matter in content")
        raise typer.Exit(code=1)

    # will validate and throw on invalid front matter
    docmodel = DocModel(fm)

    content_path = os.path.dirname(os.path.abspath(content_file))
    typer.echo(f"Content path {content_path}")

    # output.path is treated as relative to the content_path, not the current working directory
    jtex_output_path = os.path.expanduser(docmodel.get("jtex.output.path", str, "."))
    target_folder = (
        jtex_output_path
        if os.path.isabs(jtex_output_path)
        else os.path.abspath(
            os.path.join(content_path, docmodel.get("jtex.output.path", str, "."))
        )
    )
    if output_path is not None:  # option overrides jtex setting
        target_folder = str(output_path)
        os.makedirs(target_folder, exist_ok=True)
    typer.echo(f"Target output folder {target_folder}")

    jtex_working_path = target_folder

    # check for references and confirm bib file
    references = docmodel.get("jtex.input.references")
    bib_file = ""
    if references is not None:
        bib_file = Path(content_path, references)
        if bib_file.exists():
            typer.echo(f"Found bib file at {bib_file}")
        else:
            typer.echo(f"Could not find references bib file at {bib_file}")
            raise typer.Exit(code=1)

    # check for tagged content and load it
    tagged_files = docmodel.get("jtex.input.tagged", Dict[str, str], {})
    tagged = {}
    missing_tagged_files = []
    for key, tagged_file in tagged_files.items():
        tagged_file_path = os.path.join(content_path, tagged_file)
        if not os.path.exists(tagged_file_path):
            missing_tagged_files.append((key, tagged_file_path))
            continue
        with open(tagged_file_path, "r") as f:
            tagged[key] = f.read()

    if len(missing_tagged_files) > 0:
        typer.echo("Could not find the following tagged content files:")
        _ = [typer.echo(f"{k}: {v}") for k, v in missing_tagged_files]
        typer.Exit(code=1)

    template = docmodel.get("jtex.template")
    if template_path is not None:
        typer.echo(f"Using local template at: {template_path}")
        loader = TemplateLoader(jtex_working_path)
        template_options, renderer = loader.initialise_from_path(str(template_path))
    elif template is not None:
        typer.echo(
            f"Using template {docmodel.get('jtex.template')} from the Curvenote API"
        )
        loader = PublicTemplateLoader(jtex_working_path)
        template_options, renderer = loader.initialise_from_template_api(template)
    else:
        typer.echo("Using built in template")
        loader = TemplateLoader(jtex_working_path)
        template_options, renderer = loader.initialise_with_builtin_template()
    typer.echo("Template loaded")

    builder = LatexBuilder(template_options, renderer, str(target_folder))
    builder.build(
        docmodel,
        [content],
        tagged,
        bibtex=None,
        raise_if_invalid=docmodel.get("jtex.strict", bool, False),
    )

    if references is not None:
        target_bib = os.path.join(str(target_folder), "main.bib")
        if bib_file != Path(target_bib):
            copyfile(bib_file, target_bib)

    typer.echo("Checking content_path for image assets")
    typer.echo(f"Content Path: {content_path}")
    typer.echo(f"Target Folder: {target_folder}")

    copy = True
    try:
        copy = docmodel.get("jtex.output.copy_images")
    except:
        pass

    if not copy:
        typer.echo("jtex.output.copy_images option is false - not copying image assets")
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
                os.makedirs(target_folder / internal_src_path, exist_ok=True)
                dest = target_folder / internal_src_path / filename
                if Path(im_file_path) != dest:
                    copyfile(im_file_path, dest)
                    typer.echo(f"Copied {filename} to {dest}")
        else:
            typer.echo("No image assets found")

    typer.echo("Done!")
