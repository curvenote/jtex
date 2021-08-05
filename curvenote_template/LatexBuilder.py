import os
import logging
import shutil
from typing import Any, Dict, NewType, Optional, List
from .utils import log_and_raise_errors
from . import DefBuilder, TemplateOptions, TemplateRenderer, DocModel

logger = logging.getLogger()


class LatexBuilder:
    def __init__(
        self, options: TemplateOptions, renderer: TemplateRenderer, target_folder: str
    ):
        self.options = options
        self.renderer = renderer
        self.target_folder = target_folder

    def build(self, data: DocModel, content: List[str], bibtex: Optional[str] = None):
        logging.info("Rendering template...")
        if self.renderer is None:
            logging.info(
                "TemplateRender is not available, TemplateLoader not initialized"
            )
            raise ValueError(
                "TemplateRender is not available, TemplateLoader not initialized"
            )

        data["CONTENT"] = content[0]
        rendered_content = [self.renderer.render(data)]
        self._write(rendered_content, bibtex)

    @log_and_raise_errors(lambda *args: "Could not write final document")
    def _write(self, content: List[str], bibtex: Optional[str]):
        logging.info("ProjectBuilder - writing...")

        def_builder = DefBuilder()
        def_builder.build(self.options, self.target_folder)
        content_transforms = def_builder.get_content_transforms(self.options)

        if not self.options.compact:
            raise NotImplementedError(
                "LatexBuilder not implemented for books layouts yet"
            )

        logging.info("Applying content transforms")
        transformed_content = ""
        for chunk in content:
            transformed_chunk = chunk
            for transform in content_transforms:
                transformed_chunk = transform(transformed_chunk)
            transformed_content += transformed_chunk + "\n"

        logging.info("Writing main.tex...")
        with open(os.path.join(self.target_folder, "main.tex"), "w+") as file:
            file.write(transformed_content)

        logging.info("Writing main.bib...")
        if bibtex:
            with open(os.path.join(self.target_folder, "main.bib"), "w+") as file:
                file.write(bibtex)

        logging.info("Cleaning up...")
        files = ["template.tex", "template.yml"]
        for file in files:
            if os.path.exists(os.path.join(self.target_folder, file)):
                shutil.move(
                    os.path.join(self.target_folder, file),
                    os.path.join(self.target_folder, f"{file}.ignore"),
                )

        logging.info("Done!")
