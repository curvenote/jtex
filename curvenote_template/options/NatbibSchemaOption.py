import re
import logging
from .SchemaOptionDefs import SchemaOptionDefs
from .BooleanSchemaOption import BooleanSchemaOption


def citep_transform(content: str):
    logging.info("Transform: citep_transform")
    return re.sub(r"\\citep{", r"\\cite{", content)


class NatbibSchemaOption(BooleanSchemaOption):
    def __init__(self):
        super(NatbibSchemaOption, self).__init__()

        self.add(
            True,
            SchemaOptionDefs(packages=["package-natbib.def"]),
        )

        self.add(False, SchemaOptionDefs(transforms=[citep_transform]))

        self.set_default(False)
