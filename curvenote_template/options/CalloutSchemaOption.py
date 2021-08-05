from .SchemaOptionDefs import SchemaOptionDefs, CustomTemplateDefs
from .StringSchemaOption import StringSchemaOption


class CalloutSchemaOption(StringSchemaOption):
    def __init__(self):
        super(CalloutSchemaOption, self).__init__()

        self.add(
            "framed",
            SchemaOptionDefs(
                setup=["setup-callout-framed.def"],
            ),
        )

        self.add(
            "mdframed",
            SchemaOptionDefs(
                passopts=["passopts-mdframed.def"],
                packages=["package-mdframed.def"],
                setup=["setup-callout-mdframed.def"],
            ),
        )

        self.add(
            "callout",
            SchemaOptionDefs(
                passopts=["passopts-mdframed.def", "passopts-code-xcolor.def"],
                packages=["package-mdframed.def", "package-xcolor.def"],
                setup=["setup-callout.def"],
            ),
        )

        self.add("callout.def", CustomTemplateDefs(setup=["callout.def"]))

        self.set_default("framed")
