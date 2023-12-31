from dataclasses import dataclass, field
from typing import Callable

from xsdata.formats.dataclass import context, parsers, serializers
from xsdata.utils.constants import return_input


class XmlContext(context.XmlContext):
    """Pydantic BaseModel ready xml context instance."""

    def __init__(
        self,
        element_name_generator: Callable = return_input,
        attribute_name_generator: Callable = return_input,
    ):
        super().__init__(
            element_name_generator, attribute_name_generator, "pydantic-basemodel"
        )


@dataclass
class XmlParser(parsers.XmlParser):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class XmlSerializer(serializers.XmlSerializer):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonParser(parsers.JsonParser):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonSerializer(serializers.JsonSerializer):
    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class UserXmlParser(parsers.UserXmlParser):
    context: XmlContext = field(default_factory=XmlContext)
