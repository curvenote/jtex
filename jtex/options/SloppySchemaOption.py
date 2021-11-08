from .BooleanSchemaOption import BooleanSchemaOption
from .SchemaOptionDefs import SchemaOptionDefs


class SloppySchemaOption(BooleanSchemaOption):
    def __init__(self):
        super(SloppySchemaOption, self).__init__()

        self.add(True, SchemaOptionDefs(setup=["cmd-sloppy.def"]))

        self.add(False, SchemaOptionDefs())

        self.set_default(False)
