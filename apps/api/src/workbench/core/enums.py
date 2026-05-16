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

    EXPERIMENT_CREATED = "experiment_created"
    RUN_CREATED = "run_created"
    COMMAND_SUBMITTED = "command_submitted"
    PARAMETERS_VALIDATED = "parameters_validated"
    PARAMETERS_REJECTED = "parameters_rejected"
    PIPELINE_BUILT = "pipeline_built"
    JOB_CREATED = "job_created"
    JOB_QUEUED = "job_queued"
    JOB_STARTED = "job_started"
    JOB_PAUSED = "job_paused"
    JOB_RESUMED = "job_resumed"
    JOB_CANCELLING = "job_cancelling"
    JOB_CANCELLED = "job_cancelled"
    JOB_COMPLETED = "job_completed"
    JOB_FAILED = "job_failed"
    STATE_FRAME_EMITTED = "state_frame_emitted"
    ARTIFACT_WRITTEN = "artifact_written"
    METRIC_RECORDED = "metric_recorded"
    WARNING_RAISED = "warning_raised"
    VALIDATION_PASSED = "validation_passed"
    VALIDATION_FAILED = "validation_failed"
    AGENT_OUTPUT_CREATED = "agent_output_created"
    SUGGESTED_COMMAND_CREATED = "suggested_command_created"
    HUMAN_APPROVAL_RECORDED = "human_approval_recorded"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"
    RUN_CANCELLED = "run_cancelled"
    RUN_ARCHIVED = "run_archived"


class ActorType(StrEnum):
    """Types of actors that can trigger events."""

    RESEARCHER = "researcher"
    SYSTEM = "system"
    AGENT = "agent"
    ORCHESTRATOR = "orchestrator"
    VALIDATOR = "validator"
