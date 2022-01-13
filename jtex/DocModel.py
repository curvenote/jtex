import os
from typing import Any, Dict, NewType, Type, cast

from mergedeep import merge
from pykwalify.core import Core

from .TemplateOptions import SCHEMA_PATH

# DocModel = NewType("DocModel", Dict[str, Any])

DEFAULTS = dict(
    jtex=dict(
        version=1,
        strict=False,
        input=dict(),
        output=dict(
            path="_build", filename="main.tex", copy_images=True, single_file=False
        ),
        options=dict(),
    )
)


class DocModel:
    @staticmethod
    def find(element: str, data: Dict):
        keys = element.split(".")
        rv = data
        for key in keys:
            if key not in rv:
                raise KeyError(f"{key} not found")
            rv = rv[key]
        return rv

    def __init__(self, data: Dict, ensure_defaults=True):
        self.model = self.ensure_defaults(data) if ensure_defaults else data
        self._parser = Core(
            source_data=self.model,
            schema_files=[
                os.path.join(SCHEMA_PATH, "frontmatter.schema.yml"),
            ],
        )
        self._parser.validate(raise_exception=True)

    def ensure_defaults(self, data: Dict):
        x = DEFAULTS.copy()
        merge(x, data)
        return x

    def get(self, path: str, type: Type = Any, default: Any = None):
        """
        Get a value from the template options on the specified path

        raises a ValueError if the options is not found
        """
        if self.model is None:
            return default
        try:
            return cast(type, DocModel.find(path, self.model))
        except KeyError:
            return default

    def to_dict(self) -> Dict:
        return cast(Dict, self.model).copy()
