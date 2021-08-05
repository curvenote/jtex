import pytest
from curvenote_template.options.NatbibSchemaOption import citep_transform


@pytest.fixture(
    params=[
        ("", ""),
        ("hello world", "hello world"),
        ("hello\\citep{world", "hello\\cite{world"),
        ("hello \\citep{ world", "hello \\cite{ world"),
        ("hello \\citep{abc} world", "hello \\cite{abc} world"),
        ("hello \\cite{abc} world", "hello \\cite{abc} world"),
    ],
    name="citep",
)
def _citep(request):
    return request.param


def test_cite_schema_options(citep):
    example, expected = citep
    assert citep_transform(example) == expected
