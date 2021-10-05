from .BooleanSchemaOption import BooleanSchemaOption
from .SchemaOptionDefs import SchemaOptionDefs


class HideLinksSchemaOption(BooleanSchemaOption):
    def __init__(self):
        super(HideLinksSchemaOption, self).__init__()

        self.add(True, SchemaOptionDefs(setup=["setup-hyperref-hidelinks.def"]))

        self.add(False, SchemaOptionDefs())

        self.set_default(False)
