"""
Utilities for working with the ClassAd language and data structure
"""

from typing import (
    Any,
    Iterator,
    IO,
    overload,
    MutableMapping,
    Literal,
)
import enum
import datetime

# -- helper/shorthand types

# Python runtime types we get out of Expressions and ClassAds
type _PyValue = _PyConstant | _PyContainer[Any]
type _PyConstant = str | datetime.datetime | bool | int | float | Value
type _PyContainer[V: _PyValue] = list[V] | ClassAd[V]
# (Expression to Value) or (Value)
type _EoV[V: _PyValue] = V | ExprTree[V]

# -- utilities

def lastError() -> str:
    """Description of the last error for any :py:mod:`classad2` operation"""

def parseAds(
    input: str | IO[str], parser: ParserType = ParserType.Auto
) -> Iterator[ClassAd[Any]]:
    """Consecutively parse :py:class:`~.ClassAd` instances from `input`"""

def parseNext(
    input: str | IO[str], parser: ParserType = ParserType.Auto
) -> ClassAd[Any]:
    """Parse the first :py:class:`~.ClassAd` instance from `input`"""

def parseOne(
    input: str | IO[str], parser: ParserType = ParserType.Auto
) -> ClassAd[Any]:
    """Parse and merge all :py:class:`~.ClassAd` instance from `input`"""

def quote(input: str) -> str:
    """Quote `input` so that it can be interpolated into a ClassAd expression literal as a string"""

def unquote(input: str) -> str:
    """Reverse of :py:func:`~.quote` to turn a ClassAd string literal into a Python string"""

def version() -> str:
    """The version of the underlying ClassAd C library"""

# -- ExprTree

class ExprTree[V: _PyValue]:
    """A single ClassAd language expression"""

    # TODO: Is `ExprTree(None)` sensible?
    @overload
    def __init__[EV: _PyValue](self: ExprTree[EV], expr: ExprTree[EV]) -> None: ...
    @overload
    def __init__(self: ExprTree[Literal[Value.Undefined]], expr: None) -> None: ...
    @overload
    def __init__(self: ExprTree[Any], expr: str) -> None: ...
    def eval(
        self, scope: ClassAd[Any] | None = None, target: ClassAd[Any] | None = None
    ) -> V:
        """Evaluate the expression as the corresponding Python type"""

    def simplify(
        self, scope: ClassAd[Any] | None = None, target: ClassAd[Any] | None = None
    ) -> ExprTree[V]:
        """
        Evaluate the expression as a new :py:class:`~.ExprTree`

        Simplification is eager. An expression relying on external references not provided
        by `scope` or `target` will evaluate to `ExprTree[Undefined]` instead of an expression
        with free references.

        .. seealso:
            :py:meth:`.ClassAd.flatten` to partially evalute an expression if external references
            are not fully available.
        """

# -- ClassAd

class ClassAd[V: _PyValue](MutableMapping[str, _EoV[V]]):
    """A mapping from strings to :py:class:`~.ExprTree` or Python values"""

    @overload
    def __init__(self: ClassAd[Any], input: None = None) -> None: ...
    @overload
    def __init__(self: ClassAd[Any], input: str) -> None: ...
    @overload
    def __init__[DV: _PyValue](
        self: ClassAd[DV], input: dict[str, DV | ExprTree[DV]]
    ) -> None: ...
    @overload
    def __init__[DV: _PyValue, DDV: _PyValue](
        self: ClassAd[DV | ClassAd[DDV]],
        input: dict[
            str,
            _EoV[DV] | ExprTree[ClassAd[DDV]] | dict[str, _EoV[DDV]],
        ],
    ) -> None: ...
    @overload
    def __init__[DV: _PyValue, DDV: _PyValue, DDDV: _PyValue](
        self: ClassAd[DV | ClassAd[DDV | ClassAd[DDDV]]],
        input: dict[
            str,
            _EoV[DV]
            | ExprTree[ClassAd[DDV]]
            | ExprTree[ClassAd[DDV | ClassAd[DDDV]]]
            | dict[str, _EoV[DDV] | ClassAd[DDDV] | dict[str, _EoV[DDDV]]],
        ],
    ) -> None: ...
    def eval(self, attr: str) -> V:
        """Fetch and evaluate the value for the `attr` key"""

    def lookup(self, attr: str) -> ExprTree[V]:
        """Fetch the :py:class:`~.ExprTree` for the `attr` key"""

    def externalRefs(self, expr: ExprTree[Any]) -> list[str]:
        """Provide names of attributes referenced by `expr` but not provided by this ClassAd"""

    def internalRefs(self, expr: ExprTree[Any]) -> list[str]:
        """Provide names of attributes referenced by `expr` that are provided by this ClassAd"""

    @overload
    def flatten[EV: _PyConstant](self, expr: ExprTree[EV]) -> _EoV[EV]:
        """
        Partially evaluate `expr` in the context of this ClassAd

        If `expr` evalutes to a constant skalar, provides the corresponding Python value.
        If `expr` has remaining external references or evaluates to a list or ClassAd,
        provide a new :py:class:`~.ExprTree`.
        """

    @overload
    def flatten[EV: _PyContainer[Any]](self, expr: ExprTree[EV]) -> ExprTree[EV]: ...
    def matches(self, ad: ClassAd[Any]) -> bool:
        """Test that `ad["REQUIREMENTS"]` evaluates to `true` in the context of the current ClassAd"""

    def printJson(self) -> str:
        """Format (not print) the content of this ClassAd as JSON"""

    def symmetricMatch(self, ad: ClassAd[Any]) -> bool:
        """Symetrically check :py:meth:`~.matches` for this ClassAd and `ad`"""

# -- Enumerations

class ParserType(enum.IntEnum):
    Auto = -1
    Old = 0
    XML = 1
    JSON = 2
    New = 3
    FileAuto = 4

class Value(enum.IntEnum):
    Error = 1
    Undefined = 2
