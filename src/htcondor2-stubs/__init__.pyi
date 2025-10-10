from typing import Any, MutableMapping, Literal
from classad2 import ClassAd
import enum

# -- placeholders

type CredCheck = Any
type Credd = Any
type JobEvent = Any
type JobEventLog = Any
type Schedd = Any
type Startd = Any
type Submit = Any
type SubmitResult = Any
type DAGMan = Any

# -- functions and classes

def enable_debug() -> None:
    """Set logging as per `TOOL_DEBUG` to write to `stderr`"""

def disable_debug() -> None:
    """Disable logging to `stderr`"""

def enable_log() -> None:
    """Set logging as per `TOOL_DEBUG` to write to the path `TOOL_LOG`"""

def log(level: LogLevel | int, message: str) -> None:
    """Log a single `message` at `level`"""

class _Param(MutableMapping[str, str]):
    """The in-memory copy of the local HTCondor config"""

param: _Param

class RemoteParam(MutableMapping[str, str]):
    """
    The runtime configuration of the daemon at `location`

    While writing to this mapping updates the daemon's runtime configuration,
    a daemon ignores such changes unless `ENABLE_RUNTIME_CONFIG` is set.
    """

    def __init__(self, location: ClassAd[Any]) -> None: ...
    def refresh(self) -> None:
        """Refresh the mapping based on the daemon's current configuration"""

class SecurityContext:
    """Alternate security context and token for authentication to daemons"""

    preferred_token: str
    def __init__(self, token: str | None) -> None: ...

type _AuthLevel = Literal[
    "READ",
    "WRITE",
    "ADMINISTRATOR",
    "SOAP",
    "CONFIG",
    "OWNER",
    "DAEMON",
    "NEGOTIATOR",
    "ADVERTISE_MASTER",
    "ADVERTISE_STARTD",
    "ADVERTISE_SCHEDD",
    "CLIENT",
]
type _DCCommand = Literal[
    "DC_RAISESIGNAL",
    "DC_PROCESSEXIT",
    "DC_CONFIG_PERSIST",
    "DC_CONFIG_RUNTIME",
    "DC_RECONFIG",
    "DC_OFF_GRACEFUL",
    "DC_OFF_FAST",
    "DC_CONFIG_VAL",
    "DC_CHILDALIVE",
    "DC_SERVICEWAITPIDS",
    "DC_AUTHENTICATE",
    "DC_NOP",
    "DC_RECONFIG_FULL",
    "DC_FETCH_LOG",
    "DC_INVALIDATE_KEY",
    "DC_OFF_PEACEFUL",
    "DC_SET_PEACEFUL_SHUTDOWN",
    "DC_TIME_OFFSET",
    "DC_PURGE_LOG",
]

def ping(
    location: str | ClassAd[Any],
    authz: None | _AuthLevel | _DCCommand = None,
    security: SecurityContext | None = None,
) -> ClassAd[Any]:
    """
    Attempt to connect to the daemon at `location` for the `authz` level/command

    .. versionadded:
        HTCondor 25
    """

def platform() -> str:
    """String describing the platform the bindings were compiled for"""

def reload_config() -> None:
    """Reload the :py:data:`~.param` from the local HTCondor configuration"""

def send_alive(
    ad: ClassAd[Any] | None = None, pid: int | None = None, timeout: int | None = None
) -> None:
    """Send a keepalive to the daemon identified `by` from the `pid`"""

def send_command(ad: ClassAd[Any], dc: DaemonCommand, target: str | None) -> None:
    """Send the daemon command `dc` to a daemon located by `ad` with payload `target`"""

def set_ready_state(state: str = "Ready") -> None:
    """Tell the ``MASTER`` of this process that this daemon is ready in `state`"""

def set_subsystem(name: str, daemon_type: SubsystemType = SubsystemType.Auto) -> None:
    """Set this process' HTCondor subsystem name"""

def version() -> str:
    """The version of the underlying HTCondor C library"""

type _UpdateCommand = Literal[
    "UPDATE_AD_GENERIC",
    "UPDATE_CKPT_SRVR_AD",
    "UPDATE_COLLECTOR_AD",
    "UPDATE_GATEWAY_AD",
    "UPDATE_HAD_AD",
    "UPDATE_LICENSE_AD",
    "UPDATE_MASTER_AD",
    "UPDATE_NEGOTIATOR_AD",
    "UPDATE_SCHEDD_AD",
    "UPDATE_STARTD_AD",
    "UPDATE_STORAGE_AD",
    "UPDATE_SUBMITTOR_AD",
]
type _InvalidateCommand = Literal[
    "INVALIDATE_ADS_GENERIC",
    "INVALIDATE_CKPT_SRVR_ADS",
    "INVALIDATE_COLLECTOR_ADS",
    "INVALIDATE_GATEWAY_ADS",
    "INVALIDATE_HAD_ADS",
    "INVALIDATE_LICENSE_ADS",
    "INVALIDATE_MASTER_ADS",
    "INVALIDATE_NEGOTIATOR_ADS",
    "INVALIDATE_SCHEDD_ADS",
    "INVALIDATE_STARTD_ADS",
    "INVALIDATE_STORAGE_ADS",
    "INVALIDATE_SUBMITTOR_ADS",
]

class Collector:
    """The collector of a given `pool` or the locally configured one"""

    def __init__(
        self,
        # list[str] | tuple[str] are bugged in HTC 25.0.1
        pool: str | list[str] | tuple[str] | ClassAd[Any] | None = None,
        security: SecurityContext | None = None,
    ) -> None: ...
    def advertise(
        self,
        ad_list: list[ClassAd[Any]],
        command: _UpdateCommand | _InvalidateCommand = "UPDATE_AD_GENERIC",
        use_tcp: Literal[True] = True,
    ) -> None:
        """Advertise ClassAds from `ad_list` for the category of `command`"""

    def directQuery(
        self,
        daemon_type: DaemonType,
        name: str | None = None,
        projection: list[str] | None = None,
        statistics: str | None = None,
    ) -> ClassAd[Any]:
        """
        Fetch a ClassAd directly from a daemon found by `daemon_type` and `name`

        If `projection` is a list it is used as an allowlist for daemon specific attributes.
        """

    def locate(self, daemon_type: DaemonType, name: str | None = None) -> ClassAd[Any]:
        """Get connection details for a `daemon_type` daemon of `name` or local to the machine"""

    def locateAll(self, daemon_type: DaemonType) -> list[ClassAd[Any]]:
        """Get connection details for all `daemon_type` daemons in the pool"""

    def query(
        self,
        ad_type: AdType = AdType.Any,
        constraint: str | None = None,
        projection: list[str] | None = None,
        statistics: str | None = None,
    ) -> list[ClassAd[Any]]:
        """
        Fetch all ClassAd of `ad_type` matching `constraint`

        If `projection` is a list it is used as an allowlist for ad specific attributes.
        """

class Negotiator:
    """
    Client for Negotiator and state

    .. note:
        Any `user` argument must be fully qualified of the form 'user@domain'.
    """

    def __init__(self, location: ClassAd[Any] | None = None) -> None: ...
    def deleteUser(self, user: str) -> None:
        """Delete accounting information for a specific `user`"""

    def getPriorities(self, rollup: bool = False) -> list[ClassAd[Any]]:
        """Get the current accounting ads and optionally `rollup` hierarchical group quotas"""

    def getResourceUsage(self, user: str) -> list[ClassAd[Any]]:
        """Get ClassAds describing all resources (slots) currently assigned to a specific `user`"""

    def resetAllUsage(self) -> None:
        """Set the accumulated usage for all users to zero"""

    def resetUsage(self, user: str) -> None:
        """Set the accumulated usage for `user` to zero"""

    def setBeginUsage(self, user: str, when: int) -> None:
        """Set `when` (as UNIX timestamp) usage information starts for a specific `user`"""

    def setCeiling(self, user: str, ceiling: int) -> None:
        """Set the upper limit for a specific `user`"""

    def setFactor(self, user: str, factor: float) -> None:
        """Set the priority multiplier for a specific `user`"""

    def setLastUsage(self, user: str, when: int) -> None:
        """Set `when` (as UNIX timestamp) usage information ends for a specific `user`"""

    def setPriority(self, user: str, priority: float) -> None:
        """Set the `priority` for a specific `user`"""

    def setUsage(self, user: str, usage: float) -> None:
        """Set the `usage` in hours for a specific `user`"""

# -- Enumerations

class AdType(enum.IntEnum):
    Startd = 0
    Schedd = 1
    Master = 2
    StartdPrivate = 5
    Submitter = 6
    Collector = 7
    License = 8
    Any = 10
    Negotiator = 13
    HAD = 14
    Generic = 15
    Credd = 16
    Grid = 19
    Defrag = 22
    Accounting = 23
    Slot = 24
    StartDaemon = 25

class CompletionType(enum.IntEnum):
    Nothing = 0
    Resume = 1
    Exit = 2
    Restart = 3
    Reconfig = 4

class CredType(enum.IntEnum):
    Kerberos = 32
    Password = 36
    OAuth = 40

class DaemonCommand(enum.IntEnum):
    Restart = 453
    DaemonsOff = 454
    DaemonsOffFast = 461
    DaemonOff = 467
    DaemonOffFast = 468
    DaemonOn = 469
    DaemonsOn = 483
    DaemonsOffPeaceful = 484
    RestartPeaceful = 485
    Reconfig = 60004
    OffGraceful = 60005
    OffFast = 60006
    OffPeaceful = 60015
    SetPeacefulShutdown = 60016
    SetForceShutdown = 60041
    OffForce = 60042

class DaemonType(enum.IntEnum):
    none = 0
    Any = 1
    Master = 2
    Schedd = 3
    Startd = 4
    Collector = 5
    Negotiator = 6
    Credd = 13
    HAD = 17
    Generic = 18

class DrainType(enum.IntEnum):
    Graceful = 0
    Quick = 10
    Fast = 20

class FileTransferEventType(enum.IntEnum):
    IN_QUEUED = 1
    IN_STARTED = 2
    IN_FINISHED = 3
    OUT_QUEUED = 4
    OUT_STARTED = 5
    OUT_FINISHED = 6

class JobAction(enum.IntEnum):
    Hold = 1
    Release = 2
    Remove = 3
    RemoveX = 4
    Vacate = 5
    VacateFast = 6
    Suspend = 8
    Continue = 9

class JobEventType(enum.IntEnum):
    SUBMIT = 0
    EXECUTE = 1
    EXECUTABLE_ERROR = 2
    CHECKPOINTED = 3
    JOB_EVICTED = 4
    JOB_TERMINATED = 5
    IMAGE_SIZE = 6
    SHADOW_EXCEPTION = 7
    GENERIC = 8
    JOB_ABORTED = 9
    JOB_SUSPENDED = 10
    JOB_UNSUSPENDED = 11
    JOB_HELD = 12
    JOB_RELEASED = 13
    NODE_EXECUTE = 14
    NODE_TERMINATED = 15
    POST_SCRIPT_TERMINATED = 16
    GLOBUS_SUBMIT = 17
    GLOBUS_SUBMIT_FAILED = 18
    GLOBUS_RESOURCE_UP = 19
    GLOBUS_RESOURCE_DOWN = 20
    REMOTE_ERROR = 21
    JOB_DISCONNECTED = 22
    JOB_RECONNECTED = 23
    JOB_RECONNECT_FAILED = 24
    GRID_RESOURCE_UP = 25
    GRID_RESOURCE_DOWN = 26
    GRID_SUBMIT = 27
    JOB_AD_INFORMATION = 28
    JOB_STATUS_UNKNOWN = 29
    JOB_STATUS_KNOWN = 30
    JOB_STAGE_IN = 31
    JOB_STAGE_OUT = 32
    ATTRIBUTE_UPDATE = 33
    PRESKIP = 34
    CLUSTER_SUBMIT = 35
    CLUSTER_REMOVE = 36
    FACTORY_PAUSED = 37
    FACTORY_RESUMED = 38
    NONE = 39
    FILE_TRANSFER = 40
    RESERVE_SPACE = 41
    RELEASE_SPACE = 42
    FILE_COMPLETE = 43
    FILE_USED = 44
    FILE_REMOVED = 45
    DATAFLOW_JOB_SKIPPED = 46

class JobStatus(enum.IntEnum):
    IDLE = 1
    RUNNING = 2
    REMOVED = 3
    COMPLETED = 4
    HELD = 5
    TRANSFERRING_OUTPUT = 6
    SUSPENDED = 7

class LogLevel(enum.IntEnum):
    """Level at which to emit messages; combine levels using `|`"""

    Always = 0
    Error = 1
    Status = 2
    Job = 4
    Machine = 5
    Config = 6
    Protocol = 7
    Priv = 8
    DaemonCore = 9
    Verbose = 10
    Security = 11
    Network = 14
    Hostname = 22
    Audit = 24
    FullDebug = 1024
    SubSecond = 67108864
    Timestamp = 134217728
    PID = 268435456
    NoHeader = 2147483648

class QueryOpt(enum.IntEnum):
    Default = 0
    AutoCluster = 1
    GroupBy = 2
    DefaultMyJobsOnly = 4
    SummaryOnly = 8
    IncludeClusterAd = 16
    IncludeJobsetAds = 32

class SubmitMethod(enum.IntEnum):
    CondorSubmit = 0
    DAGMan = 1
    PythonBindings = 2
    HTCondorJobSubmit = 3
    HTCondorDagSubmit = 4
    HTCondorJobSetSubmit = 5
    UserSet = 100

class SubsystemType(enum.IntEnum):
    Master = 1
    Collector = 2
    Negotiator = 3
    Schedd = 4
    Shadow = 5
    Startd = 6
    Starter = 7
    GAHP = 8
    Dagman = 9
    SharedPort = 10
    Daemon = 11
    Tool = 12
    Submit = 13
    Job = 14
    Auto = 15

class TransactionFlag(enum.IntEnum):
    Default = 0
    NonDurable = 1
    SetDirty = 4
    ShouldLog = 8
