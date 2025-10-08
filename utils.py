from typing import Protocol, ClassVar
from types import ModuleType
import enum


class HTCondorEnum(Protocol):
    name: str
    names: "ClassVar[dict[str, HTCondorEnum]]"
    values: "ClassVar[dict[int, HTCondorEnum]]"


def format_htc_enum(h_enum: "type[HTCondorEnum]") -> str:
    """Format an HTCondor Enum class for type hinting"""
    body = [f"class {h_enum.__qualname__}(enum.IntEnum):"]
    for value, obj in h_enum.values.items():
        body.append(f"    {obj.name} = {value}")
    body.append(f"    names: ClassVar[dict[str, {h_enum.__qualname__}]]")
    body.append(f"    values: ClassVar[dict[int, {h_enum.__qualname__}]]")
    return "\n".join(body)


def format_exception(exception: "type[BaseException]") -> str:
    """Format an HTCondor Exception class for type hinting"""
    bases = ",".join(base.__qualname__ for base in exception.__bases__)
    return f"class {exception.__qualname__}({bases}): ..."


def format_enum(p_enum: "type[enum.Enum]") -> str:
    """Format a Python Enum class for type hinting"""
    body = [
        f"class {p_enum.__qualname__}("
        + ",".join(
            f"{base.__module__}.{base.__qualname__}" for base in p_enum.__bases__
        )
        + "):"
    ]
    # use `dict` to ensure entries are unique
    for member in dict.fromkeys(
        sorted(p_enum.__members__.values(), key=lambda item: item.value)
    ):
        body.append(f"    {member.name} = {member.value}")
    return "\n".join(body)


def get_exceptions(module: "ModuleType") -> "list[type[BaseException]]":
    """Get all exceptions of a module"""
    return [
        c
        for c in vars(module).values()
        if isinstance(c, type) and issubclass(c, BaseException)
    ]
