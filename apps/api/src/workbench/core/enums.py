"""Domain enumerations for the Research Workbench."""

from enum import StrEnum


class RunStatus(StrEnum):
    """Execution status for a Run."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class JobStatus(StrEnum):
    """Execution status for a Job."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ArtifactKind(StrEnum):
    """Categorization of generated artifacts."""

    DATASET = "DATASET"
    PLOT = "PLOT"
    STATE_DUMP = "STATE_DUMP"
    MODEL_WEIGHTS = "MODEL_WEIGHTS"
    REPORT = "REPORT"


class AgentOutputLabel(StrEnum):
    """Label indicating the nature of an agent's output."""

    OBSERVATION = "OBSERVATION"
    DIAGNOSTIC = "DIAGNOSTIC"
    HYPOTHESIS = "HYPOTHESIS"
    SUGGESTION = "SUGGESTION"
    WARNING = "WARNING"
    SUMMARY = "SUMMARY"


class ResearchClaimStatus(StrEnum):
    """Status of a researcher's claim."""

    OBSERVATION = "OBSERVATION"
    HYPOTHESIS = "HYPOTHESIS"
    UNDER_TEST = "UNDER_TEST"
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    RETIRED = "RETIRED"


class ProvenanceEventType(StrEnum):
    """Types of events recorded in the provenance ledger."""

    RUN_STARTED = "RUN_STARTED"
    RUN_COMPLETED = "RUN_COMPLETED"
    RUN_FAILED = "RUN_FAILED"
    ARTIFACT_STORED = "ARTIFACT_STORED"
    PARAMETER_CHANGED = "PARAMETER_CHANGED"
    APPROVAL_GRANTED = "APPROVAL_GRANTED"
    APPROVAL_DENIED = "APPROVAL_DENIED"


class ActorType(StrEnum):
    """Types of actors that can trigger events."""

    RESEARCHER = "RESEARCHER"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"
