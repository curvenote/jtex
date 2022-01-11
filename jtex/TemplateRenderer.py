import logging
import re
from os import path
from typing import Dict, List, Optional, Union

from jinja2 import BaseLoader, Environment, FileSystemLoader, Undefined


class SilentUndefined(Undefined):
    """
    Dont break renders because vars arent there!
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        logging.exception("Found undefined variable skipping %s %s", args, kwargs)
        return None


class TemplateRenderer:
    jinja: Optional[Environment]

    def __init__(self):
        self.jinja = None

    def reset_environment(self, loader=None):
        """
        Define our own custom jinja environment that plays nicely with LaTeX

        [# #] - blocks
        [- -] - variables
        ## ## - comments

        disabled line statements

        """
        self.jinja = Environment(
            block_start_string=r"[#",
            block_end_string="#]",
            variable_start_string=r"[-",
            variable_end_string="-]",
            line_comment_prefix=r"%%",
            comment_start_string=r"%#",
            comment_end_string="#%",
            trim_blocks=True,
            autoescape=False,
            auto_reload=True,
            loader=loader,
            undefined=SilentUndefined,
            keep_trailing_newline=True,
        )
        self.jinja.globals.update(__builtins__)

    def use_from_folder(self, searchpath: Union[str, List[str]]):
        """
        Load templates from file system
        """
        self.reset_environment(FileSystemLoader(searchpath))

    def use_loader(self, loader: BaseLoader):
        """
        Load the basic template (fallback) included in the package
        """
        self.reset_environment(loader)

    def render_from_string(self, template: str, data: Dict, content: str = ""):
        """
        Render using the template specified in a string
        """
        if self.jinja is None:
            raise ValueError("Environment not initialized")
        template_obj = self.jinja.from_string(template)
        return template_obj.render(**data, CONTENT=content)

    def list_templates(self):
        if self.jinja is None:
            raise ValueError("Environment not initialized")
        return [t for t in self.jinja.list_templates() if re.match(r".*.tex$", t)]

    def render(self, data: Dict, content: str, template_name: str = "template.tex"):
        """
        A render method which will
        """
        if self.jinja is None:
            raise ValueError("Environment not initialized")
        template = self.jinja.get_template(template_name)
        return template.render(**data, CONTENT=content)
