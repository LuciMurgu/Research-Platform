"""Identifier generation utilities."""

import uuid


def generate_id(prefix: str) -> str:
    """Generate a globally unique identifier with a given prefix.

    Args:
        prefix (str): A short string prefix indicating the entity type (e.g., 'run').

    Returns:
        str: A unique identifier formatted as '<prefix>_<uuid4_hex>'.
    """
    if not prefix:
        raise ValueError("Prefix cannot be empty")
    return f"{prefix}_{uuid.uuid4().hex}"
