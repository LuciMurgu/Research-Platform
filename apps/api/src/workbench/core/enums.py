"""Domain enumerations for the Research Workbench."""

from enum import StrEnum


class RunStatus(StrEnum):
    """Execution status for a Run."""

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class JobStatus(StrEnum):
    """Execution status for a Job."""

    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FAILED = "failed"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ArtifactKind(StrEnum):
    """Categorization of generated artifacts."""

    IMAGE = "image"
    ANIMATION = "animation"
    MESH = "mesh"
    TABLE = "table"
    ARRAY = "array"
    LOG = "log"
    REPORT = "report"
    NOTEBOOK = "notebook"
    OTHER = "other"


class AgentOutputLabel(StrEnum):
    """Label indicating the nature of an agent's output."""

    OBSERVATION = "observation"
    DIAGNOSTIC = "diagnostic"
    HYPOTHESIS = "hypothesis"
    SUGGESTION = "suggestion"
    WARNING = "warning"
    SUMMARY = "summary"


class ResearchClaimStatus(StrEnum):
    """Status of a researcher's claim."""

    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    UNDER_TEST = "under_test"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    RETIRED = "retired"


class ProvenanceEventType(StrEnum):
    """Types of events recorded in the provenance ledger."""

    EXPERIMENT_CREATION = "experiment_creation"
    RUN_CREATION = "run_creation"
    COMMAND_SUBMISSION = "command_submission"
    PARAMETER_VALIDATION = "parameter_validation"
    JOB_CREATION = "job_creation"
    JOB_START = "job_start"
    JOB_COMPLETION = "job_completion"
    JOB_FAILURE = "job_failure"
    STATEFRAME_EMISSION = "stateframe_emission"
    ARTIFACT_WRITE = "artifact_write"
    METRIC_RECORD = "metric_record"
    WARNING_RAISE = "warning_raise"
    VALIDATION_PASS = "validation_pass"
    VALIDATION_FAILURE = "validation_failure"
    AGENT_OUTPUT_CREATION = "agent_output_creation"
    HUMAN_APPROVAL = "human_approval"
    RUN_COMPLETION = "run_completion"
    RUN_FAILURE = "run_failure"
    RUN_ARCHIVE = "run_archive"


class ActorType(StrEnum):
    """Types of actors that can trigger events."""

    RESEARCHER = "researcher"
    SYSTEM = "system"
    AGENT = "agent"
    ORCHESTRATOR = "orchestrator"
    VALIDATOR = "validator"
