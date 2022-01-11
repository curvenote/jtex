import logging
import os
from re import template
from typing import Dict, List, Tuple, cast
from zipfile import ZipFile

import requests
import typer

from .TemplateLoader import TemplateLoader
from .TemplateOptions import TemplateOptions
from .TemplateRenderer import TemplateRenderer
from .utils import download

API_URL = "https://api.curvenote.com"
TEMPLATE_DOWNLOAD_URL = "{api_url}/templates/{template_name}/download"


class PublicTemplateLoader(TemplateLoader):
    def __init__(self, template_location: str):
        super().__init__(template_location)

    def initialise_from_template_api(
        self, template_name: str
    ) -> Tuple[TemplateOptions, TemplateRenderer]:
        logging.info("Writing to target folder: %s", self._target_folder)

        logging.info("Looking up template %s", template_name)
        try:
            logging.info(
                TEMPLATE_DOWNLOAD_URL.format(
                    api_url=API_URL, template_name=template_name
                )
            )
            download_info = requests.get(
                TEMPLATE_DOWNLOAD_URL.format(
                    api_url=API_URL, template_name=template_name
                )
            ).json()
            if "link" not in download_info:
                typer.echo(f"Template '{template_name}' not found")
                raise typer.Exit(-1)
        except ValueError as err:
            logging.error("could not download template %s", template_name)
            raise ValueError(f"could not download template: {template_name}") from err

        # fetch template to local folder
        logging.info(f"Found template, download url {download_info['link']}")
        logging.info("downloading...")
        zip_filename = os.path.join(
            self._target_folder, f"{template_name}.template.zip"
        )
        download(download_info["link"], zip_filename)

        # unzip
        logging.info("Download complete, unzipping...")
        with ZipFile(zip_filename, "r") as zip_file:
            zip_file.extractall(self._target_folder)
        logging.info("Unzipped to %s", self._target_folder)
        os.remove(zip_filename)
        logging.info("Removed %s", zip_filename)

        # success -- update members
        self._template_name = template_name
        renderer = TemplateRenderer()
        renderer.use_from_folder(self._target_folder)

        return TemplateOptions(self._target_folder), renderer
