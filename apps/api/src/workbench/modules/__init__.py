"""Modules layer — domain orchestrators.

Orchestrators coordinate multi-step research workflows. They call compute
kernels through ports, collect results, store artifacts, emit provenance
events, and report metrics and warnings.

Orchestrators do not compute scientific results directly — they delegate
to compute kernels.
"""
