import os
import re
import pytest
import pkg_resources
from curvenote_template.TemplateOptions import TemplateOptions

DEFAULT_TEMPLATE_PATH = pkg_resources.resource_filename(
    "curvenote_template", "builtin_template"
)


def test_defaults():
    options = TemplateOptions(DEFAULT_TEMPLATE_PATH)
    assert options.get("metadata.title") == "Plain LaTeX (built-in)"


def test_find():
    assert TemplateOptions.find("a", dict(a=1)) == 1
    with pytest.raises(KeyError):
        TemplateOptions.find("b", dict(a=1))
    assert TemplateOptions.find("a.b", dict(a=dict(b=2))) == 2
    with pytest.raises(KeyError):
        TemplateOptions.find("a.c", dict(a=dict(b=2)))


def test_default_get():
    options = TemplateOptions(DEFAULT_TEMPLATE_PATH)
    assert options.get("metadata", "default") is not None
    assert options.get("config", "default") is not None
    assert options.get("random", "default") is "default"
    assert options.get("random") is None
    assert options.get("config.build") is not None
    assert options.get("config.build.layout") == "compact"
    assert options.get("config.build.vanilla", False) is True


def test_default_compact():
    options = TemplateOptions(DEFAULT_TEMPLATE_PATH)
    assert options.get("config.build.layout") == "compact"


def test_default_version():
    options = TemplateOptions(DEFAULT_TEMPLATE_PATH)
    assert options.get("metadata.version") == "1.0.0"
