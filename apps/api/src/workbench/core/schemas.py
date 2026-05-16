"""Core domain schemas for the Research Workbench."""

import re
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator

from workbench.core.enums import JobStatus, RunStatus
from workbench.core.ids import generate_id
from workbench.core.time import utcnow

_EXP_ID_PATTERN = re.compile(r"^exp_[0-9a-f]{32}$")
_RUN_ID_PATTERN = re.compile(r"^run_[0-9a-f]{32}$")
_JOB_ID_PATTERN = re.compile(r"^job_[0-9a-f]{32}$")


class StrictBaseModel(BaseModel):
    """Base model with common strict validation rules."""

    model_config = ConfigDict(extra="forbid")

    @classmethod
    def _validate_utc_datetime(cls, v: datetime | None) -> datetime | None:
        """Validate that a datetime is timezone-aware and UTC."""
        if v is None:
            return v
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError("Datetime must be timezone-aware")
        if v.tzinfo.utcoffset(v).total_seconds() != 0:
            raise ValueError("Datetime must be UTC")
        return v

    @classmethod
    def _validate_non_empty_string(cls, v: str) -> str:
        """Validate that a string is not empty or whitespace-only."""
        if not v.strip():
            raise ValueError("String cannot be empty or whitespace-only")
        return v

    @classmethod
    def _validate_optional_non_empty_string(cls, v: str | None) -> str | None:
        """Validate optional string is not empty/whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("String cannot be empty or whitespace-only")
        return v


class Experiment(StrictBaseModel):
    """Represents a long-lived research thread."""

    schema_version: Literal["1.0"] = "1.0"
    experiment_id: StrictStr = Field(default_factory=lambda: generate_id("exp"))
    title: StrictStr
    description: StrictStr | None = None
    tags: list[StrictStr] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime | None = None
    archived_at: datetime | None = None
    metadata: dict[StrictStr, Any] = Field(default_factory=dict)

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata_type(cls, v: Any) -> Any:
        if not isinstance(v, dict):
            raise ValueError("metadata must be a dictionary")
        return v

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags_type(cls, v: Any) -> Any:
        if not isinstance(v, list):
            raise ValueError("tags must be a list")
        return v

    @field_validator("experiment_id")
    @classmethod
    def validate_experiment_id(cls, v: str) -> str:
        if not _EXP_ID_PATTERN.match(v):
            raise ValueError("experiment_id must be 'exp_' and 32 hex chars")
        return v

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        return cls._validate_non_empty_string(v)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        for tag in v:
            if not tag.strip():
                raise ValueError("tags must not contain empty strings")
        return v

    @field_validator("created_at", "updated_at", "archived_at")
    @classmethod
    def validate_datetimes(cls, v: datetime | None) -> datetime | None:
        return cls._validate_utc_datetime(v)


class Run(StrictBaseModel):
    """Represents one immutable scientific execution under an experiment."""

    schema_version: Literal["1.0"] = "1.0"
    run_id: StrictStr = Field(default_factory=lambda: generate_id("run"))
    experiment_id: StrictStr
    status: RunStatus = RunStatus.CREATED
    command_name: StrictStr
    parameters: dict[StrictStr, Any] = Field(default_factory=dict)
    parent_run_id: StrictStr | None = None
    code_version: StrictStr | None = None
    environment_hash: StrictStr | None = None
    created_at: datetime = Field(default_factory=utcnow)
    started_at: datetime | None = None
    finished_at: datetime | None = None
    metadata: dict[StrictStr, Any] = Field(default_factory=dict)

    @field_validator("metadata", "parameters", mode="before")
    @classmethod
    def validate_dict_types(cls, v: Any) -> Any:
        if not isinstance(v, dict):
            raise ValueError("Must be a dictionary")
        return v

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, v: str) -> str:
        if not _RUN_ID_PATTERN.match(v):
            raise ValueError("run_id must be 'run_' and 32 hex chars")
        return v

    @field_validator("experiment_id")
    @classmethod
    def validate_experiment_id(cls, v: str) -> str:
        if not _EXP_ID_PATTERN.match(v):
            raise ValueError("experiment_id must be 'exp_' and 32 hex chars")
        return v

    @field_validator("parent_run_id")
    @classmethod
    def validate_parent_run_id(cls, v: str | None) -> str | None:
        if v is not None and not _RUN_ID_PATTERN.match(v):
            raise ValueError("parent_run_id must be 'run_' and 32 hex chars")
        return v

    @field_validator("command_name")
    @classmethod
    def validate_command_name(cls, v: str) -> str:
        return cls._validate_non_empty_string(v)

    @field_validator("created_at", "started_at", "finished_at")
    @classmethod
    def validate_datetimes(cls, v: datetime | None) -> datetime | None:
        return cls._validate_utc_datetime(v)

    @property
    def is_terminal(self) -> bool:
        """Return True if the run is in a terminal state."""
        return self.status in {
            RunStatus.COMPLETED,
            RunStatus.FAILED,
            RunStatus.CANCELLED,
            RunStatus.ARCHIVED,
        }


class Job(StrictBaseModel):
    """Represents the local execution state of a command/run."""

    schema_version: Literal["1.0"] = "1.0"
    job_id: StrictStr = Field(default_factory=lambda: generate_id("job"))
    run_id: StrictStr
    command_name: StrictStr
    status: JobStatus = JobStatus.CREATED
    progress: float | None = None
    current_step: StrictStr | None = None
    created_at: datetime = Field(default_factory=utcnow)
    queued_at: datetime | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    error: StrictStr | None = None
    metadata: dict[StrictStr, Any] = Field(default_factory=dict)

    @field_validator("metadata", mode="before")
    @classmethod
    def validate_metadata_type(cls, v: Any) -> Any:
        if not isinstance(v, dict):
            raise ValueError("metadata must be a dictionary")
        return v

    @field_validator("progress", mode="before")
    @classmethod
    def validate_progress_type(cls, v: Any) -> Any:
        if v is not None:
            if isinstance(v, bool):
                raise ValueError("progress rejects booleans")
            if not isinstance(v, (int, float)):
                raise ValueError("progress rejects strings and non-numerics")
        return v

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v: str) -> str:
        if not _JOB_ID_PATTERN.match(v):
            raise ValueError("job_id must be 'job_' and 32 hex chars")
        return v

    @field_validator("run_id")
    @classmethod
    def validate_run_id(cls, v: str) -> str:
        if not _RUN_ID_PATTERN.match(v):
            raise ValueError("run_id must be 'run_' and 32 hex chars")
        return v

    @field_validator("command_name")
    @classmethod
    def validate_command_name(cls, v: str) -> str:
        return cls._validate_non_empty_string(v)

    @field_validator("progress")
    @classmethod
    def validate_progress(cls, v: float | None) -> float | None:
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("progress must be between 0.0 and 1.0 inclusive")
        return v

    @field_validator("current_step", "error")
    @classmethod
    def validate_optional_strings(cls, v: str | None) -> str | None:
        return cls._validate_optional_non_empty_string(v)

    @field_validator("created_at", "queued_at", "started_at", "finished_at")
    @classmethod
    def validate_datetimes(cls, v: datetime | None) -> datetime | None:
        return cls._validate_utc_datetime(v)

    @property
    def is_terminal(self) -> bool:
        """Return True if the job is in a terminal state."""
        return self.status in {
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
            JobStatus.ARCHIVED,
        }

