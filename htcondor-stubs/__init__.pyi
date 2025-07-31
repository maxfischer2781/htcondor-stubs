from typing import Any, ClassVar
import enum

from classad import ClassAd

class DaemonTypes(enum.IntEnum):
    Any = 1
    Master = 2
    Schedd = 3
    Startd = 4
    Collector = 5
    Negotiator = 6
    HAD = 17
    Generic = 18
    Credd = 13
    names: ClassVar[dict[str, DaemonTypes]]
    values: ClassVar[dict[int, DaemonTypes]]

class AdTypes(enum.IntEnum):
    Any = 10
    Generic = 15
    Slot = 24
    StartDaemon = 25
    Startd = 0
    StartdPrivate = 5
    Schedd = 1
    Master = 2
    Collector = 7
    Negotiator = 13
    Submitter = 6
    Grid = 19
    HAD = 14
    License = 8
    Credd = 16
    Defrag = 22
    Accounting = 23
    names: ClassVar[dict[str, AdTypes]]
    values: ClassVar[dict[int, AdTypes]]

class Collector:
    def __init__(self, pool: "str | list[str] | None") -> None: ...
    def advertise(
        self,
        ad_list: list[ClassAd[Any]],
        command: str = "UPDATE_AD_GENERIC",
        use_tcp: bool = True,
    ) -> None: ...
    def locate(self, daemon_type: DaemonTypes, name: str) -> ClassAd[Any]: ...
    def locateAll(self, daemon_type: DaemonTypes) -> list[ClassAd[Any]]: ...
    def query(
        self,
        ad_type: AdTypes = AdTypes.Any,
        constraint: str = "",
        projection: list[str] = [],
        statistics: str = "",
    ) -> list[ClassAd[Any]]: ...
    def directQuery(
        self,
        daemon_type: DaemonTypes,
        name: str = "",
        projection: list[str] = [],
        statistics: str = "",
    ) -> ClassAd[Any]: ...
