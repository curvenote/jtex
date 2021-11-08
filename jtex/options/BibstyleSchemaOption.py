import logging
import re

from .BooleanSchemaOption import BooleanSchemaOption
from .SchemaOptionDefs import SchemaOptionDefs


class BibstyleSchemaOption(BooleanSchemaOption):
    """
    Enables/disables the default bibstyle
    """

    def __init__(self):
        super(BibstyleSchemaOption, self).__init__()

        self.add(
            True,
            SchemaOptionDefs(
                setup=["setup-bib-style.def"],
            ),
        )

        self.add(False, SchemaOptionDefs())

        self.set_default(False)
