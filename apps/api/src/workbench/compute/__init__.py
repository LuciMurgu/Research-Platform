"""Compute layer — deterministic scientific compute kernels.

Kernels are pure functions: given identical parameters, they produce identical
results. They have no side effects, no network access, and no awareness of the
platform infrastructure around them.

BOUNDARY RULES:
- Must NOT import from workbench.api
- Must NOT import from workbench.agents
- Must NOT import from workbench.storage
- Data flows through ports, not direct access to other layers.
"""
