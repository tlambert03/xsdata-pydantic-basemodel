from __future__ import annotations

from dataclasses import MISSING, field
from typing import Any, Callable, Iterator, Literal, TypeVar

from pydantic import BaseModel, __version__

PYDANTIC2 = __version__.startswith("2")
M = TypeVar("M", bound=BaseModel)
C = TypeVar("C", bound=Callable[..., Any])


# no-op for v1, put first for typing.
def model_validator(*, mode: Literal["wrap", "before", "after"]) -> Callable[[C], C]:
    def decorator(func: C) -> C:
        return func

    return decorator


if PYDANTIC2:
    from pydantic import field_validator
    from pydantic import model_validator as model_validator  # type: ignore # noqa
    from pydantic.fields import Field as _Field
    from pydantic.fields import FieldInfo
    from pydantic.fields import _Undefined as Undefined

    def validator(*args: Any, **kwargs: Any) -> Callable[[Callable], Callable]:
        return field_validator(*args, **kwargs)

    def Field(*args, **kwargs) -> _Field:
        if "metadata" in kwargs:
            kwargs["json_schema_extra"] = kwargs.pop("metadata")
        return _Field(*args, **kwargs)

    def update_forward_refs(cls: type[M]) -> None:
        try:
            cls.model_rebuild()
        except AttributeError:
            pass

    def iter_fields(obj: type[M]) -> Iterator[tuple[str, FieldInfo]]:
        yield from obj.model_fields.items()

    def _get_metadata(pydantic_field):
        if pydantic_field.json_schema_extra:
            metadata = pydantic_field.json_schema_extra
        else:
            metadata = {}
        return metadata

    def model_config(**kwargs: Any) -> dict | type:
        return kwargs

else:
    from pydantic.fields import ModelField
    from pydantic.fields import Undefined as Undefined

    def update_forward_refs(cls: type[M]) -> None:
        cls.update_forward_refs()

    def iter_fields(obj: type[M]) -> Iterator[tuple[str, ModelField]]:
        yield from obj.__fields__.items()

    def model_config(**kwargs: Any) -> dict | type:
        return type("Config", (), kwargs)

    def _get_metadata(pydantic_field):
        return pydantic_field.field_info.extra.get("metadata", {})


def _get_defaults(pydantic_field) -> tuple[Any, Any]:
    if pydantic_field.default_factory is not None:
        default_factory: Any = pydantic_field.default_factory
        default = MISSING
    else:
        default_factory = MISSING
        default = (
            MISSING
            if pydantic_field.default in (Undefined, Ellipsis)
            else pydantic_field.default
        )
    return default_factory, default


def _pydantic_field_to_dataclass_field(name: str, pydantic_field: FieldInfo) -> Any:
    default_factory, default = _get_defaults(pydantic_field)

    metadata = _get_metadata(pydantic_field)

    dataclass_field = field(  # type: ignore
        default=default,
        default_factory=default_factory,
        # init=True,
        # hash=None,
        # compare=True,
        metadata=metadata,
        # kw_only=MISSING,
    )
    dataclass_field.name = name
    # dataclass_field.type = pydantic_field.type_
    return dataclass_field


def dataclass_fields(obj: type[M]) -> Iterator[Any]:
    for name, f in iter_fields(obj):
        yield _pydantic_field_to_dataclass_field(name, f)