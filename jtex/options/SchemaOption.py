from typing import Dict, Optional, Union

from .SchemaOptionDefs import CustomTemplateDefs, SchemaOptionDefs


class SchemaOption:
    def add(self, name: str, value: SchemaOptionDefs):
        raise TypeError("Implement in derived class")

    def set_default(self, name: str):
        raise TypeError("Implement in derived class")

    def get(
        self, name: Optional[str] = None
    ) -> Union[SchemaOptionDefs, CustomTemplateDefs]:
        raise TypeError("Implement in derived class")

    def names(self):
        raise TypeError("Implement in derived class")
