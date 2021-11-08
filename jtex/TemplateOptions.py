import logging
import os
from typing import Any, Dict, Optional, Set, Union, cast

import pkg_resources
import yaml
from pykwalify.core import Core

from jtex.TexFormat import TexFormat

SCHEMA_PATH = pkg_resources.resource_filename("jtex", "schema")


class TemplateOptions:
    def __init__(self, template_location: str):
        self._template_location: str = template_location

        template_yml = os.path.join(template_location, "template.yml")
        logging.info("Looking for template on %s", template_yml)
        if not os.path.exists(template_yml):
            logging.info("%s does not exist", template_yml)
            raise FileNotFoundError(f"{template_yml} does not exist")

        self._parser: Core = Core(
            source_file=template_yml,
            schema_files=[
                os.path.join(SCHEMA_PATH, "config.schema.yml"),
                os.path.join(SCHEMA_PATH, "template.schema.yml"),
            ],
        )
        self._parser.validate(raise_exception=True)

        # now that schemas are loaded, we can configure additional options
        self._tex_format: TexFormat = (
            TexFormat.tex
            if self.get("config.build.vanilla")
            else TexFormat.tex_curvenote
        )

    @property
    def tex_format(self) -> TexFormat:
        return self._tex_format

    @property
    def template_location(self):
        return self._template_location

    def get_allowed_tags(self) -> Set[str]:
        return set(map(lambda item: item["id"], self.tagged))

    def get(self, path: str, default: Any = None):
        """
        Get a value from the template options on the specified path

        raises a ValueError if the options is not found
        """
        if self._parser is None or self._parser.source is None:
            return default
        try:
            return TemplateOptions.find(path, self._parser.source)
        except KeyError:
            return default

    @staticmethod
    def find(element: str, data: Dict):
        keys = element.split(".")
        rv = data
        for key in keys:
            if key not in rv:
                raise KeyError(f"{key} not found")
            rv = rv[key]
        return rv

    def validate_user_options(self, user_options: Dict):
        """
        Parse a dict of user options, validate these against the template and
        register any valid options.

        Discard any option not listed in or conforming to the template config.options section
        """
        # TODO register user defined options
        pass

    @property
    def compact(self):
        return self.get("config.build.layout") == "compact"

    @property
    def schema_options(self) -> Dict[str, Union[str, bool]]:
        """
        Return the schema secton
        """
        if self._parser is None or self._parser.source is None:
            return {}
        return self._parser.source["config"]["schema"]

    @property
    def tagged(self) -> Dict:
        """
        Return the tagged section
        """
        return cast(Dict, self.get("config.tagged", {}))

    @property
    def config_options(self):
        """
        TODO
        """
        if self._parser is None or self._parser.source is None:
            return {}
        return self._parser.source["config"]["options"]
