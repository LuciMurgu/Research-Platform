"""Tests for the core lifecycle schemas."""

from datetime import UTC, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from workbench.core.enums import JobStatus, RunStatus
from workbench.core.schemas import Experiment, Job, Run


def test_experiment_creation() -> None:
    """creates valid Experiment with generated ID"""
    exp = Experiment(title="Test Experiment")
    
    assert exp.title == "Test Experiment"
    assert exp.schema_version == "1.0"
    
    # generated experiment ID starts with exp_ and has 32 lowercase hex characters
    assert exp.experiment_id.startswith("exp_")
    assert len(exp.experiment_id) == 36  # "exp_" + 32 chars
    
    # created_at is timezone-aware UTC
    assert exp.created_at.tzinfo == UTC
    
    # models serialize through model_dump()
    dump = exp.model_dump()
    assert dump["title"] == "Test Experiment"
    assert "experiment_id" in dump


def test_experiment_validation_title() -> None:
    """title is required and cannot be empty/whitespace"""
    with pytest.raises(ValidationError):
        Experiment(title="")
    
    with pytest.raises(ValidationError):
        Experiment(title="   ")


def test_experiment_validation_tags() -> None:
    """tags reject empty/whitespace-only values"""
    with pytest.raises(ValidationError):
        Experiment(title="Valid", tags=["", "valid"])
        
    with pytest.raises(ValidationError):
        Experiment(title="Valid", tags=["   "])


def test_experiment_validation_id() -> None:
    """manually provided malformed experiment_id is rejected"""
    with pytest.raises(ValidationError):
        Experiment(title="Valid", experiment_id="exp_invalid")


def test_experiment_validation_extra_fields() -> None:
    """extra fields are rejected"""
    with pytest.raises(ValidationError):
        Experiment(title="Valid", unknown_field="test")  # type: ignore


def test_run_creation() -> None:
    """creates valid Run with generated ID"""
    exp = Experiment(title="Valid")
    run = Run(experiment_id=exp.experiment_id, command_name="test_cmd")
    
    # generated run ID starts with run_ and has 32 lowercase hex characters
    assert run.run_id.startswith("run_")
    assert len(run.run_id) == 36
    
    # default status is RunStatus.CREATED
    assert run.status == RunStatus.CREATED
    
    # is_terminal is false for created and running
    assert run.is_terminal is False


def test_run_is_terminal() -> None:
    """is_terminal is true for completed, failed, cancelled, archived"""
    exp = Experiment(title="Valid")
    
    terminal_states = [
        RunStatus.COMPLETED,
        RunStatus.FAILED,
        RunStatus.CANCELLED,
        RunStatus.ARCHIVED
    ]
    for status in terminal_states:
        run = Run(experiment_id=exp.experiment_id, command_name="test", status=status)
        assert run.is_terminal is True
        
    for status in [RunStatus.CREATED, RunStatus.RUNNING]:
        run = Run(experiment_id=exp.experiment_id, command_name="test", status=status)
        assert run.is_terminal is False


def test_run_validation() -> None:
    """Validation checks for Run"""
    exp = Experiment(title="Valid")
    
    # experiment_id must be valid
    with pytest.raises(ValidationError):
        Run(experiment_id="invalid", command_name="test")
        
    # parent_run_id must be valid if provided
    with pytest.raises(ValidationError):
        Run(
            experiment_id=exp.experiment_id,
            command_name="test",
            parent_run_id="invalid"
        )
        
    # command_name cannot be empty/whitespace
    with pytest.raises(ValidationError):
        Run(experiment_id=exp.experiment_id, command_name="   ")
        
    # extra fields are rejected
    with pytest.raises(ValidationError):
        # type: ignore is needed for passing extra kwargs
        Run(experiment_id=exp.experiment_id, command_name="test", extra="field")


def test_job_creation() -> None:
    """creates valid Job with generated ID"""
    exp = Experiment(title="Valid")
    run = Run(experiment_id=exp.experiment_id, command_name="test")
    job = Job(run_id=run.run_id, command_name="test_job")
    
    # generated job ID starts with job_ and has 32 lowercase hex characters
    assert job.job_id.startswith("job_")
    assert len(job.job_id) == 36
    
    # default status is JobStatus.CREATED
    assert job.status == JobStatus.CREATED
    
    # is_terminal is false for created
    assert job.is_terminal is False


def test_job_progress() -> None:
    """progress accepts valid values and rejects invalid ones"""
    exp = Experiment(title="Valid")
    run = Run(experiment_id=exp.experiment_id, command_name="test")
    
    # progress accepts None, 0.0, 0.5, and 1.0
    for prog in [None, 0.0, 0.5, 1.0]:
        job = Job(run_id=run.run_id, command_name="test", progress=prog)
        assert job.progress == prog
        
    # progress rejects values below 0.0 or above 1.0
    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name="test", progress=-0.1)
        
    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name="test", progress=1.1)


def test_job_validation_strings() -> None:
    """current_step and error reject whitespace-only strings"""
    exp = Experiment(title="Valid")
    run = Run(experiment_id=exp.experiment_id, command_name="test")
    
    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name="test", current_step="   ")
        
    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name="test", error="   ")


def test_job_is_terminal() -> None:
    """is_terminal logic for Job"""
    exp = Experiment(title="Valid")
    run = Run(experiment_id=exp.experiment_id, command_name="test")
    
    terminal_states = [
        JobStatus.COMPLETED,
        JobStatus.FAILED,
        JobStatus.CANCELLED,
        JobStatus.ARCHIVED
    ]
    for status in terminal_states:
        job = Job(run_id=run.run_id, command_name="test", status=status)
        assert job.is_terminal is True
        
    active_states = [
        JobStatus.CREATED,
        JobStatus.QUEUED,
        JobStatus.RUNNING,
        JobStatus.PAUSED,
        JobStatus.CANCELLING
    ]
    for status in active_states:
        job = Job(run_id=run.run_id, command_name="test", status=status)
        assert job.is_terminal is False


def test_datetime_validation() -> None:
    """naive datetime is rejected, non-UTC datetime is rejected"""
    exp = Experiment(title="Valid")
    
    # Naive datetime
    naive_dt = datetime.now()
    with pytest.raises(ValidationError, match="Datetime must be timezone-aware"):
        Run(experiment_id=exp.experiment_id, command_name="test", created_at=naive_dt)
        
    # Timezone-aware but non-UTC positive offset
    tz_pos = timezone(timedelta(hours=2))
    non_utc_pos_dt = datetime.now(tz_pos)
    with pytest.raises(ValidationError, match="Datetime must be UTC"):
        Run(
            experiment_id=exp.experiment_id,
            command_name="test",
            created_at=non_utc_pos_dt,
        )

    # Timezone-aware but non-UTC negative offset
    tz_neg = timezone(timedelta(hours=-5))
    non_utc_neg_dt = datetime.now(tz_neg)
    with pytest.raises(ValidationError, match="Datetime must be UTC"):
        Run(
            experiment_id=exp.experiment_id,
            command_name="test",
            created_at=non_utc_neg_dt,
        )

    # Timezone-aware UTC is accepted
    utc_dt = datetime.now(UTC)
    run = Run(experiment_id=exp.experiment_id, command_name="test", created_at=utc_dt)
    assert run.created_at == utc_dt


def test_schema_version_strictness() -> None:
    """schema_version must be exactly '1.0'"""
    # Accepts default
    assert Experiment(title="Valid").schema_version == "1.0"
    run = Run(experiment_id="exp_" + "a" * 32, command_name="test")
    assert run.schema_version == "1.0"
    job = Job(run_id="run_" + "a" * 32, command_name="test")
    assert job.schema_version == "1.0"
    
    # Accepts manual '1.0'
    assert Experiment(title="Valid", schema_version="1.0").schema_version == "1.0"
    
    # Rejects '2.0'
    with pytest.raises(ValidationError):
        Experiment(title="Valid", schema_version="2.0")


def test_strict_type_rejections() -> None:
    """Strict types reject unintended coercion."""
    # Experiment
    with pytest.raises(ValidationError):
        Experiment(title=123)  # type: ignore
    with pytest.raises(ValidationError):
        Experiment(title="Valid", description=123)  # type: ignore
    with pytest.raises(ValidationError):
        Experiment(title="Valid", tags=[123])  # type: ignore
    with pytest.raises(ValidationError):
        Experiment(title="Valid", tags="tag")  # type: ignore

    exp = Experiment(title="Valid")

    # Run
    with pytest.raises(ValidationError):
        Run(experiment_id=123, command_name="test")  # type: ignore
    with pytest.raises(ValidationError):
        Run(experiment_id=exp.experiment_id, command_name=123)  # type: ignore
    with pytest.raises(ValidationError):
        Run(
            experiment_id=exp.experiment_id,
            command_name="test",
            parent_run_id=123,  # type: ignore
        )

    run = Run(experiment_id=exp.experiment_id, command_name="test")

    # Job
    with pytest.raises(ValidationError):
        Job(run_id=123, command_name="test")  # type: ignore
    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name=123)  # type: ignore
    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name="test", error=123)  # type: ignore


def test_dict_strictness() -> None:
    """Metadata and parameters must be true dictionaries."""
    exp = Experiment(title="Valid")
    run = Run(experiment_id=exp.experiment_id, command_name="test")

    with pytest.raises(ValidationError):
        Experiment(title="Valid", metadata=[])  # type: ignore
        
    with pytest.raises(ValidationError):
        Run(experiment_id=exp.experiment_id, command_name="test", parameters=[])  # type: ignore

    with pytest.raises(ValidationError):
        Run(experiment_id=exp.experiment_id, command_name="test", metadata=[])  # type: ignore

    with pytest.raises(ValidationError):
        Job(run_id=run.run_id, command_name="test", metadata=[])  # type: ignore


def test_progress_coercion() -> None:
    """Progress explicitly rejects strings and booleans."""
    run_id = "run_" + "a" * 32
    
    # Acceptable
    assert Job(run_id=run_id, command_name="test", progress=0.5).progress == 0.5
    assert Job(run_id=run_id, command_name="test", progress=0).progress == 0.0
    assert Job(run_id=run_id, command_name="test", progress=1).progress == 1.0
    
    # Rejected
    with pytest.raises(ValidationError):
        Job(run_id=run_id, command_name="test", progress="0.5")  # type: ignore
    with pytest.raises(ValidationError):
        Job(run_id=run_id, command_name="test", progress=True)  # type: ignore
    with pytest.raises(ValidationError):
        Job(run_id=run_id, command_name="test", progress=False)  # type: ignore


def test_enum_parsing() -> None:
    """Enums accept valid lowercase strings but reject uppercase or invalid strings."""
    exp_id = "exp_" + "a" * 32
    run_id = "run_" + "a" * 32
    
    # Accepted
    run = Run(experiment_id=exp_id, command_name="test", status="completed")
    assert run.status == RunStatus.COMPLETED
    job = Job(run_id=run_id, command_name="test", status="queued")
    assert job.status == JobStatus.QUEUED
    
    # Rejected
    with pytest.raises(ValidationError):
        Run(experiment_id=exp_id, command_name="test", status="COMPLETED")  # type: ignore
    with pytest.raises(ValidationError):
        Run(experiment_id=exp_id, command_name="test", status="unknown")  # type: ignore
    with pytest.raises(ValidationError):
        Job(run_id=run_id, command_name="test", status="QUEUED")  # type: ignore
    with pytest.raises(ValidationError):
        Job(run_id=run_id, command_name="test", status="unknown")  # type: ignore
