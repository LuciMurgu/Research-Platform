"""Identifier generation utilities."""

import re
import uuid

_PREFIX_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


def generate_id(prefix: str) -> str:
    """Generate a globally unique identifier with a given prefix.

    Args:
        prefix (str): A short string prefix indicating the entity type (e.g., 'run').

    Returns:
        str: A unique identifier formatted as '<prefix>_<uuid4_hex>'.
    """
    if not prefix:
        raise ValueError("Prefix cannot be empty")
    if not _PREFIX_PATTERN.match(prefix):
        raise ValueError(
            "Prefix must start with a lowercase letter and contain only "
            "lowercase letters, digits, and underscores."
        )
    return f"{prefix}_{uuid.uuid4().hex}"
