from datetime import datetime

import pytest
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from tests.fixtures.common import TypeC
from xsdata_pydantic_basemodel.bindings import (
    JsonParser,
    JsonSerializer,
    XmlParser,
    XmlSerializer,
)
from xsdata_pydantic_basemodel.compat import AnyElement, DerivedElement


@pytest.fixture
def type_c() -> TypeC:
    return TypeC(
        one="first",
        two=1.1,
        four=[
            datetime(2002, 1, 1, 12, 1),
            datetime(2003, 2, 5, 13, 5),
        ],
        any=AnyElement(
            children=[
                AnyElement(qname="foo", text="bar"),
                DerivedElement(qname="bar", value="1"),
                DerivedElement(qname="bar", value=2),
            ]
        ),
    )


def test_xml_bindings(type_c):
    serializer = XmlSerializer()
    serializer.config.pretty_print = True
    serializer.config.xml_declaration = False
    parser = XmlParser()
    ns_map = {
        "xs": "http://www.w3.org/2001/XMLSchema",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    expected = (
        '<TypeC xmlns:xs="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        "  <one>first</one>\n"
        "  <two>1.1</two>\n"
        "  <three>true</three>\n"
        "  <four>01 January 2002 12:01</four>\n"
        "  <four>05 February 2003 13:05</four>\n"
        "  <foo>bar</foo>\n"
        '  <bar xsi:type="xs:string">1</bar>\n'
        '  <bar xsi:type="xs:short">2</bar>\n'
        "</TypeC>\n"
    )
    assert expected == serializer.render(type_c, ns_map)
    assert type_c == parser.from_string(expected)


def test_serialize_json(type_c):
    serializer = JsonSerializer(config=SerializerConfig(pretty_print=True))
    parser = JsonParser()

    expected = (
        "{\n"
        '  "one": "first",\n'
        '  "two": 1.1,\n'
        '  "three": true,\n'
        '  "four": [\n'
        '    "01 January 2002 12:01",\n'
        '    "05 February 2003 13:05"\n'
        "  ],\n"
        '  "any": {\n'
        '    "qname": null,\n'
        '    "text": null,\n'
        '    "tail": null,\n'
        '    "children": [\n'
        "      {\n"
        '        "qname": "foo",\n'
        '        "text": "bar",\n'
        '        "tail": null,\n'
        '        "children": [],\n'
        '        "attributes": {}\n'
        "      },\n"
        "      {\n"
        '        "qname": "bar",\n'
        '        "value": "1",\n'
        '        "type": null\n'
        "      },\n"
        "      {\n"
        '        "qname": "bar",\n'
        '        "value": 2,\n'
        '        "type": null\n'
        "      }\n"
        "    ],\n"
        '    "attributes": {}\n'
        "  }\n"
        "}"
    )
    assert expected == serializer.render(type_c)
    assert type_c == parser.from_string(expected, TypeC)
