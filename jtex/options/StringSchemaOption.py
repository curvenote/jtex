from typing import Dict, Optional, Union

from .SchemaOption import SchemaOption
from .SchemaOptionDefs import CustomTemplateDefs, SchemaOptionDefs


class StringSchemaOption(SchemaOption):
    def __init__(self):
        self.value_map: Dict[str, Union[SchemaOptionDefs, CustomTemplateDefs]] = {}
        self.default: Union[str, None] = None

    def add(self, name: str, value: SchemaOptionDefs):
        if name in self.value_map:
            raise ValueError(f"Duplicate option {name}")
        self.value_map[name] = value

    def set_default(self, name: str):
        self.default = name
        self.value_map["default"] = self.value_map[name]

    def get(
        self, name: Optional[str] = None
    ) -> Union[SchemaOptionDefs, CustomTemplateDefs]:
        if name is None and self.default is None:
            raise ValueError("No default option set")
        if name is not None and name not in self.value_map:
            raise ValueError(f"Unknown option: {name}")
        if name in self.value_map:
            return self.value_map[name]
        return self.value_map[self.default]

    def names(self):
        return [k for k, v in self.value_map.items()]
