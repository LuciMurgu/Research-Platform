"""Provenance layer — append-only provenance ledger.

Records what happened during experiment execution: runs started/completed,
artifacts stored, parameters used, approvals granted. Provenance events for
finished runs are immutable.
"""
