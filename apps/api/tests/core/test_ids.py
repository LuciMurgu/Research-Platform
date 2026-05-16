"""Tests for the identifier utilities."""

import pytest

from workbench.core.ids import generate_id


def test_generate_id_with_prefix() -> None:
    """generate_id creates an ID starting with the prefix."""
    entity_id = generate_id("run")
    assert entity_id.startswith("run_")


def test_generate_id_length() -> None:
    """generate_id produces an ID of expected length (prefix + '_' + 32 hex chars)."""
    entity_id = generate_id("job")
    # "job" (3) + "_" (1) + 32 hex chars = 36
    assert len(entity_id) == 36


def test_generate_id_uniqueness() -> None:
    """generate_id produces unique IDs."""
    id1 = generate_id("test")
    id2 = generate_id("test")
    assert id1 != id2


def test_generate_id_empty_prefix_raises_error() -> None:
    """generate_id raises ValueError if prefix is empty."""
    with pytest.raises(ValueError, match="Prefix cannot be empty"):
        generate_id("")
