from .BooleanSchemaOption import BooleanSchemaOption
from .SchemaOptionDefs import SchemaOptionDefs


class CitestyleSchemaOption(BooleanSchemaOption):
    """
    Enables/disables the default cite style
    """

    def __init__(self):
        super(CitestyleSchemaOption, self).__init__()

        self.add(
            True,
            SchemaOptionDefs(setup=["setup-cite-style.def"]),
        )

        self.add(False, SchemaOptionDefs())

        self.set_default(False)
