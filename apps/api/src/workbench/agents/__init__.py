"""Agents layer — read-only AI assistant side-channel.

Agents may read approved context and produce labeled suggestions,
explanations, or summaries. They are assistants, not authorities.

SAFETY RULES:
- Must NOT mutate experiments, artifacts, code, or provenance.
- Outputs must always be labeled (suggestion / explanation / summary).
- Never presented as validated scientific fact.
- Occupies a side channel — never the main data path.
"""
