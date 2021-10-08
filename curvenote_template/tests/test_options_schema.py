import os
import shutil
import tempfile
import unittest
from typing import List

import pytest
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
                  - id: abstract
                    description: The Abstract
                    required: false
                  - id: abstract_fr
                    description: French Abstract
                    required: true
                  - id: preface
                    description: The preface. max 500 words
                    required: false
                    words:
                      max: 500
                    condition:
                      option: publication_type
                      value: proceedings
                      required: true
                  - id: acknowledgements
                    description: Acknowledge all collaborators, data and funding sources
                    required: false

                options:
                  - type: bool
                    id: draft
                    default: true
                    required: false
                  - type: str
                    id: email
                    title: Your Email
                    required: false
                  - type: choice
                    id: some_id
                    title: Another Title 1-1
                    options:
                      - option a
                      - option b
                      - option c
                    default: option b
                    required: true
                    condition:
                      option: some_option_id
                      value: some value
                  - type: choice
                    id: other_id
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

    def test_config_options_bool(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
              options:
                - type: bool
                  id: draft
                  default: false
                  required: false
            """,
        )
        schema = YamlSchema(
            source_file=yml_to_test,
            schema_files=[CONFIG_SCHEMA, self.config_schema_only],
        )
        schema.validate(raise_exception=True)

    def test_config_options_choice(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
              options:
                - type: choice
                  id: some_id
                  title: Another Title 1-1
                  options:
                    - option a
                    - option b
                    - option c
                  default: option b
                  required: true
                  condition:
                    option: some_option_id
                    value: some value
                - type: choice
                  id: other_id
            """,
        )
        schema = YamlSchema(
            source_file=yml_to_test,
            schema_files=[CONFIG_SCHEMA, self.config_schema_only],
        )
        schema.validate(raise_exception=True)

    def test_config_options_corresponding_author(self):
        yml_to_test = squirt_to_file(
            self.tmp_dir,
            """
            config:
              options:
                - id: corresponding_author
                  type: corresponding_author
                  required: true
                  multiple: true
            """,
        )
        schema = YamlSchema(
            source_file=yml_to_test,
            schema_files=[CONFIG_SCHEMA, self.config_schema_only],
        )
        schema.validate(raise_exception=True)
