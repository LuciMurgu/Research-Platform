"""Tests for the core domain enumerations."""

from workbench.core.enums import (
    ActorType,
    AgentOutputLabel,
    ArtifactKind,
    JobStatus,
    ProvenanceEventType,
    ResearchClaimStatus,
    RunStatus,
)


def test_run_status_values() -> None:
    """RunStatus has expected values."""
    assert RunStatus.CREATED == "created"
    assert RunStatus.RUNNING == "running"
    assert RunStatus.COMPLETED == "completed"
    assert RunStatus.FAILED == "failed"
    assert RunStatus.CANCELLED == "cancelled"
    assert RunStatus.ARCHIVED == "archived"


def test_job_status_values() -> None:
    """JobStatus has expected values."""
    assert JobStatus.CREATED == "created"
    assert JobStatus.QUEUED == "queued"
    assert JobStatus.RUNNING == "running"
    assert JobStatus.PAUSED == "paused"
    assert JobStatus.CANCELLING == "cancelling"
    assert JobStatus.CANCELLED == "cancelled"
    assert JobStatus.FAILED == "failed"
    assert JobStatus.COMPLETED == "completed"
    assert JobStatus.ARCHIVED == "archived"


def test_artifact_kind_values() -> None:
    """ArtifactKind has expected values."""
    assert ArtifactKind.IMAGE == "image"
    assert ArtifactKind.ANIMATION == "animation"
    assert ArtifactKind.MESH == "mesh"
    assert ArtifactKind.TABLE == "table"
    assert ArtifactKind.ARRAY == "array"
    assert ArtifactKind.LOG == "log"
    assert ArtifactKind.REPORT == "report"
    assert ArtifactKind.NOTEBOOK == "notebook"
    assert ArtifactKind.OTHER == "other"


def test_agent_output_label_values() -> None:
    """AgentOutputLabel has expected values."""
    assert AgentOutputLabel.OBSERVATION == "observation"
    assert AgentOutputLabel.DIAGNOSTIC == "diagnostic"
    assert AgentOutputLabel.HYPOTHESIS == "hypothesis"
    assert AgentOutputLabel.SUGGESTION == "suggestion"
    assert AgentOutputLabel.WARNING == "warning"
    assert AgentOutputLabel.SUMMARY == "summary"


def test_research_claim_status_values() -> None:
    """ResearchClaimStatus has expected values."""
    assert ResearchClaimStatus.OBSERVATION == "observation"
    assert ResearchClaimStatus.HYPOTHESIS == "hypothesis"
    assert ResearchClaimStatus.UNDER_TEST == "under_test"
    assert ResearchClaimStatus.SUPPORTED == "supported"
    assert ResearchClaimStatus.CONTRADICTED == "contradicted"
    assert ResearchClaimStatus.RETIRED == "retired"


def test_provenance_event_type_values() -> None:
    """ProvenanceEventType has expected values."""
    assert ProvenanceEventType.EXPERIMENT_CREATED == "experiment_created"
    assert ProvenanceEventType.RUN_CREATED == "run_created"
    assert ProvenanceEventType.PARAMETERS_VALIDATED == "parameters_validated"
    assert ProvenanceEventType.JOB_CREATED == "job_created"
    assert ProvenanceEventType.STATE_FRAME_EMITTED == "state_frame_emitted"


def test_actor_type_values() -> None:
    """ActorType has expected values."""
    assert ActorType.RESEARCHER == "researcher"
    assert ActorType.SYSTEM == "system"
    assert ActorType.AGENT == "agent"
    assert ActorType.ORCHESTRATOR == "orchestrator"
    assert ActorType.VALIDATOR == "validator"
