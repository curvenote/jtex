from .SchemaOptionDefs import SchemaOptionDefs, CustomTemplateDefs
from .StringSchemaOption import StringSchemaOption


class AsideSchemaOption(StringSchemaOption):
    def __init__(self):
        super(AsideSchemaOption, self).__init__()

        self.add("marginpar", SchemaOptionDefs(setup=["setup-aside-marginpar.def"]))

        self.add("framed", SchemaOptionDefs(setup=["setup-aside-framed.def"]))

        self.add(
            "mdframed",
            SchemaOptionDefs(
                passopts=["passopts-mdframed.def"],
                packages=["package-mdframed.def"],
                setup=["setup-aside-mdframed.def"],
            ),
        )

        self.add(
            "callout",
            SchemaOptionDefs(
                passopts=["passopts-mdframed.def"],
                packages=["package-mdframed.def"],
                setup=["setup-aside-callout.def"],
            ),
        )

        self.add("aside.def", CustomTemplateDefs(setup=["aside.def"]))

        self.set_default("marginpar")
