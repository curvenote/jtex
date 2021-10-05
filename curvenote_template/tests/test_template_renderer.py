import tempfile
from os import path

import pytest
from dateutil import parser
from jinja2.loaders import PackageLoader

from curvenote_template.TemplateRenderer import TemplateRenderer


def test_not_initialized_on_construction():
    renderer = TemplateRenderer()
    assert renderer.jinja is None


@pytest.fixture(name="renderer")
def _renderer():
    renderer = TemplateRenderer()
    renderer.use_loader(PackageLoader("curvenote_template", "builtin_template"))
    return renderer


def test_has_environment(renderer):
    assert renderer.jinja is not None


def test_syntax_variable(renderer):
    T = "lorem ipsum [-TITLE-] lorem ipsum"

    output = renderer.render_from_string(T, dict(TITLE="ABC"))

    assert output == "lorem ipsum ABC lorem ipsum"


def test_syntax_block(renderer):
    T = r"[# for _ in items #]ABC[# endfor #]"

    output = renderer.render_from_string(T, dict(x="y"))
    assert output == ""

    output = renderer.render_from_string(T, dict(x="y", items=[0, 1, 2]))
    assert output == "ABCABCABC"


def test_syntax_block_var(renderer):
    T = r"[# for i in items #]ABC[-i-][# endfor #]"

    output = renderer.render_from_string(T, dict(x="y", items=[0, 1, 2]))

    assert output == "ABC0ABC1ABC2"


def test_syntax_comment(renderer):
    T = r"just %# not this #% this"

    output = renderer.render_from_string(T, dict(x="y"))

    assert output == "just  this"


def test_syntax_zip(renderer):
    T = r"[# for a, b in zip(A,B)#][-a-][-b-]|[# endfor #]"

    output = renderer.render_from_string(T, dict(A=["x", "y", "z"], B=[1, 2, 3]))
    assert output == "x1|y2|z3|"


def test_use_filesystem_template():
    with tempfile.TemporaryDirectory() as tmp:
        print(tmp)
        a = open(path.join(tmp, "a.tex"), "w")
        a.close()
        b = open(path.join(tmp, "b.tex"), "w")
        b.close()

        renderer = TemplateRenderer()
        renderer.use_from_folder(tmp)

        assert renderer.list_templates() == ["a.tex", "b.tex"]


def test_rendering(renderer):
    """
    Rendering using the default package loader
    """
    assert renderer.list_templates() == ["template.tex"]

    data = dict(
        doc=dict(
            oxalink="https://curvenote.com",
            title="A Paper",
            authors=[dict(name=name) for name in ["Curve Note", "Io Oxa"]],
            date=parser.parse("6/18/2021"),
        ),
        tagged=dict(abstract="Lorem ispum"),
        curvenote=dict(defs="\\input{curvenote.def}"),
        CONTENT="Lorem ipsum blahdium...",
    )

    output = renderer.render(data)

    assert r"\newcommand{\logo}{" in output
    assert r"Curve Note \and Io Oxa" in output
    assert r"\title{A Paper}" in output
    assert r"\newdate{articleDate}{18}{6}{2021}" in output
    assert r"Lorem ipsum blahdium..." in output
