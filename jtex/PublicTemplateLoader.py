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

CURVENOTE_API_URL = os.getenv("CURVENOTE_API_URL")
API_URL = (
    CURVENOTE_API_URL if CURVENOTE_API_URL is not None else "https://api.curvenote.com"
)
TEMPLATE_DOWNLOAD_URL = "{api_url}/templates/tex/{template_name}/download"
OLD_TEMPLATE_DOWNLOAD_URL = "{api_url}/templates/{template_name}/download"


def do_download(URL: str, template_name: str):
    url = URL.format(api_url=API_URL, template_name=template_name)
    logging.info(f"DOWNLOAD: {url}")
    try:
        download_info = requests.get(url).json()
        if "status" in download_info and download_info["status"] != 200:
            raise ValueError(f'{template_name} not found - {download_info["status"]}')
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Requests error - {url} - {e}")
    return download_info


class PublicTemplateLoader(TemplateLoader):
    def __init__(self, template_location: str):
        super().__init__(template_location)

    def initialise_from_template_api(
        self, template_name: str
    ) -> Tuple[TemplateOptions, TemplateRenderer]:
        logging.info("Writing to target folder: %s", self._target_folder)

        logging.info("Looking up template %s", template_name)
        logging.info("latest code")
        try:
            download_info = {}
            try:
                name = (
                    template_name
                    if template_name.startswith("public/")
                    else f"public/{template_name}"
                )
                download_info = do_download(TEMPLATE_DOWNLOAD_URL, name)
            except:
                name = (
                    template_name
                    if not template_name.startswith("public/")
                    else template_name[7:]
                )
                download_info = do_download(OLD_TEMPLATE_DOWNLOAD_URL, name)
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
            self._target_folder, f"{template_name.replace('/','_')}.template.zip"
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
