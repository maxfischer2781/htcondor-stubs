from typing import (
    Any,
    ClassVar,
    Callable,
    Literal,
    SupportsInt,
    overload,
    Iterable,
    Iterator,
)
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
    ) -> QueryIterator: ...
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
    def history(
        self,
        constraint: str | ExprTree[Any] | None,
        projection: list[str],
        match: int = -1,
        since: int | str | ExprTree[Any] | None = None,
    ) -> HistoryIterator: ...
    def jobEpochHistory(
        self,
        constraint: str | ExprTree[Any] | None,
        projection: list[str],
        match: int = -1,
        since: int | str | ExprTree[Any] | None = None,
    ) -> HistoryIterator: ...
    @overload
    @deprecated("use .submit with a Submit object")
    def submit(
        self,
        description: ClassAd[Any],
        count: int = 1,
        spool: bool = False,
        ad_results: list[ClassAd[Any]] | None = None,
    ) -> int: ...
    @overload
    def submit(
        self,
        description: Submit,
        count: int = 1,
        spool: bool = False,
        *,
        itemdata: QueueItemsIterator | None = None,
    ) -> SubmitResult: ...
    def submitMany(
        self,
        cluster_ad: ClassAd[Any],
        proc_ads: list[tuple[ClassAd[Any], int]],
        spool: bool = False,
        ad_results: list[ClassAd[Any]] | None = None,
    ) -> int: ...
    def spool(self, jobs: list[ClassAd[Any]]) -> None: ...
    def retrieve(self, job_spec: str | list[ClassAd[Any]]) -> None: ...
    def refreshGSIProxy(
        self, cluster: int, proc: int, proxy_filename: str, lifetime: int
    ) -> int: ...
    def reschedule(self) -> None: ...
    def export_jobs(
        self,
        job_spec: str | list[str] | ExprTree[Any],
        export_dir: str,
        new_spool_dir: str,
    ) -> ClassAd[Any]: ...
    def import_exported_job_results(self, import_dir: str) -> ClassAd[Any]: ...
    def unexport_jobs(
        self, job_spec: str | list[str] | ExprTree[Any]
    ) -> ClassAd[Any]: ...

class HistoryIterator(Iterator[ClassAd[Any]]): ...

class QueryIterator(Iterator[ClassAd[Any]]):
    def nextAdsNonBlocking(self) -> list[ClassAd[Any]]: ...
    def tag(self) -> str: ...
    def watch(self) -> int: ...

def poll(
    queries: list[QueryIterator], timeout_ms: int = 20000
) -> BulkQueryIterator: ...

class BulkQueryIterator(Iterator[ClassAd[Any]]): ...

class JobStatus(enum.IntEnum):
    IDLE = 1
    RUNNING = 2
    REMOVED = 3
    COMPLETED = 4
    HELD = 5
    TRANSFERRING_OUTPUT = 6
    SUSPENDED = 7

# Submitting Jobs

# TODO: Type these
type Submit = Any
type QueueItemsIterator = Any
type SubmitResult = Any

# HTCondor Configuration

param: _Param

class _Param:
    def __init__(self) -> None: ...
    def __contains__(self, key: str) -> bool: ...
    def __getitem__(self, key: str) -> str: ...
    def __setitem__(self, key: str, value: str) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[str]: ...
    @overload
    def get(self, key: str) -> str | None: ...
    @overload
    def get[D](self, key: str, default: D) -> str | D: ...
    def keys(self) -> Iterator[str]: ...
    def items(self) -> Iterator[tuple[str, str]]: ...
    def setdefault(self, key: str, default: str) -> str: ...
    def update(self, other: dict[str, str] | Iterable[tuple[str, str]], /) -> None: ...

def reload_config() -> None: ...

# practically the same methods as Param but not inherited
class RemoteParam:
    def __init__(self, ad: ClassAd[Any]) -> None: ...
    def refresh(self) -> None: ...
    # Param methods
    def __contains__(self, key: str) -> bool: ...
    def __getitem__(self, key: str) -> str: ...
    def __setitem__(self, key: str, value: str) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[str]: ...
    @overload
    def get(self, key: str) -> str | None: ...
    @overload
    def get[D](self, key: str, default: D) -> str | D: ...
    def keys(self) -> Iterator[str]: ...
    def items(self) -> Iterator[tuple[str, str]]: ...
    def setdefault(self, key: str, default: str) -> str: ...
    def update(self, other: dict[str, str] | Iterable[tuple[str, str]], /) -> None: ...

def platform() -> str: ...
def version() -> str: ...

# Exceptions

class HTCondorException(Exception): ...
class HTCondorEnumError(HTCondorException, ValueError, NotImplementedError): ...
class HTCondorInternalError(HTCondorException, RuntimeError, TypeError, ValueError): ...
class HTCondorIOError(HTCondorException, OSError, RuntimeError, ValueError): ...
class HTCondorLocateError(HTCondorException, OSError, RuntimeError, ValueError): ...
class HTCondorReplyError(HTCondorException, RuntimeError, ValueError): ...
class HTCondorValueError(HTCondorException, ValueError, RuntimeError): ...
class HTCondorTypeError(HTCondorException, TypeError, RuntimeError, ValueError): ...
