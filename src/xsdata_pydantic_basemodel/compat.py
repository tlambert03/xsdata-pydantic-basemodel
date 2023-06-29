from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
)
from xml.etree.ElementTree import QName

from pydantic import BaseModel, validators
from xsdata.formats.dataclass.compat import Dataclasses, class_types
from xsdata.formats.dataclass.models.elements import XmlType
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlDuration, XmlPeriod, XmlTime

from ._pydantic_compat import (
    PYDANTIC2,
    Field,
    dataclass_fields,
    model_config,
    update_forward_refs,
)

if TYPE_CHECKING:
    pass

T = TypeVar("T", bound=object)


# don't switch to exclude ... it makes it hard to add fields to the
# schema without breaking backwards compatibility
_config = model_config(arbitrary_types_allowed=True)


class _BaseModel(BaseModel):
    """Base model for all types."""

    if PYDANTIC2:
        model_config = _config
    else:
        Config = _config  # type: ignore


class AnyElement(BaseModel):
    """Generic model to bind xml document data to wildcard fields.

    :param qname: The element's qualified name
    :param text: The element's text content
    :param tail: The element's tail content
    :param children: The element's list of child elements.
    :param attributes: The element's key-value attribute mappings.
    """

    qname: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
    tail: Optional[str] = Field(default=None)
    children: List[object] = Field(
        default_factory=list, metadata={"type": XmlType.WILDCARD}
    )
    attributes: Dict[str, str] = Field(
        default_factory=dict, metadata={"type": XmlType.ATTRIBUTES}
    )

    if PYDANTIC2:
        model_config = _config
    else:
        Config = _config  # type: ignore


class DerivedElement(BaseModel, Generic[T]):
    """Generic model wrapper for type substituted elements.

    Example: eg. <b xsi:type="a">...</b>

    :param qname: The element's qualified name
    :param value: The wrapped value
    :param type: The real xsi:type
    """

    qname: str
    value: T
    type: Optional[str] = None

    if PYDANTIC2:
        model_config = _config
    else:
        Config = _config  # type: ignore


class PydanticBaseModel(Dataclasses):
    @property
    def any_element(self) -> Type:
        return AnyElement

    @property
    def derived_element(self) -> Type:
        return DerivedElement

    def is_model(self, obj: Any) -> bool:
        clazz = obj if isinstance(obj, type) else type(obj)
        if issubclass(clazz, BaseModel):
            update_forward_refs(clazz)
            return True

        return False

    def get_fields(self, obj: Any) -> Tuple[Any, ...]:
        return tuple(dataclass_fields(obj))


class_types.register("pydantic-basemodel", PydanticBaseModel())


def make_validators(tp: Type, factory: Callable) -> List[Callable]:
    def validator(value: Any) -> Any:
        if isinstance(value, tp):
            return value

        if isinstance(value, str):
            return factory(value)
        breakpoint()
        raise ValueError

    return [validator]


_validators = {
    XmlDate: make_validators(XmlDate, XmlDate.from_string),
    XmlDateTime: make_validators(XmlDateTime, XmlDateTime.from_string),
    XmlTime: make_validators(XmlTime, XmlTime.from_string),
    XmlDuration: make_validators(XmlDuration, XmlDuration),
    XmlPeriod: make_validators(XmlPeriod, XmlPeriod),
    QName: make_validators(QName, QName),
}

if not PYDANTIC2:
    validators._VALIDATORS.extend(list(_validators.items()))
else:
    from pydantic import BaseModel
    from pydantic_core import core_schema as cs

    def _make_get_core_schema(validator: Callable) -> Callable:
        def get_core_schema(*args: Any) -> cs.PlainValidatorFunctionSchema:
            return cs.general_plain_validator_function(validator)

        return get_core_schema

    for type_, val in _validators.items():
        get_schema = _make_get_core_schema(val[0])
        type_.__get_pydantic_core_schema__ = get_schema  # type: ignore
