import pytest

from jtex.utils import parse_front_matter, stringify_front_matter

CONTENT_NO_FM = r"""
%% https://curvenote.com/oxa:RkW3EUemHJbWfgejvqYu/j4p2ktrUnpNLTYJxNZAq.5

Phase is a useful underlying property of the analytic trace model of seismic data that can be used as both an interpretation aid and a means to calibrate and check interpretations on a given seismic dataset. We introduce the analytical trace model and demonstrate some of its usages. We provide working code in python for computation of the Hilbert Transform using a robust FFT-based method and explore 2 use cases for such computed quantities. Jupyter notebooks used for computation and generation of the figures are included in this project.

%% https://curvenote.com/oxa:RkW3EUemHJbWfgejvqYu/nxoOOSUIjwn60BZbKluN.15
"""

FM_AND_CONTENT = r"""
% --- 76e87wqe
% title: The Title
% jtex:
%   version: 99
%   input:
%     name: abc
% --- sdjhsajd

%% https://curvenote.com/oxa:RkW3EUemHJbWfgejvqYu/j4p2ktrUnpNLTYJxNZAq.5

Phase is a useful underlying property of the analytic trace model of seismic data that can be used as both an interpretation aid and a means to calibrate and check interpretations on a given seismic dataset. We introduce the analytical trace model and demonstrate some of its usages. We provide working code in python for computation of the Hilbert Transform using a robust FFT-based method and explore 2 use cases for such computed quantities. Jupyter notebooks used for computation and generation of the figures are included in this project.

%% https://curvenote.com/oxa:RkW3EUemHJbWfgejvqYu/nxoOOSUIjwn60BZbKluN.15
"""

CONTENT = r"""
%% https://curvenote.com/oxa:RkW3EUemHJbWfgejvqYu/j4p2ktrUnpNLTYJxNZAq.5

Phase is a useful underlying property of the analytic trace model of seismic data that can be used as both an interpretation aid and a means to calibrate and check interpretations on a given seismic dataset. We introduce the analytical trace model and demonstrate some of its usages. We provide working code in python for computation of the Hilbert Transform using a robust FFT-based method and explore 2 use cases for such computed quantities. Jupyter notebooks used for computation and generation of the figures are included in this project.

%% https://curvenote.com/oxa:RkW3EUemHJbWfgejvqYu/nxoOOSUIjwn60BZbKluN.15
"""

FM_NO_CONTENT = r"""
% --- 9qwey9w
% title: The Title
% jtex:
%   version: 99
%   input:
%     name: abc
% --- ad8sa8d
"""


def test_parse_front_matter__no_front_matter():
    front_matter, content = parse_front_matter("")
    assert front_matter is None
    assert content == ""

    front_matter, content = parse_front_matter(CONTENT_NO_FM)
    assert front_matter is None
    assert content == ""


@pytest.fixture(
    params=[(FM_NO_CONTENT, ""), (FM_AND_CONTENT, CONTENT)],
    name="contents",
)
def _contents(request):
    return request.param


def test_parse_front_matter(contents):
    full_content, expected_content = contents
    front_matter, content = parse_front_matter(full_content)

    assert front_matter is not None
    assert front_matter["title"] == "The Title"
    assert front_matter["jtex"] is not None
    assert front_matter["jtex"]["version"] == 99
    assert front_matter["jtex"]["input"] is not None
    assert front_matter["jtex"]["input"]["name"] == "abc"
    assert content == expected_content


def test_stringify_front_matter__empty():
    assert stringify_front_matter(dict()) == ""


def test_stringify_front_matter():
    data = dict(
        title="Another Title", jtex=dict(version=33, input=dict(name="something"))
    )
    fm = stringify_front_matter(data)

    assert fm.index("% ---\n") > -1
    assert fm.index("% title: Another Title\n") > -1
    assert fm.index("% jtex:\n") > -1
    assert fm.index("%   input:\n") > -1
    assert fm.index("%   version: 33\n") > -1
    assert fm.index("%     name: something\n") > -1
