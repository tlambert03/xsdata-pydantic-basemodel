from unittest import TestCase

from xsdata.formats.dataclass.compat import class_types

from xsdata_pydantic_basemodel.compat import (
    AnyElement,
    DerivedElement,
    PydanticBaseModel,
)


class PydanticTests(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.class_type = class_types.get_type("pydantic-basemodel")

    def test_class_type(self):
        self.assertIsInstance(self.class_type, PydanticBaseModel)

    def test_property_any_element(self):
        self.assertIs(self.class_type.any_element, AnyElement)

    def test_property_derived_element(self):
        self.assertIs(self.class_type.derived_element, DerivedElement)
