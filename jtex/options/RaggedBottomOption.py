from .BooleanSchemaOption import BooleanSchemaOption
from .SchemaOptionDefs import SchemaOptionDefs


class RaggedBottomSchemaOption(BooleanSchemaOption):
    def __init__(self):
        super(RaggedBottomSchemaOption, self).__init__()

        self.add(True, SchemaOptionDefs(setup=["cmd-raggedbottom.def"]))

        self.add(False, SchemaOptionDefs())

        self.set_default(False)
