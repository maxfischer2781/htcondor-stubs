from typing import Any, Protocol, ClassVar


class HTCondorEnum(Protocol):
    name: str
    names: "ClassVar[dict[str, HTCondorEnum]]"
    values: "ClassVar[dict[int, HTCondorEnum]]"


def format_enum(enum: "type[HTCondorEnum]") -> str:
    """Format an HTCondor Enum class for type hinting"""
    body = [f"class {enum.__qualname__}(enum.IntEnum):"]
    for value, obj in enum.values.items():
        body.append(f"    {obj.name} = {value}")
    body.append(f"    names: ClassVar[dict[str, {enum.__qualname__}]]")
    body.append(f"    values: ClassVar[dict[int, {enum.__qualname__}]]")
    return "\n".join(body)


def format_exception(exception: BaseException) -> str:
    """Format an HTCondor Exception class for type hinting"""
    bases = ",".join(base.__qualname__ for base in exception.__bases__)
    return f"class {exception.__qualname__}({bases}): ..."


def get_exceptions(module: "Any") -> "list[type[BaseException]]":
    """Get all exceptions of a module"""
    return [
        c
        for c in vars(module).values()
        if isinstance(c, type) and issubclass(c, BaseException)
    ]
