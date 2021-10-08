import os
import re

import pkg_resources
import pytest
import unittest

from curvenote_template.TemplateOptions import TemplateOptions

DEFAULT_TEMPLATE_PATH = pkg_resources.resource_filename(
    "curvenote_template", "builtin_template"
)

class TestTemplateOptions(unittest.TestCase):

    def setUp(self):
        self.default_options = TemplateOptions(DEFAULT_TEMPLATE_PATH)

    def test_defaults(self):

        assert self.default_options.get("metadata.title") == "Plain LaTeX (built-in)"


    def test_find(self):
        assert TemplateOptions.find("a", dict(a=1)) == 1
        with pytest.raises(KeyError):
            TemplateOptions.find("b", dict(a=1))
        assert TemplateOptions.find("a.b", dict(a=dict(b=2))) == 2
        with pytest.raises(KeyError):
            TemplateOptions.find("a.c", dict(a=dict(b=2)))


    def test_default_get(self):
        assert self.default_options.get("metadata", "default") is not None
        assert self.default_options.get("config", "default") is not None
        assert self.default_options.get("random", "default") is "default"
        assert self.default_options.get("random") is None
        assert self.default_options.get("config.build") is not None
        assert self.default_options.get("config.build.layout") == "compact"
        assert self.default_options.get("config.build.vanilla", False) is True


    def test_default_compact(self):
        assert self.default_options.get("config.build.layout") == "compact"


    def test_default_version(self):
        assert self.default_options.get("metadata.version") == "1.0.0"

    def test_config(self):
        assert self.default_options.get("config.build") is not None
        assert isinstance(self.default_options.get("config.tagged"), list)
        assert isinstance(self.default_options.get("config.options"), list)

    def test_config_allowed_tags(self):
        atags = self.default_options.get_allowed_tags()
        assert isinstance(atags, set)
        assert len(atags) > 0