import glob
import logging
import os
from distutils.dir_util import copy_tree
from shutil import copyfile
from typing import Dict, Optional, Tuple

import pkg_resources
from jinja2.loaders import PackageLoader

from .TemplateOptions import TemplateOptions
from .TemplateRenderer import TemplateRenderer

DEFAULT_TEMPLATE_PATH = pkg_resources.resource_filename("jtex", "builtin_template")


class TemplateLoader:
    def __init__(self, target_folder: str):
        self._template_name: Optional[str] = None
        self._target_folder: str = target_folder
        os.makedirs(self._target_folder, exist_ok=True)

    @staticmethod
    def validate(template_path: str) -> int:
        logging.info("Validaing template on: %s", template_path)
        code = 0
        if os.path.exists(os.path.join(template_path, "template.tex")):
            logging.info("Found template.tex")
        else:
            logging.error("template.tex not found")
            code = 1
        if os.path.exists(os.path.join(template_path, "template.yml")):
            logging.info("Found template.yml")
            try:
                TemplateOptions(str(template_path))
            except ValueError as err:
                logging.error("Error while parsing template.yml")
                code = 1
        else:
            logging.error("template.yml not found")
            code = 1

        thumb = glob.glob(os.path.join(template_path, "thumbnail.*"))
        if len(thumb) > 1:
            logging.error("Found multiple files named thumbnail")
            logging.error("Please provide a single thumbnail.png")
            code = 1
        if os.path.exists(os.path.join(template_path, "thumbnail.png")):
            logging.info("Found thumbnail.png")
        elif thumb:
            logging.error("Found %s", thumb[0])
            logging.error("Only PNG format thumbnails are supported")
            code = 1

        if code == 1:
            raise ValueError("Template is not valid")

        return code

    def is_initialized(self):
        return self._template_name is not None

    def initialise_with_builtin_template(
        self,
    ) -> Tuple[TemplateOptions, TemplateRenderer]:
        logging.info("TemplateLoader - Initialising with builtin template")
        logging.info("Copying template assets")
        template_assets = ["curvenote.png", "template.yml"]
        for asset_filename in template_assets:
            src = os.path.join(DEFAULT_TEMPLATE_PATH, asset_filename)
            dest = os.path.join(self._target_folder, asset_filename)
            logging.info("Copying: %s to %s", src, dest)
            copyfile(src, dest)

        self._template_name = "builtin"
        renderer = TemplateRenderer()
        renderer.use_loader(PackageLoader("jtex", os.path.join("builtin_template")))

        return TemplateOptions(DEFAULT_TEMPLATE_PATH), renderer

    def initialise_from_path(
        self, local_template_path: str
    ) -> Tuple[TemplateOptions, TemplateRenderer]:
        logging.info("Using local template found at: %s", local_template_path)

        abs_path = os.path.abspath(os.path.expanduser(local_template_path))

        if not os.path.exists(abs_path):
            raise ValueError("local template path does not exist")

        if not os.path.isdir(abs_path):
            raise ValueError("local template path must point to a folder")

        try:
            copy_tree(abs_path, self._target_folder)
        except Exception as err:
            logging.error(
                "Could not copy local template from %s to %s",
                abs_path,
                self._target_folder,
            )
            logging.error(str(err))
            raise err

        self._template_name = os.path.basename(os.path.normpath(abs_path))
        renderer = TemplateRenderer()
        renderer.use_from_folder(self._target_folder)

        return TemplateOptions(self._target_folder), renderer
