from typing import Optional

import pytest
from pykwalify.errors import CoreError

from jtex.DocModel import DocModel

@pytest.fixture(
    params=[
        {},
        dict(title="title"),
        dict(jtex=dict()),
        dict(jtex=dict(version=1)),
        dict(
            title="a", jtex=dict(version=1, input=dict(), output=dict(), options=dict())
        ),
    ],
    name="ensure_defaults",
)
def _ensure_defaults(request):
    return request.param


def test_incomplete_data(ensure_defaults):
    try:
        dm = DocModel(ensure_defaults)
    except CoreError as err:
        assert False, f"Exception raised {err}"


def test_get_data():
    try:
        dm = DocModel(dict(title="a title"))
    except CoreError as err:
        assert False, f"Exception raised {err}"

    assert dm.get("title", str) == "a title"
    assert dm.get("jtex.version", int) == 1
    assert dm.get("jtex.output.filename", str) == "main.tex"
    assert dm.get("something", Optional[str]) is None
    assert dm.get("something", str, "else") == "else"
    assert dm.get("this.key.is.not.there", str) is None
