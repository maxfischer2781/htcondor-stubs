from typing import Any, ClassVar, Callable, Literal, SupportsInt
from warnings import deprecated
import enum

from classad import ClassAd, ExprTree

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

# Schedd

class QueryOpts(enum.IntEnum):
    Default = 0
    AutoCluster = 1
    GroupBy = 2
    DefaultMyJobsOnly = 4
    SummaryOnly = 8
    IncludeClusterAd = 16
    IncludeJobsetAds = 32
    ClusterAds = 80
    JobsetAds = 96
    names: ClassVar[dict[str, QueryOpts]]
    values: ClassVar[dict[int, QueryOpts]]

class JobAction(enum.IntEnum):
    Hold = 1
    Release = 2
    Remove = 3
    RemoveX = 4
    Vacate = 5
    VacateFast = 6
    Suspend = 8
    Continue = 9
    names: ClassVar[dict[str, JobAction]]
    values: ClassVar[dict[int, JobAction]]

class TransactionFlags(enum.IntEnum):
    NonDurable = 1
    SetDirty = 4
    ShouldLog = 8
    names: ClassVar[dict[str, TransactionFlags]]
    values: ClassVar[dict[int, TransactionFlags]]

class Schedd:
    def __init__(self, location_ad: ClassAd[Any] | None) -> None: ...
    @deprecated("use .submit() instead")
    def transaction(self, flags: int = 0, continue_txn: bool = False) -> Any: ...
    def query(
        self,
        constraint: str = "true",
        projection: list[str] = [],
        callback: Callable[[ClassAd[Any]], None] | None = None,
        limit: int = -1,
        opts: QueryOpts = QueryOpts.Default,
    ) -> list[ClassAd[Any]]: ...
    @deprecated("use .query() instead")
    def xquery(
        self,
        constraint: str = "true",
        projection: list[str] = [],
        callback: Callable[[ClassAd[Any]], None] | None = None,
        limit: int = -1,
        opts: QueryOpts = QueryOpts.Default,
        name: str | None = None,
    ) -> Any: ...
    def act(
        self,
        action: JobAction,
        job_spec: str | list[str] | ExprTree[Any],
        reason: str | None = None,
    ) -> ClassAd[Any]: ...
    def edit(
        self,
        job_spec: str | list[str],
        attr: str,
        value: str | ExprTree[Any],
        flags: TransactionFlags | Literal[0] = 0,
    ) -> SupportsInt: ...
