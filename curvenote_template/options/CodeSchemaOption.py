from .SchemaOptionDefs import SchemaOptionDefs, CustomTemplateDefs
from .StringSchemaOption import StringSchemaOption


class CodeSchemaOption(StringSchemaOption):
    def __init__(self):
        super(CodeSchemaOption, self).__init__()

        self.add("framed", SchemaOptionDefs(setup=["setup-code-framed.def"]))

        self.add(
            "verbatim",
            SchemaOptionDefs(
                packages=["package-fancyvrb.def"], setup=["setup-code-verbatim.def"]
            ),
        )

        self.add(
            "highlight",
            SchemaOptionDefs(
                packages=["package-fancyvrb.def"], setup=["setup-code-verbatim.def"]
            ),
        )

        # TODO needs a fix or alternative
        # self.add("minted", SchemaOptionDefs(
        #     passopts=['passopts-code-xcolor.def'],
        #     packages=['package-minted.def','package-xcolor.def'],
        #     setup=['setup-code-minted.def']
        # ))

        self.add("code.def", CustomTemplateDefs(setup=["code.def"]))

        self.set_default("verbatim")
