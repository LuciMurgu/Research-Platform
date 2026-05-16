"""Tests for the ArtifactRef schema."""

from datetime import UTC, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from workbench.core.enums import ArtifactKind
from workbench.core.schemas import ArtifactRef


def _get_valid_kwargs() -> dict:
    return {
        "run_id": "run_" + "a" * 32,
        "kind": ArtifactKind.IMAGE,
        "uri": "runs/run_abc/artifacts/output.png",
        "media_type": "image/png",
        "content_hash": "sha256:" + "a" * 64,
        "byte_size": 1024,
        "producer_step": "render",
    }


def test_artifact_ref_creation() -> None:
    """Valid ArtifactRef creation."""
    kwargs = _get_valid_kwargs()
    ref = ArtifactRef(**kwargs)
    
    assert ref.artifact_id.startswith("artifact_")
    assert len(ref.artifact_id) == 41  # "artifact_" (9) + 32 = 41
    assert ref.created_at.tzinfo == UTC
    assert ref.schema_version == "1.0"
    
    dump = ref.model_dump()
    assert dump["schema_version"] == "1.0"


def test_manual_artifact_id_validation() -> None:
    """Manual artifact_id validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ArtifactRef(artifact_id="artifact_" + "b" * 32, **kwargs)
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id="exp_" + "a" * 32, **kwargs)  # wrong prefix
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id="artifact_" + "A" * 32, **kwargs)  # uppercase hex
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id="artifact_" + "a" * 31, **kwargs)  # too short
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id="artifact_" + "a" * 33, **kwargs)  # too long
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id="artifact-" + "a" * 32, **kwargs)  # malformed separator
    with pytest.raises(ValidationError):
        ArtifactRef(artifact_id=123, **kwargs)  # type: ignore  # non-string


def test_run_id_validation() -> None:
    """run_id validation."""
    kwargs = _get_valid_kwargs()
    
    # Invalid run_id
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "run_id": "exp_" + "a" * 32})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "run_id": "run_" + "A" * 32})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "run_id": "run_" + "a" * 31})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "run_id": 123})


def test_content_hash_validation() -> None:
    """content_hash validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ArtifactRef(**{**kwargs, "content_hash": "sha256:" + "0123456789abcdef" * 4})
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "content_hash": "a" * 64})  # missing sha256: prefix
    with pytest.raises(ValidationError):
        # uppercase prefix
        ArtifactRef(**{**kwargs, "content_hash": "SHA256:" + "a" * 64})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "content_hash": "sha256:" + "A" * 64})  # uppercase hex
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "content_hash": "sha256:" + "a" * 63})  # too short
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "content_hash": "md5:" + "a" * 32})  # wrong algorithm
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "content_hash": 123})  # non-string
    
    kwargs_no_hash = kwargs.copy()
    del kwargs_no_hash["content_hash"]
    with pytest.raises(ValidationError):
        ArtifactRef(**kwargs_no_hash)  # missing


def test_kind_validation() -> None:
    """kind validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ref = ArtifactRef(**{**kwargs, "kind": ArtifactKind.IMAGE})
    assert ref.kind == ArtifactKind.IMAGE
    assert ArtifactRef(**{**kwargs, "kind": "image"}).kind == ArtifactKind.IMAGE
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "kind": "IMAGE"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "kind": "unknown"})


def test_uri_validation() -> None:
    """uri validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ArtifactRef(**{**kwargs, "uri": "artifact://sha256/aa/aa"})
    ArtifactRef(**{**kwargs, "uri": "blobs/sha256/aa/aa"})
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "uri": ""})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "uri": "   "})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "uri": 123})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "uri": "http://example.com"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "uri": "https://example.com"})


def test_media_type_validation() -> None:
    """media_type validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ArtifactRef(**{**kwargs, "media_type": "image/jpeg"})
    ArtifactRef(**{**kwargs, "media_type": "application/json"})
    ArtifactRef(**{**kwargs, "media_type": "application/octet-stream"})
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "media_type": ""})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "media_type": "image"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "media_type": "IMAGE/PNG"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "media_type": "text plain"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "media_type": 123})


def test_byte_size_validation() -> None:
    """byte_size validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ArtifactRef(**{**kwargs, "byte_size": 0})
    ArtifactRef(**{**kwargs, "byte_size": 1})
    ArtifactRef(**{**kwargs, "byte_size": 1024})
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "byte_size": -1})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "byte_size": "1024"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "byte_size": True})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "byte_size": False})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "byte_size": 1.5})


def test_producer_step_validation() -> None:
    """producer_step validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    ArtifactRef(**{**kwargs, "producer_step": "step_1"})
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "producer_step": ""})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "producer_step": "   "})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "producer_step": 123})


def test_metadata_validation() -> None:
    """metadata validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    assert ArtifactRef(**kwargs).metadata == {}
    ref = ArtifactRef(**{**kwargs, "metadata": {"key": "val"}})
    assert ref.metadata == {"key": "val"}
    
    # Invalid
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "metadata": []})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "metadata": "string"})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "metadata": 123})
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "metadata": None})


def test_datetime_validation() -> None:
    """Datetime validation."""
    kwargs = _get_valid_kwargs()
    
    # Valid
    utc_dt = datetime.now(UTC)
    ArtifactRef(**{**kwargs, "created_at": utc_dt})
    
    # Invalid (Naive)
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "created_at": datetime.now()})
        
    # Invalid (UTC+2)
    tz_pos = timezone(timedelta(hours=2))
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "created_at": datetime.now(tz_pos)})
        
    # Invalid (UTC-5)
    tz_neg = timezone(timedelta(hours=-5))
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "created_at": datetime.now(tz_neg)})


def test_extra_fields() -> None:
    """extra fields are rejected"""
    kwargs = _get_valid_kwargs()
    
    with pytest.raises(ValidationError):
        ArtifactRef(**{**kwargs, "extra": "field"})
