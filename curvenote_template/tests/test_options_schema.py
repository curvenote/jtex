import os
import tempfile
import unittest
import shutil
import pytest
from typing import List

from pykwalify.core import Core as YamlSchema


THE_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "schema",
)

CONFIG_SCHEMA = os.path.join(THE_PATH, "config.schema.yml")

THE_SCHEMAS = [CONFIG_SCHEMA, os.path.join(THE_PATH, "template.schema.yml")]

print(THE_SCHEMAS)


def squirt_to_file(tmp_dir: str, contents: str):
    temp_name = next(tempfile._get_candidate_names()) + ".yml"
    tmp = os.path.join(tmp_dir, temp_name)
    with open(tmp, "w") as file:
        file.write(contents)

    return tmp


def validate_enum_options(
    schema_file: str, tmp_dir: str, base: str, key: str, values: List[str]
):
    for value in values:
        filename = squirt_to_file(
            tmp_dir, base.replace("<key>", key).replace("<value>", value)
        )

        schema = YamlSchema(
            source_file=filename, schema_files=[CONFIG_SCHEMA, schema_file]
        )
        schema.validate(raise_exception=True)


class TestOptionsSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp_dir = tempfile.mkdtemp()
        self.config_schema_only = squirt_to_file(
            self.tmp_dir,
            """
            map:
                config:
                    include: config
            """,
            )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp_dir)

    def test_required_metadata(self):
        filename = squirt_to_file(
            self.tmp_dir,
            """
        metadata:
            title: A Title
            description: A minimal template
            source: curvenote
            version: 0.0.1
            license: CC-BY-SA
            author:
                name: Some One
            tags:
                - article
                - one-column
        """,
        )

        schema = YamlSchema(source_file=filename, schema_files=THE_SCHEMAS)

        schema.validate(raise_exception=True)

        metadata = schema.source["metadata"]
        assert metadata["title"] == "A Title"
        assert metadata["description"] == "A minimal template"
        assert metadata["version"] == "0.0.1"
        assert metadata["license"] == "CC-BY-SA"
        assert metadata["author"] is not None
        assert metadata["author"]["name"] == "Some One"

    def test_optional_metadata(self):
        filename = squirt_to_file(
            self.tmp_dir,
            """
        metadata:
            title: A Title
            description: A minimal template
            version: 0.0.1
            license: CC-BY-SA
            source: curvenote
            author:
                name: Some One
                email: hello@internet.com
                github: hello
                twitter: hello
                affiliation: somewhere
            tags:
                - article
                - one-column
            links:
                github: curvenote/templates
                source: http://curvenote.com
        """,
        )

        schema = YamlSchema(source_file=filename, schema_files=THE_SCHEMAS)

        schema.validate(raise_exception=True)

    def test_missing_metadata(self):
        filename = squirt_to_file(
            self.tmp_dir,
            """
        metadata:
            title: A Title
        """,
        )

        schema = YamlSchema(source_file=filename, schema_files=THE_SCHEMAS)

        with pytest.raises(Exception):
            schema.validate(raise_exception=True)

    def test_malformed_required_metadata(self):
        filename = squirt_to_file(
            self.tmp_dir,
            """
        metadata:
            XXXXXXtitle: A Title
            description: A minimal template
            version: 0.0.1
            license: CC-BY-SA
            author:
                name: Some One
            tags:
                - article
                - one-column
        """,
        )

        schema = YamlSchema(source_file=filename, schema_files=THE_SCHEMAS)

        with pytest.raises(Exception):
            schema.validate(raise_exception=True)

    def test_config_section(self):
        filename = squirt_to_file(
            self.tmp_dir,
            """
            config:
                build:
                    layout: compact
                    vanilla: true

                schema:
                    aside: marginpar
                    callout: default
                    code: highlight
                    raggedbottom: true
                    sloppy: true
                    hidelinks: true

                tagged:
                    abstract:
                        required: false
                    abstract_fr:
                        required: true
                    preface:
                        required: false
                    acknowledgements:
                        required: false

                options:
                    watermark:
                        type: bool
                        default: true
                        required: false
                    corresponding_email:
                        type: str
                        required: false
            """,
        )

        config = squirt_to_file(
            self.tmp_dir,
            """
        map:
            config:
                include: config
        """,
        )

        schema = YamlSchema(source_file=filename, schema_files=[CONFIG_SCHEMA, config])

        schema.validate(raise_exception=True)

        config = schema.source["config"]
        assert config is not None

    def test_config_aside(self):
        validate_enum_options(
            self.config_schema_only,
            self.tmp_dir,
            """
            config:
                schema:
                    <key>: <value>
            """,
            "aside",
            ["default", "marginpar", "framed", "aside.def"],
        )

    def test_config_callout(self):
        validate_enum_options(
            self.config_schema_only,
            self.tmp_dir,
            """
            config:
                schema:
                    <key>: <value>
            """,
            "callout",
            ["default", "framed", "mdframed", "callout.def"],
        )

    def test_config_code(self):
        validate_enum_options(
            self.config_schema_only,
            self.tmp_dir,
            """
            config:
                schema:
                    <key>: <value>
            """,
            "code",
            ["default", "verbatim", "highlight", "code.def"],
        )

    def test_config_options_draft(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
                options:
                    draft:
                        type: bool
                        default: false
                        required: false
            """
        )
        schema = YamlSchema(
            source_file=yml_to_test, schema_files=[CONFIG_SCHEMA, self.config_schema_only]
        )
        schema.validate(raise_exception=True)

    def test_config_options_bool(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
                options:
                    draft:
                        type: bool
                        default: false
                        required: false
            """
        )
        schema = YamlSchema(
            source_file=yml_to_test, schema_files=[CONFIG_SCHEMA, self.config_schema_only]
        )
        schema.validate(raise_exception=True)

    def test_config_options_choice(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
                options:
                    journal_name:
                        type: choice
                        options:
                            - option a
                            - option b
                            - option c
                        default: option b
                        required: true
            """
        )
        schema = YamlSchema(
            source_file=yml_to_test, schema_files=[CONFIG_SCHEMA, self.config_schema_only]
        )
        schema.validate(raise_exception=True)

    def test_config_options_corresponding_author(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
                options:
                    journal_name:
                        type: corresponding_author
                        required: true
            """
        )
        schema = YamlSchema(
            source_file=yml_to_test, schema_files=[CONFIG_SCHEMA, self.config_schema_only]
        )
        schema.validate(raise_exception=True)

    def test_config_options_dict(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
                options:
                    some_dict:
                        type: dict
                        properties:
                            - propA
                            - propB
                        required: true
            """
        )
        schema = YamlSchema(
            source_file=yml_to_test, schema_files=[CONFIG_SCHEMA, self.config_schema_only]
        )
        schema.validate(raise_exception=True)
