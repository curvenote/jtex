from typing import Dict, Optional, Union

from .SchemaOption import SchemaOption
from .SchemaOptionDefs import CustomTemplateDefs, SchemaOptionDefs


class BooleanSchemaOption(SchemaOption):
    def __init__(self):
        self.when_true: Union[SchemaOptionDefs, CustomTemplateDefs, None] = None
        self.when_false: Union[SchemaOptionDefs, CustomTemplateDefs, None] = None
        self.default: Union[bool, None] = None

    def add(self, flag: bool, value: SchemaOptionDefs):
        if flag:
            self.when_true = value
        else:
            self.when_false = value

    def set_default(self, flag: bool):
        self.default = flag

    def get(
        self, flag: Optional[bool] = None
    ) -> Union[SchemaOptionDefs, CustomTemplateDefs]:
        if flag is None and self.default is None:
            raise ValueError("No default option set")
        real_flag = self.default if flag is None else flag
        return self.when_true if real_flag else self.when_false

    def names(self):
        return []
