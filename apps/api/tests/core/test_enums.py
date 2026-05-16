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
    assert RunStatus.PENDING == "PENDING"
    assert RunStatus.RUNNING == "RUNNING"
    assert RunStatus.COMPLETED == "COMPLETED"
    assert RunStatus.FAILED == "FAILED"


def test_job_status_values() -> None:
    """JobStatus has expected values."""
    assert JobStatus.PENDING == "PENDING"
    assert JobStatus.RUNNING == "RUNNING"
    assert JobStatus.COMPLETED == "COMPLETED"
    assert JobStatus.FAILED == "FAILED"


def test_artifact_kind_values() -> None:
    """ArtifactKind has expected values."""
    assert ArtifactKind.DATASET == "DATASET"
    assert ArtifactKind.PLOT == "PLOT"


def test_agent_output_label_values() -> None:
    """AgentOutputLabel has expected values."""
    assert AgentOutputLabel.OBSERVATION == "OBSERVATION"
    assert AgentOutputLabel.DIAGNOSTIC == "DIAGNOSTIC"


def test_research_claim_status_values() -> None:
    """ResearchClaimStatus has expected values."""
    assert ResearchClaimStatus.OBSERVATION == "OBSERVATION"
    assert ResearchClaimStatus.UNDER_TEST == "UNDER_TEST"


def test_provenance_event_type_values() -> None:
    """ProvenanceEventType has expected values."""
    assert ProvenanceEventType.RUN_STARTED == "RUN_STARTED"
    assert ProvenanceEventType.PARAMETER_CHANGED == "PARAMETER_CHANGED"


def test_actor_type_values() -> None:
    """ActorType has expected values."""
    assert ActorType.RESEARCHER == "RESEARCHER"
    assert ActorType.AGENT == "AGENT"
    assert ActorType.SYSTEM == "SYSTEM"
