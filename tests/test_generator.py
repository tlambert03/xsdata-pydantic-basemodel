import os
from pathlib import Path

from click.testing import CliRunner
from xsdata.cli import cli
from xsdata.models.config import GeneratorConfig
from xsdata.utils.testing import ClassFactory, FactoryTestCase

from xsdata_pydantic_basemodel.generator import PydanticBaseGenerator

EXPECTED = """
from pydantic import Field, BaseModel
from typing import List, Optional

__NAMESPACE__ = "xsdata"


class ClassB(BaseModel):
    class Meta:
        name = "class_B"

    attr_b: List[str] = Field(
        default_factory=list,
        metadata={
            "name": "attr_B",
            "type": "Element",
            "max_occurs": 3,
        },
        max_items=3
    )
    attr_c: Optional[str] = Field(
        default=None,
        metadata={
            "name": "attr_C",
            "type": "Element",
        }
    )


class ClassC(BaseModel):
    class Meta:
        name = "class_C"

    attr_d: Optional[str] = Field(
        default=None,
        metadata={
            "name": "attr_D",
            "type": "Element",
        }
    )
    attr_e: Optional[str] = Field(
        default=None,
        metadata={
            "name": "attr_E",
            "type": "Element",
        }
    )
    attr_f: Optional[str] = Field(
        default=None,
        metadata={
            "name": "attr_F",
            "type": "Element",
        }
    )
"""


class PydanticBaseGeneratorTests(FactoryTestCase):
    def setUp(self):
        super().setUp()
        config = GeneratorConfig()
        self.generator = PydanticBaseGenerator(config)

    def test_render(self):
        classes = [
            ClassFactory.elements(2, package="foo"),
            ClassFactory.elements(3, package="foo"),
        ]

        classes[0].attrs[0].restrictions.max_occurs = 3

        iterator = self.generator.render(classes)

        actual = [(out.path, out.title, out.source) for out in iterator]

        self.assertEqual(2, len(actual))
        self.assertEqual(3, len(actual[1]))

        self.assertEqual("foo.tests", actual[1][1])
        self.assertEqual(EXPECTED.lstrip(), actual[1][2])

    def test_complete(self):
        runner = CliRunner()
        schema = Path(__file__).parent.joinpath("fixtures/schemas/po.xsd")
        os.chdir(Path(__file__).parent.parent)

        result = runner.invoke(
            cli,
            [
                str(schema),
                "--package",
                "tests.fixtures.po.models",
                "--structure-style=single-package",
                "--output",
                "pydantic-basemodel",
                "--config",
                "tests/fixtures/pydantic.conf.xml",
            ],
            catch_exceptions=True,
        )

        self.assertIsNone(result.exception)
