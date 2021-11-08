from typing import Callable, List, Optional


class SchemaOptionDefs:
    _passopts: List[str]
    _packages: List[str]
    _setup: List[str]
    _transforms: List[Callable[[str], str]]

    def __init__(
        self,
        passopts: List[str] = [],
        packages: List[str] = [],
        setup: List[str] = [],
        transforms: List[Callable[[str], str]] = [],
    ):
        self._passopts = passopts
        self._packages = packages
        self._setup = setup
        self._transforms = transforms

    @property
    def passopts(self):
        return self._passopts

    @property
    def packages(self):
        return self._packages

    @property
    def setup(self):
        return self._setup

    @property
    def transforms(self):
        return self._transforms

    @property
    def in_template(self):
        return False


class CustomTemplateDefs(SchemaOptionDefs):
    """
    This allow template creators to define custom options
    by adding .def files to the template directory.
    """

    def __init__(self, *args, **kwargs):
        super(CustomTemplateDefs, self).__init__(*args, **kwargs)

    @property
    def in_template(self):
        return True
