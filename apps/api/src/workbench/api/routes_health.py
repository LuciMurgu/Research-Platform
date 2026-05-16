"""Health check route.

Simple liveness endpoint. No database checks, no compute checks,
no experiment logic, no agents, no external services.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Return service health status."""
    return {
        "status": "ok",
        "service": "research-workbench-api",
        "mode": "local",
    }
