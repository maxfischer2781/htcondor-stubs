from typing import Protocol, ClassVar


class HTCondorEnum(Protocol):
    name: str
    values: "ClassVar[dict[int, HTCondorEnum]]"


def format_enum(enum: "type[HTCondorEnum]") -> str:
    """Format an HTCondor Enum class for type hinting"""
    body = [f"class {enum.__qualname__}(enum.IntEnum):"]
    for value, obj in enum.values.items():
        body.append(f"    {obj.name} = {value}")
    body.append(f"    names: ClassVar[dict[str, {enum.__qualname__}]]")
    body.append(f"    values: ClassVar[dict[int, {enum.__qualname__}]]")
    return "\n".join(body)
