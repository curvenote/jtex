import logging
import os
import shutil
from typing import Any, Dict, List, NewType, Optional

from .DefBuilder import DefBuilder
from .DocModel import DocModel
from .TemplateOptions import TemplateOptions
from .TemplateRenderer import TemplateRenderer
from .utils import log_and_raise_errors, stringify_front_matter

logger = logging.getLogger()


class LatexBuilder:
    def __init__(
        self, options: TemplateOptions, renderer: TemplateRenderer, target_folder: str
    ):
        self.options = options
        self.renderer = renderer
        self.target_folder = target_folder

    def validate(self, data: DocModel, raise_if_invalid):
        logging.info("Validating docmodel data...")
        required_options = [
            opt["id"]
            for opt in self.options.config_options
            if "required" in opt and opt["required"]
        ]
        missing_options = [
            r for r in required_options if data.get(f"jtex.options.{r}") is None
        ]
        if len(missing_options) > 0:
            logging.warn(
                "Some REQUIRED user options are not provided: %s", missing_options
            )
            if raise_if_invalid:
                raise ValueError(
                    "Some REQUIRED user options are not provided: %s" % missing_options
                )

    def build(
        self,
        data: DocModel,
        content: List[str],
        tagged: Dict[str, str],
        bibtex: Optional[str] = None,  # TODO remove as we copy the file forwards?
        raise_if_invalid: bool = True,
    ):
        logging.info("Rendering template...")
        self.validate(data, raise_if_invalid)
        if self.renderer is None:
            logging.info(
                "TemplateRender is not available, TemplateLoader not initialized"
            )
            raise ValueError(
                "TemplateRender is not available, TemplateLoader not initialized"
            )

        # prep the data object to the shape expected  by templates
        doc = data.to_dict()
        doc.pop("jtex", None)
        data_to_render = dict(doc=doc)
        data_to_render["tagged"] = tagged
        data_to_render["options"] = data.get("jtex.options", Dict[str, Any], {})

        rendered_content = [
            self.renderer.render(data=data_to_render, content=content[0])
        ]
        self._write(data, rendered_content, bibtex)

    @log_and_raise_errors(lambda *args: "Could not write final document")
    def _write(self, data: DocModel, content: List[str], bibtex: Optional[str]):
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
        with open(
            os.path.join(
                self.target_folder, data.get("jtex.output.filename", str, "main.tex")
            ),
            "w+",
        ) as file:
            file.write(stringify_front_matter(data.to_dict()))
            file.write(transformed_content)

        logging.info("Writing main.bib...")
        if bibtex:
            with open(os.path.join(self.target_folder, "main.bib"), "w+") as file:
                file.write(bibtex)

        logging.info("Cleaning up...")
        files = [
            "template.tex",
            "template.yml",
            "thumbnail.png",
            "README.md",
            "PORT.md",
        ]
        for file in files:
            if os.path.exists(os.path.join(self.target_folder, file)):
                os.remove(os.path.join(self.target_folder, file))

        logging.info("Done!")
